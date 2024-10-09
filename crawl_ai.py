import time, os, sys
import json
from crawl4ai.chunking_strategy import *
from crawl4ai.extraction_strategy import *
from crawl4ai.crawler_strategy import *
from crawl4ai.web_crawler import WebCrawler
from crawl4ai import config


crawler = WebCrawler()
crawler.warmup()


url = "https://www.jfa.jp/samuraiblue/"
url = "https://www.fifa.com/en/cat/4y0v6cXszD67eNIMVA6krL"
url = "https://www.securityweek.com/"
res = crawler.run(url, bypass_cache=True)

print(res.model_dump_json())
print(res.markdown)