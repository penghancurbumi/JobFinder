from enum import Enum


class Platform(str, Enum):
    JOBSTREET = "jobstreet"
    GLINTS = "glints"
    KALIBRR = "kalibrr"
    LINKEDIN = "linkedin"
    JOBSDB = "jobsdb"
    TECHINASIA = "techinasia"
    KITALULUS = "kitalulus"
    PINTARNYA = "pintarnya"


class JobType(str, Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    TEMPORARY = "temporary"
    VOLUNTEER = "volunteer"
    OTHER = "other"


class EmploymentType(str, Enum):
    PERMANENT = "permanent"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    APPRENTICESHIP = "apprenticeship"
    FRESH_GRADUATE = "fresh-graduate"


class WorkType(str, Enum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    EXECUTIVE = "executive"


JOB_TYPE_MAPPING: dict[str, str] = {
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
    "penuh waktu": JobType.FULL_TIME,
    "paruh waktu": JobType.PART_TIME,
    "lepas": JobType.FREELANCE,
    "sementara": JobType.TEMPORARY,
    "sukarela": JobType.VOLUNTEER,
}

WORK_TYPE_MAPPING: dict[str, str] = {
    "onsite": WorkType.ONSITE,
    "on-site": WorkType.ONSITE,
    "on site": WorkType.ONSITE,
    "office": WorkType.ONSITE,
    "remote": WorkType.REMOTE,
    "work from home": WorkType.REMOTE,
    "wfh": WorkType.REMOTE,
    "hybrid": WorkType.HYBRID,
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
    "thb": "THB",
    "vnd": "VND",
}

PROVINCE_MAPPING: dict[str, str] = {
    "jakarta": "DKI Jakarta",
    "dki jakarta": "DKI Jakarta",
    "jakarta selatan": "DKI Jakarta",
    "jakarta pusat": "DKI Jakarta",
    "jakarta barat": "DKI Jakarta",
    "jakarta timur": "DKI Jakarta",
    "jakarta utara": "DKI Jakarta",
    "bandung": "Jawa Barat",
    "bogor": "Jawa Barat",
    "depok": "Jawa Barat",
    "bekasi": "Jawa Barat",
    "cimahi": "Jawa Barat",
    "karawang": "Jawa Barat",
    "tasikmalaya": "Jawa Barat",
    "sukabumi": "Jawa Barat",
    "garut": "Jawa Barat",
    "semarang": "Jawa Tengah",
    "solo": "Jawa Tengah",
    "surakarta": "Jawa Tengah",
    "magelang": "Jawa Tengah",
    "pekalongan": "Jawa Tengah",
    "tegal": "Jawa Tengah",
    "purwokerto": "Jawa Tengah",
    "kudus": "Jawa Tengah",
    "surabaya": "Jawa Timur",
    "malang": "Jawa Timur",
    "sidoarjo": "Jawa Timur",
    "gresik": "Jawa Timur",
    "kediri": "Jawa Timur",
    "jember": "Jawa Timur",
    "mojokerto": "Jawa Timur",
    "pasuruan": "Jawa Timur",
    "yogyakarta": "DI Yogyakarta",
    "jogja": "DI Yogyakarta",
    "jogjakarta": "DI Yogyakarta",
    "sleman": "DI Yogyakarta",
    "bantul": "DI Yogyakarta",
    "tangerang": "Banten",
    "tangerang selatan": "Banten",
    "cilegon": "Banten",
    "serang": "Banten",
    "denpasar": "Bali",
    "badung": "Bali",
    "gianyar": "Bali",
    "bali": "Bali",
    "medan": "Sumatera Utara",
    "binjai": "Sumatera Utara",
    "pematangsiantar": "Sumatera Utara",
    "palembang": "Sumatera Selatan",
    "padang": "Sumatera Barat",
    "bukittinggi": "Sumatera Barat",
    "pekanbaru": "Riau",
    "dumai": "Riau",
    "batam": "Kepulauan Riau",
    "tanjungpinang": "Kepulauan Riau",
    "balikpapan": "Kalimantan Timur",
    "samarinda": "Kalimantan Timur",
    "banjarmasin": "Kalimantan Selatan",
    "makassar": "Sulawesi Selatan",
    "bandar lampung": "Lampung",
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

DEFAULT_HEADERS: dict[str, str] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}

MAX_PAGES_PER_RUN: int = 100
MAX_RETRIES: int = 3
DEFAULT_DELAY: float = 1.0
