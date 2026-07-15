"""
Tests for ValidatorService.
"""

import pytest

from job_scraper.services.validator import ValidatorService


@pytest.fixture
def validator() -> ValidatorService:
    """Create a ValidatorService instance."""
    return ValidatorService()


@pytest.fixture
def valid_item() -> dict:
    """Create a valid job item for testing."""
    return {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "platform": "glints",
        "source_url": "https://glints.com/jobs/123",
        "location": "Jakarta",
        "job_type": "full-time",
    }


class TestValidatorService:
    """Test suite for ValidatorService."""

    def test_valid_item_passes(self, validator: ValidatorService, valid_item: dict):
        """Test that a valid item passes validation."""
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is True
        assert len(errors) == 0

    def test_missing_title_fails(self, validator: ValidatorService, valid_item: dict):
        """Test that missing title fails validation."""
        del valid_item["title"]
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
        assert any("title" in e for e in errors)

    def test_missing_company_fails(self, validator: ValidatorService, valid_item: dict):
        """Test that missing company_name fails validation."""
        valid_item["company_name"] = ""
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
        assert any("company_name" in e for e in errors)

    def test_missing_source_url_fails(self, validator: ValidatorService, valid_item: dict):
        """Test that missing source_url fails validation."""
        del valid_item["source_url"]
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
        assert any("source_url" in e for e in errors)

    def test_invalid_url_format(self, validator: ValidatorService, valid_item: dict):
        """Test that invalid URL format is caught."""
        valid_item["source_url"] = "not-a-url"
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
        assert any("URL" in e for e in errors)

    def test_valid_url_formats(self, validator: ValidatorService, valid_item: dict):
        """Test various valid URL formats."""
        valid_urls = [
            "https://example.com/job/123",
            "http://example.com/job/123",
            "https://www.example.com/job/123?ref=test",
        ]
        for url in valid_urls:
            valid_item["source_url"] = url
            is_valid, _ = validator.validate(valid_item)
            assert is_valid is True, f"URL should be valid: {url}"

    def test_field_length_validation(self, validator: ValidatorService, valid_item: dict):
        """Test that overly long fields are caught."""
        valid_item["title"] = "A" * 501
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
        assert any("max length" in e for e in errors)

    def test_salary_validation_swap(self, validator: ValidatorService, valid_item: dict):
        """Test that salary_min > salary_max gets auto-swapped."""
        valid_item["salary_min"] = 10000000
        valid_item["salary_max"] = 5000000
        is_valid, _ = validator.validate(valid_item)
        assert is_valid is True
        assert valid_item["salary_min"] == 5000000
        assert valid_item["salary_max"] == 10000000

    def test_negative_salary_fails(self, validator: ValidatorService, valid_item: dict):
        """Test that negative salary values fail."""
        valid_item["salary_min"] = -1000
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
        assert any("salary" in e.lower() for e in errors)

    def test_invalid_platform(self, validator: ValidatorService, valid_item: dict):
        """Test that unknown platform is caught."""
        valid_item["platform"] = "unknown_platform"
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
        assert any("platform" in e for e in errors)

    def test_garbage_title_fails(self, validator: ValidatorService, valid_item: dict):
        """Test that garbage title is caught."""
        valid_item["title"] = "123"
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False

    def test_short_title_fails(self, validator: ValidatorService, valid_item: dict):
        """Test that too-short title fails."""
        valid_item["title"] = "AB"
        is_valid, errors = validator.validate(valid_item)
        assert is_valid is False
