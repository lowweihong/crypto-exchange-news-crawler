import scrapy
import random
import time
from datetime import datetime
from urllib.parse import urlencode
from scrapy.utils.project import get_project_settings


class UpbitSpider(scrapy.Spider):
    name = "upbit"

    def __init__(self, **kw):
        super(UpbitSpider, self).__init__(**kw)

        self.settings = get_project_settings()
        self.country = getattr(self, "country", "sg").lower()

        if self.country not in ["sg", "id", "th", "kr"]:
            raise ValueError(
                "Country must be either 'sg' (Singapore) or 'id' (Indonesia) or 'th' (Thailand) or 'kr' (Korea)"
            )

        if self.country == "kr":
            self.url = "https://api-manager.upbit.com/api/v1/announcements?"
        else:
            self.url = (
                "https://%s-api-manager.upbit.com/api/v1/announcements?" % self.country
            )

        self.headers = {
            "accept": "application/json",
            "accept-language": "ko-KR, ko;q=1, en-GB;q=0.1",
            "origin": "https://upbit.com",
            "priority": "u=1, i",
            "referer": "https://upbit.com/",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": random.choice(self.settings["USER_AGENT"]),
        }

        if self.country == "id":
            self.headers["accept-language"] = "id-ID, id;q=1, en-GB;q=0.1"
        elif self.country == "th":
            self.headers["accept-language"] = "th-TH, th;q=1, en-GB;q=0.1"
        elif self.country == "sg":
            self.headers["accept-language"] = "en-SG, en;q=1, en-GB;q=0.1"

        if self.country != "kr":
            self.headers["origin"] = "https://%s.upbit.com" % self.country
            self.headers["referer"] = "https://%s.upbit.com/" % self.country

    def start_requests(self):
        params = {
            "os": "web",
            "page": "1",
            "per_page": "20",
            "category": "all",
        }
        yield scrapy.Request(
            url=self.url + urlencode(params),
            callback=self.parse,
            headers=self.headers,
            cb_kwargs={"params": params},
        )

    def parse(self, response, params=None):
        res = response.json()["data"]

        url = f"https://upbit.com/service_center/notice?id="
        if self.country != "kr":
            url = f"https://%s.upbit.com/service_center/notice?id=" % (self.country)

        for r in res["notices"]:
            yield {
                "news_id": r["id"],
                "title": r["title"],
                "desc": "",
                "url": url + str(r["id"]),
                "category_str": r["category"],
                "exchange": self.name,
                "announced_at_timestamp": int(
                    datetime.strptime(r["listed_at"], "%Y-%m-%dT%H:%M:%S%z").timestamp()
                ),
                "timestamp": int(time.time()),
            }

        cur_page = int(params["page"])
        if cur_page < min(int(self.settings.get("MAX_PAGE")), int(res["total_pages"])):
            cur_page += 1
            params["page"] = str(cur_page)
            yield scrapy.Request(
                url=self.url + urlencode(params),
                callback=self.parse,
                headers=self.headers,
                cb_kwargs={"params": params},
            )
