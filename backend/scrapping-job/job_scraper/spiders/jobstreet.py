import re
from typing import Any

from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from job_scraper.constants import Platform
from job_scraper.spiders.base_spider import BaseSpider


class JobstreetSpider(BaseSpider):
    name = "jobstreet"
    platform_name = Platform.JOBSTREET
    start_url = "https://id.jobstreet.com/id/job-search/all-jobs-in-indonesia"
    use_playwright = True

    def _build_start_url(self) -> str:
        params = []
        if self.keyword:
            params.append(f"keyword={self.keyword}")
        if self.location_filter:
            params.append(f"location={self.location_filter}")
        params.append("page=1")
        return f"{self.start_url}?{'&'.join(params)}"

    def _get_page_methods(self) -> list:
        return [
            PageMethod("wait_for_selector", "article[data-automation='normalJob']", timeout=20000),
            PageMethod("wait_for_timeout", 2000),
        ]

    def parse(self, response: Response) -> Any:
        self.logger_custom.info("Parsing JobStreet response")
        cards = response.css("article[data-automation='normalJob']")
        if not cards:
            self.logger_custom.warning("No job cards found")
            return

        for card in cards:
            title = self._text(card, "[data-automation='jobTitle']")
            company = self._text(card, "[data-automation='jobCompany']")
            location = self._text(card, "[data-automation='jobCardLocation']")
            salary = self._text(card, "[data-automation='jobSalary']")
            description = self._text(card, "[data-automation='jobShortDescription']")

            href = card.css("a[data-automation='job-list-view-job-link']::attr(href)").get("")
            if not href:
                href = card.css("a[data-automation='job-list-item-link-overlay']::attr(href)").get("")
            if not title and not href:
                continue

            item_data = {
                "title": title,
                "company_name": company,
                "location": location,
                "source_url": response.urljoin(href) if href else response.url,
            }
            if salary:
                parsed = self._parse_salary(salary)
                if parsed:
                    item_data.update(parsed)
            if description:
                item_data["description"] = description

            if self._detail_count < self.max_detail_pages and item_data["source_url"] != response.url:
                self._detail_count += 1
                yield self._make_detail_request(item_data["source_url"], self.parse_detail, meta={"item_data": item_data})
            else:
                yield self.build_job_item(item_data)

    def parse_detail(self, response: Response) -> Any:
        self.logger_custom.info("Parsing JobStreet detail: %s", response.url)
        item_data = response.meta.get("item_data", {})

        job_type = self._text(response, "[data-automation='job-detail-work-type']")
        if job_type:
            item_data["job_type"] = self._normalize_job_type(job_type)

        work_type = self._extract_arrangement_type(response.text)
        if work_type:
            item_data["work_type"] = self._normalize_work_type(work_type)

        desc = self._desc_text(response, "[data-automation='jobAdDetails']")
        if desc:
            item_data["description"] = desc

        yield self.build_job_item(item_data)

    def _extract_arrangement_type(self, text: str) -> str:
        idx = text.find("workArrangements")
        if idx == -1:
            return ""
        window = text[idx:idx + 1200]
        m = re.search(r'"type":\s*"(\w+)"', window)
        if m and m.group(1) in ("ONSITE", "REMOTE", "HYBRID"):
            return m.group(1)
        m2 = re.search(r'(ONSITE|REMOTE|HYBRID)', window)
        return m2.group(1) if m2 else ""

    def _text(self, element, selector: str) -> str:
        return element.css(selector).xpath("string(.)").get("").strip()

    def _parse_salary(self, salary: str) -> dict:
        salary = salary.replace("\xa0", " ").strip()
        result = {"salary_currency": "IDR"}
        digits = [d.replace(".", "").replace(",", "") for d in re.findall(r"Rp[.\d\s]+", salary)]
        if not digits:
            return result
        amounts = []
        for d in digits:
            nums = re.findall(r"\d[\d.]*", d.replace("Rp", "").strip())
            if nums:
                amounts.extend(int(n.replace(".", "")) for n in nums)
        if amounts:
            result["salary_min"] = min(amounts)
            result["salary_max"] = max(amounts)
        return result
