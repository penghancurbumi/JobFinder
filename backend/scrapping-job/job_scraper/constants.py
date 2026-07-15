"""
Constants — Enums, mappings, and constant values.
=================================================

Centralized location for all enums and normalization mappings
used throughout the scraping system.
"""

from enum import Enum


class Platform(str, Enum):
    """Supported job platforms."""
    JOBSTREET = "jobstreet"
    GLINTS = "glints"
    KALIBRR = "kalibrr"
    INDEED = "indeed"
    LINKEDIN = "linkedin"
    JOBSDB = "jobsdb"
    TECHINASIA = "techinasia"


class JobType(str, Enum):
    """Job type classification."""
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    TEMPORARY = "temporary"
    VOLUNTEER = "volunteer"
    OTHER = "other"


class EmploymentType(str, Enum):
    """Employment type classification."""
    PERMANENT = "permanent"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    APPRENTICESHIP = "apprenticeship"
    FRESH_GRADUATE = "fresh-graduate"


class WorkType(str, Enum):
    """Work arrangement type."""
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


class ExperienceLevel(str, Enum):
    """Experience level classification."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    EXECUTIVE = "executive"


# ============================================
# Normalization Mappings
# ============================================

JOB_TYPE_MAPPING: dict[str, str] = {
    # English
    "full time": JobType.FULL_TIME,
    "full-time": JobType.FULL_TIME,
    "fulltime": JobType.FULL_TIME,
    "part time": JobType.PART_TIME,
    "part-time": JobType.PART_TIME,
    "parttime": JobType.PART_TIME,
    "contract": JobType.CONTRACT,
    "kontrak": JobType.CONTRACT,
    "freelance": JobType.FREELANCE,
    "freelancer": JobType.FREELANCE,
    "temporary": JobType.TEMPORARY,
    "volunteer": JobType.VOLUNTEER,
    # Indonesian
    "penuh waktu": JobType.FULL_TIME,
    "paruh waktu": JobType.PART_TIME,
    "lepas": JobType.FREELANCE,
    "sementara": JobType.TEMPORARY,
    "sukarela": JobType.VOLUNTEER,
}

WORK_TYPE_MAPPING: dict[str, str] = {
    # English
    "onsite": WorkType.ONSITE,
    "on-site": WorkType.ONSITE,
    "on site": WorkType.ONSITE,
    "office": WorkType.ONSITE,
    "remote": WorkType.REMOTE,
    "work from home": WorkType.REMOTE,
    "wfh": WorkType.REMOTE,
    "hybrid": WorkType.HYBRID,
    # Indonesian
    "di kantor": WorkType.ONSITE,
    "dari rumah": WorkType.REMOTE,
    "jarak jauh": WorkType.REMOTE,
    "kerja dari rumah": WorkType.REMOTE,
}

EMPLOYMENT_TYPE_MAPPING: dict[str, str] = {
    "permanent": EmploymentType.PERMANENT,
    "tetap": EmploymentType.PERMANENT,
    "temporary": EmploymentType.TEMPORARY,
    "sementara": EmploymentType.TEMPORARY,
    "internship": EmploymentType.INTERNSHIP,
    "intern": EmploymentType.INTERNSHIP,
    "magang": EmploymentType.INTERNSHIP,
    "apprenticeship": EmploymentType.APPRENTICESHIP,
    "fresh graduate": EmploymentType.FRESH_GRADUATE,
    "fresh grad": EmploymentType.FRESH_GRADUATE,
    "entry level": EmploymentType.FRESH_GRADUATE,
}

EXPERIENCE_LEVEL_MAPPING: dict[str, str] = {
    "entry": ExperienceLevel.ENTRY,
    "entry level": ExperienceLevel.ENTRY,
    "entry-level": ExperienceLevel.ENTRY,
    "junior": ExperienceLevel.JUNIOR,
    "mid": ExperienceLevel.MID,
    "mid level": ExperienceLevel.MID,
    "mid-level": ExperienceLevel.MID,
    "middle": ExperienceLevel.MID,
    "senior": ExperienceLevel.SENIOR,
    "lead": ExperienceLevel.LEAD,
    "principal": ExperienceLevel.LEAD,
    "manager": ExperienceLevel.MANAGER,
    "managerial": ExperienceLevel.MANAGER,
    "executive": ExperienceLevel.EXECUTIVE,
    "director": ExperienceLevel.EXECUTIVE,
    "c-level": ExperienceLevel.EXECUTIVE,
    # Indonesian
    "pemula": ExperienceLevel.ENTRY,
    "menengah": ExperienceLevel.MID,
    "berpengalaman": ExperienceLevel.SENIOR,
}

CURRENCY_MAPPING: dict[str, str] = {
    "rp": "IDR",
    "rp.": "IDR",
    "idr": "IDR",
    "rupiah": "IDR",
    "$": "USD",
    "usd": "USD",
    "sgd": "SGD",
    "s$": "SGD",
    "myr": "MYR",
    "rm": "MYR",
    "php": "PHP",
    "₱": "PHP",
    "thb": "THB",
    "฿": "THB",
    "vnd": "VND",
    "₫": "VND",
}

# ============================================
# Indonesian Province & City Mappings
# ============================================

PROVINCE_MAPPING: dict[str, str] = {
    # DKI Jakarta
    "jakarta": "DKI Jakarta",
    "dki jakarta": "DKI Jakarta",
    "jakarta selatan": "DKI Jakarta",
    "jakarta pusat": "DKI Jakarta",
    "jakarta barat": "DKI Jakarta",
    "jakarta timur": "DKI Jakarta",
    "jakarta utara": "DKI Jakarta",
    # Jawa Barat
    "bandung": "Jawa Barat",
    "bogor": "Jawa Barat",
    "depok": "Jawa Barat",
    "bekasi": "Jawa Barat",
    "cimahi": "Jawa Barat",
    "karawang": "Jawa Barat",
    "tasikmalaya": "Jawa Barat",
    "sukabumi": "Jawa Barat",
    "garut": "Jawa Barat",
    # Jawa Tengah
    "semarang": "Jawa Tengah",
    "solo": "Jawa Tengah",
    "surakarta": "Jawa Tengah",
    "magelang": "Jawa Tengah",
    "pekalongan": "Jawa Tengah",
    "tegal": "Jawa Tengah",
    "purwokerto": "Jawa Tengah",
    "kudus": "Jawa Tengah",
    # Jawa Timur
    "surabaya": "Jawa Timur",
    "malang": "Jawa Timur",
    "sidoarjo": "Jawa Timur",
    "gresik": "Jawa Timur",
    "kediri": "Jawa Timur",
    "jember": "Jawa Timur",
    "mojokerto": "Jawa Timur",
    "pasuruan": "Jawa Timur",
    # DI Yogyakarta
    "yogyakarta": "DI Yogyakarta",
    "jogja": "DI Yogyakarta",
    "jogjakarta": "DI Yogyakarta",
    "sleman": "DI Yogyakarta",
    "bantul": "DI Yogyakarta",
    # Banten
    "tangerang": "Banten",
    "tangerang selatan": "Banten",
    "cilegon": "Banten",
    "serang": "Banten",
    # Bali
    "denpasar": "Bali",
    "badung": "Bali",
    "gianyar": "Bali",
    "bali": "Bali",
    # Sumatera Utara
    "medan": "Sumatera Utara",
    "binjai": "Sumatera Utara",
    "pematangsiantar": "Sumatera Utara",
    # Sumatera Selatan
    "palembang": "Sumatera Selatan",
    # Sumatera Barat
    "padang": "Sumatera Barat",
    "bukittinggi": "Sumatera Barat",
    # Riau
    "pekanbaru": "Riau",
    "dumai": "Riau",
    # Kepulauan Riau
    "batam": "Kepulauan Riau",
    "tanjungpinang": "Kepulauan Riau",
    # Kalimantan Timur
    "balikpapan": "Kalimantan Timur",
    "samarinda": "Kalimantan Timur",
    # Kalimantan Selatan
    "banjarmasin": "Kalimantan Selatan",
    # Sulawesi Selatan
    "makassar": "Sulawesi Selatan",
    # Lampung
    "bandar lampung": "Lampung",
    # Aceh
    "banda aceh": "Aceh",
}

CITY_NORMALIZATION: dict[str, str] = {
    "jaksel": "Jakarta Selatan",
    "jakpus": "Jakarta Pusat",
    "jakbar": "Jakarta Barat",
    "jaktim": "Jakarta Timur",
    "jakut": "Jakarta Utara",
    "tangsel": "Tangerang Selatan",
    "jogja": "Yogyakarta",
    "jogjakarta": "Yogyakarta",
    "solo": "Surakarta",
    "bandung barat": "Bandung",
}

# ============================================
# Spider Configuration
# ============================================

DEFAULT_HEADERS: dict[str, str] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}

# Maximum number of pages to scrape per spider run (safety limit)
MAX_PAGES_PER_RUN: int = 100

# Maximum number of retries per request
MAX_RETRIES: int = 3

# Delay between requests in seconds
DEFAULT_DELAY: float = 1.0
