import re
from html import unescape as html_unescape


def get_cleaner_pipeline():
    cleaners = [
        trim_strings,
        clean_html,
        normalize_whitespace,
        clean_title,
        clean_salary,
        clean_url,
    ]

    def clean(item: dict) -> dict:
        for cleaner in cleaners:
            item = cleaner(item)
        return item

    return clean


def trim_strings(item: dict) -> dict:
    for key, value in item.items():
        if isinstance(value, str):
            item[key] = value.strip()
    return item


def clean_html(item: dict) -> dict:
    for key in ["description", "benefits"]:
        value = item.get(key)
        if not value:
            continue
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        if isinstance(value, str):
            value = re.sub(r"<[^>]+>", " ", value)
            value = html_unescape(value)
            item[key] = value
    return item


def normalize_whitespace(item: dict) -> dict:
    for key, value in item.items():
        if isinstance(value, str):
            item[key] = re.sub(r"\s+", " ", value).strip()
    return item


def clean_title(item: dict) -> dict:
    title = item.get("title", "")
    if title:
        title = re.sub(r"\s*-\s*(Remote|WFH|Hybrid|Onsite|Full-time|Part-time)$", "", title, flags=re.IGNORECASE)
        item["title"] = title.strip()
    return item


def clean_salary(item: dict) -> dict:
    for key in ["salary_min", "salary_max"]:
        value = item.get(key)
        if value is not None:
            try:
                item[key] = float(value) if "." in str(value) else int(value)
            except (ValueError, TypeError):
                item[key] = None
    return item


def clean_url(item: dict) -> dict:
    for key in ["source_url", "apply_url", "company_website", "company_logo"]:
        value = item.get(key)
        if value and isinstance(value, str):
            value = value.strip()
            if value.startswith("//"):
                value = "https:" + value
            item[key] = value
    return item
