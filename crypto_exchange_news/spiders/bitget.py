import scrapy
import json
import random
import time
import re
from scrapy.utils.project import get_project_settings


class BitgetSpider(scrapy.Spider):
    name = "bitget"
    settings = get_project_settings()
    custom_settings = {
        "CONCURRENT_REQUESTS": 2,
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": "",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 3,
        "PLAYWRIGHT_MAX_CONTEXTS": 1,
    }

    url = "https://www.bitget.com/en/support/sections/"

    def start_requests(self):
        dict_url = {
            "360007868532": "Latest News.Bitget News",
            "5955813039257": "New Listings.Spot",
            "12508313405000": "New Listings.Futures",
            "12508313443168": "New Listings.Margin",
            "12508313405075": "New Listings.Copy Trading",
            "12508313443194": "New Listings.Bots",
            "4413154768537": "Competitions and promotions.Ongoing competitions and promotions",
            "4413127530649": "Competitions and promotions.Previous competitions & events",
            "4411481755417": "Competitions and promotions.Reward Distribution",
            "6483596785177": "Competitions and promotions.KCGI",
            "12508313446623": "Maintenance or system updates.Asset maintenance",
            "12508313404850": "Maintenance or system updates.Spot Maintenance",
            "12508313405050": "Maintenance or system updates.System Updates",
            "12508313404950": "Maintenance or system updates.Futures Maintenance",
        }

        for id, cat in dict_url.items():
            for page in range(int(self.settings["MAX_PAGE"])):
                url = self.url + id

                if page > 0:
                    url += "/%i" % (page + 1)

                meta_dict = {
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_context_kwargs": {
                        "java_script_enabled": True,
                        "ignore_https_errors": True,
                        "user_agent": random.choice(self.settings["USER_AGENT"]),
                    },
                    "cat": cat,
                    "cat_name": dict_url[id],
                    "id": id,
                    "errback": self.close_context_on_error,
                }

                if self.settings["PROXY_LIST"] != []:
                    proxy = random.choice(self.settings["PROXY_LIST"])
                    user_pass = re.sub(r"^https?://", "", proxy.split("@")[0])
                    meta_dict["playwright_context_kwargs"]["proxy"] = {
                        "server": proxy,
                        "username": user_pass.split(":")[0],
                        "password": user_pass.split(":")[1],
                    }

                yield scrapy.Request(url, meta=meta_dict, callback=self.parse_page)

    async def close_context_on_error(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        cat = response.meta["cat"]
        inner_html = await page.locator('//script[@id="__NEXT_DATA__"]').inner_html()
        try:
            res = json.loads(inner_html)
            try:
                containers = res["props"]["pageProps"]["sectionArticle"]["items"]
            except KeyError:
                containers = res["props"]["pageProps"]["list"]

            for content in containers:
                data = {
                    "news_id": content["contentId"],
                    "title": content["title"],
                    "desc": "",
                    "url": "https://www.bitget.com/support/articles/" + content["contentId"],
                    "category_str": cat,
                    "exchange": self.name,
                    "announced_at_timestamp": int(content["showTime"]) // 1000,
                    "timestamp": int(time.time()),
                }

                yield data

        except:
            await page.close()
        await page.close()
