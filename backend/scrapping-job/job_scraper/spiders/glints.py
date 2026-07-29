okeimport json
import re
from datetime import datetime, timezone
from typing import Any

import scrapy

from job_scraper.constants import Platform
from job_scraper.items import JobItem
from job_scraper.logger import get_logger, get_stats_logger


class GlintsSpider(scrapy.Spider):
    # =====================================================
    # GLINTS SPIDER
    # =====================================================
    # Cara kerja:
    # 1. Spider ngirim request ke halaman Glints explore
    # 2. TAPI Scrapy biasa kena block sama Cloudflare
    # 3. Makanya kita pake meta {"impersonate": True}
    # 4. Middleware CloudflareBypassMiddleware tangkap request itu
    # 5. Middleware pake curl_cffi (library C) yang meniru TLS fingerprint Chrome asli
    # 6. Cloudflare mikir kita browser beneran → kasih akses
    # 7. HTML balik ke sini, kita extract data job dari JSON embedded
    #
    # Kenapa gak pake Playwright (browser sungguhan)?
    # Karena Glints punya Cloudflare yang juga detect headless browser.
    # curl_cffi lebih ringan dan lebih reliable buat bypass TLS check.

    name = "glints"
    platform_name = Platform.GLINTS

    base_url = "https://glints.com/id/opportunities/jobs/explore"
    # start_urls dikosongin dulu, nanti diisi di __init__
    start_urls = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # __init__ jalan pertama kali pas spider dibuat
        # kwargs是 dari command line: scrapy crawl glints -a keyword=python
        super().__init__(*args, **kwargs)
        self.logger_custom = get_logger(f"spiders.{self.name}")
        self.stats_logger = get_stats_logger()

        # Argumen opsional dari CLI
        self.max_pages = int(kwargs.get("max_pages", 1))
        self.keyword = kwargs.get("keyword", None)
        self.location_filter = kwargs.get("location", None)

        # Counter buat laporan
        self._page_count = 0
        self._item_count = 0
        self._error_count = 0
        self._start_time = datetime.now(timezone.utc)

        # Bangun URL awal dengan filter keyword/lokasi
        url = self.base_url
        params = []
        if self.keyword:
            params.append(f"keyword={self.keyword}")
        if self.location_filter:
            params.append(f"locations={self.location_filter}")
        if params:
            url = f"{url}?{'&'.join(params)}"
        self.start_urls = [url]

    async def start(self):
        # =====================================================
        # START — Method pertama yang dipanggil Scrapy
        # =====================================================
        # Scrapy 2.x pake "async def start()" bukan "start_requests()"
        # Ini async generator: yield Request → Scrapy proses → callback parse()
        #
        # Alur:
        # start() → yield Request → CloudflareBypassMiddleware → curl_cffi → response → parse()

        self.logger_custom.info("start() called")
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
                # meta["impersonate"] = True → middleware tahu ini perlu bypass Cloudflare
                meta={"impersonate": True, "handle_httpstatus_list": [403, 429]},
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                },
            )

    def parse(self, response):
        # =====================================================
        # PARSE — Ngolah response HTML dari Glints
        # =====================================================
        # Response di sini udah lolos Cloudflare (berkat middleware)
        # Tapi response ini HTML biasa, bukan hasil render JavaScript
        # Untungnya Glints (Next.js) embed data job langsung di HTML
        # dalam bentuk JSON di dalem tag <script>

        self.logger_custom.info("Parsing listing page: %s", response.url)

        # Kalau kena block, status 403 (Cloudflare) atau 429 (rate limit)
        if response.status in (403, 429):
            self.logger_custom.error("Blocked by Cloudflare or rate limited (%d)", response.status)
            return

        # Ambil data job dari JSON yang nempel di HTML
        jobs = self._extract_jobs(response.text)
        if not jobs:
            self.logger_custom.warning("No jobs found in embedded JSON")
            return

        # Loop tiap job → konversi ke format Item → kirim ke pipeline
        for job in jobs:
            item = self._build_item(job)
            if item:
                yield item

    def _extract_jobs(self, html: str) -> list[dict]:
        # =====================================================
        # EKSTRAK JSON dari HTML
        # =====================================================
        # Glints pake Next.js. Pas pertama load, Next.js render data
        # di server dan nempel hasilnya di HTML bentuk JSON.
        # JSON ini ada di dalem <script> tag.
        #
        # Struktur JSON:
        # {
        #   "props": {
        #     "pageProps": {
        #       "initialJobs": {
        #         "jobsInPage": [ ... 30 job objects ... ],
        #         "hasMore": true,
        #         "expInfo": ...
        #       }
        #     }
        #   }
        # }
        #
        # Dua pendekatan:
        # 1. Cari <script>{...}</script> yang startsWith "{" dan ada "initialJobs"
        # 2. Fallback: cari __NEXT_DATA__ = {...};

        # Pendekatan 1: cari script tag yang isinya JSON object
        for script in re.findall(r'<script[^>]*>([\s\S]*?)</script>', html):
            s = script.strip()
            if s.startswith("{") and "initialJobs" in s:
                try:
                    data = json.loads(s)
                    return (
                        data.get("props", {})
                        .get("pageProps", {})
                        .get("initialJobs", {})
                        .get("jobsInPage", [])
                    )
                except json.JSONDecodeError:
                    continue

        # Pendekatan 2: cari __NEXT_DATA__ (format standar Next.js)
        m = re.search(r'__NEXT_DATA__\s*=\s*({.*?});', html, re.DOTALL)
        if m:
            try:
                d = json.loads(m.group(1))
                return (
                    d.get("props", {})
                    .get("pageProps", {})
                    .get("initialJobs", {})
                    .get("jobsInPage", [])
                )
            except (json.JSONDecodeError, AttributeError):
                pass
        return []

    def _build_item(self, job: dict) -> JobItem | None:
        # =====================================================
        # KONVERSI data JSON Glints → Item Scrapy
        # =====================================================
        # Setiap job dari JSON Glints punya struktur:
        # {
        #   "id": "uuid",
        #   "title": "SALES GENERALIS",
        #   "type": "CONTRACT",           # FULL_TIME / PART_TIME / CONTRACT / INTERNSHIP
        #   "workArrangementOption": "ONSITE",  # ONSITE / REMOTE / HYBRID
        #   "company": { "name": "PT Maju", "brandName": null, "logo": "xxx.jpeg" },
        #   "location": { "formattedName": "Jakarta", ... },
        #   "salaries": { "CurrencyCode": "IDR", "minAmount": 5000000, "maxAmount": 8000000 },
        #   "createdAt": "2026-05-20T09:28:23.248Z",
        #   "skills": [ { "skill": { "name": "Python" }, "mustHave": true } ],
        #   "minYearsOfExperience": 1,
        #   "maxYearsOfExperience": 3,
        #   ...
        # }
        # Kita map ke JobItem (schema Scrapy) yang udah ditentukan.

        item = JobItem()
        item["platform"] = self.platform_name
        item["title"] = (job.get("title") or "").strip()
        # source_url: link ke halaman detail job di Glints
        item["source_url"] = f"https://glints.com/id/opportunities/jobs/{job.get('id', '')}"

        company = job.get("company") or {}
        item["company_name"] = ((company.get("brandName") or company.get("name")) or "").strip()
        item["company_logo"] = company.get("logo") or ""

        loc = job.get("location") or {}
        city = job.get("city") or {}
        item["location"] = loc.get("formattedName") or city.get("name") or ""
        item["country"] = (job.get("country") or {}).get("code", "ID")

        # Mapping tipe pekerjaan dari string Glints ke format standar
        # Glints pake FULL_TIME, PART_T
        IME, CONTRACT, INTERNSHIP, FREELANCE
        # Kita simpen sebagai "full-time", "part-time", etc.
        raw_type = job.get("type", "")
        job_type_map = {
            "FULL_TIME": "full-time", "PART_TIME": "part-time",
            "CONTRACT": "contract", "INTERNSHIP": "internship",
            "FREELANCE": "freelance",
        }
        item["job_type"] = job_type_map.get(raw_type, "other")

        work_type_map = {
            "ONSITE": "onsite", "REMOTE": "remote", "HYBRID": "hybrid",
        }
        item["work_type"] = work_type_map.get(job.get("workArrangementOption", ""), "")
        item["is_internship"] = raw_type == "INTERNSHIP"

        # Experience level
        item["experience_level"] = ""
        mn = job.get("minYearsOfExperience")
        mx = job.get("maxYearsOfExperience")
        if mn is not None and mx is not None:
            item["experience_level"] = f"{mn}-{mx} years"
        elif mn is not None:
            item["experience_level"] = f"min {mn} years"

        # Tanggal posting — format ISO 8601
        created = job.get("createdAt", "")
        if created:
            try:
                item["posting_date"] = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except ValueError:
                pass

        updated = job.get("updatedAt", "")
        if updated:
            try:
                item["updated_at"] = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            except ValueError:
                pass

        # Skills — array of { skill: { name: "..." }, mustHave: bool }
        skills = job.get("skills") or []
        item["skills"] = [s.get("skill", {}).get("name", "") for s in skills if s.get("skill")]
        item["tags"] = []

        # Salary — bisa null, bisa object { CurrencyCode, minAmount, maxAmount }
        sal = job.get("salaries")
        item["salary_currency"] = ""
        item["salary_min"] = 0.0
        item["salary_max"] = 0.0
        if sal and isinstance(sal, dict):
            item["salary_currency"] = sal.get("CurrencyCode") or ""
            item["salary_min"] = float(sal.get("minAmount", 0) or 0)
            item["salary_max"] = float(sal.get("maxAmount", 0) or 0)

        # Description — kadang ada, kadang kosong
        desc = job.get("description") or ""
        if not desc and item.get("skills"):
            desc = ", ".join(item["skills"])
        item["description"] = desc

        # Timestamps
        item["scraped_at"] = datetime.now(timezone.utc)
        if not item.get("updated_at"):
            item["updated_at"] = item["scraped_at"]

        # Validasi: job harus punya minimal title dan company_name
        if not item.get("title") or not item.get("company_name"):
            self.logger_custom.debug("Skipping job missing title/company: %s", job.get("id"))
            return None

        self._item_count += 1
        return item

    def closed(self, reason: str) -> None:
        # =====================================================
        # CLOSED — Dipanggil pas spider selesai
        # =====================================================
        # Buat laporan statistik: berapa item, berapa lama, dll.
        duration = (datetime.now(timezone.utc) - self._start_time).total_seconds()
        self.logger_custom.info("Spider '%s' closed. Items: %d | Duration: %.1fs", self.name, self._item_count, duration)
        self.stats_logger.info("SPIDER CLOSED | Name: %s | Items: %d | Errors: %d | Duration: %.1fs", self.name, self._item_count, self._error_count, duration)
