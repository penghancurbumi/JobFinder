"""
Scheduler — Cron-based job scheduling.
======================================

Uses APScheduler to run spiders on a recurring schedule.
Supports hourly, every 6 hours, and daily intervals.

Usage:
    python scheduler.py
"""

import os
import subprocess
import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()


def run_spider(spider_name: str) -> None:
    """
    Run a single spider via subprocess.

    Args:
        spider_name: Name of the spider to run.
    """
    print(f"[{datetime.now()}] Running spider: {spider_name}")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "scrapy", "crawl", spider_name],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        if result.returncode == 0:
            print(f"[{datetime.now()}] Spider '{spider_name}' completed successfully.")
        else:
            print(f"[{datetime.now()}] Spider '{spider_name}' failed:")
            print(result.stderr[-500:] if result.stderr else "No error output")

    except Exception as e:
        print(f"[{datetime.now()}] Error running spider '{spider_name}': {e}")


def run_all_spiders() -> None:
    """Run all configured spiders sequentially."""
    spiders = [
        "glints",
        "jobstreet",
        "kalibrr",
        "indeed",
        "linkedin",
        "jobsdb",
        "techinasia",
    ]

    print(f"[{datetime.now()}] Starting scheduled crawl for all spiders...")
    for spider in spiders:
        run_spider(spider)
    print(f"[{datetime.now()}] All spiders completed.")


def main() -> None:
    """Start the scheduler."""
    interval_hours = int(os.getenv("SCHEDULER_INTERVAL_HOURS", "6"))

    scheduler = BlockingScheduler()

    # Schedule based on interval
    if interval_hours == 1:
        # Every hour
        trigger = CronTrigger(minute=0)
        print("Scheduler configured: Every hour")
    elif interval_hours == 6:
        # Every 6 hours (00:00, 06:00, 12:00, 18:00)
        trigger = CronTrigger(hour="0,6,12,18", minute=0)
        print("Scheduler configured: Every 6 hours")
    elif interval_hours == 24:
        # Once daily at 02:00 (off-peak)
        trigger = CronTrigger(hour=2, minute=0)
        print("Scheduler configured: Daily at 02:00")
    else:
        # Custom interval
        trigger = CronTrigger(hour=f"*/{interval_hours}", minute=0)
        print(f"Scheduler configured: Every {interval_hours} hours")

    scheduler.add_job(
        run_all_spiders,
        trigger=trigger,
        id="crawl_all",
        name="Crawl all job platforms",
        max_instances=1,
        replace_existing=True,
    )

    print(f"[{datetime.now()}] Scheduler started. Press Ctrl+C to exit.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\nScheduler stopped.")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
