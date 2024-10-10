from crawl4ai.web_crawler import WebCrawler
from crawl4ai.extraction_strategy import *
from crawl4ai.chunking_strategy import *
from crawl4ai.crawler_strategy import *
from llama_index.llms.groq import Groq
from datetime import datetime

class WebScraper:
    def __init__(self, llm_model, groq_api_key, verbose=True):
        # Logging
        self.verbose = verbose
        
        # Crawler
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        self.crawler = WebCrawler()
        self.crawler.warmup()
        self.todays_date_string = datetime.now().strftime("%d %B %Y")
        
        # LLM
        self.llm = Groq(model=llm_model, api_key=groq_api_key)
        self.prompt_template = """
        [SYSTEM]
        Given the context answer the user question
        You are given a website content regarding the official japan team for the world cup, samurai blue. Extract what the user asks: 

        Context: {scraped}

        Answer in a structured format for a newsletter regarding football events. Be enthusiastic and supportive for the team! Be straight to the point without repeting too much!
        It is forbidden to add links or URLs in the answer.
        [USER]
        {user_question}
        """
        
        self.schedule_prompt = f"Question: Today is {self.todays_date_string}, what are all the upcoming matches, against which team and where?\n"
        self.tv_stream_prompt = f"Question: Where can i watch the match and at which time?"
        self.next_match_prompt = f"Question: When is the next match and where?"


    # Function used to substitute runtime values in the prompt
    def generate_prompt(self, scraped_content, user_question):
            return self.prompt_template.format(scraped=scraped_content, user_question=user_question)

    def scrape_url_with_css_selector(self, url, selector, return_type="md"):
        scraped_content = self.crawler.run(url, bypass_cache=True, user_agent=self.user_agent, css_selector=selector, verbose=self.verbose)
        
        # return links or markdown
        if return_type == "md":
            return scraped_content.markdown
        elif return_type == "links":
            return scraped_content.links

    def scrape_next_match(self):
        url = "https://www.jfa.jp/samuraiblue/"
        selector = ".nextmatch-block"
        return self.scrape_url_with_css_selector(url, selector)

    def scrape_tv_stream(self):
        url = "https://www.jfa.jp/samuraiblue/worldcup_2026/final_q_2026/20241015/tv.html#pankz"
        selector = "#container #main-colum"
        return self.scrape_url_with_css_selector(url, selector)

    def scrape_schedule(self):
        url = "https://www.jfa.jp/samuraiblue/schedule_result/2024.html"
        selector = ".outer-block .outer-inner"
        return self.scrape_url_with_css_selector(url, selector)

    def scrape_news(self):
        url = "https://www.jfa.jp/samuraiblue/news/2024/10/"
        selector = ".news-list02"
        return self.scrape_url_with_css_selector(url, selector, return_type="links")

    # Function to return all the data from JFA
    # TODO: extract news sublinks
    def scrape_all(self):
        
        if (self.verbose):
            print("Scraping JFA")
            
        next_match_result = self.scrape_next_match()
        tv_stream_result = self.scrape_tv_stream()
        schedule_result = self.scrape_schedule()
        #news_result = self.scrape_news()

        return {
            'next_match': next_match_result,
            'tv_stream': tv_stream_result,
            'schedule': schedule_result,
        }
        #   'news': news_result
    
    # Function to get the LLM response, for now Groq
    def query_llm(self, prompt):
        
        """Query the LLM, extract the answer which is in ``` answer ``` and return it"""
        response = self.llm.complete(prompt).text

        return response
    
    def process_next_match(self, data):
        
        if (self.verbose):
            print("Processing next match data")
        
        prompt = self.generate_prompt(data, self.next_match_prompt)
        response = self.query_llm(prompt)
        
        return {"content_type": "next_match_info", "content": response}

    def process_tv_stream(self, data):
        
        if (self.verbose):
            print("Processing TV stream data")
            
        prompt = self.generate_prompt(data, self.tv_stream_prompt)
        response = self.query_llm(prompt)
        
        return {"content_type": "tv_stream_info", "content": response}

    def process_schedule(self, data):
        
        if (self.verbose):
            print("Processing schedule data")
        
        prompt = self.generate_prompt(data, self.schedule_prompt)
        response = self.query_llm(prompt)
        
        return {"content_type": "schedule_info", "content": response}

    def process_news(self, data):
        
        if (self.verbose):
            print("Processing news data")
        

    def extract_samuraiblue_info(self):
        
        result = []
        
        # Scrape content for next match, schedule and tv stream updates
        all_data = self.scrape_all()
        next_match = self.process_next_match(all_data["next_match"])
        tv_stream = self.process_tv_stream(all_data["tv_stream"])
        schedule = self.process_schedule(all_data["schedule"])
        
        result.append(next_match)
        result.append(tv_stream)
        result.append(schedule)
        
        return result
        

llm_model = "llama-3.1-70b-versatile"        
groq_api_key = ""

scraper = WebScraper(llm_model, groq_api_key, verbose=True)
all_results = scraper.extract_samuraiblue_info()

