# Scraping National Anthems Across the World

This script will:

- scrape this website: https://nationalanthems.info/
- get these data from each page: country, national anthem name, start date, end date (can be a number or "present" indicating the current national anthem), composer, and download the sheet music, change its name to its .htm name (while keeping the extension), for example music in abk.htm becomes abk.mp3 and create a path link to the downloaded file
- store each page data into a json file, with file name the same as its .htm name, for example abk.htm data will be stored in abk.json
- the result should have anthem music folder with all the music files and anthem data folder with all the json files
