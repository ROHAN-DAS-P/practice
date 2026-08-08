import os
import requests

CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "catalogue-page-1.html")
TARGET_URL = "https://books.toscrape.com/catalogue/page-1.html"

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_page():
    """Fetches the page from cache if available, otherwise from the web."""
    
    # 1. Check the cache first
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
        print("CACHE HIT")
        print(f"Response size: {len(html_content)} bytes")
        return html_content

    # 2. If not in cache, prepare a polite request
    headers = {
        # Replace with your actual GitHub username/repo if you want!
        "User-Agent": "PoliteScraper/1.0 (+https://github.com/yourusername/scraper)"
    }
    
    try:
        # 3. Request with a strict timeout
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        
        # 4. Check status code before proceeding
        if response.status_code != 200:
            print(f"Failed to fetch. Status code: {response.status_code}")
            return None
            
        html_content = response.text
        
        # 5. Save to cache for next time
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("FETCH")
        print(f"Response size: {len(html_content)} bytes")
        return html_content
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    fetch_page()