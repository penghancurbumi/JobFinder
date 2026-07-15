"""
JobStreet Spider — Scrapes job listings from JobStreet (Seek Platform).
"""

import json
import re
from typing import Any
import urllib.parse

import scrapy
from scrapy.http import Response

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class JobstreetSpider(BaseSpider):
    """Spider for JobStreet platform using their frontend Redux data."""

    name = "jobstreet"
    platform_name = Platform.JOBSTREET
    use_playwright = False
    
    # Generic starting URL for Jobstreet ID
    base_search_url = "https://id.jobstreet.com/id/job-search/{query}-jobs-in-indonesia?page={page}"

    async def start(self) -> Any:
        """Generate initial request."""
        url = self._build_search_url(page=1)
        self.logger_custom.info("Starting JobStreet spider: %s", url)
        
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={"page": 1},
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )

    def _build_search_url(self, page: int) -> str:
        # Build query
        query_parts = []
        if self.keyword:
            query_parts.append(urllib.parse.quote(self.keyword.replace(" ", "-")))
        
        if self.job_type_filter == "internship":
            query_parts.append("internship")
            
        query_str = "-".join(query_parts) if query_parts else "all"
        
        url = self.base_search_url.format(query=query_str, page=page)
        return url

    def parse(self, response: Response) -> Any:
        """Parse JobStreet HTML response and extract Redux JSON."""
        self.logger_custom.info("Parsing JobStreet response")
        
        # Extract window.SEEK_REDUX_DATA using regex
        match = re.search(r'window\.SEEK_REDUX_DATA\s*=\s*(\{.*?\});\s*window\.', response.text, re.DOTALL)
        if not match:
            self.logger_custom.error("Failed to find SEEK_REDUX_DATA in %s", response.url)
            return
            
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            self.logger_custom.error("Failed to parse SEEK_REDUX_DATA JSON")
            return

        jobs = data.get("results", {}).get("results", {}).get("jobs", [])
        if not jobs:
            self.logger_custom.info("No jobs found in response.")
            return

        for job in jobs:
            # Extract basic info
            title = job.get("title", "")
            
            # Company
            advertiser = job.get("advertiser", {})
            company_name = advertiser.get("description", "")
            company_logo = ""
            
            # Location
            locations = job.get("locations", [])
            location = locations[0].get("label", "") if locations else ""
            
            # Work Type
            work_type_val = job.get("workType", "")
            
            # Build URL
            job_id = job.get("id", "")
            detail_url = f"https://id.jobstreet.com/id/job/{job_id}"
            
            # Extract requirements/description
            desc = job.get("teaser", "")
            
            # Build item
            item_data = {
                "title": title,
                "company_name": company_name,
                "company_logo": company_logo,
                "location": location,
                "job_type": work_type_val,
                "work_type": "onsite", # default
                "salary_min": None,
                "salary_max": None,
                "salary_currency": "IDR",
                "source_url": detail_url,
                "description": desc,
                "requirements": "",
            }
            
            yield self.build_job_item(item_data)

        # Pagination
        current_page = response.meta.get("page", 1)
        total_pages = data.get("results", {}).get("results", {}).get("totalPages", 1)
        
        if current_page < total_pages and self._should_continue_pagination():
            next_page = current_page + 1
            next_url = self._build_search_url(page=next_page)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={"page": next_page},
                headers=response.request.headers
            )
