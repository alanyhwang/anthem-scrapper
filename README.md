# Scraping National Anthems Across the World

This script will:

- scrape this website: https://nationalanthems.info/ for all current countries and their national anthems
  - NOTE: past anthems that are not currently used are excluded from this script, including royal anthems
- extracted data are in the following format:

  - in data/json : each country an information are in its own json file (example: Canada.json)

  - in data/music : stores each country's music (example Canada.mp3)
  - in data/data.csv : all countries and information extracted are put in a csv format (encoding = "utf-8")

- JSON exmaple:

```
        {
            "country": "Canada",
            "anthem_names": [
                "“O Canada” (English)",
                "“Ô Canada” (French)"
            ],
            "start_year": "1980",
            "end_year": "Present",
            "composers": [
                "Calixa Lavallée"
            ],
            "link": "https://nationalanthems.info/ca.htm",
            "music_path": "data/music/Canada.mp3"
        }
```

- SOURCE: The extracted data is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). For more information, go to https://nationalanthems.info/faq.html
