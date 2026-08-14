from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

# Initialize Tavily client
tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

# Creating first tool using Tavily API to search the web
@tool
def web_search(query: str)-> str:
    """Search the web for recent and reliable information on a given topic. Returns title, URLs and snippets"""
    result = tavily.search(query, max_results = 5) #call tavily search API

    out = []
    for r in result.get('results', []):
        out.append(
            f"Title: {r.get('title')}\nURL: {r.get('url')}\nSnippet: {r.get('content','')[:300]}\n"
        )

    return "\n----\n".join(out)

#Invoke kar k print krenege
#print(web_search.invoke("what are the recent news on AI?"))

# Creating second tool using BeautifulSoup to scrape a webpage
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
