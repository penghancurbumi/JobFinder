"""
Utils — General utility functions.
==================================

Provides helper functions for date parsing, URL normalization,
text extraction, and other common operations used across the
scraping system.
"""

import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

from dateutil import parser as dateutil_parser

from job_scraper.logger import get_logger

logger = get_logger("utils")


def parse_date(date_string: str | None) -> datetime | None:
    """
    Parse a date string into a timezone-aware datetime.

    Supports various formats including ISO 8601, relative dates
    (e.g., '3 days ago', '2 jam lalu'), and common date formats.

    Args:
        date_string: Date string to parse.

    Returns:
        Parsed datetime or None if parsing fails.
    """
    if not date_string:
        return None

    date_string = date_string.strip()

    # Handle relative dates (English)
    relative_en = re.match(
        r"(\d+)\s*(second|minute|hour|day|week|month|year)s?\s*ago",
        date_string,
        re.IGNORECASE,
    )
    if relative_en:
        return _parse_relative_date(
            int(relative_en.group(1)),
            relative_en.group(2).lower(),
        )

    # Handle relative dates (Indonesian)
    relative_id = re.match(
        r"(\d+)\s*(detik|menit|jam|hari|minggu|bulan|tahun)\s*(lalu|yang lalu)",
        date_string,
        re.IGNORECASE,
    )
    if relative_id:
        unit_mapping = {
            "detik": "second",
            "menit": "minute",
            "jam": "hour",
            "hari": "day",
            "minggu": "week",
            "bulan": "month",
            "tahun": "year",
        }
        return _parse_relative_date(
            int(relative_id.group(1)),
            unit_mapping[relative_id.group(2).lower()],
        )

    # Try standard parsing
    try:
        parsed = dateutil_parser.parse(date_string, fuzzy=True)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (ValueError, OverflowError):
        logger.warning("Could not parse date: '%s'", date_string)
        return None


def _parse_relative_date(amount: int, unit: str) -> datetime:
    """Convert a relative date to absolute datetime."""
    from datetime import timedelta

    now = datetime.now(timezone.utc)
    deltas = {
        "second": timedelta(seconds=amount),
        "minute": timedelta(minutes=amount),
        "hour": timedelta(hours=amount),
        "day": timedelta(days=amount),
        "week": timedelta(weeks=amount),
        "month": timedelta(days=amount * 30),
        "year": timedelta(days=amount * 365),
    }
    return now - deltas.get(unit, timedelta())


def normalize_url(url: str | None, base_url: str | None = None) -> str | None:
    """
    Normalize a URL by resolving relative paths and removing fragments.

    Args:
        url: URL to normalize.
        base_url: Base URL for resolving relative URLs.

    Returns:
        Normalized absolute URL or None.
    """
    if not url:
        return None

    url = url.strip()

    # Resolve relative URLs
    if base_url and not url.startswith(("http://", "https://")):
        url = urljoin(base_url, url)

    # Parse and rebuild without fragment
    parsed = urlparse(url)
    normalized = parsed._replace(fragment="").geturl()

    return normalized


def extract_salary(salary_text: str | None) -> tuple[int | None, int | None, str]:
    """
    Extract min/max salary and currency from a salary string.

    Handles formats like:
    - "Rp 5.000.000 - Rp 8.000.000"
    - "5 - 8 juta"
    - "IDR 5,000,000 - 8,000,000"
    - "$1,000 - $2,000"

    Args:
        salary_text: Raw salary string.

    Returns:
        Tuple of (min_salary, max_salary, currency).
    """
    if not salary_text:
        return None, None, "IDR"

    text = salary_text.strip().upper()
    currency = "IDR"

    # Detect currency
    from job_scraper.constants import CURRENCY_MAPPING
    for key, val in CURRENCY_MAPPING.items():
        if key.upper() in text:
            currency = val
            break

    # Remove currency symbols and text
    cleaned = re.sub(r"[^\d\s.,\-–]", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Extract numbers
    numbers = re.findall(r"[\d.,]+", cleaned)
    parsed_numbers: list[int] = []

    for num_str in numbers:
        # Remove thousand separators and parse
        num_str = num_str.replace(".", "").replace(",", "")
        try:
            parsed_numbers.append(int(num_str))
        except ValueError:
            continue

    # Handle "juta" (million) in original text
    if "JUTA" in salary_text.upper() or "JT" in salary_text.upper():
        parsed_numbers = [n * 1_000_000 for n in parsed_numbers]

    if len(parsed_numbers) >= 2:
        return min(parsed_numbers), max(parsed_numbers), currency
    elif len(parsed_numbers) == 1:
        return parsed_numbers[0], parsed_numbers[0], currency
    else:
        return None, None, currency


def clean_text(text: str | None) -> str | None:
    """
    Clean text by removing extra whitespace and special characters.

    Args:
        text: Raw text to clean.

    Returns:
        Cleaned text or None.
    """
    if not text:
        return None

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Remove zero-width characters
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)

    return text if text else None


def generate_hash(text: str) -> str:
    """
    Generate a SHA256 hash of the given text.

    Useful for deduplication and fingerprinting.

    Args:
        text: Text to hash.

    Returns:
        Hex-encoded SHA256 hash.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_skills_from_text(text: str | None) -> list[str]:
    """
    Extract potential skills/technologies from job description text.

    Args:
        text: Job description or requirements text.

    Returns:
        List of identified skills.
    """
    if not text:
        return []

    # Common tech skills to look for
    skill_patterns: list[str] = [
        "Python", "Java", "JavaScript", "TypeScript", "Go", "Golang",
        "Rust", "C\\+\\+", "C#", "PHP", "Ruby", "Swift", "Kotlin",
        "React", "Vue", "Angular", "Next\\.js", "Node\\.js", "Express",
        "Django", "Flask", "FastAPI", "Laravel", "Spring", "Rails",
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Docker", "Kubernetes", "AWS", "GCP", "Azure",
        "Git", "CI/CD", "Jenkins", "GitHub Actions",
        "REST", "GraphQL", "gRPC", "API",
        "Machine Learning", "Deep Learning", "AI", "NLP",
        "SQL", "NoSQL", "Linux", "Terraform", "Ansible",
        "Figma", "Sketch", "Adobe", "Photoshop", "Illustrator",
        "Agile", "Scrum", "Jira", "Confluence",
        "HTML", "CSS", "SASS", "Tailwind",
        "Pandas", "NumPy", "TensorFlow", "PyTorch",
    ]

    found_skills: list[str] = []
    text_lower = text.lower()

    for skill in skill_patterns:
        if re.search(rf"\b{skill}\b", text, re.IGNORECASE):
            # Use the pattern as-is for display (proper casing)
            clean_skill = skill.replace("\\", "")
            if clean_skill not in found_skills:
                found_skills.append(clean_skill)

    return found_skills


def truncate_text(text: str | None, max_length: int = 5000) -> str | None:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate.
        max_length: Maximum character count.

    Returns:
        Truncated text or None.
    """
    if not text:
        return None
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
