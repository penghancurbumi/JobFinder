import json
import os
from datetime import datetime, timezone

from scrapy import Spider, signals
from scrapy.exceptions import DropItem

from job_scraper.items import JobItem
from job_scraper.logger import get_logger
from job_scraper.services.cleaner import get_cleaner_pipeline
from job_scraper.services.validator import ValidatorService

logger = get_logger("pipelines")


class DuplicateFilterPipeline:
    def __init__(self):
        self.seen: set = set()

    def process_item(self, item: JobItem, spider: Spider) -> JobItem:
        dedup_key = f"{item.get('source_url', '')}|{item.get('title', '')}|{item.get('company_name', '')}"
        if dedup_key in self.seen:
            raise DropItem(f"Duplicate item: {item.get('title', '')}")
        self.seen.add(dedup_key)
        return item


class CleanerPipeline:
    def __init__(self):
        self._clean = get_cleaner_pipeline()

    def process_item(self, item: JobItem, spider: Spider) -> JobItem:
        cleaned = self._clean(dict(item))
        for key, value in cleaned.items():
            item[key] = value
        return item


class ValidatorPipeline:
    def __init__(self):
        self._validator = ValidatorService()

    def process_item(self, item: JobItem, spider: Spider) -> JobItem:
        is_valid, errors = self._validator.validate(dict(item))
        if not is_valid:
            logger.warning("Dropping invalid item: %s", "; ".join(errors))
            raise DropItem(f"Validation failed: {'; '.join(errors)}")
        return item


class JsonExportPipeline:
    def __init__(self):
        self._items: list[dict] = []

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def process_item(self, item: JobItem, spider: Spider) -> JobItem:
        self._items.append(dict(item))
        return item

    def spider_closed(self, spider: Spider) -> None:
        if not self._items:
            return

        from scrapy.utils.project import get_project_settings
        settings = get_project_settings()
        export_dir = settings.get("EXPORT_JSON_DIR", "exports/json")
        os.makedirs(export_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{spider.name}_{timestamp}.json"
        filepath = os.path.join(export_dir, filename)

        def serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return str(obj)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self._items, f, indent=2, default=serialize)

        logger.info("Exported %d items to %s", len(self._items), filepath)
