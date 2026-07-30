import json
import re
from typing import Any

from scrapy.http import Response

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class JobstreetSpider(BaseSpider):
    name = "jobstreet"
    platform_name = Platform.JOBSTREET
    start_url = "https://id.jobstreet.com/id/job-search/all-jobs-in-indonesia"

    def _build_start_url(self) -> str:
        params = []
        if self.keyword:
            params.append(f"keyword={self.keyword}")
        if self.location_filter:
            params.append(f"location={self.location_filter}")
        params.append("page=1")
        return f"{self.start_url}?{'&'.join(params)}"

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing JobStreet response")
        script = response.css('script[data-automation="server-state"]::text').get()
        if not script:
            self.logger_custom.warning("No server-state script found")
            return

        try:
            data = json.loads(script)
        except json.JSONDecodeError:
            self.logger_custom.error("Failed to parse server-state JSON: %s", script[:300])
            return

        results = (data.get("results", {})
                   .get("RESULTS", {})
                   .get("resultsList", []))

        if not results:
            self.logger_custom.info("No jobs found")
            return

        for job in results:
            item_data = {
                "title": (job.get("title") or "").strip(),
                "company_name": (job.get("company", {}).get("name") or "").strip(),
                "location": (job.get("location") or "").strip(),
                "salary_min": self._parse_salary(job.get("salary")),
                "salary_max": self._parse_salary(job.get("salaryMax")),
                "salary_currency": "IDR",
                "source_url": f"https://id.jobstreet.com/id/job/{job.get('id', '')}",
            }
            yield self.build_job_item(item_data)

    def _parse_salary(self, value) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
