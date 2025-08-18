import csv
import os

CSV_PATH = "data/data.csv"
CSV_HEADERS = [
    "country",
    "anthem_names",
    "start_year",
    "end_year",
    "composers",
    "link",
    "music_path",
]


def write_to_csv(data, csv_path=CSV_PATH):
    row = {
        "country": data["country"],
        "anthem_names": " | ".join(data["anthem_names"]),
        "start_year": data["start_year"],
        "end_year": data["end_year"],
        "composers": " | ".join(data["composers"]),
        "link": data["link"],
        "music_path": data["music_path"],
    }

    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
