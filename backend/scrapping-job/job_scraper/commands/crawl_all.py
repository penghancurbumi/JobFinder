from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Command(ScrapyCommand):
    requires_project = True
    default_settings = {"LOG_LEVEL": "INFO"}

    def syntax(self) -> str:
        return "[options]"

    def short_desc(self) -> str:
        return "Run all job scraper spiders sequentially"

    def add_options(self, parser) -> None:
        super().add_options(parser)
        parser.add_argument("--job-type", dest="job_type", default=None, help="Filter by job type")
        parser.add_argument("--work-type", dest="work_type", default=None, help="Filter by work type")
        parser.add_argument("--max-pages", dest="max_pages", type=int, default=None, help="Max pages per spider")

    def run(self, args, opts) -> None:
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        spider_loader = process.spider_loader
        spider_names = spider_loader.list()

        if not spider_names:
            print("No spiders found!")
            return

        print(f"Running {len(spider_names)} spiders: {', '.join(spider_names)}")

        spider_kwargs = {}
        if opts.job_type:
            spider_kwargs["job_type"] = opts.job_type
        if opts.work_type:
            spider_kwargs["work_type"] = opts.work_type
        if opts.max_pages:
            spider_kwargs["max_pages"] = opts.max_pages

        for spider_name in spider_names:
            print(f"  -> Queueing: {spider_name}")
            process.crawl(spider_name, **spider_kwargs)

        process.start()
        print("All spiders completed.")
