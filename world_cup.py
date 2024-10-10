from deep_translator import GoogleTranslator
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import re

################################################################################
## Utility functions
def remove_list_duplicates(lst):
    return list(set(lst))

def translate_to_target_language(input_text, target_language, default_src_language='ja'):
    if target_language == default_src_language:
        return input_text
    
    translator = GoogleTranslator(source=default_src_language, target=str(target_language))
    
    # Split in chunks to process longer texts
    chunks = [input_text[i:i+1000] for i in range(0, len(input_text), 4900)]
    
    complete_translation = ""
    for chunk in chunks:
        translated_chunk = translator.translate(chunk)
        complete_translation += translated_chunk
    
    return complete_translation

def scrape_url(url):
    response = requests.get(url, headers={"User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

scrape_url("https://www.tecnomat.it/")
################################################################################
## nbc_sport_news

def scrape_nbc_sport_news():
    nbc_url = "https://www.nbcsports.com/soccer/news/asian-afc-2026-world-cup-qualifying-schedule-results-table"
    
    soup = scrape_url(nbc_url)
    article_main = soup.find(class_="ArticlePage-main")
    
    if article_main:
        # Find the content div
        content_div = article_main.find(class_="RichTextArticleBody")
        
        if content_div:
            # Remove all script tags
            for script in content_div(["script", "style"]):
                script.decompose()
            
            # Get the text content
            content = content_div.get_text(separator='\n', strip=True)
            
            return content
    
    return -1

################################################################################
## Gekisaka

def scrape_gekisaka_news_urls(url, minimum_date):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    article_main = soup.find(class_="entry-body")
    
    if article_main:
        post_items = soup.find_all(class_="post-title")
        
        articles = []
        for item in post_items:
            link = item.find('a')
            time_elem = item.find('time')
            
            if link and time_elem:
                title_text = link.get_text(strip=True)
                href = link.get('href')
                date_str = time_elem.text.strip()
                article_date = datetime.strptime(date_str, '%Y-%m-%d')
                if article_date > minimum_date:
                    articles.append({
                        'text': title_text,
                        'href': href,
                        'date': date_str
                    })
        
        return articles
    
    return -1

def scrape_gekisaka_news_from_url(news_url):
    response = requests.get("http:"+news_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    article_main = soup.find(class_="geki_contentitem")

    if article_main:
        # Find all <br> tags and extract the content between them
        article_content = ""
        for element in article_main.contents:
            if element.name != 'br':
                text = element.strip() if isinstance(element, str) else element.get_text().strip()
                if text:
                    article_content += text

    return article_content

def get_gekisaka_news():
    gekisaka_world_cup_news_url = "https://web.gekisaka.jp/searchtag/news?tag=233832"

    gekisaka_links = scrape_gekisaka_news_urls(gekisaka_world_cup_news_url, date_threshold)

    gekisaka_news = []
    for gekisaka_news_link in gekisaka_links:
        news = scrape_gekisaka_news_from_url(gekisaka_news_link['href'])
        gekisaka_news.append(news)

    return remove_list_duplicates(gekisaka_news)

################################################################################
## Sponichi

def scrape_sponichi_news_urls(url, minimum_date):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    list_items = soup.find_all('li', class_="cateSoccer")

    for item in list_items:
        a_tag = item.find('a')
        if a_tag:
            href = a_tag.get('href')
            title_elem = a_tag.find('p', class_="title")
            date_elem = a_tag.find('p', attrs={"data-component": "date-format"})
            
            if title_elem and date_elem:
                title_text = title_elem.get_text(strip=True)
                date_text = str(date_elem.get_text(strip=True))
                pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'

                match = re.search(pattern, date_text)

                if match:
                    year, month, day = match.groups()
                    date_str = f"{year}-{month}-{day}"
                    article_date = datetime.strptime(date_str, '%Y-%m-%d')


                if article_date > minimum_date:
                    articles.append({
                        'text': title_text,
                        'href': href,
                        'date': date_str
                    })
    
    return articles

def scrape_sponichi_news_from_url(link):
    response = requests.get("https://www.sponichi.co.jp"+link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract data-component="article-body"
    article_body = soup.find(attrs={"data-component": "article-body"})
    
    if article_body:
        # get all p tags
        paragraphs = article_body.find_all('p')
        
        # Get all text in paragraphs
        paragraph_texts = [p.get_text(strip=True) for p in paragraphs]
    # Join the list to a string
    return ' '.join(paragraph_texts)

def get_sponichi_news():
    sponichi_main_page_url = "https://www.sponichi.co.jp/soccer/tokusyu/japan/"
    sponichi_links = scrape_sponichi_news_urls(sponichi_main_page_url, date_threshold)

    sponichi_news = []
    
    for sponichi_news_link in sponichi_links:
        news = scrape_sponichi_news_from_url(sponichi_news_link['href'])
        sponichi_news.append(news)

    return remove_list_duplicates(sponichi_news)

################################################################################
## Sponichi

def scrape_nikkan_news_urls(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_articles = []

    list_items = soup.find_all('ul', class_="newslist")

    for item in list_items:
        a_tag = item.find('a')
        if a_tag:
            href = a_tag.get('href')

            news_articles.append(href)

    return news_articles

def scrape_nikkan_news_from_url(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    article_body = soup.find_all(class_="article-body")

    if article_body:
        # Get all paragraphs from all article-body elements
        paragraphs = []
        for body in article_body:
            paragraphs.extend(body.find_all('p'))
        
        # Get all text in paragraphs
        paragraph_texts = [p.get_text(strip=True) for p in paragraphs]
    
        return ' '.join(paragraph_texts)
    return ""

def get_nikkan_news():
    nikkan_news_page_url = "https://www.nikkansports.com/soccer/wc2026/qualifiers/"

    nikkan_links = scrape_nikkan_news_urls(nikkan_news_page_url)

    nikkan_news = []
    
    for nikkan_news_link in nikkan_links:
        news = scrape_nikkan_news_from_url(nikkan_news_link)
        nikkan_news.append(news)

    # remove duplicates
    return remove_list_duplicates(nikkan_news)

################################################################################


# filter dates newer than 20 september 24
date_threshold = datetime(2024, 9, 20)

nbc = scrape_nbc_sport_news()
nikkan = get_nikkan_news()
sponichi = get_sponichi_news()
gekisaka = get_gekisaka_news()

news_outlets = [nikkan, sponichi, gekisaka]
translated_articles = []

for news_outlet in news_outlets:
    for news in news_outlet:
        translation = translate_to_target_language(news, 'en')
        translated_articles.append(str(translation))


translated_articles =remove_list_duplicates(translated_articles)
translated_articles

from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama

llm_model = "llama3.2:1b-instruct-q4_0"
llm_model = "llama3.2:3b-instruct-q4_1"
llm = Ollama(model=llm_model, request_timeout=400)

llm_model = "llama-3.1-70b-versatile"
llm = Groq(model=llm_model, api_key="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")


prompt = f"""
[SYSTEM]
You are an expert on the FIFA World Cup Asian qualifiers, with a focus on the Japan national team (Samurai Blue). Your task is to create engaging content for a newsletter tailored to Japanese football fans. The newsletter is titled "FIFA World Cup 26 Flash News: Lens on Japan".
Please compile a well-formatted newsletter that includes the following sections:

Latest News Roundup: Provide a concise summary of recent developments related to the Japan national team and their World Cup qualification journey.
Upcoming Matches: List Japan's next two qualification matches, including dates, times, and opponents.
Pre-Match Analysis: Offer insightful analysis for the upcoming games, considering factors such as team form, key players, historical performance against the opponents, and potential strategies.
Probable Lineups: Present the likely starting eleven for Japan in their next two matches. Include any notable changes or tactical adjustments.
Player Spotlight: Highlight a standout player or rising star in the Japan squad, discussing their recent performances and importance to the team.
Qualification Standings: Provide a brief update on Japan's current position in the qualification group, including points, goal difference, and games played.
Where to Watch: Include information on how fans can watch the upcoming matches, listing TV channels, streaming services, or official viewing parties (if applicable).
Fan Corner: Add a brief section for fan engagement, such as a trivia question about Japan's World Cup history or a call for fans to share their match predictions.

Ensure the content is informative, engaging, and formatted in a visually appealing manner suitable for a newsletter. Use appropriate headings, bullet points, and brief paragraphs to enhance readability.
Be enthusiastic about the support of the team of samurai blue (Japan national team)

[USER]
Below are reported news from different outlets:
{translated_articles}
"""

"""
- NBC: {nbc}
- Nikkan: {str(nikkan)}
- Sponichi: {str(sponichi)}
- Gekisaka: {str(gekisaka)}
"""
response = llm.complete(prompt).text

print(response)

print(prompt)