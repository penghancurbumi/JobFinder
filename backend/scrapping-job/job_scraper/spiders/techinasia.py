import json
from typing import Any

from scrapy.http import Response

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class TechInAsiaSpider(BaseSpider):
    name = "techinasia"
    platform_name = Platform.TECHINASIA
    start_url = "https://www.techinasia.com/jobs"

    def _build_start_url(self) -> str:
        params = []
        if self.keyword:
            params.append(f"search={self.keyword}")
        url = self.start_url
        if params:
            url = f"{url}?{'&'.join(params)}"
        return url

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing TechInAsia listing page: %s", response.url)
        script = response.css('script#__NEXT_DATA__::text').get()
        if not script:
            self.logger_custom.warning("No __NEXT_DATA__ found")
            return

        try:
            data = json.loads(script)
        except json.JSONDecodeError:
            self.logger_custom.error("Failed to parse __NEXT_DATA__")
            return

        jobs = (data.get("props", {})
                .get("pageProps", {})
                .get("jobs", []))

        if not jobs:
            self.logger_custom.info("No jobs found")
            return

        for job in jobs:
            item_data = {
                "title": job.get("title", "").strip(),
                "company_name": (job.get("company", {}).get("name") or "").strip(),
                "location": job.get("location", "").strip(),
                "source_url": f"https://www.techinasia.com/jobs/{job.get('id', '')}",
            }
            if item_data["title"] and item_data["company_name"]:
                yield self.build_job_item(item_data)
