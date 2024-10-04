import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

def get_main_content(soup):
    # Try common selectors for main content
    main_selectors = ['main', '#content', '.main-content', 'article', '.post-content']
    for selector in main_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            return main_content
    
    # If no common selector works, try to remove header and footer
    body = soup.body
    if body:
        for tag in body.select('header, footer, nav, aside'):
            tag.decompose()
        return body
    
    return soup  # Fallback to entire soup if nothing else works

def scrape_article(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title.string if soup.title else "No title found"
        
        main_content = get_main_content(soup)
        
        # Extract text content
        content = ' '.join([p.get_text(strip=True) for p in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        
        return {
            'title': title,
            'url': url,
            'content': content
        }
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def scrape_news_site(url):
    articles = []
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        
        main_content = get_main_content(soup)
        
        # Extract all links from the main content
        links = main_content.find_all('a', href=True)
        
        for link in links:
            full_url = urljoin(url, link['href'])
            if full_url.startswith(('http://', 'https://')):
                article = scrape_article(full_url)
                if article:
                    articles.append(article)
                    print(f"Scraped: {article['title']}")
                    time.sleep(1)  # Be polite, delay between requests
            
            if len(articles) >= 5:  # Limit to 5 articles per site
                break
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
    
    return articles

def save_to_json(news, filename='detailed_news.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=4)

# Example usage
news_sites = [
    "https://www.bbc.com/news",
    "https://crypto.news/news/"
]

all_articles = []
for site in news_sites:
    print(f"\nScraping {site}...")
    site_articles = scrape_news_site(site)
    all_articles.extend(site_articles)
    print(f"Scraped {len(site_articles)} articles from {site}")

save_to_json(all_articles)

print(f"\nTotal articles scraped: {len(all_articles)}")
print("Saved to detailed_news.json")

# Print a sample of the first article
if all_articles:
    sample = all_articles[0]
    print("\nSample article:")
    print(f"Title: {sample['title']}")
    print(f"URL: {sample['url']}")
    print(f"Content preview: {sample['content'][:200]}...")