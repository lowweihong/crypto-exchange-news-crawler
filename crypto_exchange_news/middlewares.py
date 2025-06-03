# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging, random
from scrapy.exceptions import NotConfigured


class MyProxyMiddleware(RetryMiddleware):
    def __init__(self, crawler, proxy_list):
        super(MyProxyMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler
        self.proxies = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        proxy_list = s.getlist('PROXY_LIST')
        if not proxy_list:
            raise NotConfigured()
        mw = cls(
            crawler=crawler,
            proxy_list=proxy_list
        )
        return mw

    def process_request(self, request, spider):
        if len(self.proxies):
            proxy = random.choice(self.proxies)
            print('using proxy: {}'.format(proxy))
            request.meta['proxy'] = proxy
            request.meta['download_slot'] = proxy