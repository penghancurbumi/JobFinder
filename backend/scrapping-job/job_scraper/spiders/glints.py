import json
import re
from datetime import datetime, timezone
from typing import Any

import scrapy

from job_scraper.constants import Platform
from job_scraper.items import JobItem
from job_scraper.logger import get_logger, get_stats_logger


class GlintsSpider(scrapy.Spider):
    name = "glints"
    platform_name = Platform.GLINTS
    base_url = "https://glints.com/id/opportunities/jobs/explore"
    start_urls = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.logger_custom = get_logger(f"spiders.{self.name}")
        self.stats_logger = get_stats_logger()
        self.max_pages = int(kwargs.get("max_pages", 1))
        self.keyword = kwargs.get("keyword", None)
        self.location_filter = kwargs.get("location", None)
        self._page_count = 0
        self._item_count = 0
        self._error_count = 0
        self._start_time = datetime.now(timezone.utc)

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
        self.logger_custom.info("start() called")
        for url in self.start_urls:
            yield scrapy.Request(
                url=url, callback=self.parse, dont_filter=True,
                meta={"impersonate": True, "handle_httpstatus_list": [403, 429]},
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                },
            )

    def parse(self, response):
        self.logger_custom.info("Parsing listing page: %s", response.url)
        if response.status in (403, 429):
            self.logger_custom.error("Blocked by Cloudflare or rate limited (%d)", response.status)
            return

        jobs = self._extract_jobs(response.text)
        if not jobs:
            self.logger_custom.warning("No jobs found in embedded JSON")
            return

        for job in jobs:
            item = self._build_item(job)
            if item:
                yield item

    def _extract_jobs(self, html: str) -> list[dict]:
        for script in re.findall(r'<script[^>]*>([\s\S]*?)</script>', html):
            s = script.strip()
            if s.startswith("{") and "initialJobs" in s:
                try:
                    data = json.loads(s)
                    return (data.get("props", {}).get("pageProps", {}).get("initialJobs", {}).get("jobsInPage", []))
                except json.JSONDecodeError:
                    continue

        m = re.search(r'__NEXT_DATA__\s*=\s*({.*?});', html, re.DOTALL)
        if m:
            try:
                d = json.loads(m.group(1))
                return (d.get("props", {}).get("pageProps", {}).get("initialJobs", {}).get("jobsInPage", []))
            except (json.JSONDecodeError, AttributeError):
                pass
        return []

    def _build_item(self, job: dict) -> JobItem | None:
        item = JobItem()
        item["platform"] = self.platform_name
        item["title"] = (job.get("title") or "").strip()
        item["source_url"] = f"https://glints.com/id/opportunities/jobs/{job.get('id', '')}"

        company = job.get("company") or {}
        item["company_name"] = ((company.get("brandName") or company.get("name")) or "").strip()
        raw_logo = company.get("logo") or ""
        item["company_logo"] = raw_logo if raw_logo.startswith("http") else ""

        loc = job.get("location") or {}
        city = job.get("city") or {}
        item["location"] = loc.get("formattedName") or city.get("name") or ""
        item["country"] = (job.get("country") or {}).get("code", "ID")

        raw_type = job.get("type", "")
        job_type_map = {
            "FULL_TIME": "full-time", "PART_TIME": "part-time",
            "CONTRACT": "contract", "INTERNSHIP": "internship", "FREELANCE": "freelance",
        }
        item["job_type"] = job_type_map.get(raw_type, "other")
        work_type_map = {"ONSITE": "onsite", "REMOTE": "remote", "HYBRID": "hybrid"}
        item["work_type"] = work_type_map.get(job.get("workArrangementOption", ""), "")
        item["is_internship"] = raw_type == "INTERNSHIP"

        item["experience_level"] = ""
        mn = job.get("minYearsOfExperience")
        mx = job.get("maxYearsOfExperience")
        if mn is not None and mx is not None:
            item["experience_level"] = f"{mn}-{mx} years"
        elif mn is not None:
            item["experience_level"] = f"min {mn} years"

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

        skills = job.get("skills") or []
        item["skills"] = [s.get("skill", {}).get("name", "") for s in skills if s.get("skill")]
        item["tags"] = []

        sal = job.get("salaries")
        item["salary_currency"] = ""
        item["salary_min"] = 0.0
        item["salary_max"] = 0.0
        if sal and isinstance(sal, dict):
            item["salary_currency"] = sal.get("CurrencyCode") or ""
            item["salary_min"] = float(sal.get("minAmount", 0) or 0)
            item["salary_max"] = float(sal.get("maxAmount", 0) or 0)

        desc = job.get("description") or ""
        if not desc and item.get("skills"):
            desc = ", ".join(item["skills"])
        item["description"] = desc

        item["scraped_at"] = datetime.now(timezone.utc)
        if not item.get("updated_at"):
            item["updated_at"] = item["scraped_at"]

        if not item.get("title") or not item.get("company_name"):
            self.logger_custom.debug("Skipping job missing title/company: %s", job.get("id"))
            return None

        self._item_count += 1
        return item

    def closed(self, reason: str) -> None:
        duration = (datetime.now(timezone.utc) - self._start_time).total_seconds()
        self.logger_custom.info("Spider '%s' closed. Items: %d | Duration: %.1fs", self.name, self._item_count, duration)
        self.stats_logger.info("SPIDER CLOSED | Name: %s | Items: %d | Errors: %d | Duration: %.1fs | Reason: %s", self.name, self._item_count, self._error_count, duration, reason)
