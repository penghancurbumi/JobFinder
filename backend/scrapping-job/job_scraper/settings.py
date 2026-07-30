"""
Settings — Scrapy project configuration.
=========================================

Configures Playwright, custom middlewares, and pipeline chain.
"""

import os

# ============================================
# DOWNLOAD HANDLERS
# ============================================
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Enable Playwright for all HTTPS by default
# Spiders that don't need it can opt out via meta
PLAYWRIGHT_ENABLED = True

# ============================================
# SCRAPY-PLAYWRIGHT CONFIGURATION
# ============================================
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = os.getenv("PLAYWRIGHT_BROWSER_TYPE", "chromium")
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true",
    "timeout": int(os.getenv("PLAYWRIGHT_TIMEOUT", "30000")),
}

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = int(
    os.getenv("PLAYWRIGHT_TIMEOUT", "30000")
)

# ============================================
# BOT CONFIGURATION
# ============================================
BOT_NAME = "job_scraper"
SPIDER_MODULES = ["job_scraper.spiders"]
NEWSPIDER_MODULE = "job_scraper.spiders"
COMMANDS_MODULE = "job_scraper.commands"

# ============================================
# MIDDLEWARES
# ============================================
DOWNLOADER_MIDDLEWARES = {
    "job_scraper.middlewares.RandomUserAgentMiddleware": 400,
    "job_scraper.middlewares.ProxyMiddleware": 600,
    "job_scraper.middlewares.ScrapingStatsMiddleware": 700,
    "job_scraper.middlewares.CloudflareBypassMiddleware": 150,
}

# ============================================
# ITEM PIPELINES
# ============================================
ITEM_PIPELINES = {
    "job_scraper.pipelines.DuplicateFilterPipeline": 100,
    "job_scraper.pipelines.CleanerPipeline": 200,
    "job_scraper.pipelines.ValidatorPipeline": 300,
    "job_scraper.pipelines.JsonExportPipeline": 400,
}

# ============================================
# EXTENSIONS
# ============================================
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

# ============================================
# REQUEST & CONCURRENCY
# ============================================
CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS", "4"))
DOWNLOAD_DELAY = float(os.getenv("DOWNLOAD_DELAY", "1.0"))
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS_PER_DOMAIN = int(os.getenv("CONCURRENT_REQUESTS_PER_DOMAIN", "2"))
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = float(os.getenv("AUTOTHROTTLE_START_DELAY", "1.0"))
AUTOTHROTTLE_MAX_DELAY = float(os.getenv("AUTOTHROTTLE_MAX_DELAY", "10.0"))
AUTOTHROTTLE_TARGET_CONCURRENCY = float(os.getenv("AUTOTHROTTLE_TARGET_CONCURRENCY", "1.0"))

# ============================================
# ROBOTS & CACHE
# ============================================
ROBOTSTXT_OBEY = os.getenv("ROBOTSTXT_OBEY", "false").lower() == "true"
HTTPCACHE_ENABLED = os.getenv("HTTPCACHE_ENABLED", "false").lower() == "true"
HTTPCACHE_EXPIRATION_SECS = int(os.getenv("HTTPCACHE_EXPIRATION_SECS", "3600"))

# ============================================
# COOKIES
# ============================================
COOKIES_ENABLED = True
COOKIES_DEBUG = os.getenv("COOKIES_DEBUG", "false").lower() == "true"

# ============================================
# LOGGING
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", None)

# ============================================
# EXPORTS
# ============================================
EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")
EXPORT_JSON_DIR = os.path.join(EXPORT_DIR, "json")

# ============================================
# FAILURE HANDLING
# ============================================
RETRY_ENABLED = True
RETRY_TIMES = int(os.getenv("RETRY_TIMES", "3"))
RETRY_HTTP_CODES = [429, 500, 502, 503, 504]
