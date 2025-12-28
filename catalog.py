from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv

def extract_catalog_details(driver, url):
    """Extract details from a Roblox catalog page"""
    details = {
        'url': url,
        'name': '',
        'best_price': '',
        'tradeable': '',
        'holding_period': '',
        'type': '',
        'created': '',
        'description': '',
        'material': ''
    }
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        # Wait for page to load
        time.sleep(2)
        
        # Extract Name
        try:
            name_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item-details-name-row h1'))
            )
            details['name'] = name_element.text.strip()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Name not found: {e}")
        
        # Extract Best Price
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, 'span.text-robux-lg')
            details['best_price'] = price_element.text.strip()
        except NoSuchElementException:
            details['best_price'] = 'N/A'
        
        # Extract Tradeable
        try:
            tradeable_element = driver.find_element(
                By.XPATH, 
                "//div[text()='Tradable']/following-sibling::span[@id='tradable-content']"
            )
            details['tradeable'] = tradeable_element.text.strip()
        except NoSuchElementException:
            details['tradeable'] = 'N/A'
        
        # Extract Holding Period
        try:
            holding_element = driver.find_element(
                By.XPATH, 
                "//div[text()='Holding Period']/following-sibling::span//span[@class='font-body text']"
            )
            details['holding_period'] = holding_element.text.strip()
        except NoSuchElementException:
            details['holding_period'] = 'N/A'
        
        # Extract Type
        try:
            type_element = driver.find_element(By.CSS_SELECTOR, 'span#type-content')
            details['type'] = type_element.text.strip()
        except NoSuchElementException:
            details['type'] = 'N/A'
        
        # Extract Created
        try:
            created_element = driver.find_element(
                By.XPATH, 
                "//div[text()='Created']/following-sibling::span[@id='tradable-content']"
            )
            details['created'] = created_element.text.strip()
        except NoSuchElementException:
            details['created'] = 'N/A'
        
        # Extract Description
        try:
            description_element = driver.find_element(
                By.CSS_SELECTOR, 
                'div.row-content p div'
            )
            details['description'] = description_element.text.strip()
        except NoSuchElementException:
            details['description'] = 'N/A'
        
        # Extract Material
        try:
            material_element = driver.find_element(
                By.XPATH, 
                "//div[text()='Materials']/following-sibling::span//span[@class='font-body text']"
            )
            details['material'] = material_element.text.strip()
        except NoSuchElementException:
            details['material'] = 'N/A'  # Material not available for this item
        
    except Exception as e:
        print(f"Error processing {url}: {e}")
    
    return details

def main():
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    # Uncomment the line below to run in headless mode
    # options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Read URLs from catalog.txt
        with open('catalog.txt', 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        
        print(f"Found {len(urls)} URLs to process")
        
        all_details = []
        
        # Process each URL
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing {i}/{len(urls)}: {url}")
            details = extract_catalog_details(driver, url)
            all_details.append(details)
            
            # Print extracted details
            print(f"  Name: {details['name']}")
            print(f"  Best Price: {details['best_price']}")
            print(f"  Tradeable: {details['tradeable']}")
            print(f"  Type: {details['type']}")
            
            # Be nice to the server
            time.sleep(2)
        
        # Save to CSV
        csv_filename = 'roblox_catalog_data.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'name', 'best_price', 'tradeable', 'holding_period', 
                         'type', 'created', 'description', 'material']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(all_details)
        
        print(f"\n✓ Data saved to {csv_filename}")
        
    except FileNotFoundError:
        print("Error: catalog.txt file not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()