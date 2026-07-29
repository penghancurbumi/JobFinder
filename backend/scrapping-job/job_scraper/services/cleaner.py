"""
Cleaner — HTML cleaning and text sanitization service.
======================================================

Removes HTML tags, decodes entities, strips special characters,
and produces clean text suitable for database storage.
"""

import re
from html import unescape

from bs4 import BeautifulSoup

from job_scraper.logger import get_logger

logger = get_logger("services.cleaner")


class CleanerService:
    """
    Service for cleaning raw scraped text content.

    Handles HTML removal, entity decoding, and character normalization
    to produce consistent, clean text for storage.
    """

    @staticmethod
    def clean_html(html_content: str | None) -> str | None:
        """
        Remove HTML tags and decode entities from content.

        Preserves paragraph structure by converting block elements
        to newlines before stripping tags.

        Args:
            html_content: Raw HTML string.

        Returns:
            Clean text with HTML removed, or None.
        """
        if not html_content:
            return None

        # Decode HTML entities first
        text = unescape(html_content)

        # Convert block elements to newlines for structure preservation
        block_tags = r"</?(?:p|div|br|li|h[1-6]|tr|td|th|section|article)[^>]*>"
        text = re.sub(block_tags, "\n", text, flags=re.IGNORECASE)

        # Remove all remaining HTML tags
        soup = BeautifulSoup(text, "lxml")
        text = soup.get_text(separator="\n")

        # Clean up whitespace
        text = CleanerService.normalize_whitespace(text)

        return text if text else None

    @staticmethod
    def remove_special_characters(text: str | None) -> str | None:
        """
        Remove special and control characters while preserving readability.

        Keeps alphanumeric, common punctuation, and whitespace.

        Args:
            text: Text to clean.

        Returns:
            Text with special characters removed, or None.
        """
        if not text:
            return None

        # Remove zero-width characters
        text = re.sub(r"[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad]", "", text)

        # Remove control characters (except newline, tab)
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

        # Normalize unicode quotes and dashes
        replacements = {
            "\u2018": "'", "\u2019": "'",  # Smart quotes
            "\u201c": '"', "\u201d": '"',  # Smart double quotes
            "\u2013": "-", "\u2014": "-",  # Em/en dash
            "\u2026": "...",               # Ellipsis
            "\u00a0": " ",                 # Non-breaking space
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        return text if text.strip() else None

    @staticmethod
    def normalize_whitespace(text: str | None) -> str | None:
        """
        Normalize whitespace: collapse multiple spaces and blank lines.

        Args:
            text: Text to normalize.

        Returns:
            Text with normalized whitespace, or None.
        """
        if not text:
            return None

        # Collapse multiple blank lines to single
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        # Collapse multiple spaces within lines
        text = re.sub(r"[ \t]+", " ", text)
        # Strip leading/trailing whitespace per line
        lines = [line.strip() for line in text.split("\n")]
        text = "\n".join(lines)

        return text.strip() if text.strip() else None

    @staticmethod
    def clean_company_name(name: str | None) -> str | None:
        """
        Clean and normalize a company name.

        Removes common suffixes like PT, CV, Ltd, etc. for consistency
        while keeping them if they're the only content.

        Args:
            name: Raw company name.

        Returns:
            Cleaned company name, or None.
        """
        if not name:
            return None

        name = name.strip()

        # Remove leading "PT." or "PT " or "CV." etc.
        name = re.sub(r"^(?:PT\.?\s*|CV\.?\s*)", "", name, flags=re.IGNORECASE).strip()

        # Remove trailing legal suffixes
        name = re.sub(
            r"\s*(?:,?\s*(?:Tbk|Ltd|Inc|Corp|LLC|Pte|Sdn Bhd|GmbH|Co\.?)\.?\s*)$",
            "",
            name,
            flags=re.IGNORECASE,
        ).strip()

        return name if name else None

    @staticmethod
    def clean_url(url: str | None) -> str | None:
        """
        Clean and validate a URL.

        Args:
            url: Raw URL string.

        Returns:
            Cleaned URL or None if invalid.
        """
        if not url:
            return None

        url = url.strip()

        # Must start with http/https
        if not url.startswith(("http://", "https://")):
            return None

        # Remove tracking parameters (utm_*)
        url = re.sub(r"[?&]utm_[^&]*", "", url)
        # Clean up resulting URL
        url = re.sub(r"\?$", "", url)
        url = re.sub(r"\?&", "?", url)

        return url

    def clean_item(self, item: dict) -> dict:
        """
        Apply all cleaning operations to a scraped item.

        Args:
            item: Raw scraped item dictionary.

        Returns:
            Cleaned item dictionary.
        """
        # Clean HTML from text fields
        text_fields = [
            "description", "requirements", "responsibilities",
            "qualifications",
        ]
        for field in text_fields:
            if item.get(field):
                item[field] = self.clean_html(item[field])
                item[field] = self.remove_special_characters(item[field])

        # Handle benefits — bisa string (comma-separated) atau list
        if item.get("benefits"):
            if isinstance(item["benefits"], list):
                item["benefits"] = ", ".join(str(b) for b in item["benefits"] if b)
            item["benefits"] = self.remove_special_characters(item["benefits"])

        # Clean simple text fields
        simple_fields = ["title", "location", "category"]
        for field in simple_fields:
            if item.get(field):
                item[field] = self.remove_special_characters(item[field])
                if item[field]:
                    item[field] = item[field].strip()

        # Clean company name
        if item.get("company_name"):
            item["company_name"] = self.remove_special_characters(item["company_name"])

        # Clean URLs
        url_fields = ["apply_url", "source_url", "company_website", "company_logo"]
        for field in url_fields:
            if item.get(field):
                item[field] = self.clean_url(item[field])

        logger.debug("Cleaned item: %s", item.get("title", "unknown"))
        return item
