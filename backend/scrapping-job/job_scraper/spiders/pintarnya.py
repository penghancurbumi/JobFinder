from typing import Any

from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class PintarnyaSpider(BaseSpider):
    name = "pintarnya"
    platform_name = Platform.PINTARNYA
    start_url = "https://www.pintarnya.com/kerja/search"
    use_playwright = True

    def _build_start_url(self) -> str:
        url = self.start_url
        params = []
        if self.keyword:
            params.append(f"keyword={self.keyword}")
        if self.location_filter:
            params.append(f"location={self.location_filter}")
        if params:
            url = f"{url}?{'&'.join(params)}"
        return url

    def _get_page_methods(self) -> list:
        return [
            PageMethod("wait_for_selector", "a[href*='/lowongan/']", timeout=30000),
            PageMethod("wait_for_timeout", 2000),
        ]

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing listing page: %s", response.url)

        cards = response.css("a[href*='/lowongan/']")
        if not cards:
            self.logger_custom.warning("No job cards found")
            return

        for card in cards:
            title = card.css("[data-testid='cardjob-text-title']::text").get("").strip()
            company = card.css("[data-testid='cardjob-text-company']::text").get("").strip()
            location = card.css("[data-testid='cardjob-text-location']::text").get("").strip()
            salary = card.css("[data-testid='cardjob-text-salary']::text").get("").strip()
            href = card.attrib.get("href", "")

            item_data = {
                "title": title,
                "company_name": company,
                "location": location,
                "source_url": response.urljoin(href) if href else response.url,
            }

            if salary:
                cleaned = salary.replace("Rp", "").replace(".", "").replace(",", "").strip()
                parts = [p.strip() for p in cleaned.split("-") if p.strip()]
                if len(parts) >= 1:
                    try:
                        item_data["salary_min"] = int(parts[0])
                    except ValueError:
                        pass
                if len(parts) >= 2:
                    try:
                        item_data["salary_max"] = int(parts[1])
                    except ValueError:
                        pass
                if item_data.get("salary_min") or item_data.get("salary_max"):
                    item_data["salary_currency"] = "IDR"

            if item_data["title"] and item_data["company_name"]:
                if self._detail_count < self.max_detail_pages and item_data["source_url"] != response.url:
                    self._detail_count += 1
                    yield self._make_detail_request(item_data["source_url"], self.parse_detail, meta={"item_data": item_data})
                else:
                    yield self.build_job_item(item_data)

    def parse_detail(self, response: Response) -> Any:
        self.logger_custom.info("Parsing Pintarnya detail: %s", response.url)
        item_data = response.meta.get("item_data", {})

        desc = self._desc_text(response, "[data-testid*='description']")
        if desc:
            item_data["description"] = desc

        job_type = self._desc_text(response, "[data-testid='detailjob-text-time']")
        if job_type:
            item_data["job_type"] = self._normalize_job_type(job_type)

        work_type = self._desc_text(response, "[data-testid='detailjob-text-typework']")
        if work_type:
            item_data["work_type"] = self._normalize_work_type(work_type.lstrip(", "))

        yield self.build_job_item(item_data)
