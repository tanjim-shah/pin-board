import json
import time
from playwright.sync_api import sync_playwright

def auto_scroll(page, scroll_count=15, delay=1):
    previous_height = 0
    for _ in range(scroll_count):
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(delay)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def scrape_board_names(username, section="_saved"):
    url = f"https://www.pinterest.com/{username}/{section}/"
    fake_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=fake_user_agent)
        page = context.new_page()
        print(f"Visiting: {url}")
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")

        auto_scroll(page)

        board_titles = set()
        h2_elements = page.query_selector_all("h2[title]")

        for h2 in h2_elements:
            title = h2.get_attribute("title")
            if title and not title.startswith("_"):
                board_titles.add(title.strip())

        browser.close()

        result = sorted(board_titles)
        with open("pinterest_boards.json", "w") as f:
            json.dump(result, f, indent=2)

        print("✅ Boards found:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    scrape_board_names("beacleaner", "_saved")
