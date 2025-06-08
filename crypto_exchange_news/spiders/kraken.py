import scrapy
import random
import time
from urllib.parse import urlencode
from datetime import datetime
from scrapy.utils.project import get_project_settings


class KrakenSpider(scrapy.Spider):
    name = "kraken"

    settings = get_project_settings()

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": random.choice(settings["USER_AGENT"]),
    }

    asset_dict = {}

    # json api url:https://blog.kraken.com/wp-json/wp/v2/

    def start_requests(self):
        yield scrapy.Request(
            url="https://blog.kraken.com/wp-json/wp/v2/categories?per_page=100",
            headers=self.headers,
            callback=self.parse_category,
        )

    def parse_category(self, response):
        for r in response.json():
            self.asset_dict[r["id"]] = r["name"]
        params = {"per_page": 50, "page": 1, "order": "desc", "orderby": "date"}

        for page in range(self.settings["MAX_PAGE"]):
            params["page"] = page + 1
            yield scrapy.Request(
                url="https://blog.kraken.com/wp-json/wp/v2/posts?" + urlencode(params),
                headers=self.headers,
                callback=self.parse_post,
            )

    def parse_post(self, response):
        for item in response.json():
            yield {
                "news_id": item["id"],
                "title": item["title"]["rendered"],
                "desc": item["excerpt"]["rendered"],
                "url": "https://blog.kraken.com/?p=" + str(item["id"]),
                "category_str": ",".join(
                    [self.asset_dict[i] for i in item["categories"]]
                ),
                "exchange": self.name,
                "announced_at_timestamp": int(
                    datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S").timestamp()
                ),
                "timestamp": int(time.time()),
            }
