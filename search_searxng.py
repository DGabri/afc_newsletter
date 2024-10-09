import requests

def searxng_query(query, country):
    url = "http://192.168.2.73:32768/search"
    params = {
        "q": query,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    
    return response

# Example usage
results = searxng_query("What is an esg", "us-en")
print(results.json())