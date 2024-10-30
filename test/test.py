from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    # 'followall' is the name of one of the spiders of the project.
    process.crawl("website", config="config/allsharktankproducts.yaml",
                  url="https://allsharktankproducts.com/sharktankproducts/season-12-products/",
                  # LOG_LEVEL="INFO"
                  # DOWNLOAD_DELAY=3
                  )
    process.start()
    process.stop()
