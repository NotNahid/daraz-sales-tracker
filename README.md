# Daraz Sales Tracker

This project is a Python script that automatically scrapes product and sales data from Daraz store pages.

## Features

- **Store Scraping**: Traverses a Daraz store page to discover all product links.
- **Dynamic Content Handling**: Uses Selenium and a headless Chrome browser to correctly render JavaScript-heavy pages, ensuring all products are found.
- **Sales Data Extraction**: For each product found, it navigates to the product page and scrapes key information:
  - Product Name
  - Monthly Sales Data (e.g., "15 sold/month")
- **Data Storage**: Saves the collected data with a timestamp into a `sales_database.csv` file for easy analysis.

## How to Use

### 1. Installation

Make sure you have Python 3 installed. Then, install the necessary libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 2. Configuration

Open the `sales_tracker.py` file and add the Daraz store URLs you want to track to the `STORE_URLS_TO_TRACK` list at the top of the file.

```python
# --- PASTE YOUR COMPETITOR STORE LINKS IN THIS LIST ---
STORE_URLS_TO_TRACK = [
    "https://www.daraz.com.bd/shop/your-store-name/",
    # Add more of your store links here
]
# ----------------------------------------------------
```

### 3. Running the Script

Execute the script from your terminal:

```bash
python3 sales_tracker.py
```

The script will first discover all products from the configured store URLs and then proceed to scrape the sales data for each one.

## Output

The script will generate a `sales_database.csv` file with the following columns:

- **Timestamp**: The date and time when the data was scraped.
- **Product Name**: The name of the product.
- **30-Day Sales**: The number of units sold in the last month.
- **URL**: The URL of the product page.
