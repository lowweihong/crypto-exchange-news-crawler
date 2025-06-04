import scrapy
import random
from scrapy.utils.project import get_project_settings
import re
import time
from datetime import datetime


class XtSpider(scrapy.Spider):
    name = "xt"

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

    url = "https://xtsupport.zendesk.com/hc/en-us/categories/10304894611993-Important-Announcements"

    def start_requests(self):
        meta_dict = {
            "playwright": True,
            "playwright_include_page": True,
            "playwright_context_kwargs": {
                "java_script_enabled": True,
                "ignore_https_errors": True,
                "user_agent": random.choice(self.settings["USER_AGENT"]),
            },
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

        yield scrapy.Request(url=self.url, meta=meta_dict, callback=self.get_section)

    async def get_section(self, response):
        for r in response.xpath("//h2[@class='section-tree-title']/a"):
            response.meta["category_str"] = r.xpath("text()").get().strip()
            for page in range(int(self.settings["MAX_PAGE"])):
                url = response.urljoin(r.xpath("@href").extract()[0])
                if page > 0:
                    url += "?page=%i#articles" % (page + 1)

                yield scrapy.Request(
                    url=url, meta=response.meta, callback=self.parse_section
                )

    async def parse_section(self, response):
        for r in response.xpath("//li[@class='article-list-item ']/a"):
            url = response.urljoin(r.xpath("@href").extract()[0])
            yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_news)

    async def clean_desc(self, desc_parts):
        raw_text = " ".join(desc_parts)
        cleaned_text = re.sub(
            r"\s+", " ", raw_text
        )  # Replace multiple whitespace with single space
        cleaned_text = re.sub(r"&nbsp;", " ", cleaned_text)  # Replace &nbsp; with space
        cleaned_text = cleaned_text.strip()
        return cleaned_text

    async def parse_news(self, response):
        desc_parts = response.xpath("//div[@class='article-body']//text()").getall()

        yield {
            "news_id": re.search(r"/articles/(\d+)-", response.url).group(1),
            "title": response.xpath("//title/text()").extract()[0],
            "desc": await self.clean_desc(desc_parts),
            "url": response.url,
            "category_str": response.meta["category_str"],
            "exchange": self.name,
            "announced_at_timestamp": int(
                datetime.fromisoformat(
                    response.xpath("//time/@datetime").extract()[0][:-1]
                ).timestamp()
            ),
            "timestamp": int(time.time()),
        }

    async def close_context_on_error(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
