# Roblox Catalog Scraper

Simple Selenium-based scrapers for Roblox catalog pages. These scripts read a list of item URLs from `catalog.txt`, extract item metadata (name, price, tradeable, type, created date, description, materials, etc.), and save the results to a CSV file (`roblox_catalog_data.csv`).

**Files**
- [catalog1.py](catalog1.py): Improved scraper with retry logic for missing names and a summary of missing items.
- [catalog.py](catalog.py): Original scraper without retry logic.
- [catalog.txt](catalog.txt): Input — one Roblox catalog URL per line.
- [roblox_catalog_data.csv](roblox_catalog_data.csv): Output CSV produced after running a script.

**Prerequisites**
- Python 3.8 or newer
- Google Chrome (matching your ChromeDriver version)
- ChromeDriver available on your PATH or provide its path in the script
- Python package: `selenium`

Install the Python dependency:

```bash
pip install selenium
```

Optional: create and activate a virtual environment before installing.

**Usage**
1. Put one Roblox catalog URL per line into `catalog.txt`.
2. Adjust Chrome / ChromeDriver settings if needed (the scripts use `webdriver.Chrome()` with options). `catalog1.py` includes a commented `--headless` option.
3. Run the scraper you prefer:

```bash
python catalog1.py
# or
python catalog.py
```

The script will process the URLs, print progress to the console, and write `roblox_catalog_data.csv` in the same folder.

**Notes & Troubleshooting**
- If you see WebDriver or 'executable not found' errors, download ChromeDriver that matches your Chrome version and either put it on your PATH or pass its path when constructing the driver.
- To run without opening a browser window, uncomment `options.add_argument('--headless')` in the script.
- `catalog1.py` adds retry logic for missing names and prints a summary of any items that still have missing fields.
- Respect Roblox's terms of service and rate limits when scraping; the scripts include short sleeps between requests to be polite.

**CSV fields**
- `url`, `name`, `best_price`, `tradeable`, `holding_period`, `type`, `created`, `description`, `material`
