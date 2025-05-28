# .github/scripts/scrape_boards_playwright.py
import json
from playwright.sync_api import sync_playwright

def scrape_pinterest_boards(username):
    url = f"https://www.pinterest.com/{username}/boards/"
    fake_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=fake_user_agent)
        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("a[href*='/beacleaner/']", timeout=20000)

        links = page.query_selector_all("a[href*='/beacleaner/']")
        boards = set()

        for link in links:
            href = link.get_attribute("href")
            if href and href.startswith(f"/{username}/") and href.count("/") == 2:
                board = href.split("/")[2].strip("/")
                boards.add(board)

        browser.close()

        boards_list = sorted(list(boards))
        with open("pinterest_boards.json", "w") as f:
            json.dump(boards_list, f, indent=2)

        print("Scraped boards:", boards_list)

if __name__ == "__main__":
    scrape_pinterest_boards("beacleaner")
