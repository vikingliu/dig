# coding=utf-8
import logging
import scrapy
import random
from urllib.parse import urlparse
from typing import Any, Iterable
from scrapy.crawler import Crawler
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from dig_spider.engine.extract import ExtractEngine

logger = logging.getLogger(__name__)


class WebsiteSpider(scrapy.Spider):
    name = "website"
    custom_settings = {}
    extract_engine = None
    start_urls = []
    allowed_domains = []

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.paging = getattr(self, 'paging', True)
        self.go_detail = getattr(self, 'go_detail', True)
        self.extract_link = getattr(self, 'extract_link', False)
        self.url_cache = {}

    def parse(self, response: Response, **kwargs: Any) -> Any:
        if self.extract_link:
            if self.extract_engine:
                links = self.extract_engine.extract_links(response)
            else:
                link_extractor = LinkExtractor(allow_domains=self.allowed_domains)
                links = link_extractor.extract_links(response)
            for link in links:
                url = response.urljoin(link.url)
                if self.go_detail and url not in self.url_cache:
                    self.logger.info("link page url: %s", url)
                    proxy = self.get_proxy()
                    meta = {'proxy': proxy} if proxy else {}
                    self.url_cache[url] = url
                    yield response.follow(url, meta=meta, callback=self.parse)

        if self.extract_engine:
            items, next_page_url = self.extract_engine.extract_page(response)
            if next_page_url and self.paging and not self.extract_link:
                self.logger.info("next_page_url: %s", next_page_url)
                proxy = self.get_proxy()
                meta = {'proxy': proxy} if proxy else {}
                yield response.follow(next_page_url, meta=meta, callback=self.parse)

            for item in items:
                item['url'] = response.urljoin(item['url'])
                if 'url' in item and self.go_detail and not self.extract_link:
                    self.logger.info("item page url: %s", item['url'])
                    proxy = self.get_proxy()
                    meta = {'proxy': proxy} if proxy else {}
                    yield response.follow(item['url'], meta=meta, callback=self.parse)
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
    def init_spider(cls, **kwargs: Any):
        config_file = kwargs.get('config', '')
        if config_file:
            cls.extract_engine = ExtractEngine(config_file)
            settings = cls.extract_engine.config.get_settings()
            cls.custom_settings.update(settings)
        else:
            logger.error("No config, please set -a config=xxx")

        urls = kwargs.get('start_urls', [])
        if type(urls) == str:
            with open(urls, "r") as f:
                urls = f.read().splitlines()

        if cls.extract_engine and cls.extract_engine.config:
            cls.allowed_domains = cls.extract_engine.config.get_allowed_domains()
            if len(urls) == 0:
                urls = cls.extract_engine.config.get_start_urls()

        cls.start_urls = urls
        if not cls.allowed_domains:
            domains = set()
            for url in urls:
                domain = urlparse(url).netloc
                domains.add(domain)
            cls.allowed_domains = list(domains)
        cls.custom_settings.update(kwargs)

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any):
        cls.init_spider(**kwargs)
        spider = super().from_crawler(crawler, *args, **kwargs)
        if not spider.settings.frozen:
            cls.update_settings(spider.settings)
            logger.info("config custom settings: %s", cls.custom_settings)
        return spider
