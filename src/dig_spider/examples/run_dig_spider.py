import os
from dig_spider.running import crawl_pages, extract_page
from dig_spider.pipelines import DigEnginePipeline
from dig_spider.middlewares import DigEngineDownloaderMiddleware, DigEngineSpiderMiddleware

cwd = os.path.dirname(__file__)


class ItemPipeline(DigEnginePipeline):
    def process_item(self, item, spider):
        super().process_item(item, spider)
        print("ItemPipeline: ", item)
        # spider.config
        # save and send to kafka
        return item


class SpiderMiddleware(DigEngineSpiderMiddleware):
    pass


class DownloaderMiddleware(DigEngineDownloaderMiddleware):
    pass


def run_config():
    crawl_pages(
        config=cwd + "/config/css_example.yaml",
        # start_urls=["https://allsharktankproducts.com/sharktankproducts/season-12-products/"],
        start_urls=["https://allsharktankproducts.com/shark-tank-products-arts/da-vinci-eye-ar-drawing-tools/"],
        # start_urls = "a.txt",
        # extract_link=True,
        ITEM_PIPELINES={ItemPipeline: 200},
        SPIDER_MIDDLEWARES={SpiderMiddleware: 200},
        DOWNLOADER_MIDDLEWARES={DownloaderMiddleware: 200},
        LOG_LEVEL="DEBUG",
        # DOWNLOAD_DELAY=3
    )


def run_text():
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
    print(extract_page(config, url, 'utf-8', text))

def run_github():
    crawl_pages(
        # spider='github2',
        config=cwd + "/config/github.yaml",
        ITEM_PIPELINES={ItemPipeline: 200},
        SPIDER_MIDDLEWARES={SpiderMiddleware: 200},
        DOWNLOADER_MIDDLEWARES={DownloaderMiddleware: 200},
        LOG_LEVEL="DEBUG",
        # DOWNLOAD_DELAY=3
    )

if __name__ == "__main__":
    # run_text()
    # run_config()
    run_github()
