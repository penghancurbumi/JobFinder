"""
Tech In Asia Spider — Scrapes job listings from Tech In Asia.
"""

import json
from typing import Any

import scrapy
from scrapy.http import Response

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class TechInAsiaSpider(BaseSpider):
    """Spider for Tech In Asia platform using their Job Postings API."""

    name = "techinasia"
    platform_name = Platform.TECHINASIA
    start_url = "https://www.techinasia.com/api/2.0/job-postings?page={page}&per_page=15"
    use_playwright = False

    async def start(self) -> Any:
        """Generate initial API request."""
        url = self._build_api_url(page=1)
        self.logger_custom.info("Starting Tech In Asia API spider: %s", url)
        
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={"page": 1},
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
        )

    def _build_api_url(self, page: int) -> str:
        url = self.start_url.format(page=page)
        
        # Tech In Asia doesn't have standard query params, but this works generally
        if self.keyword:
            url += f"&query={self.keyword}"
            
        return url

    def parse(self, response: Response) -> Any:
        """Parse API JSON response."""
        self.logger_custom.info("Parsing Tech In Asia API response")
        
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger_custom.error("Failed to parse JSON from %s", response.url)
            return

        jobs = data.get("data", [])
        if not jobs:
            self.logger_custom.info("No jobs found in response.")
            return

        for job in jobs:
            # Basic info
            title = job.get("title", "")
            status = job.get("status", "")
            
            if status != "published":
                continue
                
            # Company
            company = job.get("company", {})
            company_name = company.get("name", "")
            company_logo = company.get("avatar_url", "")
            
            # Location
            location = job.get("location_name", "")
            
            # Job Type
            job_type_data = job.get("job_type", {})
            if isinstance(job_type_data, dict):
                job_type = job_type_data.get("name", "")
            else:
                job_type = str(job_type_data)
                
            work_type = "Remote" if job.get("is_remote") else "Onsite"
            
            # Salary
            salary_min = job.get("min_salary")
            salary_max = job.get("max_salary")
            salary_currency = job.get("salary_currency", "IDR")
            
            # Build URL
            slug = job.get("slug", "")
            job_id = job.get("id", "")
            url_part = slug if slug else job_id
            detail_url = f"https://www.techinasia.com/jobs/{url_part}"
            
            # Extract requirements/description
            desc = job.get("description", "")
            reqs = job.get("requirements", "")
            
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
        current_page = response.meta.get("page", 1)
        total_pages = data.get("total_pages", 1)
        
        if current_page < total_pages and self._should_continue_pagination():
            next_page = current_page + 1
            next_url = self._build_api_url(page=next_page)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={"page": next_page},
                headers=response.request.headers
            )
