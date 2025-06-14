import scrapy
import random
import time
import copy
from urllib.parse import urlencode
from datetime import datetime
from scrapy.utils.project import get_project_settings


class MexcSpider(scrapy.Spider):
    name = "mexc"

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

    params = {
        "page": "1",
        "perPage": "10",
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.mexc.com/help/announce/api/en-US/section/360000254192/sections",
            callback=self.get_section,
            method="GET",
            headers=self.headers,
        )

    def get_section(self, response):
        for r in response.json()["data"]:
            yield scrapy.Request(
                (
                    "https://www.mexc.com/help/announce/api/en-US/section/%s/articles?"
                    % r["id"]
                )
                + urlencode(self.params),
                headers=self.headers,
                callback=self.parse,
                meta={"section_id": r["id"], "page": self.params["page"]},
            )

    def parse(self, response):
        res = response.json()
        for r in res["data"]["results"]:
            yield {
                "news_id": r["id"],
                "title": r["title"],
                "desc": "",
                "url": "https://www.mexc.com/support/articles/" + str(r["id"]),
                "category_str": ", ".join([i["name"] for i in r["parentSections"]]),
                "exchange": self.name,
                "announced_at_timestamp": int(
                    datetime.timestamp(
                        datetime.strptime(r["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
                    )
                ),
                "timestamp": int(time.time()),
            }
        cur_page = int(response.meta["page"])
        if (cur_page < int(self.settings.get("MAX_PAGE"))) and (
            cur_page < int(res["data"]["pageCount"])
        ):
            cur_page += 1
            params = copy.deepcopy(self.params)
            params["page"] = str(cur_page)
            yield scrapy.Request(
                "https://www.mexc.com/help/announce/api/en-US/section/%s/articles?"
                % response.meta["section_id"]
                + urlencode(params),
                callback=self.parse,
                headers=self.headers,
                meta={
                    "section_id": response.meta["section_id"],
                    "page": params["page"],
                },
            )
