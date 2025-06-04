import scrapy
import random
import json
import time
from scrapy.utils.project import get_project_settings


class BybitSpider(scrapy.Spider):
    name = "bybit"

    settings = get_project_settings()

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://announcements.bybit.com",
        "priority": "u=1, i",
        "referer": "https://announcements.bybit.com/",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": random.choice(settings["USER_AGENT"]),
    }

    url = (
        "https://api2.bybit.com/announcements/api/search/v1/index/announcement-posts_en"
    )

    def start_requests(self):
        json_data = {
            "data": {
                "query": "",
                "page": 0,
                "hitsPerPage": 8,
            },
        }

        for p in range(self.settings.get("MAX_PAGE")):
            json_data["data"]["page"] = p
            yield scrapy.Request(
                url=self.url,
                headers=self.headers,
                method="POST",
                body=json.dumps(json_data),
                callback=self.parse,
            )

    def parse(self, response):
        for r in response.json()["result"]["hits"]:
            data = {
                "news_id": r["url"].split("-")[-1].replace("/", ""),
                "title": r["title"],
                "desc": r["description"],
                "url": response.urljoin(r["url"]),
                "category_str": r["category"]["key"],
                "exchange": self.name,
                "announced_at_timestamp": int(r["date_timestamp"]),
                "timestamp": int(time.time()),
            }

            yield data
