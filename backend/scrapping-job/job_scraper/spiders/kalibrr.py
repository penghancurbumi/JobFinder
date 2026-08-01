from typing import Any

from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class KalibrrSpider(BaseSpider):
    name = "kalibrr"
    platform_name = Platform.KALIBRR
    start_url = "https://www.kalibrr.id/job-board/te/all"
    use_playwright = True

    def _build_start_url(self) -> str:
        params = []
        if self.keyword:
            params.append(f"q={self.keyword}")
        url = self.start_url
        if params:
            url = f"{url}?{'&'.join(params)}"
        return url

    def _get_page_methods(self) -> list:
        return [
            PageMethod("wait_for_selector", "div[itemtype='http://schema.org/ItemList']", timeout=20000),
            PageMethod("wait_for_timeout", 2000),
        ]

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing Kalibrr response")
        cards = response.css("div[itemtype='http://schema.org/ItemList'] > div")
        if not cards:
            self.logger_custom.warning("No job cards found")
            return

        for card in cards:
            title = self._text(card, "a[itemprop='name']")
            company = self._text(card, "a.k-text-subdued.k-font-bold")
            location = self._text(card, "span.k-text-gray-500.k-block")
            job_type = self._text(card, "span[itemprop='employmentType']")

            href = card.css("a[itemprop='name']::attr(href)").get("").strip()
            if not title and not href:
                continue

            item_data = {
                "title": title,
                "company_name": company,
                "location": location,
                "source_url": response.urljoin(href) if href else response.url,
            }
            if job_type:
                item_data["job_type"] = job_type

            if self._detail_count < self.max_detail_pages and item_data["source_url"] != response.url:
                self._detail_count += 1
                yield self._make_detail_request(item_data["source_url"], self.parse_detail, meta={"item_data": item_data})
            else:
                yield self.build_job_item(item_data)

    def parse_detail(self, response: Response) -> Any:
        self.logger_custom.info("Parsing Kalibrr detail: %s", response.url)
        item_data = response.meta.get("item_data", {})

        desc = self._desc_text(response, "div[itemprop='description']")
        if desc:
            item_data["description"] = desc

        yield self.build_job_item(item_data)

    def _text(self, element, selector: str) -> str:
        return element.css(f"{selector}::text").get("").strip()
