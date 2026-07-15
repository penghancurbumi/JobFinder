"""
Settings — Scrapy project settings.
====================================

Reads configuration from .env file and sets up Scrapy with
Playwright, custom middlewares, and pipeline chain.
"""

import os
import sys

from dotenv import load_dotenv

if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables
load_dotenv()

# ============================================
# Project Identity
# ============================================
BOT_NAME = "job_scraper"
SPIDER_MODULES = ["job_scraper.spiders"]
NEWSPIDER_MODULE = "job_scraper.spiders"

# Custom commands module
COMMANDS_MODULE = "job_scraper.commands"

# ============================================
# Scrapy-Playwright Configuration (DISABLED on Windows)
# ============================================
# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }
# 
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# 
# PLAYWRIGHT_BROWSER_TYPE = os.getenv("PLAYWRIGHT_BROWSER_TYPE", "chromium")
# PLAYWRIGHT_LAUNCH_OPTIONS = {
#     "headless": os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true",
#     "timeout": int(os.getenv("PLAYWRIGHT_TIMEOUT", "30000")),
# }

# Playwright default navigation timeout (ms)
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = int(
    os.getenv("PLAYWRIGHT_TIMEOUT", "30000")
)

# ============================================
# Crawl Politeness
# ============================================
ROBOTSTXT_OBEY = False  # Many job sites block bots via robots.txt

DOWNLOAD_DELAY = float(os.getenv("DOWNLOAD_DELAY", "1.0"))
RANDOMIZE_DOWNLOAD_DELAY = os.getenv(
    "RANDOMIZE_DOWNLOAD_DELAY", "true"
).lower() == "true"

CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS", "8"))
CONCURRENT_REQUESTS_PER_DOMAIN = int(
    os.getenv("CONCURRENT_REQUESTS_PER_DOMAIN", "2")
)

# ============================================
# Download Settings
# ============================================
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "30"))

# ============================================
# Retry Settings
# ============================================
RETRY_ENABLED = os.getenv("RETRY_ENABLED", "true").lower() == "true"
RETRY_TIMES = int(os.getenv("RETRY_TIMES", "3"))
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# ============================================
# AutoThrottle
# ============================================
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# ============================================
# Middlewares
# ============================================
DOWNLOADER_MIDDLEWARES = {
    # Disable default User-Agent middleware
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,

    # Custom middlewares
    "job_scraper.middlewares.RandomUserAgentMiddleware": 400,
    "job_scraper.middlewares.ProxyMiddleware": 410,
    "job_scraper.middlewares.ScrapingStatsMiddleware": 420,
}

# ============================================
# Item Pipelines (ordered by priority)
# ============================================
# ITEM_PIPELINES = {
#     "job_scraper.pipelines.ValidationPipeline": 100,
#     "job_scraper.pipelines.CleanerPipeline": 200,
#     "job_scraper.pipelines.NormalizerPipeline": 300,
#     "job_scraper.pipelines.DeduplicatorPipeline": 400,
#     "job_scraper.pipelines.PostgresPipeline": 500,
#     "job_scraper.pipelines.ExportPipeline": 600,
# }
ITEM_PIPELINES = {
    "job_scraper.pipelines.ValidationPipeline": 100,
    "job_scraper.pipelines.CleanerPipeline": 200,
    "job_scraper.pipelines.NormalizerPipeline": 300,
    "job_scraper.pipelines.DeduplicatorPipeline": 400,
    # "job_scraper.pipelines.PostgresPipeline": 500,  # Disabled, using simple JSON export
    "job_scraper.pipelines.ExportPipeline": 600,
}

# ============================================
# Logging
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# Disable Scrapy's default log file (we use our own)
LOG_FILE = None

# ============================================
# HTTP Cache (disabled by default, enable for development)
# ============================================
HTTPCACHE_ENABLED = False
# HTTPCACHE_EXPIRATION_SECS = 3600
# HTTPCACHE_DIR = "storage/httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = [403, 429, 500, 502, 503]

# ============================================
# Feed Export Defaults
# ============================================
FEED_EXPORT_ENCODING = "utf-8"

# ============================================
# Request Fingerprinter
# ============================================
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
