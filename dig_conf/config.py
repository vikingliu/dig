# coding=utf-8
import logging
import re
import yaml

logger = logging.getLogger(__name__)


class DigConfig(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.get_yaml_data()
        self.valid_config()
        self._parse_config()

    def get_yaml_data(self):
        with open(self.config_file, encoding='utf-8') as file:
            content = file.read()
            data = yaml.load(content, Loader=yaml.FullLoader)
            return data

    def valid_config(self):
        if self.config is None:
            raise Exception("config is empty")

        if 'start_urls' not in self.config:
            raise Exception("start_urls is not in config")

        if 'extract' not in self.config:
            raise Exception("extract is not in config")

        for item in self.config.get('extract'):
            if "page" in item:
                for key in ["url_patterns", "item_rules"]:
                    if key not in item.get("page"):
                        raise Exception("{} is must in page config".format(key))
            else:
                raise Exception("page is must in extract config")

    def get_start_urls(self):
        return self.config.get('start_urls')

    def get_allowed_domains(self):
        return self.config.get('allowed_domains', [])

    def get_proxies(self):
        return self.config.get('proxies', [])

    def _parse_config(self):
        self.pages = []
        for page_config in self.config.get('extract'):
            self.pages.append(Page(page_config.get('page')))

    def get_page_config(self, url):
        for page in self.pages:
            for url_pattern in page.url_patterns:
                if re.match(url_pattern, url):
                    return page
        return None

    def get_headers(self):
        return self.config.get("headers", None)


class Page(object):
    def __init__(self, config):
        self.config = config
        self._parse_config()

    def _parse_config(self):
        self.url_patterns = [re.compile(url_pattern) for url_pattern in self.config.get('url_patterns')]
        self.next_page_rule = Rule('next_page_rule',
                                   self.config.get('next_page_rule')) if 'next_page_rule' in self.config else None
        self.list_rule = Rule('list_rule', self.config.get('list_rule')) if 'list_rule' in self.config else None
        self.item_rules = {key: Rule(key, value) for key, value in self.config.get('item_rules', {}).items()}


class Rule(object):
    def __init__(self, name, rule):
        self.name = name
        if rule:
            self.__parse_path(rule)
        else:
            raise Exception("path is empty")

    def __parse_path(self, rule):
        if rule.startswith('css{'):
            self.path_type = 'css'
            self.path, self.funcs = self.get_path_funcs(rule, 'css')

        elif rule.startswith('xpath{'):
            self.path_type = 'xpath'
            self.path, self.funcs = self.get_path_funcs(rule, 'xpath')

        else:
            raise Exception("{} path not support".format(rule.split('.')[0]))

    def get_path_funcs(self, rule, path_type='css'):
        rule = rule.replace(path_type + '{', '')
        path, funcs = rule.split('}')
        return path, funcs

    def process_funcs(self, value):

        try:
            digstr = DigString(value)
            digstr = eval('digstr' + self.funcs)
            return digstr.value
        except Exception as e:
            logging.error("%s is not work for: %s", self.funcs, value)
            return value

    def _get_func_rule(self, prefix):
        return self.func.replace(prefix, '')[:-1]


class DigString(object):
    def __init__(self, value):
        self.value = value

    def re(self, rule, index=0):
        groups = re.findall(rule, self.value)
        if groups:
            return DigString(groups[index])
        return self

    def replace(self, old, new, count=-1):
        return DigString(self.value.replace(old, new, count))

    def split(self, sep=None, maxsplit=-1):
        return [DigString(v) for v in self.value.split(sep, maxsplit)]
