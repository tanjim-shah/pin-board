import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "beacleaner"
URL = f"https://www.pinterest.com/{USERNAME}/boards/"

def scrape_boards():
    # Setup headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(URL)

    # Scroll to the bottom of the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find board titles
    board_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='board-card'] div[title]")
    board_names = list({el.get_attribute("title").strip() for el in board_elements if el.get_attribute("title")})

    driver.quit()

    # Save to JSON
    os.makedirs("output", exist_ok=True)
    with open("output/boards.json", "w") as f:
        json.dump(board_names, f, indent=2)

    print(f"✅ Scraped {len(board_names)} boards.")

if __name__ == "__main__":
    scrape_boards()
