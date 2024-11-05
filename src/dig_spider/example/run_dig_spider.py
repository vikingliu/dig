from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

cwd = os.path.dirname(__file__)


def run_config():
    os.environ.setdefault("XDG_CONFIG_HOME", cwd + "/../")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl("website",
                  config=cwd + "/config/css_example.yaml",
                  # start_urls=["https://allsharktankproducts.com/sharktankproducts/season-12-products/"],
                  start_urls=["https://allsharktankproducts.com/shark-tank-products-arts/da-vinci-eye-ar-drawing-tools/"],
                  # start_urls = "a.txt",
                  LOG_LEVEL="DEBUG",
                  # DOWNLOAD_DELAY=3
                  COOKIES_ENABLED=False
                  )
    process.start()
    process.stop()


def run_text():
    from dig_spider.engine.extract import ExtractEngine
    config = cwd + "/config/json_example.yaml"
    url = 'https://jsonplaceholder.typicode.com/todos/1'
    text = '''
    {
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
    '''
    extract = ExtractEngine(config)
    results, next_page_url = extract.extract_by_text(text, url, 'utf-8')
    print(results, next_page_url)


if __name__ == "__main__":
    # run_text()
    run_config()
