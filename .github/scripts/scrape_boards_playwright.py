# .github/scripts/scrape_boards_playwright.py
import json
from playwright.sync_api import sync_playwright
import time

def auto_scroll(page):
    previous_height = None
    for _ in range(10):  # scroll 10 times
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(1)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def scrape_pinterest_boards(username):
    url = f"https://www.pinterest.com/{username}/boards/"
    fake_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=fake_user_agent)
        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")
        
        auto_scroll(page)

        board_titles = set()
        elements = page.query_selector_all("div[data-test-id='board-item'] div[title]")

        for el in elements:
            title = el.get_attribute("title")
            if title and not title.startswith("_"):
                board_titles.add(title.strip())

        browser.close()

        sorted_boards = sorted(list(board_titles))
        with open("pinterest_boards.json", "w") as f:
            json.dump(sorted_boards, f, indent=2)

        print("Scraped boards:", sorted_boards)

if __name__ == "__main__":
    scrape_pinterest_boards("beacleaner")
