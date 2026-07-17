import re
from typing import Any, Generator

import scrapy
from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class PintarnyaSpider(BaseSpider):
    name = "pintarnya"
    platform_name = Platform.PINTARNYA
    start_url = "https://www.pintarnya.com/kerja/search"

    use_playwright = True

    def _build_start_url(self) -> str:
        url = self.start_url
        params = []
        if self.keyword:
            params.append(f"search={self.keyword}")
        if self.location_filter:
            params.append(f"lokasi={self.location_filter}")
        if params:
            url = f"{url}?{'&'.join(params)}"
        return url

    def _get_page_methods(self) -> list:
        return [
            PageMethod("wait_for_load_state", "networkidle"),
            PageMethod("wait_for_timeout", 3000),
        ]

    def parse(self, response: Response) -> Generator[Any, None, None]:
        self.logger_custom.info("Parsing listing page: %s", response.url)

        job_cards = response.css("a[href*='/pekerjaan/'], a[href*='/job/'], div[class*='job'] a[href]")
        if not job_cards:
            job_cards = response.css("div[class*='card'] a[href], div[class*='item'] a[href], div[class*='list'] a[href]")

        if not job_cards:
            self.logger_custom.warning("No job cards found on %s", response.url)
            return

        seen_urls = set()
        for card in job_cards:
            detail_url = card.attrib.get("href", "")
            if not detail_url or detail_url in seen_urls:
                continue
            seen_urls.add(detail_url)

            full_url = response.urljoin(detail_url)

            container = card.xpath("ancestor::div[contains(@class, 'card') or contains(@class, 'item')] | .")
            if isinstance(container, list):
                container = card

            title = container.css("h1::text, h2::text, h3::text, [class*='title'] ::text, [class*='position'] ::text, [class*='name'] ::text").get()
            if not title:
                title = card.css("::text").get()

            company = container.css("[class*='company'] ::text, [class*='employer'] ::text, [class*='perusahaan'] ::text").get()

            location = container.css("[class*='location'] ::text, [class*='lokasi'] ::text, [class*='place'] ::text").get()

            salary_text = container.css("[class*='salary'] ::text, [class*='gaji'] ::text").get()
            salary_min, salary_max = None, None
            if salary_text:
                numbers = re.findall(r"(\d[\d.]*)", salary_text.replace("Rp", "").replace("rp", ""))
                parsed = []
                for n in numbers:
                    clean = n.replace(".", "")
                    try:
                        parsed.append(int(clean))
                    except ValueError:
                        pass
                if len(parsed) >= 2:
                    salary_min, salary_max = parsed[0], parsed[1]
                elif len(parsed) == 1:
                    salary_min = parsed[0]

            item_data = {
                "title": title,
                "company_name": company,
                "location": location,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_currency": "IDR" if salary_min or salary_max else None,
                "source_url": full_url,
            }

            yield self.build_job_item(item_data)

        if self._should_continue_pagination():
            next_btn = response.css("a[rel='next'], a[aria-label='Next'], button[aria-label='Next'], [class*='pagination'] a:last-child, [class*='next'] a, [class*='next'] button")
            if next_btn:
                next_url = next_btn.attrib.get("href")
                if next_url:
                    yield self._make_request(response.urljoin(next_url), callback=self.parse)
