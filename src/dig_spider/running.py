from typing import Any

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dig_spider.engine.extract import ExtractEngine
import os


def crawl_pages(spider='website', *args: Any, **kwargs: Any):
    cwd = os.path.dirname(__file__)
    os.environ.setdefault("XDG_CONFIG_HOME", cwd)
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(spider, *args, **kwargs)
    process.start()
    process.stop()


def extract_page(config, html, encoding='utf-8', url=None):
    return ExtractEngine(config).extract_by_text(html, url, encoding)
