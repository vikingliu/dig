# coding=utf-8
import logging
import jsonpath

from scrapy.http.response.html import HtmlResponse
from scrapy.selector import SelectorList
from dig_spider.engine.config import DigConfig
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)


class ExtractEngine(object):
    def __init__(self, config_file):
        self.config = DigConfig(config_file)

    def extract_by_text(self, text, url, encoding='utf-8'):
        response = HtmlResponse(encoding=encoding, url=url, body=text)
        return self.extract_page(response)

    def extract_links(self, response):
        page_config = self.config.get_page_extract_config(response.url)
        link_params = page_config.link_params if page_config else {}
        if 'allowed_domains' not in link_params:
            link_params['allow_domains'] = self.config.get_allowed_domains()
        link_extractor = LinkExtractor(**page_config.link_params)
        return link_extractor.extract_links(response)

    def extract_page(self, response):
        page_config = self.config.get_page_extract_config(response.url)
        if page_config is None:
            logger.error("not find page extract config for url: %s", response.url)
            return [], ''
        list_items = self.extract_by_path(page_config.list_rule, response) if page_config.list_rule else []

        results = []
        list_items = list_items if list_items else [response]
        for item in list_items:
            result = self.extract_item(page_config.item_rules, item, page_config.page_type)
            results.append(result)

        next_page_url = self.extract_by_path(page_config.next_page_rule, response) if page_config.next_page_rule else ''
        if isinstance(next_page_url, SelectorList):
            next_page_url = next_page_url.get()
        next_page_url = response.urljoin(next_page_url) if next_page_url else ''
        if page_config.code:
            exec(page_config.code)

        for result in results:
            for key in ['url', 'urls', 'img', 'imgs']:
                if key in result:
                    result[key] = [response.urljoin(url) for url in result[key]] \
                        if type(result[key]) is list else response.urljoin(result[key])
        return results, next_page_url

    def extract_by_path(self, rule, response):
        if rule.path_type == 'css' and rule.path:
            return response.css(rule.path)
        elif rule.path_type == 'xpath' and rule.path:
            return response.xpath(rule.path)
        elif rule.path_type == 're' and rule.path:
            return eval(rule.path)
        elif rule.path_type == 'json' and rule.path:
            if type(response) != dict:
                response = response.json()
            return jsonpath.jsonpath(response, rule.path)[0]
        elif rule.path_type == 'code' and rule.path:
            return eval(rule.path)
        elif rule.path_type == 'text' and rule.path:
            return rule.path
        logger.error("name: %s, path: %s not work for url: %s", rule.name, rule.path, response.url)
        return None

    def extract_item(self, rules, response, page_type=None):
        item = {'page_type': page_type} if page_type else {}
        for key, rule in rules.items():
            node = self.extract_by_path(rule, response)
            values = node.getall() if isinstance(node, SelectorList) else [node]
            if not values:
                logger.info("%s: %s  extract empty", key, rule.path)
            item[key] = []
            for value in values:
                value = rule.process_funcs(value) if rule.funcs else value
                item[key].append(value)
            if len(item[key]) == 1:
                item[key] = item[key][0]
        return item
