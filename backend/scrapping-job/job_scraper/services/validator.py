import re
from urllib.parse import urlparse

from job_scraper.logger import get_logger

logger = get_logger("services.validator")


class ValidationError(Exception):
    def __init__(self, field: str, reason: str) -> None:
        self.field = field
        self.reason = reason
        super().__init__(f"Validation failed for '{field}': {reason}")


class ValidatorService:
    REQUIRED_FIELDS: list[str] = ["title", "company_name", "platform", "source_url"]

    MAX_LENGTHS: dict[str, int] = {
        "title": 500, "company_name": 300, "location": 300,
        "city": 100, "province": 100, "country": 100,
        "category": 200, "platform": 50, "job_type": 50,
        "employment_type": 50, "work_type": 50, "experience_level": 50,
        "salary_currency": 10, "company_website": 500,
    }

    def validate(self, item: dict) -> tuple[bool, list[str]]:
        errors: list[str] = []

        for field in self.REQUIRED_FIELDS:
            if not item.get(field):
                errors.append(f"Missing required field: {field}")

        for url_field in ["source_url", "apply_url", "company_website", "company_logo"]:
            if item.get(url_field) and not self._is_valid_url(item[url_field]):
                errors.append(f"Invalid URL for {url_field}: {item[url_field]}")

        for field, max_len in self.MAX_LENGTHS.items():
            if item.get(field) and len(str(item[field])) > max_len:
                errors.append(f"Field '{field}' exceeds max length ({max_len}): {len(str(item[field]))} chars")

        salary_errors = self._validate_salary(item)
        errors.extend(salary_errors)

        if item.get("platform"):
            valid_platforms = [
                "jobstreet", "glints", "kalibrr",
                "linkedin", "techinasia",
                "kitalulus", "pintarnya",
            ]
            if item["platform"] not in valid_platforms:
                errors.append(f"Unknown platform: {item['platform']}")

        if item.get("title") and not self._is_valid_title(item["title"]):
            errors.append(f"Invalid title: {item['title']}")

        if errors:
            logger.warning(
                "Validation failed for item '%s': %s",
                item.get("title", "unknown"), "; ".join(errors),
            )

        return len(errors) == 0, errors

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme in ("http", "https"), result.netloc])
        except Exception:
            return False

    @staticmethod
    def _validate_salary(item: dict) -> list[str]:
        errors: list[str] = []
        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")

        if salary_min is not None:
            if not isinstance(salary_min, (int, float)) or salary_min < 0:
                errors.append(f"Invalid salary_min: {salary_min}")

        if salary_max is not None:
            if not isinstance(salary_max, (int, float)) or salary_max < 0:
                errors.append(f"Invalid salary_max: {salary_max}")

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                item["salary_min"], item["salary_max"] = salary_max, salary_min

        return errors

    @staticmethod
    def _is_valid_title(title: str) -> bool:
        if len(title) < 3:
            return False
        if re.match(r"^[\d\W]+$", title):
            return False
        if re.match(r"^(.)\1{4,}$", title):
            return False
        return True
