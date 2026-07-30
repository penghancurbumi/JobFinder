import json
import re
from typing import Any

import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.logger import get_logger, get_stats_logger
from job_scraper.spiders.base_spider import BaseSpider


class LinkedInSpider(BaseSpider):
    name = "linkedin"
    platform_name = Platform.LINKEDIN
    start_url = "https://www.linkedin.com/jobs/search"
    use_playwright = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._page_count = 0
        self._item_count = 0
        self._error_count = 0

    async def start(self):
        url = self._build_start_url()
        self.logger_custom.info("Starting LinkedIn spider | URL: %s", url)
        yield Request(
            url=url,
            callback=self.parse,
            meta=self._playwright_meta(self._get_page_methods()),
            dont_filter=True,
        )

    def _build_start_url(self) -> str:
        params = []
        if self.keyword:
            params.append(f"keywords={self.keyword}")
        params.append(f"location={self.location_filter or 'Indonesia'}")
        params.append("start=0")
        return f"{self.start_url}?{'&'.join(params)}"

    def _get_page_methods(self) -> list:
        return [
            PageMethod("wait_for_selector",
                       "ul.jobs-search__results-list, div.jobs-search-results-list, "
                       "ul.job-search-results, li[data-occludable-job-id]",
                       timeout=30000),
            PageMethod("wait_for_timeout", 2000),
        ]

    def _make_request(self, url: str, callback, meta: dict | None = None) -> Request:
        if meta and meta.get("_detail_page"):
            req_meta = dict(
                playwright=True,
                playwright_page_goto_kwargs={"wait_until": "domcontentloaded", "timeout": 15000},
                playwright_page_methods=[PageMethod("wait_for_timeout", 1000)],
            )
        else:
            req_meta = self._playwright_meta(self._get_page_methods())
        if meta:
            req_meta.update(meta)
        return Request(url=url, callback=callback, meta=req_meta)

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing LinkedIn listing page: %s", response.url)

        page_text = response.css("title::text").get("")
        self.logger_custom.info("Page title: %s", page_text)

        job_cards = self._extract_job_cards(response)
        if not job_cards:
            self.logger_custom.warning("No job cards found. LinkedIn may be showing login/block page.")
            return

        for card in job_cards:
            item_data = self._extract_card_data(card, response)
            detail_url = item_data.get("source_url", "")
            if not detail_url:
                yield self.build_job_item(item_data)
                continue
            yield self._make_request(url=detail_url, callback=self.parse_detail, meta={"item_data": item_data, "_detail_page": True})

        if self._should_continue_pagination():
            next_url = self._next_page_url(response.url)
            if next_url:
                self.logger_custom.info("Following pagination to: %s", next_url)
                yield self._make_request(next_url, callback=self.parse)

    def _extract_job_cards(self, response) -> list:
        selectors = [
            "ul.jobs-search__results-list > li",
            "div.jobs-search-results-list li",
            "ul.job-search-results > li",
            "div.scaffold-layout__list-container li",
            "li[data-occludable-job-id]",
            "div.job-card-container",
            "div[data-job-id]",
        ]
        for selector in selectors:
            cards = response.css(selector)
            if cards:
                return cards
        return []

    def _extract_card_data(self, card, response: Response) -> dict:
        job_id = card.attrib.get("data-occludable-job-id", "")

        title = self._extract_text(card, [
            "h3.base-search-card__title::text",
            "a.job-card-list__title::text",
            "span[class*='job-title']::text",
            "a[class*='job-title'] span::text",
            "a[data-tracking-control-name*='job-card'] span::text",
            "div.job-card-container__job-title::text",
            "a.job-card-search__title::text",
        ])

        company = self._extract_text(card, [
            "h4.base-search-card__subtitle::text",
            "a.job-card-container__company-name::text",
            "span[class*='company-name']::text",
            "div.job-card-container__company-name::text",
        ])

        location = self._extract_text(card, [
            "span.job-search-card__location::text",
            "span[class*='location']::text",
            "li.job-card-container__metadata-item::text",
        ])

        detail_url = self._extract_attr(card, [
            "a.base-card__full-link::attr(href)",
            "a.job-card-list__title::attr(href)",
            "a[class*='job-title']::attr(href)",
            "a[data-tracking-control-name*='result']::attr(href)",
            "a.job-card-search__title::attr(href)",
            "a::attr(href)",
        ])

        if not detail_url and job_id:
            detail_url = f"https://www.linkedin.com/jobs/view/{job_id}/"

        return {
            "title": title.strip() if title else "",
            "company_name": company.strip() if company else "",
            "location": location.strip() if location else "",
            "source_url": response.urljoin(detail_url) if detail_url else response.url,
        }

    def _extract_text(self, element, selectors: list) -> str:
        for selector in selectors:
            text = element.css(selector).get()
            if text:
                return text.strip()
        return ""

    def _extract_attr(self, element, selectors: list) -> str:
        for selector in selectors:
            val = element.css(selector).get()
            if val:
                return val.strip()
        return ""

    def _next_page_url(self, current_url: str) -> str | None:
        start_match = re.search(r'[?&]start=(\d+)', current_url)
        current_start = int(start_match.group(1)) if start_match else 0
        next_start = current_start + 25
        if '?' not in current_url:
            return None
        base_url = re.sub(r'[?&]start=\d+', '', current_url)
        separator = '&' if '?' in base_url else '?'
        return f"{base_url}{separator}start={next_start}"

    def parse_detail(self, response: Response) -> Any:
        self.logger_custom.info("Parsing detail page: %s", response.url)
        item_data = response.meta.get("item_data", {})

        json_data = self._extract_json_ld(response)
        if json_data:
            item_data.update(self._parse_json_ld(json_data))

        desc = self._extract_description(response)
        if desc:
            item_data["description"] = desc

        criteria = self._extract_criteria(response)
        item_data.update(criteria)

        skills = self._extract_skills(response)
        if skills:
            item_data["skills"] = skills

        yield self.build_job_item(item_data)

    def _extract_json_ld(self, response) -> dict | list | None:
        script = response.css('script[type="application/ld+json"]::text').get()
        if not script:
            return None
        try:
            return json.loads(script)
        except (json.JSONDecodeError, ValueError):
            return None

    def _parse_json_ld(self, data) -> dict:
        if isinstance(data, list):
            data = data[0] if data else {}
        result = {}
        if data.get("title"):
            result["title"] = data["title"]
        if data.get("description"):
            result["description"] = data["description"]
        if data.get("datePosted"):
            result["posting_date"] = data["datePosted"]
        if data.get("validThrough"):
            result["expired_date"] = data["validThrough"]
        if data.get("employmentType"):
            result["job_type"] = data["employmentType"]

        hiring_org = data.get("hiringOrganization") or data.get("hiring_organization") or {}
        if isinstance(hiring_org, dict):
            if hiring_org.get("name"):
                result["company_name"] = hiring_org["name"]
            if hiring_org.get("logo"):
                result["company_logo"] = hiring_org["logo"]

        job_location = data.get("jobLocation") or data.get("job_location") or []
        if isinstance(job_location, list) and job_location:
            loc = job_location[0]
        elif isinstance(job_location, dict):
            loc = job_location
        else:
            loc = {}

        if isinstance(loc, dict):
            address = loc.get("address", {}) or loc
            if isinstance(address, dict):
                address_locality = address.get("addressLocality", "")
                address_region = address.get("addressRegion", "")
                address_country = address.get("addressCountry", "")
                result["location"] = address_locality or address_region or address_country
                if address_country:
                    result["country"] = address_country

        base_salary = data.get("baseSalary") or data.get("salary") or {}
        if isinstance(base_salary, dict):
            result["salary_currency"] = base_salary.get("currency", "IDR")
            value = base_salary.get("value", {})
            if isinstance(value, dict):
                result["salary_min"] = value.get("minValue")
                result["salary_max"] = value.get("maxValue")

        skills = data.get("skills", [])
        if skills:
            if isinstance(skills[0], dict):
                skills = [s.get("name", "") for s in skills if isinstance(s, dict)]
            result["skills"] = [s for s in skills if s]

        return result

    def _extract_description(self, response) -> str:
        for selector in [
            "div.description__text",
            "div.show-more-less-html__markup",
            "article",
            "div[class*='description']",
            "section[class*='description']",
        ]:
            container = response.css(selector)
            if container:
                texts = container.css("::text").getall()
                return "\n".join(t.strip() for t in texts if t.strip())
        return ""

    def _extract_criteria(self, response) -> dict:
        criteria = {}
        criteria_items = response.css("li.description__job-criteria-item")
        if not criteria_items:
            criteria_items = response.css(
                "div[class*='job-criteria'] li, ul[class*='criteria'] li, div[class*='metadata'] li"
            )

        for item in criteria_items:
            label = (item.css("h3::text").get() or item.css("span:first-child::text").get() or "").lower().strip()
            value = (item.css("span[class*='criteria']::text").get() or item.css("span:last-child::text").get() or "").strip()

            if "employment" in label or "job type" in label:
                criteria["job_type"] = value
            elif "seniority" in label or "experience" in label:
                criteria["experience_level"] = value
            elif "work" in label or "remote" in label:
                criteria["work_type"] = value

        return criteria

    def _extract_skills(self, response) -> list:
        skills = response.css(
            "a[class*='skill']::text, span[class*='skill']::text, "
            "li[class*='skill']::text, div[class*='skill']::text"
        ).getall()
        return list(set(s.strip() for s in skills if s.strip()))
