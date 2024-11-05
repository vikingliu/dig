import logging
import os
import shutil

from scrapy.cmdline import execute
from scrapy.commands import ScrapyCommand

logging = logging.getLogger(__name__)


class GenTemplate(ScrapyCommand):

    def short_desc(self):
        return "Generate dig-spider config and run shell templates"

    def run(self, args, opts):
        if len(args) < 1 or len(args) > 1:
            print("=== Usage")
            print("  dig-spider gentemplate <dir>")
            print("---------")
            print("dir: save the gentemplate to dir")

            if len(args) > 1:
                print(
                    "running 'dig-spider gentemplate' with more than one dir is not supported"
                )
            return
        self.copy_template(args[0])

    def copy_template(self, dst):
        src = os.path.dirname(__file__) + '/template'
        shutil.copytree(src, dst, dirs_exist_ok=True)
        logging.info("Generating dig-spider template to %s successfully!", dst)


class GenExample(ScrapyCommand):

    def short_desc(self):
        return "Generate dig-spider examples"

    def run(self, args, opts):
        if len(args) < 1 or len(args) > 1:
            print("=== Usage")
            print("  dig-spider genexamples <dir>")
            print("---------")
            print("dir: save the examples to dir")

            if len(args) > 1:
                print(
                    "running 'dig-spider genexamples' with more than one dir is not supported"
                )
            return
        self.copy_template(args[0] + '/examples')

    def copy_template(self, dst):
        src = os.path.dirname(__file__) + '/examples'
        shutil.copytree(src, dst, dirs_exist_ok=True)
        logging.info("Generating dig-spider examples to %s successfully!", dst)


def exec():
    """
     execute dig-spider as a scrapy shell command
    :return:
    """
    os.environ.setdefault("XDG_CONFIG_HOME", os.path.dirname(__file__))
    execute()


if __name__ == "__main__":
    exec()
