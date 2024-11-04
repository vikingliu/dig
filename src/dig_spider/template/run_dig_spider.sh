dig-spider crawl website -a config=code_template.yaml

# dig-spider crawl website -a config=code_template.yaml -a url=xxx
# params
#  paging=False, default True, whether crawl next_page_url
#  go_detail=False, default True, whether crawl item["url"]
#
#  other params same to scrapy
#   DOWNLOAD_DELAY=1, default 0
#   LOG_LEVEl=DEBUG, default INFO