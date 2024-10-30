# coding=utf-8
import logging

from scrapy.http import HtmlResponse

from dig_spider.engine.config import DigConfig

logger = logging.getLogger(__name__)


class ExtractEngine(object):
    def __init__(self, config_file):
        self.config = DigConfig(config_file)

    def extract_page(self, response):
        page_config = self.config.get_page_config(response.url)
        if page_config is None:
            logger.error("not find page extract config for url: %s", response.url)
            return [], ''
        list_items = self.extract_by_path(page_config.list_rule, response) if page_config.list_rule else []
        next_page_url = self.extract_by_path(page_config.next_page_rule, response) if page_config.next_page_rule else ''
        next_page_url = response.urljoin(next_page_url.get()) if next_page_url else ''

        result = []
        if list_items:
            for item in list_items:
                result.append(self.extract_item(page_config.item_rules, item))
        else:
            result.append(self.extract_item(page_config.item_rules, response))
        return result, next_page_url

    def extract_by_path(self, rule, response):
        if rule.path_type == 'css' and rule.path:
            return response.css(rule.path)
        elif rule.path_type == 'xpath' and rule.path:
            return response.xpath(rule.path)
        logger.error("name: %s, path: %s not work for url: %s", rule.name, rule.path, response.url)
        return None

    def extract_item(self, rules, response):
        item = {}
        for key, rule in rules.items():
            node = self.extract_by_path(rule, response)
            node = response if node is None else node
            value = node.get() if not isinstance(node, HtmlResponse) else ''
            if not value:
                logger.error("%s: %s not work for %s", key, rule.path, response.url)
            item[key] = rule.process_funcs(value) if rule.funcs else value
        return item
