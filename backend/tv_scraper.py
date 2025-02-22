import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

def scrape_tv_series_titles(max_clicks=5):
    print("Starting TV series title scraping...")
    # Set up Selenium (visible mode; uncomment headless if needed)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    
    collected_titles = set()
    click_count = 0

    try:
        # TV series URL on IMDb sorted by votes
        url = "https://www.imdb.com/search/title/?title_type=tv_series&sort=num_votes,desc"
        print(f"Navigating to URL: {url}")
        driver.get(url)
        time.sleep(3)  # allow page to load

        # (Optional) Accept cookies if needed
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//text()[contains(., 'Accept')]]"))
            )
            print("Cookie banner found. Clicking 'Accept'.")
            accept_button.click()
            time.sleep(2)
        except (NoSuchElementException, TimeoutException):
            print("No cookie banner found. Skipping...")

        # Function to update titles using CSS selectors
        def update_titles(page_source):
            soup = BeautifulSoup(page_source, "html.parser")
            # Selector for the TV series title element (similar to movies)
            links = soup.select("a.ipc-title-link-wrapper h3.ipc-title__text")
            for link in links:
                text = link.get_text(strip=True)
                # Remove any leading numbering like "1. "
                text = re.sub(r'^\d+\.\s*', '', text)
                if text.lower() != "recently viewed":
                    collected_titles.add(text)
            print(f"Collected {len(collected_titles)} unique titles so far.")

        # Initial update from first page load
        update_titles(driver.page_source)

        # Click the "50 more" button a set number of times (if available)
        while click_count < max_clicks:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                see_more_button = driver.find_element(
                    By.XPATH,
                    "//span[@class='ipc-see-more__text' and text()='50 more']/ancestor::button"
                )
                print(f"Attempting to click button: '{see_more_button.text}'")
                driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)
                time.sleep(1)
                try:
                    see_more_button.click()
                except ElementClickInterceptedException:
                    print("Element click intercepted. Using JavaScript click instead.")
                    driver.execute_script("arguments[0].click();", see_more_button)
                click_count += 1
                print(f"'50 more' button clicked {click_count} time(s).")
                time.sleep(2)
            except NoSuchElementException:
                print("No more '50 more' button found.")
                break
            except Exception as e:
                print(f"Error clicking '50 more' button: {e}")
                break

            update_titles(driver.page_source)

        final_page_source = driver.page_source
        print("Final page source obtained.")
    finally:
        driver.quit()
        print("Driver quit.")

    # Final parse to capture any missed titles
    soup = BeautifulSoup(final_page_source, "html.parser")
    links = soup.select("a.ipc-title-link-wrapper h3.ipc-title__text")
    for link in links:
        text = link.get_text(strip=True)
        text = re.sub(r'^\d+\.\s*', '', text)
        if text.lower() != "recently viewed":
            collected_titles.add(text)

    final_titles = sorted(collected_titles)
    print(f"\nTotal '50 more' button clicks: {click_count}")
    print(f"Found {len(final_titles)} unique TV series titles:")
    for t in final_titles:
        print(t)

    # Save unique TV series titles to a file
    with open("unique_tv_series_titles.txt", "w", encoding="utf-8") as file:
        for title in final_titles:
            file.write(title + "\n")
    print("Unique TV series titles saved to 'unique_tv_series_titles.txt'.")

    return final_titles

if __name__ == "__main__":
    scrape_tv_series_titles(max_clicks=30)
