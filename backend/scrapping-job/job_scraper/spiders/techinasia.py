from typing import Any

from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class TechInAsiaSpider(BaseSpider):
    name = "techinasia"
    platform_name = Platform.TECHINASIA
    start_url = "https://www.techinasia.com/jobs/search"
    use_playwright = True

    def _build_start_url(self) -> str:
        params = []
        if self.keyword:
            params.append(f"keyword={self.keyword}")
        url = self.start_url
        if params:
            url = f"{url}?{'&'.join(params)}"
        return url

    def _get_page_methods(self) -> list:
        return [
            PageMethod("wait_for_selector", "div.job-item", timeout=20000),
            PageMethod("wait_for_timeout", 2000),
        ]

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing TechInAsia listing page: %s", response.url)
        cards = response.css("div.job-item")
        if not cards:
            self.logger_custom.warning("No job cards found")
            return

        for card in cards:
            title = self._text(card, "h3.job-title a")
            company = self._text(card, "div.company-name a")
            industry = self._text(card, "span.industry")
            location = self._text(card, "div.job-details-item span.label")
            work_type = self._text(card, "div.work-type-badge span")

            href = card.css("h3.job-title a::attr(href)").get("").strip()
            if not href:
                href = card.css("div.job-header-inner a::attr(href)").get("").strip()
            if not title and not href:
                continue

            item_data = {
                "title": title,
                "company_name": company,
                "location": location,
                "source_url": response.urljoin(href) if href else response.url,
            }
            if industry:
                item_data["category"] = industry
            if work_type:
                item_data["work_type"] = work_type

            if self._detail_count < self.max_detail_pages and item_data["source_url"] != response.url:
                self._detail_count += 1
                yield self._make_detail_request(item_data["source_url"], self.parse_detail, meta={"item_data": item_data})
            else:
                yield self.build_job_item(item_data)

    def parse_detail(self, response: Response) -> Any:
        self.logger_custom.info("Parsing TechInAsia detail: %s", response.url)
        item_data = response.meta.get("item_data", {})

        desc = response.xpath(
            "//section[contains(normalize-space(.), 'Job description & requirements')]"
        ).xpath("string(.)").get("").strip()
        if desc:
            for prefix in ("Job description & requirements", "Job Description", "Job Description & Requirements"):
                if desc.startswith(prefix):
                    desc = desc[len(prefix):].strip()
                    break
            item_data["description"] = desc

        yield self.build_job_item(item_data)

    def _text(self, element, selector: str) -> str:
        return element.css(f"{selector}::text").get("").strip()
