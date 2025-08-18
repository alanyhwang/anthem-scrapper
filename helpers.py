import os
from pathlib import Path
import re
from urllib.parse import urljoin
import requests
from scraper import BASE_URL

MUSIC_DIR = Path("data/music")
DATA_DIR = Path("data/json")

__all__ = ['title_has_year', 'is_royal_anthem', 'get_years', 'get_country_title', 'get_anthem_names', 'get_composer', 'download_music']

def title_has_year(title):
    return bool(re.search(r'\b\d{4}\b', title))

def is_royal_anthem(title):
    return 'royal anthem' in title.lower()

def get_years(soup):
    start_year = "Unknown"
    end_year = "Present"

    field_ids = ['custom-field-13', 'custom-field-11', 'custom-field-6']
    for field_id in field_ids:
        div = soup.find('div', {'id': field_id})
        if div:
            match = re.search(r'\b(\d{4})\b', div.text)
            if match:
                start_year = match.group(1)

    return [start_year, end_year]

def get_country_title(soup):
    return soup.find('h1').text.strip()

def get_anthem_names(soup):
    anthem_title_section = soup.find('div', {'id': 'custom-field-5'})
    if not anthem_title_section:
        return None
    anthem_names = [line for line in anthem_title_section.find('div', class_='customvalue').stripped_strings]

    return anthem_names

def get_composer(soup):
    return soup.find('div', {'id': 'custom-field-4'}).find('div', class_='customvalue').text.strip()
    

def download_file(url, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "audio/mpeg, audio/*;q=0.9, */*;q=0.8",
        "Referer": BASE_URL,
    }
    resp = requests.get(url, headers=headers, stream=True)
    resp.raise_for_status()
    with open(path, "wb") as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)

def download_music(country, soup):
    music_file_path = None

    link_tag = soup.find('a', {'id': 'mp3j_dlanchor_0'})
    print(link_tag)
    if not link_tag or not link_tag.get("href"):
        return None
    link_tail = link_tag["href"]
    
    music_link = urljoin(BASE_URL, link_tail)
    _, ext = os.path.splitext(music_link)

    safe_country = country.replace(" ", "_") 
    music_file_path = MUSIC_DIR / f"{safe_country}{ext}"

    download_file(music_link, music_file_path)
    
    return music_file_path