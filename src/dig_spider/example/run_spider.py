from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

if __name__ == "__main__":
    cwd = os.path.dirname(__file__)

    os.environ.setdefault("XDG_CONFIG_HOME", cwd + "/../")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    # 'followall' is the name of one of the spiders of the project.
    process.crawl("website",
                  config=cwd + "/config/re_example.yaml",
                  # config=cwd + "/config/allsharktankproducts.yaml",
                  # url="https://allsharktankproducts.com/sharktankproducts/season-12-products/",
                  # LOG_LEVEL="DEBUG",
                  # DOWNLOAD_DELAY=3
                  COOKIES_ENABLED=False
                  )
    process.start()
    process.stop()
