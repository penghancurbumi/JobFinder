"""
Glints Spider — Scrapes job listings from Glints.
=================================================

Handles dynamic rendering via Playwright.
"""

from typing import Any, Generator

import scrapy
from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class GlintsSpider(BaseSpider):
    """Spider for Glints platform."""

    name = "glints"
    platform_name = Platform.GLINTS
    start_url = "https://glints.com/id/opportunities/jobs/explore"

    # Glints uses intense client-side rendering
    use_playwright = True

    def _build_start_url(self) -> str:
        """Add filters to URL if provided."""
        url = self.start_url
        params = []

        if self.keyword:
            params.append(f"keyword={self.keyword}")
        if self.location_filter:
            params.append(f"locations={self.location_filter}")

        if params:
            url = f"{url}?{'&'.join(params)}"

        return url

    def _get_page_methods(self) -> list:
        """Wait for job cards to render."""
        return [
            PageMethod("wait_for_selector", "div.JobCardsc__JobcardContainer-sc-1f9hdu8-0, div[class*='JobCardsc']", timeout=30000),
            PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
            PageMethod("wait_for_timeout", 2000),  # Give time for images/data to load
        ]

    def parse(self, response: Response) -> Generator[Any, None, None]:
        """Parse job cards from listing page."""
        self.logger_custom.info("Parsing listing page: %s", response.url)

        # Job card selector (might change over time)
        job_cards = response.css("div.JobCardsc__JobcardContainer-sc-1f9hdu8-0, div[class*='JobCardsc']")

        if not job_cards:
            self.logger_custom.warning("No job cards found on page %s. Selectors might have changed.", response.url)
            # Try to grab page source for debugging
            # html_preview = response.text[:500]
            # self.logger_custom.debug("Page preview: %s", html_preview)
            return

        for card in job_cards:
            # Extract basic info
            title = card.css("h3::text, h2::text, div[class*='Title']::text").get()
            company = card.css("a[class*='Company']::text, div[class*='Company']::text, span[class*='Company']::text").get()
            location = card.css("div[class*='Location'] span::text, span[class*='Location']::text").get()
            salary = card.css("div[class*='Salary'] span::text, span[class*='Salary']::text").get()
            
            # Find the detail link
            detail_url = card.css("a::attr(href)").get()

            # Sometimes title/company might be deeply nested. Fallbacks:
            if not title:
                title = card.css("::text").get()
            
            if not company:
                links = card.css("a::text").getall()
                if len(links) > 1:
                    company = links[1]

            # If we don't have a detail URL, just build item from what we have
            if not detail_url:
                data = {
                    "title": title,
                    "company_name": company,
                    "location": location,
                    "_raw_salary": salary,
                    "source_url": response.url,  # Fallback to current page
                }
                yield self.build_job_item(data)
                continue

            # Follow detail page
            full_url = response.urljoin(detail_url)
            
            # Pass data to detail parser
            meta = {
                "item_data": {
                    "title": title,
                    "company_name": company,
                    "location": location,
                    "_raw_salary": salary,
                    "source_url": full_url,
                }
            }
            
            yield self._make_request(
                url=full_url,
                callback=self.parse_detail,
                meta=meta,
                # Detail pages also need Playwright for Glints
            )

        # Handle pagination
        if self._should_continue_pagination():
            # Find next page button
            next_btn = response.css("button[aria-label='Next Page']:not([disabled]), a[aria-label='Next Page']")
            if next_btn:
                self.logger_custom.info("Found next page button, following...")
                # Unfortunately Glints pagination relies heavily on React state.
                # A more robust approach is modifying URL ?page=X if they support it.
                # Let's try incrementing page parameter
                import re
                current_page = 1
                page_match = re.search(r'page=(\d+)', response.url)
                if page_match:
                    current_page = int(page_match.group(1))
                
                next_page = current_page + 1
                
                if '?' in response.url:
                    if 'page=' in response.url:
                        next_url = re.sub(r'page=\d+', f'page={next_page}', response.url)
                    else:
                        next_url = f"{response.url}&page={next_page}"
                else:
                    next_url = f"{response.url}?page={next_page}"
                    
                yield self._make_request(next_url, callback=self.parse)
            else:
                self.logger_custom.info("No next page button found. Stopping pagination.")

    def parse_detail(self, response: Response) -> Generator[Any, None, None]:
        """Parse the job detail page."""
        self.logger_custom.info("Parsing detail page: %s", response.url)
        item_data = response.meta.get("item_data", {})

        # Refine data from detail page
        # Glints detail page has a specific structure
        
        # Try to find description
        desc_container = response.css("div.JobDescription__Container-sc-19h7vwe-0, div[class*='JobDescription']")
        if desc_container:
            item_data["description"] = desc_container.get()
            
        # Try to find requirements specifically
        req_container = response.css("div[class*='Requirement']")
        if req_container:
            item_data["requirements"] = req_container.get()

        # Job type, experience, etc are usually in an overview section
        overview_items = response.css("div[class*='Overview'] span::text").getall()
        for item in overview_items:
            item = item.lower()
            if "tahun" in item or "year" in item:
                item_data["experience_level"] = item
            elif any(x in item for x in ["full-time", "part-time", "contract", "internship"]):
                item_data["job_type"] = item

        # Company website/logo
        logo = response.css("img[class*='CompanyLogo']::attr(src)").get()
        if logo:
            item_data["company_logo"] = logo

        yield self.build_job_item(item_data)
