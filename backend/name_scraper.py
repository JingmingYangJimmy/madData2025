import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

def scrape_imdb_titles_selenium(max_clicks=5):
    print("Starting IMDb title scraping...")

    # 1) Set up Selenium (Headless Mode or visible)
    chrome_options = Options()
    # Uncomment the next line to run headless
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    
    # This set will hold unique titles found so far.
    collected_titles = set()
    click_count = 0  # Counter for "50 more" button clicks

    try:
        url = "https://www.imdb.com/search/title/?title_type=feature&sort=num_votes,desc"
        print(f"Navigating to URL: {url}")
        driver.get(url)
        time.sleep(3)  # Let the page load fully

        # 2) Accept cookies if a banner appears (optional, may vary by region)
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//text()[contains(., 'Accept')]]"))
            )
            print("Cookie banner found. Clicking 'Accept'.")
            accept_button.click()
            time.sleep(2)
        except (NoSuchElementException, TimeoutException):
            print("No cookie banner found or timed out waiting. Skipping...")

        # Function to update titles using a CSS selector based on your provided HTML
        def update_titles(page_source):
            soup = BeautifulSoup(page_source, "html.parser")
            # Select the <h3> element that holds the title within an anchor
            links = soup.select("a.ipc-title-link-wrapper h3.ipc-title__text")
            for link in links:
                text = link.get_text(strip=True)
                # Remove any leading numbering (e.g., "1. ")
                text = re.sub(r'^\d+\.\s*', '', text)
                if text.lower() != "recently viewed":
                    collected_titles.add(text)
            print(f"Collected {len(collected_titles)} unique titles so far.")

        # Update titles from the initial page load
        update_titles(driver.page_source)

        # 3) Repeatedly scroll and click "50 more" if present, but stop after max_clicks
        while click_count < max_clicks:
            # Scroll to bottom so that the "50 more" button is in view
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            try:
                # Use an XPath to locate the "50 more" button by its span text then go up to the ancestor button.
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

            # 4) Update the list of titles after each click
            update_titles(driver.page_source)

        # 5) After finishing (or if something breaks), get the final page source
        final_page_source = driver.page_source
        print("Final page source obtained.")

    finally:
        driver.quit()
        print("Driver quit.")

    # Final parsing in case anything was missed
    soup = BeautifulSoup(final_page_source, "html.parser")
    links = soup.select("a.ipc-title-link-wrapper h3.ipc-title__text")
    for link in links:
        text = link.get_text(strip=True)
        text = re.sub(r'^\d+\.\s*', '', text)
        if text.lower() != "recently viewed":
            collected_titles.add(text)

    final_titles = sorted(collected_titles)  # Sorted list for consistency

    print(f"\nTotal '50 more' button clicks: {click_count}")
    print(f"Found {len(final_titles)} unique titles:")
    for t in final_titles:
        print(t)

    # Save the unique titles to a file
    with open("unique_titles.txt", "w", encoding="utf-8") as file:
        for title in final_titles:
            file.write(title + "\n")
    print("Unique titles saved to 'unique_titles.txt'.")

    return final_titles

if __name__ == "__main__":
    scrape_imdb_titles_selenium(max_clicks=100)
