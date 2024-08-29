import time
import json
import boto3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os

# AWS S3 Configuration
s3_client = boto3.client('s3')
bucket_name = 'your-s3-bucket-name'
s3_key = 'scraped_data.json'

# Function to initialize and return the Chrome browser
def initialize_browser():
    chrome_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()  # Maximize the browser window
    return browser


columns = ['No.', 'Combination Registration No.', 'Description', 'Under Section', 'Decision Date', 'Order']

# Local file path
local_file_path = r'C:\Users\Premkumar.8265\Desktop\aws\scraped_data_local.json'


# Function to scrape data from the table on the current page
def scrape_table(browser):
    data = []
    try:
        time.sleep(5)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table#datatable_ajax tbody tr'))
        ) 
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            cols_text = [col.text for col in cols]

            # Extract the anchor tag link
            anchor_tag = cols[-1].find_element(By.TAG_NAME, 'a')
            link = anchor_tag.get_attribute('href')
            cols_text[-1] = link
            
             # Create a dictionary using the columns as keys
            record = {columns[i]: cols_text[i] for i in range(len(columns))}
            data.append(record)
    except Exception as e:
        print(f"Error in scrape_table: {e}")
    return data

# Function to handle pagination and scrape all pages
def scrape_all_pages(browser):
    all_data = []
    
    # Scrape the first page
    first_page_data = scrape_table(browser)
    all_data.extend(first_page_data)
    
    while True:
        try:
            time.sleep(5)
            next_button = browser.find_element(By.CSS_SELECTOR, '#datatable_ajax_next a')
            if 'disabled' in next_button.get_attribute('class'):
                break
            else:
                next_button.click()
                # Wait for the table to refresh
                WebDriverWait(browser, 20).until(
                    EC.staleness_of(browser.find_element(By.CSS_SELECTOR, 'table#datatable_ajax tbody tr'))
                )
                # Scrape the data from the new page
                all_data.extend(scrape_table(browser))
        except Exception as e:
            print(f"Error in scrape_all_pages: {e}")
            break
    return all_data

# Function to fetch existing data from S3
def fetch_existing_data_from_s3():
    try:
        response = s3_client.get_object(Bucket='needle-45', Key='scraped_data32.json')
        print("resoponse\n\n", response)
        existing_data = json.loads(response['Body'].read().decode('utf-8'))
        return existing_data
    except s3_client.exceptions.NoSuchKey:
        return []

# Function to upload data to S3
def upload_to_s3(data):
    s3_client.put_object(Bucket='needle-45', Key= 'scraped_data32.json', Body=json.dumps(data))
    print(f"Uploaded data to {s3_key} in S3 bucket {bucket_name}")



# def save_to_local(data):
#     with open(local_file_path, 'w') as f:
#         json.dump(data, f, indent=2)
#     print(f"Saved data to local file: {local_file_path}")




def save_to_local(data):
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create filename with timestamp
    filename = f"scraped_data_{timestamp}.json"
    
    # Combine with the directory path
    full_path = os.path.join(r'C:\Users\Premkumar.8265\Desktop\aws', filename)
    
    # Save the data
    with open(full_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved data to local file: {full_path}")

    return full_path  # Return the path for use in upload_to_s3 if needed


# Function to perform incremental scraping and upload only new data to S3
def incremental_scraping():
    # Initialize the browser and open the webpage
    browser = initialize_browser()
    url = 'https://www.cci.gov.in/combination/orders-section43a_44'
    browser.get(url)

    # Scrape all pages
    new_data = scrape_all_pages(browser)
    print("new-data\n\n", new_data)
    browser.quit()
    
     
    # Save to local file
    save_to_local(new_data)


    # file_path = r'C:\Users\Premkumar.8265\Desktop\aws\scraped_data.json'
    # with open(file_path, 'r') as file:
    #    new_data = json.load(file)
    # upload_to_s3(new_data)

    # Fetch existing data from S3
    existing_data = fetch_existing_data_from_s3()
    

    # Convert lists of dictionaries to sets of frozensets for comparison
    existing_data_set = set(frozenset(item.items()) for item in existing_data)
    new_data_set = set(frozenset(item.items()) for item in new_data)

    # Find only new data
    only_new_data = [dict(item) for item in (new_data_set - existing_data_set)]

    print("only_new_data\n\n", only_new_data)

    if only_new_data:
        # Combine existing data with new data
        combined_data = existing_data + only_new_data
        
        # Upload combined data to S3
        upload_to_s3(combined_data )
        pass
    else:
        print("No new data found.")



incremental_scraping()