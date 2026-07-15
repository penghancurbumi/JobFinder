"""
Kalibrr Spider — Scrapes job listings from Kalibrr API.
"""

import json
from typing import Any, Generator

import scrapy
from scrapy.http import Response

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class KalibrrSpider(BaseSpider):
    """Spider for Kalibrr platform using their GraphQL/REST API."""

    name = "kalibrr"
    platform_name = Platform.KALIBRR
    start_url = "https://www.kalibrr.com/api/job_board/search?limit=15&offset={offset}"
    use_playwright = False  # Pure API scraping, no browser needed!

    async def start(self) -> Any:
        """Generate initial API request."""
        url = self._build_api_url(offset=0)
        self.logger_custom.info("Starting Kalibrr API spider: %s", url)
        
        # Pass offset in meta for pagination
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={"offset": 0},
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )

    def _build_api_url(self, offset: int) -> str:
        url = self.start_url.format(offset=offset)
        # Add filters
        if self.keyword:
            url += f"&text={self.keyword}"
        if self.location_filter:
            url += f"&location={self.location_filter}"
        if self.job_type_filter == "internship":
            url += "&job_type=Internship"
        elif self.job_type_filter == "fulltime":
            url += "&job_type=Full-Time"
            
        return url

    def parse(self, response: Response) -> Generator[Any, None, None]:
        """Parse API JSON response."""
        self.logger_custom.info("Parsing Kalibrr API response")
        
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger_custom.error("Failed to parse JSON from %s", response.url)
            return

        jobs = data.get("jobs", [])
        if not jobs:
            self.logger_custom.info("No jobs found in response.")
            return

        for job in jobs:
            # Extract company data
            company_info = job.get("company_info", {})
            company_name = company_info.get("name")
            company_logo = company_info.get("logo")
            
            # Extract basic info
            title = job.get("name")
            status = job.get("status")
            
            # Skip closed jobs
            if status == "CLOSED":
                continue
                
            location = job.get("location", "")
            job_type = job.get("job_type", "")
            work_type = "Remote" if job.get("work_from_home") else "Onsite"
            
            # Salary
            salary_min = None
            salary_max = None
            salary_currency = "IDR"
            
            salary_info = job.get("base_salary")
            if isinstance(salary_info, dict):
                salary_currency = salary_info.get("currency", "IDR")
                salary_min = salary_info.get("min")
                salary_max = salary_info.get("max")
            elif isinstance(salary_info, (int, float)):
                salary_min = float(salary_info)
            
            # Build URL
            job_id = job.get("id", "")
            company_code = company_info.get("code", "")
            detail_url = f"https://www.kalibrr.com/c/{company_code}/jobs/{job_id}/{job.get('slug', '')}"
            
            # Extract requirements/description
            reqs = job.get("requirements", "")
            desc = job.get("description", "")
            
            # Build item
            item_data = {
                "title": title,
                "company_name": company_name,
                "company_logo": company_logo,
                "location": location,
                "job_type": job_type,
                "work_type": work_type,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_currency": salary_currency,
                "source_url": detail_url,
                "description": desc,
                "requirements": reqs,
            }
            
            yield self.build_job_item(item_data)

        # Pagination
        current_offset = response.meta.get("offset", 0)
        next_offset = current_offset + 15
        
        # Check if we should continue (Kalibrr total jobs)
        total_count = data.get("total_count", 0)
        
        if next_offset < total_count and self._should_continue_pagination():
            next_url = self._build_api_url(offset=next_offset)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={"offset": next_offset},
                headers=response.request.headers
            )
