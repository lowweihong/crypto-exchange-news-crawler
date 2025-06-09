import scrapy
import random
import time
from scrapy.utils.project import get_project_settings

class CryptocomSpider(scrapy.Spider):
    name = "cryptocom"
    
    settings = get_project_settings()
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'origin': 'https://crypto.com',
        'priority': 'u=1, i',
        'referer': 'https://crypto.com/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': random.choice(settings["USER_AGENT"])}
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://static2.crypto.com/exchange/announcements_en.json",
            callback=self.parse,
            method="GET",
        )

    def parse(self, response):
        for r in response.json():
            yield  {
                'news_id': r['id'],
                'title': r['title'],
                'desc': r['content'],
                'url': "https://crypto.com/exchange/announcements/%s/%s"%(r['category'],r['id']),
                'category_str': r['category']+'.'+r['productType'],
                'exchange': 'crypto.com',
                'announced_at_timestamp': r['announcedAt']//1000,
                'timestamp': int(time.time())
            }
            
