"""
Deduplicator — Duplicate detection service.
============================================

Detects and handles duplicate job listings using multiple
strategies: exact URL match and fuzzy title+company+location match.
"""

from job_scraper.logger import get_logger
from job_scraper.utils import generate_hash

logger = get_logger("services.deduplicator")


class DeduplicatorService:
    """
    Service for detecting duplicate job listings.

    Uses an in-memory set for fast duplicate detection during
    a single crawl run, plus database-level checks for
    cross-run deduplication.
    """

    def __init__(self) -> None:
        """Initialize with empty seen sets."""
        self._seen_urls: set[str] = set()
        self._seen_fingerprints: set[str] = set()
        self._duplicate_count: int = 0
        self._total_checked: int = 0

    def is_duplicate(self, item: dict) -> bool:
        """
        Check if an item is a duplicate using multiple strategies.

        Strategy 1: Exact match on source_url
        Strategy 2: Fuzzy match on title + company_name + city

        Args:
            item: Scraped item dictionary.

        Returns:
            True if the item is a duplicate.
        """
        self._total_checked += 1

        # Strategy 1: Exact URL match
        source_url = item.get("source_url", "")
        if source_url and source_url in self._seen_urls:
            self._duplicate_count += 1
            logger.debug("Duplicate (URL match): %s", source_url)
            return True

        # Strategy 2: Fingerprint match (title + company + city)
        fingerprint = self._generate_fingerprint(item)
        if fingerprint and fingerprint in self._seen_fingerprints:
            self._duplicate_count += 1
            logger.debug(
                "Duplicate (fingerprint match): %s at %s",
                item.get("title", ""),
                item.get("company_name", ""),
            )
            return True

        # Not a duplicate — register it
        if source_url:
            self._seen_urls.add(source_url)
        if fingerprint:
            self._seen_fingerprints.add(fingerprint)

        return False

    @staticmethod
    def _generate_fingerprint(item: dict) -> str | None:
        """
        Generate a fingerprint hash from title + company + city.

        The fingerprint is case-insensitive and whitespace-normalized
        to catch near-duplicates across platforms.

        Args:
            item: Scraped item dictionary.

        Returns:
            SHA256 hash fingerprint or None.
        """
        title = (item.get("title") or "").strip().lower()
        company = (item.get("company_name") or "").strip().lower()
        city = (item.get("city") or "").strip().lower()

        if not title or not company:
            return None

        # Normalize whitespace
        combined = f"{' '.join(title.split())}|{' '.join(company.split())}|{' '.join(city.split())}"
        return generate_hash(combined)

    def get_stats(self) -> dict[str, int]:
        """
        Get deduplication statistics.

        Returns:
            Dictionary with total_checked, duplicates_found, unique_items.
        """
        return {
            "total_checked": self._total_checked,
            "duplicates_found": self._duplicate_count,
            "unique_items": self._total_checked - self._duplicate_count,
            "seen_urls": len(self._seen_urls),
            "seen_fingerprints": len(self._seen_fingerprints),
        }

    def reset(self) -> None:
        """Reset all tracking sets and counters."""
        self._seen_urls.clear()
        self._seen_fingerprints.clear()
        self._duplicate_count = 0
        self._total_checked = 0
        logger.info("Deduplicator state reset.")
