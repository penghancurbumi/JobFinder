"""
Pipelines — Scrapy item processing pipeline chain.
===================================================

Defines the ordered pipeline chain:
1. ValidationPipeline — Validate required fields
2. CleanerPipeline — Clean HTML and special characters
3. NormalizerPipeline — Normalize location, types, salary
4. DeduplicatorPipeline — Remove duplicates
5. PostgresPipeline — Save to database
6. ExportPipeline — Export to JSON/CSV/Excel
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from scrapy import Spider
from scrapy.exceptions import DropItem

from job_scraper.database import create_db_engine, create_session_factory, init_database
from job_scraper.logger import get_logger, get_stats_logger
from job_scraper.models.job import Job
from job_scraper.services.cleaner import CleanerService
from job_scraper.services.deduplicator import DeduplicatorService
from job_scraper.services.normalizer import NormalizerService
from job_scraper.services.validator import ValidatorService

logger = get_logger("pipelines")
stats_logger = get_stats_logger()


class ValidationPipeline:
    """
    Pipeline step 1: Validate required fields and data quality.

    Drops items that don't meet minimum quality standards.
    """

    def __init__(self) -> None:
        self.validator = ValidatorService()
        self._valid_count: int = 0
        self._invalid_count: int = 0

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Validate the item and drop if invalid."""
        is_valid, errors = self.validator.validate(dict(item))

        if not is_valid:
            self._invalid_count += 1
            raise DropItem(
                f"Validation failed for '{item.get('title', 'unknown')}': "
                f"{'; '.join(errors)}"
            )

        self._valid_count += 1
        return item

    def close_spider(self, spider: Spider) -> None:
        """Log validation statistics."""
        stats_logger.info(
            "VALIDATION | Spider: %s | Valid: %d | Invalid: %d",
            spider.name, self._valid_count, self._invalid_count,
        )


class CleanerPipeline:
    """
    Pipeline step 2: Clean HTML, special characters, and text.
    """

    def __init__(self) -> None:
        self.cleaner = CleanerService()

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Clean the item content."""
        return self.cleaner.clean_item(dict(item))


class NormalizerPipeline:
    """
    Pipeline step 3: Normalize location, types, salary, and skills.
    """

    def __init__(self) -> None:
        self.normalizer = NormalizerService()

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Normalize all fields."""
        normalized = self.normalizer.normalize_item(dict(item))

        # Set metadata timestamps
        now = datetime.now(timezone.utc)
        if not normalized.get("scraped_at"):
            normalized["scraped_at"] = now
        normalized["updated_at"] = now

        return normalized


class DeduplicatorPipeline:
    """
    Pipeline step 4: Detect and drop duplicate items.
    """

    def __init__(self) -> None:
        self.deduplicator = DeduplicatorService()

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Check for duplicates and drop if found."""
        if self.deduplicator.is_duplicate(dict(item)):
            raise DropItem(
                f"Duplicate item: '{item.get('title', 'unknown')}' "
                f"from {item.get('source_url', 'unknown')}"
            )
        return item

    def close_spider(self, spider: Spider) -> None:
        """Log deduplication statistics."""
        stats = self.deduplicator.get_stats()
        stats_logger.info(
            "DEDUP | Spider: %s | Checked: %d | Duplicates: %d | Unique: %d",
            spider.name,
            stats["total_checked"],
            stats["duplicates_found"],
            stats["unique_items"],
        )


class PostgresPipeline:
    """
    Pipeline step 5: Save items to PostgreSQL using upsert.

    Uses INSERT ... ON CONFLICT UPDATE for idempotent writes.
    """

    def __init__(self) -> None:
        self._engine = None
        self._session_factory = None
        self._saved_count: int = 0
        self._updated_count: int = 0
        self._error_count: int = 0

    def open_spider(self, spider: Spider) -> None:
        """Initialize database connection."""
        try:
            self._engine = create_db_engine()
            init_database(self._engine)
            self._session_factory = create_session_factory(self._engine)
            logger.info("PostgresPipeline: Database connected.")
        except Exception as e:
            logger.error("PostgresPipeline: Failed to connect to database: %s", e)
            logger.warning("PostgresPipeline: Items will NOT be saved to database.")
            self._session_factory = None

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Save or update the item in the database."""
        if self._session_factory is None:
            return item

        session = self._session_factory()
        try:
            item_dict = dict(item)

            # Remove internal fields
            item_dict.pop("_raw_salary", None)

            # Check if exists by source_url
            existing = session.query(Job).filter_by(
                source_url=item_dict.get("source_url")
            ).first()

            if existing:
                # Update existing record
                for key, value in item_dict.items():
                    if hasattr(existing, key) and value is not None:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now(timezone.utc)
                self._updated_count += 1
                logger.debug("Updated: %s", item_dict.get("title"))
            else:
                # Insert new record
                job = Job(**{
                    k: v for k, v in item_dict.items()
                    if hasattr(Job, k)
                })
                session.add(job)
                self._saved_count += 1
                logger.debug("Saved: %s", item_dict.get("title"))

            session.commit()

        except Exception as e:
            session.rollback()
            self._error_count += 1
            logger.error(
                "Failed to save '%s': %s",
                item.get("title", "unknown"), e,
            )
        finally:
            session.close()

        return item

    def close_spider(self, spider: Spider) -> None:
        """Log save statistics and close engine."""
        stats_logger.info(
            "DATABASE | Spider: %s | Saved: %d | Updated: %d | Errors: %d",
            spider.name, self._saved_count, self._updated_count, self._error_count,
        )

        if self._engine:
            self._engine.dispose()
            logger.info("PostgresPipeline: Database connection closed.")


