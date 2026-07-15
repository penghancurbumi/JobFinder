"""
Middlewares — Custom Scrapy middleware components.
==================================================

Provides:
- RandomUserAgentMiddleware: Rotates User-Agent headers
- ProxyMiddleware: Optional proxy rotation support
"""

import os
import random

from fake_useragent import UserAgent
from scrapy import Request, Spider, signals
from scrapy.http import Response

from job_scraper.logger import get_logger

logger = get_logger("middlewares")


class RandomUserAgentMiddleware:
    """
    Middleware that rotates User-Agent headers on each request.

    Uses the fake-useragent library to generate realistic
    browser User-Agent strings.
    """

    def __init__(self) -> None:
        """Initialize with a UserAgent instance."""
        try:
            self._ua = UserAgent(
                browsers=["Chrome", "Firefox", "Edge"],
                os=["Windows", "Linux"],
                min_percentage=1.0,
            )
            logger.info("RandomUserAgentMiddleware: Initialized with fake-useragent.")
        except Exception as e:
            logger.warning(
                "RandomUserAgentMiddleware: Failed to init fake-useragent (%s). "
                "Using fallback list.",
                e,
            )
            self._ua = None

        # Fallback User-Agents
        self._fallback_agents: list[str] = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) "
            "Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        ]

    @classmethod
    def from_crawler(cls, crawler):
        """Create middleware from crawler."""
        middleware = cls()
        return middleware

    def process_request(self, request: Request, spider: Spider) -> None:
        """Set a random User-Agent header on the request."""
        try:
            if self._ua:
                user_agent = self._ua.random
            else:
                user_agent = random.choice(self._fallback_agents)
        except Exception:
            user_agent = random.choice(self._fallback_agents)

        request.headers["User-Agent"] = user_agent


class ProxyMiddleware:
    """
    Middleware for optional proxy rotation.

    Only active when PROXY_ENABLED=true in environment.
    Supports single proxy URL or a list from a file.
    """

    def __init__(self) -> None:
        """Initialize proxy configuration."""
        self._enabled = os.getenv("PROXY_ENABLED", "false").lower() == "true"
        self._proxies: list[str] = []

        if self._enabled:
            self._load_proxies()

    def _load_proxies(self) -> None:
        """Load proxy list from config."""
        # Single proxy URL
        proxy_url = os.getenv("PROXY_URL", "")
        if proxy_url:
            self._proxies.append(proxy_url)

        # Proxy list file
        proxy_list = os.getenv("PROXY_LIST", "")
        if proxy_list and os.path.isfile(proxy_list):
            with open(proxy_list, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self._proxies.append(line)

        if self._proxies:
            logger.info(
                "ProxyMiddleware: Loaded %d proxies.", len(self._proxies)
            )
        else:
            logger.warning("ProxyMiddleware: Enabled but no proxies configured.")
            self._enabled = False

    @classmethod
    def from_crawler(cls, crawler):
        """Create middleware from crawler."""
        return cls()

    def process_request(self, request: Request, spider: Spider) -> None:
        """Assign a random proxy to the request."""
        if not self._enabled or not self._proxies:
            return

        proxy = random.choice(self._proxies)
        request.meta["proxy"] = proxy
        logger.debug("Using proxy: %s for %s", proxy, request.url)


class ScrapingStatsMiddleware:
    """
    Middleware that tracks and logs scraping statistics.

    Records request/response counts, error rates, and timing
    for monitoring and debugging.
    """

    def __init__(self) -> None:
        self._request_count: int = 0
        self._response_count: int = 0
        self._error_count: int = 0

    @classmethod
    def from_crawler(cls, crawler):
        """Create middleware from crawler."""
        middleware = cls()
        crawler.signals.connect(
            middleware.spider_closed, signal=signals.spider_closed
        )
        return middleware

    def process_request(self, request: Request, spider: Spider) -> None:
        """Count outgoing requests."""
        self._request_count += 1

    def process_response(
        self, request: Request, response: Response, spider: Spider
    ) -> Response:
        """Count successful responses."""
        self._response_count += 1

        # Log non-200 responses
        if response.status != 200:
            logger.warning(
                "Non-200 response (%d) for %s",
                response.status, request.url,
            )

        return response

    def process_exception(
        self, request: Request, exception: Exception, spider: Spider
    ) -> None:
        """Count and log errors."""
        self._error_count += 1
        logger.error(
            "Request failed for %s: %s", request.url, exception,
        )

    def spider_closed(self, spider: Spider) -> None:
        """Log final statistics."""
        from job_scraper.logger import get_stats_logger

        stats_logger = get_stats_logger()
        stats_logger.info(
            "STATS | Spider: %s | Requests: %d | Responses: %d | Errors: %d",
            spider.name,
            self._request_count,
            self._response_count,
            self._error_count,
        )
