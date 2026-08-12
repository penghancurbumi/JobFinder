import re

from job_scraper.constants import CLOSED_MARKERS

_TAG_RE = re.compile(r"<[^>]+>")


def _plain(text: str) -> str:
    return _TAG_RE.sub(" ", text or "").lower()


def has_closed_content(text: str, platform: str | None = None) -> bool:
    haystack = _plain(text)
    for marker in CLOSED_MARKERS.get("general", []):
        if marker.lower() in haystack:
            return True
    if platform:
        for marker in CLOSED_MARKERS.get(platform, []):
            if marker.lower() in haystack:
                return True
    return False