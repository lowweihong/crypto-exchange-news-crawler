import scrapy
import json
import random
import time
import re
import asyncio
from datetime import datetime
from scrapy.utils.project import get_project_settings


class BingxSpider(scrapy.Spider):
    name = "bingx"
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

    url = "https://bingx.com/en/support/notice-center/"

    def __init__(self):
        super().__init__()
        self.sections = []
        self.sections_loaded_event = None

    def create_playwright_meta(self, section_info={}):
        """Helper function to create fresh meta dict for each request"""
        meta = {
            "playwright": True,
            "playwright_include_page": True,
            "playwright_page_init_callback": self.init_page,
            "playwright_context_kwargs": {
                "java_script_enabled": True,
                "ignore_https_errors": True,
                "user_agent": random.choice(self.settings["USER_AGENT"]),
            },
            "errback": self.close_context_on_error,
        }

        if section_info:
            meta["section_info"] = section_info

        # Add proxy if needed
        if self.settings["PROXY_LIST"] != []:
            proxy = random.choice(self.settings["PROXY_LIST"])
            user_pass = re.sub(r"^https?://", "", proxy.split("@")[0])
            meta["playwright_context_kwargs"]["proxy"] = {
                "server": proxy,
                "username": user_pass.split(":")[0],
                "password": user_pass.split(":")[1],
            }

        return meta

    async def init_page(self, page, request):
        """Initialize page before navigation - set up route interception"""
        self.sections_loaded_event = asyncio.Event()
        await page.route("**/*", self.intercept_sections_request)

    def start_requests(self):
        yield scrapy.Request(
            self.url,
            meta=self.create_playwright_meta(),
            callback=self.get_section,
        )

    async def intercept_sections_request(self, route):
        request = route.request
        self.logger.info(f"Intercepting request: {request.url}")

        # Intercept AJAX requests for sections
        if "listSections" in request.url:
            self.logger.info("Found listSections request - fetching...")
            response = await route.fetch()
            body = await response.text()
            try:
                ajax_data = json.loads(body)
                self.sections = ajax_data
                self.logger.info("Successfully captured sections data")

                # Signal that sections are loaded
                if self.sections_loaded_event:
                    self.sections_loaded_event.set()

            except json.JSONDecodeError as e:
                self.logger.warning(f"Failed to parse JSON: {e}")

        await route.continue_()

    async def get_section(self, response):
        page = response.meta["playwright_page"]

        # Route interception was already set up in init_page
        # Page has already loaded and made requests
        # Wait for the sections to be intercepted (with timeout)

        try:
            await asyncio.wait_for(self.sections_loaded_event.wait(), timeout=30.0)
            self.logger.info("Sections intercepted successfully!")
        except asyncio.TimeoutError:
            self.logger.error("Timeout waiting for sections to be intercepted")
            await page.close()
            return

        for section in self.sections["data"]["result"]:
            section_info = {
                "id": section.get("sectionId", ""),
                "name": section.get("sectionName", ""),
            }

            yield scrapy.Request(
                f"{self.url}{section_info.get('id')}/",
                meta=self.create_playwright_meta(section_info),
                callback=self.parse_section,
            )

        await page.close()

    async def parse_section(self, response):
        page = response.meta["playwright_page"]
        section_info = response.meta["section_info"]

        # Create event for articles
        articles_loaded_event = asyncio.Event()
        captured_articles = []

        async def intercept_articles(route):
            request = route.request
            if "listArticles" in request.url:
                self.logger.info(
                    f"Found listArticles request for section {section_info['name']}"
                )
                response_data = await route.fetch()
                body = await response_data.text()
                try:
                    ajax_data = json.loads(body)["data"]["result"]
                    if ajax_data != []:
                        captured_articles.extend(ajax_data)
                    articles_loaded_event.set()
                    self.logger.info(f"Captured {len(ajax_data)} articles")
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse articles JSON")
            await route.continue_()

        await page.route("**/*", intercept_articles)

        # Navigate to section to trigger articles request
        section_url = f"{self.url}{section_info.get('id')}/"
        await page.goto(section_url)

        # Wait for articles to be loaded
        try:
            await asyncio.wait_for(articles_loaded_event.wait(), timeout=30.0)
            self.logger.info(f"Articles loaded for section {section_info.get('name')}")

            # Process and yield articles
            for article in captured_articles:
                yield {
                    "news_id": article["articleId"],
                    "title": article["title"],
                    "desc": "",
                    "url": f"https://bingx.com/en/support/articles/{article['articleId']}",
                    "category_str": section_info["name"],
                    "exchange": self.name,
                    "announced_at_timestamp": int(
                        datetime.fromisoformat(
                            article["createTime"].replace("Z", "+00:00")
                        ).timestamp()
                    ),
                    "timestamp": int(time.time()),
                }

        except asyncio.TimeoutError:
            self.logger.error(
                f"Timeout waiting for articles in section {section_info['name']}"
            )

        await page.close()

    async def close_context_on_error(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
