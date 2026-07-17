import scrapy
import json
from datetime import datetime

class FastworkSpider(scrapy.Spider):
    name = 'fastwork'
    allowed_domains = ['fastwork.id']
    
    def __init__(self, job_type=None, work_type=None, max_pages=None, *args, **kwargs):
        super(FastworkSpider, self).__init__(*args, **kwargs)
        self.job_type = job_type
        self.work_type = work_type
        self.max_pages = int(max_pages) if max_pages else 3
        self.current_page = 1
        
        # Fastwork is heavily API driven. This is a basic implementation 
        # targeting freelance programming/tech jobs.
        self.base_url = "https://fastwork.id/api/v2/products/search"
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def start_requests(self):
        # We simulate a search request to their API for tech jobs
        payload = {
            "query": "programming",
            "page": self.current_page,
            "limit": 20
        }
        
        yield scrapy.Request(
            url=f"{self.base_url}?query=programming&page={self.current_page}&limit=20",
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            products = data.get('data', {}).get('products', [])
            
            for item in products:
                # Fastwork is a platform for freelancers to sell services, 
                # but we interpret them as freelance opportunities / projects
                
                title = item.get('title', '')
                username = item.get('user', {}).get('username', 'Unknown')
                price = item.get('price', 0)
                
                yield {
                    'title': title,
                    'company_name': f"Client: {username}",
                    'location': "Remote",
                    'job_type': "Contract",
                    'work_type': "Remote",
                    'skills': ["Freelance", "Project"],
                    'platform': 'Fastwork',
                    'source_url': f"https://fastwork.id/user/{username}/{item.get('seo_url', '')}",
                    'description': item.get('detail', title),
                    'updated_at': datetime.now().isoformat(),
                    'salary_min': price,
                    'salary_max': price,
                    'salary_currency': 'IDR'
                }
                
            # Pagination
            total_pages = data.get('data', {}).get('total_pages', 1)
            if self.current_page < total_pages and self.current_page < self.max_pages:
                self.current_page += 1
                yield scrapy.Request(
                    url=f"{self.base_url}?query=programming&page={self.current_page}&limit=20",
                    headers=self.headers,
                    callback=self.parse
                )
                
        except Exception as e:
            self.logger.error(f"Error parsing fastwork response: {str(e)}")
