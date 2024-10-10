import requests

def searxng_query(query, country):
    url = "http://192.168.2.73:32768/search"
    params = {
        "q": query,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    
    return response
import requests

SEARXNG_URL = "http://192.168.2.73:32768"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
REQUEST_TIMEOUT = 10

def searxng(query: str, categories: str = "general") -> list:
    searxng_url = f"{SEARXNG_URL}/search?q={query}&categories={categories}&format=json&time_range=month"
    try:
        response = requests.get(searxng_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        return [{"error": f"Search query failed with error: {e}"}]

    search_results = response.json()
    return search_results

searxng("AFC Samurai blue", "sport")

# Example usage
results = searxng_query("What is an esg", "us-en")
print(results.json())