import json
import re
from typing import Any

import scrapy
from scrapy.http import Response

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class KalibrrSpider(BaseSpider):
    name = "kalibrr"
    platform_name = Platform.KALIBRR
    start_url = "https://www.kalibrr.id/job-board/te/all"

    def _build_start_url(self) -> str:
        params = []
        if self.keyword:
            params.append(f"keyword={self.keyword}")
        url = self.start_url
        if params:
            url = f"{url}?{'&'.join(params)}"
        return url

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing Kalibrr response")
        jobs = response.css("a[data-url]")
        if not jobs:
            self.logger_custom.warning("No job cards found")
            return

        for job in jobs:
            item_data = {
                "title": job.css("span[class*='title']::text, h2::text").get("").strip(),
                "company_name": job.css("span[class*='company']::text").get("").strip(),
                "location": job.css("span[class*='location']::text, span[class*='loc']::text").get("").strip(),
                "source_url": response.urljoin(job.attrib.get("data-url", "")),
            }
            if item_data["title"] and item_data["company_name"]:
                yield self.build_job_item(item_data)
