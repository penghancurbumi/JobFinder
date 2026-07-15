"""
Items — Scrapy Item definitions.
================================

Defines the JobItem with all fields that will be collected
from each job listing across all platforms.
"""

import scrapy


class JobItem(scrapy.Item):
    """
    Represents a single job listing scraped from any platform.

    All fields are optional except those marked as required in the
    ValidationPipeline (title, company_name, platform, source_url).
    """

    # Core Info
    title: scrapy.Field = scrapy.Field()
    company_name: scrapy.Field = scrapy.Field()
    company_logo: scrapy.Field = scrapy.Field()
    company_website: scrapy.Field = scrapy.Field()
    platform: scrapy.Field = scrapy.Field()

    # Job Classification
    job_type: scrapy.Field = scrapy.Field()
    employment_type: scrapy.Field = scrapy.Field()
    work_type: scrapy.Field = scrapy.Field()
    is_internship: scrapy.Field = scrapy.Field()
    experience_level: scrapy.Field = scrapy.Field()

    # Salary
    salary_min: scrapy.Field = scrapy.Field()
    salary_max: scrapy.Field = scrapy.Field()
    salary_currency: scrapy.Field = scrapy.Field()

    # Location
    location: scrapy.Field = scrapy.Field()
    city: scrapy.Field = scrapy.Field()
    province: scrapy.Field = scrapy.Field()
    country: scrapy.Field = scrapy.Field()

    # Description (full text)
    description: scrapy.Field = scrapy.Field()
    requirements: scrapy.Field = scrapy.Field()
    responsibilities: scrapy.Field = scrapy.Field()
    qualifications: scrapy.Field = scrapy.Field()
    benefits: scrapy.Field = scrapy.Field()

    # Tags & Skills
    skills: scrapy.Field = scrapy.Field()
    category: scrapy.Field = scrapy.Field()
    tags: scrapy.Field = scrapy.Field()

    # Dates
    posting_date: scrapy.Field = scrapy.Field()
    expired_date: scrapy.Field = scrapy.Field()

    # URLs
    apply_url: scrapy.Field = scrapy.Field()
    source_url: scrapy.Field = scrapy.Field()

    # Metadata
    scraped_at: scrapy.Field = scrapy.Field()
    updated_at: scrapy.Field = scrapy.Field()
