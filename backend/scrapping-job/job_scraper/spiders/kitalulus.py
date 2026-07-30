import json
import re
from typing import Any

import scrapy
from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class KitalulusSpider(BaseSpider):
    name = "kitalulus"
    platform_name = Platform.KITALULUS
    start_url = "https://www.kitalulus.com/lowongan"
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
        return [PageMethod("wait_for_load_state", "networkidle")]

    def _extract_rsf_payload(self, text: str) -> list:
        chunks = []
        for match in re.finditer(r'self\.__next_f\.push\(\[(\d+),("(?:[^"\\]|\\.)*")\]\)', text):
            try:
                raw = json.loads(match.group(2))
                chunks.append(raw)
            except json.JSONDecodeError:
                continue
        return chunks

    def _extract_vacancy_list(self, chunks: list) -> dict | None:
        combined = "".join(chunks)
        idx = combined.find('"vacancyList":')
        if idx == -1:
            return None
        start = idx + len('"vacancyList":')
        depth = 0
        in_str = False
        escape = False
        for i in range(start, len(combined)):
            ch = combined[i]
            if escape:
                escape = False
                continue
            if ch == '\\' and in_str:
                escape = True
                continue
            if ch == '"' and not escape:
                in_str = not in_str
                continue
            if in_str:
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(combined[start:i + 1])
                    except json.JSONDecodeError:
                        return None
        return None

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing listing page: %s", response.url)

        chunks = self._extract_rsf_payload(response.text)
        if not chunks:
            self.logger_custom.error("Failed to find RSC payload in %s", response.url)
            return

        vacancy_list = self._extract_vacancy_list(chunks)
        if not vacancy_list:
            self.logger_custom.error("Failed to extract vacancyList from RSC payload")
            return

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
            city_obj = job.get("city", {}) or {}

            location_parts = []
            if city_obj.get("name"):
                location_parts.append(city_obj["name"])
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
