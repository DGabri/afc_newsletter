from llama_index.llms.ollama import Ollama
from afc_newsletter.prompts import news_summarization_prompt
import json

llm = Ollama(model="llama3.2:3b-instruct-q4_1")
#llm = Ollama(model="mistral:v0.3")


def read_json_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

# Example usage
file_path = 'detailed_news.json'
json_data = read_json_from_file(file_path)

for news in json_data:
    title = news['title']
    url = news['url']
    news_content = news['content']
    
    news_summarization_prompt += title + "\n" + "Content: " + news_content + "\n" + "Source: " + url
    
    response = llm.complete(news_summarization_prompt).text
    
    print(response)
