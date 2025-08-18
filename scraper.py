from time import time
import requests
from bs4 import BeautifulSoup
import re
from helpers import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://nationalanthems.info/"

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=chrome_options
)

def get_subpages():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")

    links = set()
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href.endswith('.htm') and href not in links:
            links.add(href)
    
    return list(links)

def write_links_to_file(links):
    with open('data/links.txt', 'w') as file:
        for link in links:
            file.write(link + '\n')

def scrape_page(link):
    url = BASE_URL + link
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mp3j_dlanchor_0"))
        )
    except:
        print("Timed out waiting for page to load.")
        return None

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    
    country = get_country_title(soup)
    if title_has_year(country) or is_royal_anthem(country):
        return None

    anthem_names = get_anthem_names(soup)
    if not anthem_names:
        return None

    [start_year, end_year] = get_years(soup)

    print("Downloading music...")
    music_path = download_music(country, soup)
    print("Music downloaded.")

    data = {
        "country": country,
        "anthem_names": anthem_names,
        "start_year": start_year,
        "end_year": end_year,
        "composer": get_composer(soup),
        "link": url,
        "music_path": music_path
    }

    return data


if __name__ == "__main__":
    # pages = get_subpages()

    link = "na.htm"
    data = scrape_page(link)
    print(data)

    driver.quit()
    
