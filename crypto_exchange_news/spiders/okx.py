import scrapy
import random
import json
import time
import math
from datetime import datetime
from scrapy.utils.project import get_project_settings


class OkxSpider(scrapy.Spider):
    name = "okx"

    settings = get_project_settings()

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "priority": "u=0, i",
        "referer": "https://www.okx.com/en-sg/help/section/announcements-trading-updates/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "service-worker-navigation-preload": "true",
        "upgrade-insecure-requests": "1",
        "user-agent": random.choice(settings["USER_AGENT"]),
    }
    
    url_section = 'https://www.okx.com/help/section/'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.okx.com/help/category/announcements",
            headers=self.headers,
            callback=self.get_section,
        )

    def get_section(self, response):
        res_json = json.loads(
            response.xpath(
                "//script[@data-id='__app_data_for_ssr__']/text()"
            ).extract()[0]
        )

        for section in res_json["appContext"]["initialProps"]["sectionData"][
            "allSections"
        ]:
            cat_str = section["title"]
            
            yield scrapy.Request(
                self.url_section
                + section["slug"],
                method="GET",
                headers=self.headers,
                callback=self.parse_page,
                cb_kwargs={
                    "params": {
                        "cat_str": cat_str,
                        "page": 1,
                        "section_slug": section["slug"],
                    }
                },
            )

    def parse_page(self, response, params=None):
        res_json = json.loads(
            response.xpath(
                "//script[@data-id='__app_data_for_ssr__']/text()"
            ).extract()[0]
        )

        arc_ls = res_json["appContext"]["initialProps"]["sectionData"]["articleList"]

        for item in arc_ls["items"]:
            data = {
                "news_id": item["id"],
                "title": item["title"],
                "desc": "",
                "url": "https://www.okx.com/help/" + item["slug"],
                "category_str": params["cat_str"],
                "exchange": self.name,
                "announced_at_timestamp": int(
                    datetime.timestamp(
                        datetime.strptime(item["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    )
                ),
                "timestamp": int(time.time()),
            }

            yield data

        max_page = math.ceil(arc_ls["total"] / arc_ls["limit"])

        if (max_page > params["page"]) and (
            params["page"] < self.settings.get("MAX_PAGE")
        ):
            page = params["page"] + 1
            yield scrapy.Request(
                self.url_section
                + params["section_slug"]
                + "/page/%i" % (page),
                method="GET",
                headers=self.headers,
                callback=self.parse_page,
                cb_kwargs={
                    "params": {
                        "cat_str": params["cat_str"],
                        "page": page,
                        "section_slug": params["section_slug"],
                    }
                },
            )
