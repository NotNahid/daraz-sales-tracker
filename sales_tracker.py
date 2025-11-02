
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import time
from urllib.parse import urljoin, urlparse

# Selenium imports for advanced browser automation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- PASTE YOUR COMPETITOR STORE LINKS IN THIS LIST ---
STORE_URLS_TO_TRACK = [
    "https://www.daraz.com.bd/new-udoy-electronics/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2",
    # Add more of your store links here
]
# ----------------------------------------------------

# The name of the CSV file where the data will be saved
CSV_FILENAME = "sales_database.csv"

def get_product_links_from_store(store_url):
    """
    Uses a headless browser (Selenium) to find all unique product links 
    from a JavaScript-heavy Daraz store page.
    """
    product_links = set()
    print(f"\n--- Discovering products in store: {store_url} ---")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(store_url)
        time.sleep(5)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        product_cards = soup.find_all("div", attrs={"data-tracking": "product-card"})
        for card in product_cards:
            a_tag = card.find('a', href=True)
            if a_tag:
                href = a_tag['href']
                absolute_url = urljoin(store_url, href)
                cleaned_url = urljoin(absolute_url, urlparse(absolute_url).path)
                product_links.add(cleaned_url)
        
        print(f"Found {len(product_links)} unique products.")
        return list(product_links)

    except Exception as e:
        print(f"    ! An error occurred while discovering products in {store_url}: {e}")
        return []
    finally:
        driver.quit()

def scrape_sales_data(url, driver): # Accept driver as an argument
    """
    Scrapes the product name and 30-day sales data from a given Daraz product URL using Selenium.
    """
    try:
        url_with_trick = url + "?sort=order"
        print(f"  - Fetching data for: {url}")
        driver.get(url_with_trick)
        time.sleep(3) # Wait for the page to load

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        product_name_element = soup.find("span", class_="pdp-mod-product-badge-title")
        product_name = product_name_element.text.strip() if product_name_element else "Product Name Not Found"

        sales_text = None
        # Look for the new text format "sold/month"
        for element in soup.find_all(string=True):
            if "sold/month" in element.strip():
                sales_text = element.strip()
                break
        
        sales_count = 0
        if sales_text:
            sales_count_str = sales_text.split()[0].replace(',', '')
            sales_count = int(sales_count_str)
        
        return product_name, sales_count

    except Exception as e:
        print(f"    ! An error occurred while processing {url}: {e}")
        return None, None

def append_to_csv(filename, data):
    """
    Appends a new row of data to the CSV file.
    """
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Timestamp", "Product Name", "30-Day Sales", "URL"])
        writer.writerow(data)

def main():
    print("--- Starting Automated Store Sales Tracker (Advanced) ---")
    
    all_product_links = []
    for store_url in STORE_URLS_TO_TRACK:
        product_links = get_product_links_from_store(store_url)
        all_product_links.extend(product_links)
    
    if not all_product_links:
        print("\nNo products found to track. Exiting. Please check the store URL and the script's link discovery logic.")
        return

    print(f"\n--- Starting to scrape data for {len(all_product_links)} products ---")
    
    # --- Selenium Setup for scraping individual pages ---
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # --------------------------------------------------

    try:
        for url in all_product_links:
            product_name, sales_count = scrape_sales_data(url, driver)
            
            if product_name and sales_count is not None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data_row = [timestamp, product_name, sales_count, url]
                
                append_to_csv(CSV_FILENAME, data_row)
                print(f"    > Saved: {product_name} | 30-Day Sales: {sales_count}")
    finally:
        driver.quit() # Always close the browser at the end
            
    print(f"\n--- Finished. Data saved to {CSV_FILENAME} ---")

if __name__ == "__main__":
    main()
