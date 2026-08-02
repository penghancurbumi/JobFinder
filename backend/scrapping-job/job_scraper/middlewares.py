import os
import random

from fake_useragent import UserAgent
from scrapy import Request, Spider, signals
from scrapy.http import Response

from job_scraper.logger import get_logger

logger = get_logger("middlewares")


class RandomUserAgentMiddleware:
    def __init__(self) -> None:
        try:
            self._ua = UserAgent(
                browsers=["Chrome", "Firefox", "Edge"],
                os=["Windows", "Linux"],
                min_percentage=1.0,
            )
            logger.info("RandomUserAgentMiddleware: Initialized with fake-useragent.")
        except Exception as e:
            logger.warning(
                "RandomUserAgentMiddleware: Failed to init fake-useragent (%s). Using fallback list.", e,
            )
            self._ua = None

        self._fallback_agents: list[str] = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request: Request, spider: Spider) -> None:
        try:
            if self._ua:
                user_agent = self._ua.random
            else:
                user_agent = random.choice(self._fallback_agents)
        except Exception:
            user_agent = random.choice(self._fallback_agents)
        request.headers["User-Agent"] = user_agent


class ProxyMiddleware:
    def __init__(self) -> None:
        self._enabled = os.getenv("PROXY_ENABLED", "false").lower() == "true"
        self._proxies: list[str] = []
        if self._enabled:
            self._load_proxies()

    def _load_proxies(self) -> None:
        proxy_url = os.getenv("PROXY_URL", "")
        if proxy_url:
            self._proxies.append(proxy_url)
        proxy_list = os.getenv("PROXY_LIST", "")
        if proxy_list and os.path.isfile(proxy_list):
            with open(proxy_list, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self._proxies.append(line)
        if self._proxies:
            logger.info("ProxyMiddleware: Loaded %d proxies.", len(self._proxies))
        else:
            logger.warning("ProxyMiddleware: Enabled but no proxies configured.")
            self._enabled = False

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request: Request, spider: Spider) -> None:
        if not self._enabled or not self._proxies:
            return
        proxy = random.choice(self._proxies)
        request.meta["proxy"] = proxy


class ScrapingStatsMiddleware:
    def __init__(self) -> None:
        self._request_count: int = 0
        self._response_count: int = 0
        self._error_count: int = 0

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request: Request, spider: Spider) -> None:
        self._request_count += 1

    def process_response(self, request: Request, response: Response, spider: Spider) -> Response:
        self._response_count += 1
        if response.status != 200:
            logger.warning("Non-200 response (%d) for %s", response.status, request.url)
        return response

    def process_exception(self, request: Request, exception: Exception, spider: Spider) -> None:
        self._error_count += 1
        logger.error("Request failed for %s: %s", request.url, exception)

    def spider_closed(self, spider: Spider) -> None:
        from job_scraper.logger import get_stats_logger
        stats_logger = get_stats_logger()
        stats_logger.info(
            "STATS | Spider: %s | Requests: %d | Responses: %d | Errors: %d",
            spider.name, self._request_count, self._response_count, self._error_count,
        )


class CloudflareBypassMiddleware:
    def process_request(self, request: Request, spider: Spider):
        if not request.meta.get("impersonate"):
            return None

        from curl_cffi import requests as curl_requests

        spider.logger_custom.info(
            "CloudflareBypass: Fetching %s via curl_cffi impersonation", request.url
        )

        headers = dict(request.headers.to_unicode_dict())
        headers.setdefault("Accept-Language", "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7")
        headers.setdefault("Referer", "https://www.google.com/")

        body = request.body
        method = request.method.upper()
        url = request.url
        cookies = request.cookies

        try:
            if method == "POST":
                resp = curl_requests.post(
                    url, impersonate="chrome131", headers=headers,
                    json=request.meta.get("json_body"),
                    data=body if not request.meta.get("json_body") else None,
                    cookies=cookies, timeout=30,
                )
            else:
                resp = curl_requests.get(
                    url, impersonate="chrome131", headers=headers,
                    cookies=cookies, timeout=30,
                )
        except Exception as e:
            spider.logger_custom.error("CloudflareBypass: Request failed for %s: %s", url, e)
            return None

        from scrapy.http import TextResponse

        return TextResponse(
            url=url, status=resp.status_code,
            headers=dict(resp.headers), body=resp.content,
            encoding="utf-8", request=request,
        )


class NotFoundCollectorMiddleware:
    """Records job-detail URLs that return 404/410 so the backend can delete
    expired listings. URLs are appended to exports/json/not_found.txt, which the
    Node backend consumes after each scrape cycle."""

    def __init__(self) -> None:
        export_dir = os.getenv("EXPORT_DIR", "exports")
        self._file = os.path.join(export_dir, "json", "not_found.txt")
        self._urls: set[str] = set()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_response(self, request: Request, response: Response, spider: Spider) -> Response:
        if response.status in (404, 410):
            self._urls.add(request.url)
        return response

    def spider_closed(self, spider: Spider) -> None:
        if not self._urls:
            return
        try:
            os.makedirs(os.path.dirname(self._file), exist_ok=True)
            with open(self._file, "a", encoding="utf-8") as f:
                for url in sorted(self._urls):
                    f.write(url + "\n")
            logger.info(
                "NotFoundCollectorMiddleware: wrote %d not-found URL(s) for %s",
                len(self._urls), spider.name,
            )
        except Exception as e:
            logger.error("NotFoundCollectorMiddleware: failed to write not-found file: %s", e)
