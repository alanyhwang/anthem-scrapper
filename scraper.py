import requests
from bs4 import BeautifulSoup

BASE_URL = "https://nationalanthems.info/"

def get_subpages():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    links = [a['href'] for a in soup.find_all('a') if a.get('href', '').endswith('.htm')]
    return links

if __name__ == "__main__":
    pages = get_subpages()
    print("Number of links found:", len(pages))
    for page in pages:
        print(1)
        print(page)
