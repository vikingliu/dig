# install dig-spider
pip3 install dig-spider

# if you want the config template
dig-spider gentemplate dst

# if you want same examples
dig-spider genexamples dst

# if you want to crawl the website config in yaml file
dig-spider crawl website -a config=css_template.yaml

# if you want to crawl the specific urls
dig-spider crawl website -a config=css_template.yaml -a start_urls=[url1]

# dig-spider crawl <options> website
# Options
#  -a start_urls=[url1, url2....] or urls.txt, replace the start_urls config in  css_template
#  -a paging=False, default True, whether crawl next_page_url
#  -a go_detail=False, default True, whether crawl item["url"]
#  -O myjson.json:json  overwrite myjson.json
#  -o myjson.json:json  append to myjson.json

# Global Options
# -L DEBUG, default INFO
# -s DOWNLOAD_DELAY=1, default 0
# -s JOBDIR=crawls/somespider-1, pausing and resuming crawls
#



# if you want to test in shell
dig-spider shell <url>

# if you want to see the response visually
dig-spider view <url>