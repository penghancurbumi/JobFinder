"""
Tests for DeduplicatorService.
"""

import pytest

from job_scraper.services.deduplicator import DeduplicatorService


@pytest.fixture
def deduplicator() -> DeduplicatorService:
    """Create a fresh DeduplicatorService instance."""
    return DeduplicatorService()


class TestDeduplicatorService:
    """Test suite for DeduplicatorService."""

    def test_first_item_not_duplicate(self, deduplicator: DeduplicatorService):
        """Test that the first item is never a duplicate."""
        item = {
            "title": "Software Engineer",
            "company_name": "Google",
            "source_url": "https://example.com/job/1",
            "city": "Jakarta",
        }
        assert deduplicator.is_duplicate(item) is False

    def test_same_url_is_duplicate(self, deduplicator: DeduplicatorService):
        """Test that same source_url is detected as duplicate."""
        item1 = {
            "title": "Software Engineer",
            "company_name": "Google",
            "source_url": "https://example.com/job/1",
            "city": "Jakarta",
        }
        item2 = {
            "title": "Different Title",
            "company_name": "Different Company",
            "source_url": "https://example.com/job/1",
            "city": "Bandung",
        }
        assert deduplicator.is_duplicate(item1) is False
        assert deduplicator.is_duplicate(item2) is True

    def test_same_fingerprint_is_duplicate(self, deduplicator: DeduplicatorService):
        """Test that same title+company+city is detected as duplicate."""
        item1 = {
            "title": "Software Engineer",
            "company_name": "Google",
            "source_url": "https://glints.com/job/1",
            "city": "Jakarta",
        }
        item2 = {
            "title": "Software Engineer",
            "company_name": "Google",
            "source_url": "https://jobstreet.com/job/1",  # Different URL
            "city": "Jakarta",
        }
        assert deduplicator.is_duplicate(item1) is False
        assert deduplicator.is_duplicate(item2) is True

    def test_case_insensitive_fingerprint(self, deduplicator: DeduplicatorService):
        """Test that fingerprint matching is case-insensitive."""
        item1 = {
            "title": "Software Engineer",
            "company_name": "Google",
            "source_url": "https://example.com/1",
            "city": "Jakarta",
        }
        item2 = {
            "title": "software engineer",
            "company_name": "GOOGLE",
            "source_url": "https://example.com/2",
            "city": "jakarta",
        }
        assert deduplicator.is_duplicate(item1) is False
        assert deduplicator.is_duplicate(item2) is True

    def test_different_items_not_duplicate(self, deduplicator: DeduplicatorService):
        """Test that different items are not duplicates."""
        item1 = {
            "title": "Software Engineer",
            "company_name": "Google",
            "source_url": "https://example.com/1",
            "city": "Jakarta",
        }
        item2 = {
            "title": "Data Scientist",
            "company_name": "Google",
            "source_url": "https://example.com/2",
            "city": "Jakarta",
        }
        assert deduplicator.is_duplicate(item1) is False
        assert deduplicator.is_duplicate(item2) is False

    def test_stats_tracking(self, deduplicator: DeduplicatorService):
        """Test that statistics are tracked correctly."""
        items = [
            {"title": "Job 1", "company_name": "A", "source_url": "https://a.com/1", "city": "Jakarta"},
            {"title": "Job 2", "company_name": "B", "source_url": "https://b.com/1", "city": "Jakarta"},
            {"title": "Job 1", "company_name": "A", "source_url": "https://c.com/1", "city": "Jakarta"},  # dup
        ]
        for item in items:
            deduplicator.is_duplicate(item)

        stats = deduplicator.get_stats()
        assert stats["total_checked"] == 3
        assert stats["duplicates_found"] == 1
        assert stats["unique_items"] == 2

    def test_reset(self, deduplicator: DeduplicatorService):
        """Test reset clears all state."""
        item = {
            "title": "Job 1", "company_name": "A",
            "source_url": "https://a.com/1", "city": "Jakarta",
        }
        deduplicator.is_duplicate(item)
        deduplicator.reset()

        stats = deduplicator.get_stats()
        assert stats["total_checked"] == 0
        assert stats["duplicates_found"] == 0

        # Same item should not be duplicate after reset
        assert deduplicator.is_duplicate(item) is False

    def test_missing_city_in_fingerprint(self, deduplicator: DeduplicatorService):
        """Test fingerprint works without city."""
        item1 = {
            "title": "Job 1", "company_name": "A",
            "source_url": "https://a.com/1",
        }
        item2 = {
            "title": "Job 1", "company_name": "A",
            "source_url": "https://b.com/1",
        }
        assert deduplicator.is_duplicate(item1) is False
        assert deduplicator.is_duplicate(item2) is True
