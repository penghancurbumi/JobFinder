"""
Job Model — SQLAlchemy ORM model for job listings.
===================================================

Maps to the 'jobs' table in PostgreSQL with proper indexes
for efficient querying and deduplication.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class Job(Base):
    """
    ORM model for a job listing.

    Stores all scraped job data with proper indexing for
    search, filtering, and deduplication.
    """

    __tablename__ = "jobs"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Core Info
    title = Column(String(500), nullable=False)
    company_name = Column(String(300), nullable=False)
    company_logo = Column(Text, nullable=True)
    company_website = Column(String(500), nullable=True)
    platform = Column(String(50), nullable=False)

    # Job Classification
    job_type = Column(String(50), nullable=True)
    employment_type = Column(String(50), nullable=True)
    work_type = Column(String(50), nullable=True)
    is_internship = Column(Boolean, default=False)
    experience_level = Column(String(50), nullable=True)

    # Salary
    salary_min = Column(BigInteger, nullable=True)
    salary_max = Column(BigInteger, nullable=True)
    salary_currency = Column(String(10), default="IDR")

    # Location
    location = Column(String(300), nullable=True)
    city = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    country = Column(String(100), default="Indonesia")

    # Description
    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    qualifications = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)

    # Tags & Skills (JSONB arrays)
    skills = Column(JSONB, default=list)
    category = Column(String(200), nullable=True)
    tags = Column(JSONB, default=list)

    # Dates
    posting_date = Column(DateTime(timezone=True), nullable=True)
    expired_date = Column(DateTime(timezone=True), nullable=True)

    # URLs
    apply_url = Column(Text, nullable=True)
    source_url = Column(Text, nullable=False, unique=True)

    # Metadata
    scraped_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, default=True)

    # Table-level indexes
    __table_args__ = (
        # Single column indexes
        Index("idx_jobs_platform", "platform"),
        Index("idx_jobs_company", "company_name"),
        Index("idx_jobs_city", "city"),
        Index("idx_jobs_province", "province"),
        Index("idx_jobs_job_type", "job_type"),
        Index("idx_jobs_work_type", "work_type"),
        Index("idx_jobs_is_internship", "is_internship"),
        Index("idx_jobs_experience_level", "experience_level"),
        Index("idx_jobs_posting_date", posting_date.desc()),
        Index("idx_jobs_scraped_at", scraped_at.desc()),
        Index("idx_jobs_is_active", "is_active"),

        # GIN indexes for JSONB
        Index("idx_jobs_skills", "skills", postgresql_using="gin"),
        Index("idx_jobs_tags", "tags", postgresql_using="gin"),

        # Composite index for deduplication
        Index(
            "idx_jobs_dedup",
            func.lower(Column("title")),
            func.lower(Column("company_name")),
            func.lower(Column("city")),
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<Job(title='{self.title}', "
            f"company='{self.company_name}', "
            f"platform='{self.platform}')>"
        )

    def to_dict(self) -> dict:
        """Convert the Job instance to a dictionary."""
        return {
            "id": str(self.id),
            "title": self.title,
            "company_name": self.company_name,
            "company_logo": self.company_logo,
            "company_website": self.company_website,
            "platform": self.platform,
            "job_type": self.job_type,
            "employment_type": self.employment_type,
            "work_type": self.work_type,
            "is_internship": self.is_internship,
            "experience_level": self.experience_level,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_currency": self.salary_currency,
            "location": self.location,
            "city": self.city,
            "province": self.province,
            "country": self.country,
            "description": self.description,
            "requirements": self.requirements,
            "responsibilities": self.responsibilities,
            "qualifications": self.qualifications,
            "benefits": self.benefits,
            "skills": self.skills,
            "category": self.category,
            "tags": self.tags,
            "posting_date": self.posting_date.isoformat() if self.posting_date else None,
            "expired_date": self.expired_date.isoformat() if self.expired_date else None,
            "apply_url": self.apply_url,
            "source_url": self.source_url,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }
