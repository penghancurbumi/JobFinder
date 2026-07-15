"""
Normalizer — Data normalization service.
========================================

Normalizes location, job type, work type, employment type,
salary, and company names to consistent formats using the
mappings defined in constants.py.
"""

import re

from job_scraper.constants import (
    CITY_NORMALIZATION,
    CURRENCY_MAPPING,
    EMPLOYMENT_TYPE_MAPPING,
    EXPERIENCE_LEVEL_MAPPING,
    JOB_TYPE_MAPPING,
    PROVINCE_MAPPING,
    WORK_TYPE_MAPPING,
)
from job_scraper.logger import get_logger
from job_scraper.utils import extract_salary

logger = get_logger("services.normalizer")


class NormalizerService:
    """
    Service for normalizing scraped data to consistent formats.

    Uses predefined mappings from constants.py to ensure all data
    follows the same conventions regardless of source platform.
    """

    def normalize_item(self, item: dict) -> dict:
        """
        Apply all normalization rules to a scraped item.

        Args:
            item: Scraped item dictionary.

        Returns:
            Normalized item dictionary.
        """
        item = self.normalize_location(item)
        item = self.normalize_job_type(item)
        item = self.normalize_work_type(item)
        item = self.normalize_employment_type(item)
        item = self.normalize_experience_level(item)
        item = self.normalize_salary(item)
        item = self.normalize_skills(item)
        item = self.normalize_country(item)

        logger.debug("Normalized item: %s", item.get("title", "unknown"))
        return item

    @staticmethod
    def normalize_location(item: dict) -> dict:
        """
        Normalize location fields: city, province, and location string.

        Attempts to extract city and province from the location string
        if they are not already set.

        Args:
            item: Item with location data.

        Returns:
            Item with normalized location fields.
        """
        location = item.get("location", "")
        city = item.get("city", "")
        province = item.get("province", "")

        if not location and not city:
            return item

        # Try to extract city from location string
        if location and not city:
            city = NormalizerService._extract_city(location)
            if city:
                item["city"] = city

        # Normalize city name
        if city:
            city_lower = city.strip().lower()
            if city_lower in CITY_NORMALIZATION:
                item["city"] = CITY_NORMALIZATION[city_lower]
                city = item["city"]

        # Derive province from city
        if city and not province:
            city_lower = city.strip().lower()
            if city_lower in PROVINCE_MAPPING:
                item["province"] = PROVINCE_MAPPING[city_lower]

        # Also try to derive province from location string
        if location and not item.get("province"):
            location_lower = location.strip().lower()
            for key, prov in PROVINCE_MAPPING.items():
                if key in location_lower:
                    item["province"] = prov
                    if not item.get("city"):
                        item["city"] = key.title()
                    break

        return item

    @staticmethod
    def _extract_city(location: str) -> str | None:
        """
        Extract city name from a location string.

        Handles formats like:
        - "Jakarta Selatan, DKI Jakarta"
        - "Bandung, Jawa Barat, Indonesia"
        - "Remote - Jakarta"

        Args:
            location: Raw location string.

        Returns:
            Extracted city name or None.
        """
        if not location:
            return None

        # Split by common separators
        parts = re.split(r"[,\-|/]", location)
        if parts:
            # First part is usually the city
            city = parts[0].strip()
            # Remove "Area" prefix
            city = re.sub(r"^Area\s+", "", city, flags=re.IGNORECASE)
            return city if city else None

        return None

    @staticmethod
    def normalize_job_type(item: dict) -> dict:
        """
        Normalize job_type to standard values.

        Args:
            item: Item with job_type field.

        Returns:
            Item with normalized job_type.
        """
        job_type = item.get("job_type")
        if not job_type:
            return item

        job_type_lower = job_type.strip().lower()
        item["job_type"] = JOB_TYPE_MAPPING.get(job_type_lower, job_type_lower)

        return item

    @staticmethod
    def normalize_work_type(item: dict) -> dict:
        """
        Normalize work_type to standard values (onsite/remote/hybrid).

        Args:
            item: Item with work_type field.

        Returns:
            Item with normalized work_type.
        """
        work_type = item.get("work_type")
        if not work_type:
            return item

        work_type_lower = work_type.strip().lower()
        item["work_type"] = WORK_TYPE_MAPPING.get(work_type_lower, work_type_lower)

        return item

    @staticmethod
    def normalize_employment_type(item: dict) -> dict:
        """
        Normalize employment_type and detect internships.

        Args:
            item: Item with employment_type field.

        Returns:
            Item with normalized employment_type and is_internship flag.
        """
        emp_type = item.get("employment_type")
        if not emp_type:
            return item

        emp_type_lower = emp_type.strip().lower()
        normalized = EMPLOYMENT_TYPE_MAPPING.get(emp_type_lower, emp_type_lower)
        item["employment_type"] = normalized

        # Auto-detect internship
        if normalized == "internship" or "magang" in emp_type_lower or "intern" in emp_type_lower:
            item["is_internship"] = True

        return item

    @staticmethod
    def normalize_experience_level(item: dict) -> dict:
        """
        Normalize experience_level to standard values.

        Args:
            item: Item with experience_level field.

        Returns:
            Item with normalized experience_level.
        """
        level = item.get("experience_level")
        if not level:
            return item

        level_lower = level.strip().lower()
        item["experience_level"] = EXPERIENCE_LEVEL_MAPPING.get(level_lower, level_lower)

        return item

    @staticmethod
    def normalize_salary(item: dict) -> dict:
        """
        Normalize salary fields.

        If salary_min/salary_max are not set but a raw salary string
        exists in the item, attempt to parse it.

        Args:
            item: Item with salary data.

        Returns:
            Item with normalized salary fields.
        """
        # If we already have parsed values, just ensure currency
        if item.get("salary_min") is not None or item.get("salary_max") is not None:
            currency = item.get("salary_currency", "IDR")
            if currency:
                currency_upper = currency.strip().upper()
                item["salary_currency"] = CURRENCY_MAPPING.get(
                    currency_upper.lower(), currency_upper
                )
            return item

        # Try to extract from a raw salary string if available
        raw_salary = item.get("_raw_salary")
        if raw_salary:
            salary_min, salary_max, currency = extract_salary(raw_salary)
            item["salary_min"] = salary_min
            item["salary_max"] = salary_max
            item["salary_currency"] = currency

        return item

    @staticmethod
    def normalize_skills(item: dict) -> dict:
        """
        Normalize skills list to consistent format.

        Args:
            item: Item with skills field.

        Returns:
            Item with normalized skills list.
        """
        skills = item.get("skills")
        if not skills:
            item["skills"] = []
            return item

        if isinstance(skills, str):
            # Split comma-separated or semicolon-separated
            skills = re.split(r"[,;|]", skills)

        # Clean and deduplicate
        cleaned: list[str] = []
        seen: set[str] = set()
        for skill in skills:
            if isinstance(skill, str):
                s = skill.strip()
                if s and s.lower() not in seen:
                    seen.add(s.lower())
                    cleaned.append(s)

        item["skills"] = cleaned
        return item

    @staticmethod
    def normalize_country(item: dict) -> dict:
        """
        Normalize country field.

        Args:
            item: Item with country data.

        Returns:
            Item with normalized country.
        """
        country = item.get("country")
        if not country:
            item["country"] = "Indonesia"
            return item

        country_mapping = {
            "id": "Indonesia",
            "indonesia": "Indonesia",
            "sg": "Singapore",
            "singapore": "Singapore",
            "my": "Malaysia",
            "malaysia": "Malaysia",
            "ph": "Philippines",
            "philippines": "Philippines",
            "th": "Thailand",
            "thailand": "Thailand",
            "vn": "Vietnam",
            "vietnam": "Vietnam",
        }

        item["country"] = country_mapping.get(country.strip().lower(), country.strip())
        return item
