import scrapy
import random
import time
from datetime import datetime
from scrapy.utils.project import get_project_settings


class DeepcoinSpider(scrapy.Spider):
    name = "deepcoin"

    settings = get_project_settings()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': random.choice(settings["USER_AGENT"]),
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://support.deepcoin.online/hc/en-001/categories/360003875752-Important-Announcements",
            headers=self.headers,
            callback=self.get_sections,
        )

    def get_sections(self, response):
        if response.status in [403, 429]:
            print('yo', response.text)
        # print(response.text)
        for section in response.xpath("//h2[@class='section-tree-title']"):
            section_url = response.urljoin(section.xpath("./a/@href").extract()[0])
            yield scrapy.Request(
                url=section_url,
                headers=self.headers,
                callback=self.parse_sections,
                cb_kwargs={
                    "params": {
                        "section_name": section.xpath("./a/text()").extract()[0],
                        "section_url": section_url,
                        "page": 1,
                    }
                },
            )

    def parse_sections(self, response, params=None):
        if response.status in [403, 429]:
            print('yoyo', response.text)
            
        for article in response.xpath("//ul[@class='article-list']/li"):
            yield scrapy.Request(
                url=response.urljoin(article.xpath("./a/@href").extract()[0]),
                headers=self.headers,
                callback=self.parse_articles,
                cb_kwargs={"params": params},
            )

            
        if (params["page"] < int(self.settings.get("MAX_PAGE"))) and (
            len(response.xpath("//li[@class='pagination-next']").extract()) > 0
        ):
            params["page"] += 1
            yield scrapy.Request(
                url=params["section_url"] + "?page=%i#articles" % params["page"],
                callback=self.parse_sections,
                headers=self.headers,
                cb_kwargs={"params": params},
            )

    def parse_articles(self, response, params=None):
        yield {
            "news_id": response.url.split("/")[-1].split("-")[0],
            "title": response.xpath("//title/text()").extract()[0],
            "desc": ' '.join(response.xpath(
                "//div[@class='article-body']//text()"
            ).extract()),
            "url": response.url,
            "category_str": params["section_name"],
            "exchange": self.name,
            "announced_at_timestamp": int(
                datetime.strptime(
                    response.xpath("//time/@datetime").extract()[0],
                    "%Y-%m-%dT%H:%M:%SZ",
                ).timestamp()
            ),
            "timestamp": int(time.time()),
        }
