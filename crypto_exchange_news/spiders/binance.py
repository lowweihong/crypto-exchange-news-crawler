import scrapy
import random
import time
import copy
from scrapy.utils.project import get_project_settings
from urllib.parse import urlencode

class BinanceSpider(scrapy.Spider):
    name = 'binance'
    
    settings = get_project_settings()
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'clienttype': 'web',
        'content-type': 'application/json',
        'lang': 'en',
        'priority': 'u=1, i',
        'referer': 'https://www.binance.com/en/support/announcement/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': random.choice(settings["USER_AGENT"]),
    }
    
    params = {
        'type': '1',
        'pageNo': '1',
        'pageSize': '50',
    }

    url = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?"
    
    
    def start_requests(self):
        for page in range(int(self.settings["MAX_PAGE"])):
            params = copy.deepcopy(self.params)
            params["pageNo"] = str(page+1)
            yield scrapy.Request(url = self.url + urlencode(params),
                                        headers=self.headers,
                                        dont_filter=True,
                                        method='GET',
                                        callback=self.parse)
        

    def parse(self, response):
        for item in response.json()["data"]["catalogs"]:
            for cat_item in item['articles']:
                data =  {
                    'news_id': cat_item['code'],
                    'title': cat_item['title'],
                    'desc': '',
                    'url': response.urljoin(cat_item['code']),
                    'category_str': item['catalogName'],
                    'exchange': self.name,
                    'announced_at_timestamp': cat_item['releaseDate']//1000,
                    "timestamp": int(time.time()),
                }

                yield data
                
            