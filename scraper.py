import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers import *
from csv_helpers import write_to_csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://nationalanthems.info/"
MUSIC_DIR = Path("data/music")
DATA_DIR = Path("data/json")

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
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
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href.endswith(".htm") and href not in links:
            links.add(href)

    return list(links)


def save_to_json(data, country):
    safe_country = country.replace(" ", "_")
    json_file_path = DATA_DIR / f"{safe_country}.json"
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def scrape_page(link):
    driver.get(link)
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

    music_path = download_music(country, soup)

    data = {
        "country": country,
        "anthem_names": anthem_names,
        "start_year": start_year,
        "end_year": end_year,
        "composers": get_composers(soup),
        "link": link,
        "music_path": music_path,
    }

    save_to_json(data, country)

    return data


if __name__ == "__main__":
    pages = get_subpages()

    for page in tqdm(pages):
        print(f"Processing {page}...")
        data = scrape_page(page)
        if data:
            write_to_csv(data)

    driver.quit()
