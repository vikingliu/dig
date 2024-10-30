from scrapy.cmdline import execute
import os

def exec():
    os.environ.setdefault("XDG_CONFIG_HOME", os.path.dirname(__file__))
    execute()

if __name__ == "__main__":
    exec()
