# coding=utf-8
import logging
import scrapy
import random
from typing import Any, Iterable
from scrapy.crawler import Crawler
from scrapy.http import Response
from dig_spider.engine.extract import ExtractEngine

logger = logging.getLogger(__name__)


class WebsiteSpider(scrapy.Spider):
    name = "website"
    custom_settings = {}
    extract = None

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.paging = getattr(self, 'paging', True)
        self.go_detail = getattr(self, 'go_detail', True)
        self.config = self.extract.config if self.extract else None
        self.start_urls = self.__get_start_urls()
        if self.config:
            self.allowed_domains = self.config.get_allowed_domains()

    def __get_start_urls(self):
        urls = getattr(self, 'start_urls', [])
        if type(urls) == str:
            with open(urls, "r") as f:
                urls = f.read().splitlines()
        if len(urls) == 0 and self.config:
            urls = self.config.get_start_urls()
        return urls

    def parse(self, response: Response, **kwargs: Any) -> Any:
        if self.extract:
            items, next_page_url = self.extract.extract_page(response)
            if next_page_url and self.paging:
                self.logger.info("next_page_url: %s", next_page_url)
                proxy = self.get_proxy()
                meta = {'proxy': proxy} if proxy else {}
                yield response.follow(next_page_url, meta=meta, callback=self.parse)

            for item in items:
                if 'url' in item and self.go_detail:
                    item['url'] = response.urljoin(item['url'])
                    self.logger.info("item page url: %s", item['url'])
                    proxy = self.get_proxy()
                    meta = {'proxy': proxy} if proxy else {}
                    yield scrapy.Request(item['url'], meta=meta, callback=self.parse)
                yield item

    def start_requests(self) -> Iterable[scrapy.Request]:
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            proxy = self.get_proxy()
            meta = {'proxy': proxy} if proxy else {}
            yield scrapy.Request(url, meta=meta, dont_filter=True)

    def get_proxy(self):
        if 'PROXIES' in self.settings:
            proxy = random.choice(self.settings['PROXIES'])
            self.logger.info("Set Proxy: %s" % proxy)
            return proxy
        return None

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any):
        config_file = kwargs.get('config', '')
        if config_file:
            cls.extract = ExtractEngine(config_file)
            settings = cls.extract.config.get_settings()
            cls.custom_settings.update(settings)
        else:
            logger.error("No config, please set -a config=xxx")

        cls.custom_settings.update(kwargs)
        spider = super().from_crawler(crawler, *args, **kwargs)
        if not spider.settings.frozen:
            cls.update_settings(spider.settings)
            logger.info("config custom settings: %s", cls.custom_settings)
        return spider
