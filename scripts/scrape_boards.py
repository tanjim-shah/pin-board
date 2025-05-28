import requests
from bs4 import BeautifulSoup
import json

USERNAME = "beacleaner"
BASE_URL = f"https://www.pinterest.com/{USERNAME}/boards/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_boards():
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    boards = []

    # Find script tag that contains board data
    for script in soup.find_all("script"):
        if "application/ld+json" in str(script):
            try:
                data = json.loads(script.string.strip())
                if isinstance(data, dict) and "mainEntityofPage" in data:
                    boards.append({
                        "name": data.get("name"),
                        "url": data.get("url")
                    })
            except Exception:
                continue

    # Fallback: extract from href tags
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if f"/{USERNAME}/" in href and "/boards/" not in href and "/pins/" not in href:
            board_name = href.split("/")[-2]
            if board_name and not any(b['name'] == board_name for b in boards):
                boards.append({
                    "name": board_name.replace("-", " ").title(),
                    "url": "https://www.pinterest.com" + href
                })

    with open("output/boards.json", "w") as f:
        json.dump(boards, f, indent=2)
    print("Scraped", len(boards), "boards.")

if __name__ == "__main__":
    scrape_boards()
