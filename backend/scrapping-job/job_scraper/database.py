"""
Database — SQLAlchemy engine and session management.
====================================================

Provides database connection pooling, session factory,
and table creation utilities for PostgreSQL.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from job_scraper.logger import get_logger

load_dotenv()

logger = get_logger("database")


def get_database_url() -> str:
    """
    Build PostgreSQL connection URL from environment variables.

    Returns:
        PostgreSQL connection string.
    """
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "job_scraper")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def create_db_engine() -> Engine:
    """
    Create a SQLAlchemy engine with connection pooling.

    Returns:
        Configured SQLAlchemy Engine.
    """
    url = get_database_url()

    engine = create_engine(
        url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
        echo=False,
    )

    logger.info("Database engine created: %s:%s/%s",
                os.getenv("DB_HOST", "localhost"),
                os.getenv("DB_PORT", "5432"),
                os.getenv("DB_NAME", "job_scraper"))

    return engine


def create_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    """
    Create a session factory bound to the engine.

    Args:
        engine: SQLAlchemy engine. Creates new one if None.

    Returns:
        Configured sessionmaker.
    """
    if engine is None:
        engine = create_db_engine()

    return sessionmaker(bind=engine, expire_on_commit=False)


def init_database(engine: Engine | None = None) -> Engine:
    """
    Initialize the database by creating all tables.

    Args:
        engine: SQLAlchemy engine. Creates new one if None.

    Returns:
        The engine used for initialization.
    """
    from job_scraper.models.job import Base

    if engine is None:
        engine = create_db_engine()

    Base.metadata.create_all(engine)
    logger.info("Database tables created successfully.")
    return engine


def test_connection(engine: Engine | None = None) -> bool:
    """
    Test the database connection.

    Args:
        engine: SQLAlchemy engine. Creates new one if None.

    Returns:
        True if connection is successful, False otherwise.
    """
    if engine is None:
        engine = create_db_engine()

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection test: OK")
        return True
    except Exception as e:
        logger.error("Database connection test FAILED: %s", e)
        return False
