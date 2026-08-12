from collections.abc import AsyncIterator
from typing import Any

import scrapy
from scrapy.http import Request, Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.items import JobItem
from job_scraper.logger import get_logger, get_stats_logger


class BaseSpider(scrapy.Spider):
    name: str = ""
    platform_name: Platform | None = None
    start_url: str = ""
    use_playwright: bool = False

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.logger_custom = get_logger(f"spiders.{self.name}")
        self.stats_logger = get_stats_logger()

        self.max_pages = int(kwargs.get("max_pages", 100))
        self.max_detail_pages = int(kwargs.get("max_detail_pages", 15))
        self.keyword = kwargs.get("keyword", None)
        self.location_filter = kwargs.get("location", None)

        self._page_count = 0
        self._item_count = 0
        self._error_count = 0
        self._detail_count = 0

    async def start(self) -> AsyncIterator[Any]:
        url = self._build_start_url()
        self.logger_custom.info("Starting spider '%s' for platform '%s' | URL: %s", self.name, self.platform_name, url)
        if self.use_playwright:
            yield Request(url=url, callback=self.parse, meta=self._playwright_meta(self._get_page_methods()), dont_filter=True)
        else:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def _build_start_url(self) -> str:
        return self.start_url

    def _get_page_methods(self) -> list:
        return [PageMethod("wait_for_load_state", "networkidle")]

    def _playwright_meta(self, page_methods: list | None = None) -> dict:
        return dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_goto_kwargs={"wait_until": "domcontentloaded", "timeout": 30000},
            playwright_page_methods=page_methods or self._get_page_methods(),
        )

    def _should_continue_pagination(self, force: bool = False) -> bool:
        if force:
            return True
        return self._page_count < self.max_pages

    def _make_request(self, url: str, callback, meta: dict | None = None) -> Request:
        if self.use_playwright:
            req_meta = self._playwright_meta()
            if meta:
                req_meta.update(meta)
            return Request(url=url, callback=callback, meta=req_meta)
        return Request(url=url, callback=callback, meta=meta or {})

    def _make_detail_request(self, url: str, callback, meta: dict | None = None) -> Request:
        req_meta = dict(
            playwright=True,
            playwright_page_goto_kwargs={"wait_until": "domcontentloaded", "timeout": 30000},
            playwright_page_methods=[PageMethod("wait_for_timeout", 2000)],
            is_detail=True,
        )
        if meta:
            req_meta.update(meta)
        return Request(url=url, callback=callback, meta=req_meta)

    def _desc_text(self, response: Response, selector: str) -> str:
        return response.css(selector).xpath("string(.)").get("").strip()

    def _normalize_job_type(self, raw: str) -> str:
        if not raw:
            return ""
        t = raw.strip().lower()
        if ("full" in t and "time" in t) or "penuh waktu" in t:
            return "Full-time"
        if ("part" in t and "time" in t) or "paruh waktu" in t:
            return "Part-time"
        if "contract" in t or "kontrak" in t:
            return "Contract"
        if "freelance" in t:
            return "Freelance"
        if "intern" in t or "magang" in t:
            return "Internship"
        if "temporary" in t or "sementara" in t:
            return "Temporary"
        return raw.strip()

    def _normalize_work_type(self, raw: str) -> str:
        if not raw:
            return ""
        w = raw.strip().lower()
        if "remote" in w or "wfh" in w or "jarak jauh" in w or "dari manapun" in w:
            return "Remote"
        if "hybrid" in w:
            return "Hybrid"
        if "lapangan" in w or "fieldwork" in w:
            return "On-site"
        if "onsite" in w or "on-site" in w or "kantor" in w:
            return "On-site"
        return raw.strip()

    def build_job_item(self, data: dict) -> JobItem:
        item = JobItem()
        item["platform"] = self.platform_name
        for key, value in data.items():
            if value is not None:
                item[key] = value
        self._item_count += 1
        return item

    def closed(self, reason: str) -> None:
        duration = (self.stats_logger or self.logger_custom)
        duration.info(
            "SPIDER CLOSED | Name: %s | Platform: %s | Pages: %d | Items: %d | Errors: %d | Reason: %s",
            self.name, self.platform_name, self._page_count, self._item_count, self._error_count, reason,
        )
