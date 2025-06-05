import scrapy
import random
import json
import time
import copy
from scrapy.utils.project import get_project_settings
from urllib.parse import urlencode


class BitfinexSpider(scrapy.Spider):
    name = "bitfinex"

    settings = get_project_settings()

    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "origin": "https://www.bitfinex.com",
        "priority": "u=1, i",
        "referer": "https://www.bitfinex.com/",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": random.choice(settings["USER_AGENT"]),
    }

    params = {"limit": 20, "type": 1}

    url = "https://api-pub.bitfinex.com/v2/posts/hist/?"

    def start_requests(self):

        yield scrapy.Request(
            url=self.url + urlencode(self.params),
            headers=self.headers,
            callback=self.parse,
            meta={"page": 1},
            cb_kwargs={"params": self.params},
        )

    def parse(self, response, params=None):
        data = json.loads(response.text)
        page = response.meta.get("page", 1)

        # Process current page data here - yield items
        for item in data:
            yield {
                "news_id": item[0],
                "title": item[3],
                "desc": item[4],
                "url": "https://www.bitfinex.com/posts/" + str(item[0]),
                "category_str": "",
                "exchange": self.name,
                "announced_at_timestamp": item[1] //1000,
                "timestamp": int(time.time()),
            }

        # Get last element's ID and make next request if within max pages
        if data and page < int(self.settings["MAX_PAGE"]):
            last_id = data[-1][0]  # Get ID from last element

            # Update params with the ID for next page
            next_params = copy.deepcopy(params)
            next_params["id"] = last_id

            yield scrapy.Request(
                url=self.url + urlencode(next_params),
                headers=self.headers,
                callback=self.parse,
                meta={"page": page + 1},
                cb_kwargs={"params": next_params},
            )
