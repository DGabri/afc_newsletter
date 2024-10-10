import time, os, sys
import json
from crawl4ai.chunking_strategy import *
from crawl4ai.extraction_strategy import *
from crawl4ai.crawler_strategy import *
from crawl4ai.web_crawler import WebCrawler
from crawl4ai import config
from llama_index.llms.groq import Groq

llm_model = "llama-3.1-70b-versatile"
llm = Groq(model=llm_model, api_key="")


crawler = WebCrawler()
crawler.warmup()


url = "https://www.fifa.com/en/cat/4y0v6cXszD67eNIMVA6krL"
url = "https://www.securityweek.com/"

url = "https://www.jfa.jp/samuraiblue/"
res = crawler.run(url, bypass_cache=True, user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                  css_selector=".nextmatch-block")

tv_stream_url_samurai_blue = "https://www.jfa.jp/samuraiblue/worldcup_2026/final_q_2026/20241015/tv.html#pankz"
res = crawler.run(tv_stream_url_samurai_blue, bypass_cache=True, user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                  css_selector="#container #main-colum")

samurai_blue_schedule_url = "https://www.jfa.jp/samuraiblue/schedule_result/2024.html"
res = crawler.run(samurai_blue_schedule_url, bypass_cache=True, user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                  css_selector=".outer-block .outer-inner")

# Description with month
samurai_blue_news_url = "https://www.jfa.jp/samuraiblue/news/2024/10/"
res = crawler.run(samurai_blue_news_url, bypass_cache=True, user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                  css_selector=".news-list02")


#print(res.html)
#print(res.model_dump_json())
print(res.markdown)
links = res.links
scraped = res.markdown


prompt = f"""
[SYSTEM]
Given the context answer the user question
You are given a website content regarding the official japan team for the world cup, samurai blue. Extract what the user asks: 

Context: {scraped}

PUT THE ANSWER INSIDE THRE BACKTICKS LIKE: ``` ANSWER ```
Answer in a structured format for a newsletter regarding football events. Be enthusiastic and supportive for the team!

[USER]
Question: Today is 10 october 2024, what are the next matches, against which team and where? 
"""

#Question: Where can i watch the match and at which time? Answer in a structured format for a newsletter regarding football events
#Question: When is the next match and where? Answer in a structured format for a newsletter regarding football events

response = llm.complete(prompt).text
print(response)