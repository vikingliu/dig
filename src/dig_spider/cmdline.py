import logging
from scrapy.cmdline import execute
import os
import shutil

from scrapy.commands import ScrapyCommand

logging = logging.getLogger(__name__)


class GenTemplate(ScrapyCommand):

    def short_desc(self):
        return "Generate dig-spider config and run shell templates"

    def run(self, args, opts):
        if not args:
            print("=== Usage")
            print("  dig-spider gentemplate <dst>")
            print("---------")
            print("dst: save the templates to dir")
            return
        dst = args[0] if args else 'dig_spider_template'
        self.copy_template(dst)

    def copy_template(self, dst):
        src = os.path.dirname(__file__) + '/template'
        shutil.copytree(src, dst, dirs_exist_ok=True)
        logging.info("Generating dig-spider template to %s successfully!", dst)


def exec():
    """
     execute dig-spider as a scrapy shell command
    :return:
    """
    os.environ.setdefault("XDG_CONFIG_HOME", os.path.dirname(__file__))
    execute()


if __name__ == "__main__":
    exec()