class ExportPipeline:
    """
    Pipeline step 6: Export items to JSON/CSV/Excel files.

    Only active when EXPORT_ENABLED=true in environment.
    """

    def __init__(self) -> None:
        self._items: list[dict] = []
        self._enabled: bool = os.getenv("EXPORT_ENABLED", "false").lower() == "true"
        self._format: str = os.getenv("EXPORT_FORMAT", "json").lower()
        self._export_dir: str = os.getenv("EXPORT_DIR", "exports")

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Collect items for export."""
        if self._enabled:
            self._items.append(dict(item))
        return item

    def close_spider(self, spider: Spider) -> None:
        """Export collected items to file."""
        if not self._enabled or not self._items:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{spider.name}_{timestamp}"

        try:
            if self._format == "json":
                self._export_json(filename)
            elif self._format == "csv":
                self._export_csv(filename)
            elif self._format == "excel":
                self._export_excel(filename)
            else:
                logger.warning("Unknown export format: %s", self._format)
        except Exception as e:
            logger.error("Export failed: %s", e)

    def _export_json(self, filename: str) -> None:
        """Export items to JSON file."""
        export_path = Path(self._export_dir) / "json"
        export_path.mkdir(parents=True, exist_ok=True)

        filepath = export_path / f"{filename}.json"
        serializable_items = self._make_serializable(self._items)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable_items, f, ensure_ascii=False, indent=2, default=str)

        logger.info("Exported %d items to %s", len(self._items), filepath)

    def _export_csv(self, filename: str) -> None:
        """Export items to CSV file."""
        export_path = Path(self._export_dir) / "csv"
        export_path.mkdir(parents=True, exist_ok=True)

        filepath = export_path / f"{filename}.csv"
        df = pd.DataFrame(self._items)
        df.to_csv(filepath, index=False, encoding="utf-8")

        logger.info("Exported %d items to %s", len(self._items), filepath)

    def _export_excel(self, filename: str) -> None:
        """Export items to Excel file."""
        export_path = Path(self._export_dir) / "excel"
        export_path.mkdir(parents=True, exist_ok=True)

        filepath = export_path / f"{filename}.xlsx"
        df = pd.DataFrame(self._items)
        df.to_excel(filepath, index=False, engine="openpyxl")

        logger.info("Exported %d items to %s", len(self._items), filepath)

    @staticmethod
    def _make_serializable(items: list[dict]) -> list[dict]:
        """Convert datetime objects to strings for JSON serialization."""
        serializable = []
        for item in items:
            clean_item = {}
            for key, value in item.items():
                if isinstance(value, datetime):
                    clean_item[key] = value.isoformat()
                else:
                    clean_item[key] = value
            serializable.append(clean_item)
        return serializable
