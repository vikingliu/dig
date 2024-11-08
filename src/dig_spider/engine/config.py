# coding=utf-8
import logging
import re
import yaml
import os

logger = logging.getLogger(__name__)


class DigConfig(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.__get_yaml_data()
        self.code = self.__get_code()
        self.pages = self.__get_pages()
        self.login = self.__get_login()

    def __get_yaml_data(self):
        with open(self.config_file, encoding='utf-8') as file:
            content = file.read()
            data = yaml.load(content, Loader=yaml.FullLoader)
            return data

    def __get_pages(self):
        pages = []
        for page_config in self.config.get('extract', []):
            pages.append(Page(page_config.get('page'), self.code))
        return pages

    def __get_code(self):
        code = ''
        if 'code_file' in self.config:
            cwd = os.path.dirname(self.config_file)
            with open(cwd + '/' + self.config.get('code_file'), encoding='utf-8') as file:
                code = file.read()
        return code

    def __get_login(self):
        if 'login' in self.config:
            return Login(self.config.get('login'), self.code)
        return None

    def get_start_urls(self):
        return self.config.get('start_urls')

    def get_allowed_domains(self):
        return self.config.get('allowed_domains', [])

    def get_settings(self):
        return self.config.get('settings', {})

    def get_proxies(self):
        return self.config.get('proxies', {})

    def get_page_extract_config(self, url):
        for page in self.pages:
            for url_pattern in page.url_patterns:
                if re.match(url_pattern, url):
                    return page
        return None


class Page(object):
    def __init__(self, config, code):
        self.config = config
        self.code = code
        self.__parse_config()

    def __parse_config(self):
        self.page_type = self.config.get('page_type', '')
        self.code += '\n' + process_code(self.config.get('code', ''))

        self.url_patterns = [re.compile(url_pattern) for url_pattern in self.config.get('url_patterns')]
        self.next_page_rule = Rule('next_page_rule',
                                   self.config.get('next_page_rule')) if 'next_page_rule' in self.config else None
        self.list_rule = Rule('list_rule', self.config.get('list_rule')) if 'list_rule' in self.config else None
        self.item_rules = {key: Rule(key, value) for key, value in self.config.get('item_rules', {}).items()}
        self.link_params = self.config.get('link_params', {})


class Rule(object):
    def __init__(self, name, rule):
        self.name = name
        if rule:
            self.__parse_path(rule)
        else:
            raise Exception("path is empty")

    def __parse_path(self, rule):
        if '{' in rule:
            self.path_type, rule = rule.split('{', 1)
            self.path, self.funcs = rule.split('}', 1)
        else:
            self.path_type = 'text'
            self.path = rule
            self.funcs = ''

    def process_funcs(self, value):
        try:
            digstr = DigString(value)
            digstr = eval('digstr' + self.funcs)
            return digstr.value
        except Exception as e:
            logging.error("%s is not work for: %s", self.funcs, value)
            return value


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

    def strip(self, *args, **kwargs):
        return DigString(self.value.strip(*args, **kwargs))

    def to_markdown(self):
        import html2text
        '''
         clear html tag
        :return:
        '''
        return DigString(html2text.HTML2Text().handle(self.value))


class Login(object):
    def __init__(self, config, code):
        self.config = config
        self.code = code
        self.__parse_config()

    def __parse_config(self):
        self.url = self.config.get('url', '')
        self.load_page = self.config.get('load_page', True)
        self.params = self.config.get('params', {})
        self.code += '\n' + process_code(self.config.get('code', ''))
        self.form_data = {key: Rule(key, value) for key, value in self.config.get('form_data', {}).items()}


def process_code(code):
    if code:
        code = code.replace('\\n', '\n').replace('\\t', '\t')
        lines = code.split('\n')
        code = ''
        for line in lines:
            line = line.strip(' ') + '\n'
            code += line
    return code
