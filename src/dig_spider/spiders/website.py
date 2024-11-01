import logging
from typing import Any

import scrapy

from scrapy.crawler import Crawler
from scrapy.http import Response
from dig_spider.engine.extract import ExtractEngine


class WebsiteSpider(scrapy.Spider):
    name = "website"
    custom_settings = {}

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        config_file = getattr(self, 'config', "")
        if not config_file:
            raise Exception("No config, please set -a config=xxx")
        self.extract = ExtractEngine(config_file)
        self.config = self.extract.config
        url = getattr(self, 'url', "")
        if url:
            self.start_urls = [url]
        else:
            self.start_urls = self.config.get_start_urls()
        self.allowed_domains = self.config.get_allowed_domains()

    def parse(self, response: Response, **kwargs: Any) -> Any:
        items, next_page_url = self.extract.extract_page(response)
        if next_page_url:
            self.logger.info("next_page: %s", next_page_url)
            yield response.follow(next_page_url, callback=self.parse)

        for item in items:
            if 'url' in item:
                item['url'] = response.urljoin(item['url'])
                self.logger.info("item page: %s", item['url'])
                yield scrapy.Request(item['url'], callback=self.parse)
            yield item

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any):
        spider = super().from_crawler(crawler,  *args, **kwargs)
        if kwargs:
            cls.custom_settings.update(kwargs)
            cls.update_settings(spider.settings)
            logging.info("config custom settings: %s", cls.custom_settings)
        return spider
