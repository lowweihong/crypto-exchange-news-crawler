import scrapy
import random
import copy
import math
import time
from urllib.parse import urlencode
from scrapy.utils.project import get_project_settings


class KucoinSpider(scrapy.Spider):
    name = "kucoin"

    category_dict = {
        "latest-announcements": "Latest Announcements",
        "activities": "Latest Events",
        "new-listings": "New Listings",
        "product-updates": "Product Updates",
        "vip": "Institutions and VIPs",
        "maintenance-updates": "System Maintenance",
        "delistings": "Delisting",
        "others": "Others",
    }

    settings = get_project_settings()

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "priority": "u=1, i",
        "referer": "",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": random.choice(settings["USER_AGENT"]),
        "x-site": "global",
    }

    params = {
        "category": "",
        "lang": "en_US",
        "page": "1",
        "pageSize": "10",
    }

    def start_requests(self):
        for cat, cat_name in self.category_dict.items():
            params_ = copy.deepcopy(self.params)
            params_["category"] = cat
            headers = copy.deepcopy(self.headers)
            headers["referer"] = "https://www.kucoin.com/announcement/%s" % cat

            yield scrapy.Request(
                url="https://www.kucoin.com/_api/cms/articles?" + urlencode(params_),
                method="GET",
                headers=headers,
                callback=self.parse,
                cb_kwargs={
                    "params": {
                        "cat_name": cat_name,
                        "cat_slug": cat,
                        "page": 1,
                    }
                },
            )

    def parse(self, response, params=None):
        res_json = response.json()
        if "total_page" not in params:
            total_page = math.ceil(
                int(res_json["totalNum"]) / int(self.params["pageSize"])
            )
        else:
            total_page = params["total_page"]

        cur_page = params["page"]
        headers = copy.deepcopy(self.headers)

        for item in response.json()["items"]:
            yield {
                "news_id": item["id"],
                "title": item["title"],
                "desc": item["summary"],
                "url": "https://www.kucoin.com/announcement%s" % item["path"],
                "category_str": params["cat_name"],
                "exchange": self.name,
                "announced_at_timestamp": item["publish_ts"],
                "timestamp": int(time.time()),
            }

        if (cur_page < int(self.settings.get("MAX_PAGE"))) and (cur_page < total_page):
            cur_page += 1
            headers = copy.deepcopy(self.headers)
            headers["referer"] = "https://www.kucoin.com/announcement/%s/page/%i" % (
                params["cat_slug"],
                cur_page,
            )
            params_ = copy.deepcopy(self.params)
            params_["category"] = params["cat_slug"]
            params_["page"] = str(cur_page)
            yield scrapy.Request(
                url="https://www.kucoin.com/_api/cms/articles?" + urlencode(params_),
                method="GET",
                headers=headers,
                callback=self.parse,
                cb_kwargs={
                    "params": {
                        "cat_name": params["cat_name"],
                        "cat_slug": params["cat_slug"],
                        "page": cur_page,
                        "total_page": total_page,
                    }
                },
            )
