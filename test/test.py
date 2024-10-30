from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
if __name__ == "__main__":

    os.environ.setdefault("XDG_CONFIG_HOME", os.path.dirname(__file__) +"/../src/dig_spider")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    # 'followall' is the name of one of the spiders of the project.
    process.crawl("website", config="config/allsharktankproducts.yaml",
                  url="https://allsharktankproducts.com/sharktankproducts/season-12-products/",
                  # LOG_LEVEL="INFO"
                  # DOWNLOAD_DELAY=3
                  )
    process.start()
    process.stop()

