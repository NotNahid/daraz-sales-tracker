# 📈 Daraz Sales Tracker

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)

This project is a Python script that automatically scrapes product and sales data from Daraz store pages.

## Features

- **Store Scraping**: Traverses a Daraz store page to discover all product links.
- **Dynamic Content Handling**: Uses Selenium and a headless Chrome browser to correctly render JavaScript-heavy pages.
- **Sales Data Extraction**: For each product, it scrapes the product name and monthly sales data.
- **Data Storage**: Saves the collected data with a timestamp into a `.csv` file for easy analysis.

## How It Works

The script operates in two main phases:

1.  **Discovery Phase**: It uses a Selenium-controlled headless browser to navigate to a Daraz store page, scroll to the bottom to ensure all products are loaded, and then parses the final page HTML to collect a unique list of all product URLs.
2.  **Scraping Phase**: It then iterates through the list of discovered URLs. For each URL, it uses the same headless browser to visit the product page, waits for the dynamic content (like sales data) to load, and extracts the required information.

This two-phase, browser-automated approach ensures that even modern, JavaScript-reliant websites can be scraped effectively.

## Project Structure

```
daraz-sales-tracker/
├── sales_tracker.py      # The main script to run.
├── requirements.txt      # A list of all the Python libraries needed.
└── README.md             # This file.
```
- `sales_database.csv` will be created in this directory on the first successful run.

## How to Use

#### 1. Installation

Make sure you have Python 3 installed. Clone the repository and install the necessary libraries:

```bash
# Navigate to the project directory
cd daraz-sales-tracker

# Install required libraries
pip install -r requirements.txt
```

#### 2. Configuration

Open the `sales_tracker.py` file and add the Daraz store URLs you want to track to the `STORE_URLS_TO_TRACK` list at the top of the file.

```python
# --- PASTE YOUR COMPETITOR STORE LINKS IN THIS LIST ---
STORE_URLS_TO_TRACK = [
    "https://www.daraz.com.bd/shop/your-store-name/",
    # Add more of your store links here
]
# ----------------------------------------------------
```

#### 3. Running the Script

Execute the script from your terminal:

```bash
python3 sales_tracker.py
```

The script will show its progress in the terminal and save the results to `sales_database.csv`.

## Future Improvements

- [ ] Add support for multiple e-commerce websites.
- [ ] Create a web-based dashboard to visualize the collected data.
- [ ] Implement price change alerts (e.g., via email).
- [ ] Schedule the script to run automatically at set intervals (e.g., daily).
