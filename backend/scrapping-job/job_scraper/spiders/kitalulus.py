import json
import re
from typing import Any, Generator

import scrapy
from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class KitalulusSpider(BaseSpider):
    name = "kitalulus"
    platform_name = Platform.KITALULUS
    start_url = "https://www.kitalulus.com/lowongan"

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
            PageMethod("wait_for_load_state", "networkidle"),
        ]

    def parse(self, response: Response) -> Generator[Any, None, None]:
        self.logger_custom.info("Parsing listing page: %s", response.url)

        match = re.search(r'<script id="__NEXT_DATA__"[^>]*type="application/json"[^>]*>({.*?})</script>', response.text, re.DOTALL)
        if not match:
            self.logger_custom.error("Failed to find __NEXT_DATA__ in %s", response.url)
            return

        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            self.logger_custom.error("Failed to parse __NEXT_DATA__ JSON")
            return

        props = data.get("props", {}).get("pageProps", {})
        vacancy_list = props.get("vacancyList", {})
        jobs = vacancy_list.get("list", [])

        if not jobs:
            self.logger_custom.info("No jobs found on page %s", response.url)
            return

        for job in jobs:
            if job.get("isClosed"):
                continue

            slug = job.get("slug", "")
            detail_url = f"https://www.kitalulus.com/job/{slug}" if slug else response.url

            company = job.get("company", {}) or {}
            province = job.get("province", {}) or {}
            city = job.get("city", {}) or {}

            location_parts = []
            if city.get("name"):
                location_parts.append(city["name"])
            if province.get("name"):
                location_parts.append(province["name"])
            location = ", ".join(location_parts) if location_parts else None

            salary_min = job.get("salaryLowerBound")
            salary_max = job.get("salaryUpperBound")

            item_data = {
                "title": job.get("positionName"),
                "company_name": company.get("name"),
                "location": location,
                "salary_min": salary_min if salary_min and salary_min > 0 else None,
                "salary_max": salary_max if salary_max and salary_max > 0 else None,
                "salary_currency": "IDR",
                "source_url": detail_url,
                "updated_at": job.get("updatedAtStr"),
            }

            yield self.build_job_item(item_data)

        if self._should_continue_pagination():
            has_next = vacancy_list.get("hasNextPage", False)
            if not has_next:
                self.logger_custom.info("No more pages. Stopping pagination.")
                return

            current_page = vacancy_list.get("page", 1)
            next_page = current_page + 1

            if "?" in response.url:
                if "page=" in response.url:
                    next_url = re.sub(r"page=\d+", f"page={next_page}", response.url)
                else:
                    next_url = f"{response.url}&page={next_page}"
            else:
                next_url = f"{response.url}?page={next_page}"

            yield self._make_request(next_url, callback=self.parse)
