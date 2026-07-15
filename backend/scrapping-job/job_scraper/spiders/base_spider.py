"""
BaseSpider — Abstract base class for all job spiders.
=====================================================

Provides shared functionality for all platform-specific spiders:
- Playwright request helpers
- Pagination handling
- Error handling and retry logic
- Item construction
- Stats tracking
"""

from abc import abstractmethod
from datetime import datetime, timezone
from typing import Any, Generator

import scrapy
from scrapy.http import Response

from job_scraper.constants import DEFAULT_HEADERS, MAX_PAGES_PER_RUN, Platform
from job_scraper.items import JobItem
from job_scraper.logger import get_logger, get_stats_logger
from job_scraper.utils import extract_skills_from_text, normalize_url, parse_date


class BaseSpider(scrapy.Spider):
    """
    Abstract base spider with shared scraping functionality.

    All platform-specific spiders must extend this class and implement:
    - platform_name: The platform identifier
    - start_url: The starting URL for scraping
    - parse(): Parse listing pages
    - parse_detail(): Parse individual job detail pages

    Provides common helpers for Playwright requests, pagination,
    and JobItem construction.
    """

    # Must be overridden by subclasses
    platform_name: str = ""
    start_url: str = ""

    # Configuration
    max_pages: int = MAX_PAGES_PER_RUN
    use_playwright: bool = True

    # Custom settings per spider (can be overridden)
    custom_settings: dict[str, Any] = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the spider with tracking counters.

        Accepts optional keyword arguments:
        - max_pages: Override maximum pages to scrape
        - job_type: Filter by job type ('fulltime', 'parttime', etc.)
        - work_type: Filter by work type ('remote', 'onsite', etc.)
        - keyword: Search keyword
        - location: Search location
        """
        super().__init__(*args, **kwargs)

        self.logger_custom = get_logger(f"spiders.{self.name}")
        self.stats_logger = get_stats_logger()

        # Override from CLI arguments
        self.max_pages = int(kwargs.get("max_pages", self.max_pages))
        self.job_type_filter = kwargs.get("job_type", None)
        self.work_type_filter = kwargs.get("work_type", None)
        self.keyword = kwargs.get("keyword", None)
        self.location_filter = kwargs.get("location", None)

        # Tracking
        self._page_count: int = 0
        self._item_count: int = 0
        self._error_count: int = 0
        self._start_time: datetime = datetime.now(timezone.utc)

    async def start(self) -> Any:
        """
        Generate the initial requests.

        Uses Playwright for JavaScript-rendered pages.
        """
        url = self._build_start_url()
        self.logger_custom.info(
            "Starting spider '%s' for platform '%s' | URL: %s",
            self.name, self.platform_name, url,
        )

        yield self._make_request(url, callback=self.parse)

    def _build_start_url(self) -> str:
        """
        Build the starting URL with optional filters.

        Override in subclasses for platform-specific URL building.

        Returns:
            The starting URL string.
        """
        return self.start_url

    def _make_request(
        self,
        url: str,
        callback: Any = None,
        meta: dict | None = None,
        errback: Any = None,
        dont_filter: bool = False,
    ) -> scrapy.Request:
        """
        Create a Scrapy request with Playwright support.

        Args:
            url: URL to request.
            callback: Response callback function.
            meta: Additional request metadata.
            errback: Error callback function.
            dont_filter: If True, don't filter duplicate requests.

        Returns:
            Configured Scrapy Request.
        """
        request_meta: dict[str, Any] = {
            "playwright": self.use_playwright,
            "playwright_include_page": False,
        }

        if self.use_playwright:
            request_meta["playwright_page_methods"] = self._get_page_methods()

        if meta:
            request_meta.update(meta)

        return scrapy.Request(
            url=url,
            callback=callback or self.parse,
            errback=errback or self.handle_error,
            meta=request_meta,
            headers=DEFAULT_HEADERS,
            dont_filter=dont_filter,
        )

    def _get_page_methods(self) -> list:
        """
        Get Playwright page methods for waiting on dynamic content.

        Override in subclasses for platform-specific wait conditions.

        Returns:
            List of PageMethod instances.
        """
        from scrapy_playwright.page import PageMethod

        return [
            PageMethod("wait_for_load_state", "networkidle"),
        ]

    def _should_continue_pagination(self) -> bool:
        """
        Check if pagination should continue.

        Returns:
            True if more pages should be scraped.
        """
        self._page_count += 1

        if self._page_count > self.max_pages:
            self.logger_custom.info(
                "Reached max pages limit (%d). Stopping pagination.",
                self.max_pages,
            )
            return False

        return True

    def build_job_item(self, data: dict) -> JobItem:
        """
        Build a JobItem from extracted data dictionary.

        Sets platform, timestamps, and extracts skills if not provided.

        Args:
            data: Dictionary of extracted job data.

        Returns:
            Populated JobItem instance.
        """
        item = JobItem()

        # Set all provided fields
        for field in JobItem.fields:
            if field in data and data[field] is not None:
                item[field] = data[field]

        # Ensure platform is set
        if "platform" not in item or not item["platform"]:
            item["platform"] = self.platform_name

        # Set timestamps
        now = datetime.now(timezone.utc)
        if "scraped_at" not in item:
            item["scraped_at"] = now
        if "updated_at" not in item:
            item["updated_at"] = now

        # Set defaults
        if "country" not in item or not item.get("country"):
            item["country"] = "Indonesia"
        if "is_internship" not in item:
            item["is_internship"] = False
        if "skills" not in item:
            item["skills"] = []
        if "tags" not in item:
            item["tags"] = []

        # Auto-extract skills from description if empty
        if not item.get("skills") and item.get("description"):
            item["skills"] = extract_skills_from_text(item["description"])

        # Parse dates if they're strings
        for date_field in ["posting_date", "expired_date"]:
            if item.get(date_field) and isinstance(item[date_field], str):
                item[date_field] = parse_date(item[date_field])

        # Normalize URLs
        if item.get("source_url"):
            item["source_url"] = normalize_url(item["source_url"])
        if item.get("apply_url"):
            item["apply_url"] = normalize_url(item["apply_url"])

        self._item_count += 1
        return item

    def handle_error(self, failure) -> None:
        """
        Handle request errors with logging.

        Args:
            failure: Twisted Failure instance.
        """
        self._error_count += 1
        self.logger_custom.error(
            "Request failed: %s | URL: %s",
            failure.getErrorMessage(),
            failure.request.url if hasattr(failure, "request") else "unknown",
        )

    @abstractmethod
    def parse(self, response: Response) -> Any:
        """
        Parse the listing page.

        Must be implemented by subclasses to extract job listings
        and follow pagination.

        Args:
            response: Scrapy Response object.

        Yields:
            JobItem instances or further Requests.
        """
        raise NotImplementedError

    def parse_detail(self, response: Response) -> Any:
        """
        Parse an individual job detail page.

        Override in subclasses that follow detail pages.

        Args:
            response: Scrapy Response object.

        Yields:
            JobItem instance.
        """
        raise NotImplementedError

    def closed(self, reason: str) -> None:
        """
        Called when the spider closes. Logs final statistics.

        Args:
            reason: Reason for closing.
        """
        duration = (datetime.now(timezone.utc) - self._start_time).total_seconds()

        self.logger_custom.info(
            "Spider '%s' closed. Reason: %s", self.name, reason,
        )

        self.stats_logger.info(
            "SPIDER CLOSED | Name: %s | Platform: %s | "
            "Pages: %d | Items: %d | Errors: %d | Duration: %.1fs | Reason: %s",
            self.name,
            self.platform_name,
            self._page_count,
            self._item_count,
            self._error_count,
            duration,
            reason,
        )
