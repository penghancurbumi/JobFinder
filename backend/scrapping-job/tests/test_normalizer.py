"""
Tests for NormalizerService.
"""

import pytest

from job_scraper.services.normalizer import NormalizerService


@pytest.fixture
def normalizer() -> NormalizerService:
    """Create a NormalizerService instance."""
    return NormalizerService()


class TestNormalizerService:
    """Test suite for NormalizerService."""

    # Location tests
    def test_normalize_location_jakarta(self, normalizer: NormalizerService):
        """Test Jakarta location normalization."""
        item = {"location": "Jakarta Selatan, DKI Jakarta"}
        result = normalizer.normalize_location(item)
        assert result["city"] == "Jakarta Selatan"
        assert result["province"] == "DKI Jakarta"

    def test_normalize_location_bandung(self, normalizer: NormalizerService):
        """Test Bandung location normalization."""
        item = {"location": "Bandung, Indonesia"}
        result = normalizer.normalize_location(item)
        assert result["city"] == "Bandung"
        assert result["province"] == "Jawa Barat"

    def test_normalize_location_jogja(self, normalizer: NormalizerService):
        """Test Jogja/Yogyakarta normalization."""
        item = {"location": "Jogja", "city": "jogja"}
        result = normalizer.normalize_location(item)
        assert result["city"] == "Yogyakarta"
        assert result["province"] == "DI Yogyakarta"

    def test_normalize_location_empty(self, normalizer: NormalizerService):
        """Test empty location."""
        item = {"location": ""}
        result = normalizer.normalize_location(item)
        assert result.get("city") is None or result.get("city") == ""

    def test_normalize_location_with_city_only(self, normalizer: NormalizerService):
        """Test that province is derived from city."""
        item = {"city": "Surabaya"}
        result = normalizer.normalize_location(item)
        assert result["province"] == "Jawa Timur"

    # Job type tests
    def test_normalize_job_type_fulltime(self, normalizer: NormalizerService):
        """Test full-time job type normalization."""
        variants = ["Full Time", "full-time", "Penuh Waktu", "fulltime"]
        for variant in variants:
            item = {"job_type": variant}
            result = normalizer.normalize_job_type(item)
            assert result["job_type"] == "full-time", f"Failed for: {variant}"

    def test_normalize_job_type_parttime(self, normalizer: NormalizerService):
        """Test part-time job type normalization."""
        variants = ["Part Time", "part-time", "Paruh Waktu"]
        for variant in variants:
            item = {"job_type": variant}
            result = normalizer.normalize_job_type(item)
            assert result["job_type"] == "part-time", f"Failed for: {variant}"

    def test_normalize_job_type_contract(self, normalizer: NormalizerService):
        """Test contract job type normalization."""
        item = {"job_type": "Kontrak"}
        result = normalizer.normalize_job_type(item)
        assert result["job_type"] == "contract"

    # Work type tests
    def test_normalize_work_type_remote(self, normalizer: NormalizerService):
        """Test remote work type normalization."""
        variants = ["Remote", "WFH", "Work From Home", "Dari Rumah"]
        for variant in variants:
            item = {"work_type": variant}
            result = normalizer.normalize_work_type(item)
            assert result["work_type"] == "remote", f"Failed for: {variant}"

    def test_normalize_work_type_onsite(self, normalizer: NormalizerService):
        """Test onsite work type normalization."""
        variants = ["On-site", "Office", "Di Kantor"]
        for variant in variants:
            item = {"work_type": variant}
            result = normalizer.normalize_work_type(item)
            assert result["work_type"] == "onsite", f"Failed for: {variant}"

    # Employment type tests
    def test_normalize_employment_internship(self, normalizer: NormalizerService):
        """Test internship detection."""
        variants = ["Internship", "Magang", "intern"]
        for variant in variants:
            item = {"employment_type": variant}
            result = normalizer.normalize_employment_type(item)
            assert result["employment_type"] == "internship", f"Failed for: {variant}"
            assert result["is_internship"] is True

    # Experience level tests
    def test_normalize_experience_level(self, normalizer: NormalizerService):
        """Test experience level normalization."""
        test_cases = {
            "Entry Level": "entry",
            "Junior": "junior",
            "Mid Level": "mid",
            "Senior": "senior",
            "Lead": "lead",
            "Pemula": "entry",
        }
        for input_val, expected in test_cases.items():
            item = {"experience_level": input_val}
            result = normalizer.normalize_experience_level(item)
            assert result["experience_level"] == expected, f"Failed for: {input_val}"

    # Skills tests
    def test_normalize_skills_from_string(self, normalizer: NormalizerService):
        """Test skills normalization from comma-separated string."""
        item = {"skills": "Python, JavaScript, React, Python"}
        result = normalizer.normalize_skills(item)
        assert "Python" in result["skills"]
        assert "JavaScript" in result["skills"]
        assert "React" in result["skills"]
        # No duplicates
        assert len(result["skills"]) == 3

    def test_normalize_skills_from_list(self, normalizer: NormalizerService):
        """Test skills normalization from list."""
        item = {"skills": ["Python", "JavaScript"]}
        result = normalizer.normalize_skills(item)
        assert result["skills"] == ["Python", "JavaScript"]

    def test_normalize_skills_empty(self, normalizer: NormalizerService):
        """Test empty skills."""
        item = {"skills": None}
        result = normalizer.normalize_skills(item)
        assert result["skills"] == []

    # Country tests
    def test_normalize_country_default(self, normalizer: NormalizerService):
        """Test default country is Indonesia."""
        item = {}
        result = normalizer.normalize_country(item)
        assert result["country"] == "Indonesia"

    def test_normalize_country_code(self, normalizer: NormalizerService):
        """Test country code normalization."""
        item = {"country": "sg"}
        result = normalizer.normalize_country(item)
        assert result["country"] == "Singapore"

    # Full normalization
    def test_normalize_item_full(self, normalizer: NormalizerService):
        """Test full item normalization."""
        item = {
            "title": "Software Engineer",
            "location": "Bandung",
            "job_type": "Full Time",
            "work_type": "Remote",
            "employment_type": "Magang",
            "experience_level": "Entry Level",
            "skills": "Python, React",
        }
        result = normalizer.normalize_item(item)
        assert result["province"] == "Jawa Barat"
        assert result["job_type"] == "full-time"
        assert result["work_type"] == "remote"
        assert result["employment_type"] == "internship"
        assert result["is_internship"] is True
        assert result["experience_level"] == "entry"
        assert result["country"] == "Indonesia"
