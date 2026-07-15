"""
Tests for CleanerService.
"""

import pytest

from job_scraper.services.cleaner import CleanerService


@pytest.fixture
def cleaner() -> CleanerService:
    """Create a CleanerService instance."""
    return CleanerService()


class TestCleanerService:
    """Test suite for CleanerService."""

    def test_clean_html_basic(self, cleaner: CleanerService):
        """Test basic HTML tag removal."""
        html = "<p>Hello <strong>World</strong></p>"
        result = cleaner.clean_html(html)
        assert "Hello" in result
        assert "World" in result
        assert "<p>" not in result
        assert "<strong>" not in result

    def test_clean_html_preserves_structure(self, cleaner: CleanerService):
        """Test that block elements are converted to newlines."""
        html = "<p>Line 1</p><p>Line 2</p>"
        result = cleaner.clean_html(html)
        assert "Line 1" in result
        assert "Line 2" in result

    def test_clean_html_none_input(self, cleaner: CleanerService):
        """Test that None input returns None."""
        assert cleaner.clean_html(None) is None

    def test_clean_html_empty_string(self, cleaner: CleanerService):
        """Test that empty string returns None."""
        assert cleaner.clean_html("") is None

    def test_clean_html_entities(self, cleaner: CleanerService):
        """Test HTML entity decoding."""
        html = "&amp; &lt; &gt; &quot;"
        result = cleaner.clean_html(html)
        assert "&" in result
        assert "<" in result

    def test_remove_special_characters(self, cleaner: CleanerService):
        """Test special character removal."""
        text = "Hello\u200bWorld\u200cTest"
        result = cleaner.remove_special_characters(text)
        assert "HelloWorldTest" == result

    def test_remove_special_characters_smart_quotes(self, cleaner: CleanerService):
        """Test smart quote normalization."""
        text = "\u201cHello\u201d \u2018World\u2019"
        result = cleaner.remove_special_characters(text)
        assert '"Hello"' in result
        assert "'World'" in result

    def test_normalize_whitespace(self, cleaner: CleanerService):
        """Test whitespace normalization."""
        text = "Hello    World\n\n\n\nNew    Paragraph"
        result = cleaner.normalize_whitespace(text)
        assert "Hello World" in result
        assert "\n\n\n" not in result

    def test_clean_company_name_pt(self, cleaner: CleanerService):
        """Test PT prefix removal from company names."""
        assert cleaner.clean_company_name("PT. Tokopedia") == "Tokopedia"
        assert cleaner.clean_company_name("PT Gojek Indonesia") == "Gojek Indonesia"

    def test_clean_company_name_suffix(self, cleaner: CleanerService):
        """Test legal suffix removal."""
        assert cleaner.clean_company_name("Google Inc.") == "Google"
        assert cleaner.clean_company_name("Grab Holdings Ltd") == "Grab Holdings"

    def test_clean_company_name_none(self, cleaner: CleanerService):
        """Test None company name."""
        assert cleaner.clean_company_name(None) is None

    def test_clean_url_basic(self, cleaner: CleanerService):
        """Test basic URL cleaning."""
        url = "https://example.com/job/123"
        assert cleaner.clean_url(url) == url

    def test_clean_url_removes_utm(self, cleaner: CleanerService):
        """Test UTM parameter removal."""
        url = "https://example.com/job?utm_source=google&ref=test"
        result = cleaner.clean_url(url)
        assert "utm_source" not in result
        assert "ref=test" in result

    def test_clean_url_invalid(self, cleaner: CleanerService):
        """Test invalid URL returns None."""
        assert cleaner.clean_url("not-a-url") is None
        assert cleaner.clean_url("ftp://files.com") is None

    def test_clean_url_none(self, cleaner: CleanerService):
        """Test None URL."""
        assert cleaner.clean_url(None) is None

    def test_clean_item(self, cleaner: CleanerService):
        """Test full item cleaning."""
        item = {
            "title": "  Software Engineer  ",
            "company_name": "PT. Test Corp Inc.",
            "description": "<p>Join our <b>team</b></p>",
            "source_url": "https://example.com/job?utm_source=test",
            "location": "Jakarta\u200b",
        }
        result = cleaner.clean_item(item)
        assert result["title"] == "Software Engineer"
        assert "<p>" not in result["description"]
        assert "utm_source" not in result["source_url"]
