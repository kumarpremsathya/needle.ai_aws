import time
import requests
import pdfplumber
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# Paths
pdf_path = r'C:\Users\Premkumar.8265\Desktop\Pfrda_aggregators-demo\Pfrda_aggregators-demo\Aggregaters_PFRDA\gem_supplier.pdf'
excel_output_path = r'C:\Users\Premkumar.8265\Desktop\Pfrda_aggregators-demo\Pfrda_aggregators-demo\Aggregaters_PFRDA\gem_suppliersss.xlsx'

# Setup WebDriver
browser = webdriver.Chrome()

# URL to scrape
url = "https://gem.gov.in/incidentmanagement/non-compliance-suspended-sellers"
browser.get(url)
browser.maximize_window()

# Download PDF function
def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("PDF file downloaded successfully!")
    else:
        print("Failed to download PDF file. Status code:", response.status_code)

# Locate and download PDF
gem_pdf = browser.find_element(By.XPATH, '//*[@id="skip_main_content"]/div/div[2]/div[1]/p[1]/a')
time.sleep(2)
link = gem_pdf.get_attribute('href')
gem_pdf.click()
time.sleep(2)

pdf_filename = 'gem_supplier.pdf'
time.sleep(10)  # Ensure the PDF is fully downloaded
download_pdf(link, pdf_filename)


import time
import requests
import pdfplumber
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# Paths
pdf_path = r'C:\Users\Premkumar.8265\Desktop\Pfrda_aggregators-demo\Pfrda_aggregators-demo\Aggregaters_PFRDA\gem_supplier.pdf'
excel_output_path = r'C:\Users\Premkumar.8265\Desktop\Pfrda_aggregators-demo\Pfrda_aggregators-demo\Aggregaters_PFRDA\gem_supplier_123.xlsx'

# Setup WebDriver
browser = webdriver.Chrome()

# URL to scrape
url = "https://gem.gov.in/incidentmanagement/non-compliance-suspended-sellers"
browser.get(url)
browser.maximize_window()

# Download PDF function
def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("PDF file downloaded successfully!")
    else:
        print("Failed to download PDF file. Status code:", response.status_code)

# Locate and download PDF
gem_pdf = browser.find_element(By.XPATH, '//*[@id="skip_main_content"]/div/div[2]/div[1]/p[1]/a')
time.sleep(2)
link = gem_pdf.get_attribute('href')
gem_pdf.click()
time.sleep(2)

pdf_filename = 'gem_supplier.pdf'
time.sleep(10)  # Ensure the PDF is fully downloaded
download_pdf(link, pdf_filename)




def extract_tables_from_pdf(pdf_path):
    all_tables = {}
    header = ["Sr. No.", "Supplier Name", "Category Name", "Brand"]
    current_date = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                if "As on" in line:
                    current_date = line.split("As on")[1].strip()
                    if current_date not in all_tables:
                        all_tables[current_date] = []
                    print(f"New date found: {current_date}")
                elif current_date and line.strip() and line[0].isdigit():
                    parts = line.split()
                    if len(parts) >= 4:
                        sr_no = parts[0]
                        brand = parts[-1]
                        category = ' '.join(parts[-2::-1])[::-1].strip()
                        supplier = ' '.join(parts[1:-2])
                        row = [sr_no, supplier, category, brand]
                        if row not in all_tables[current_date]:
                            all_tables[current_date].append(row)
                            print(f"Added row: {row}")
            
            # Also process the extracted table to catch any missed data
            table = page.extract_table()
            if table:
                for row in table[1:]:  # Skip the header row
                    if row[0] and row[0].isdigit():  # Check if it's a new entry
                        cleaned_row = [cell.replace('\n', ' ').strip() if cell else '' for cell in row[:4]]
                        if current_date and cleaned_row not in all_tables[current_date]:
                            all_tables[current_date].append(cleaned_row)
                            print(f"Added row from table: {cleaned_row}")

    # Remove duplicate entries and sort by Sr. No.
    # for date in all_tables:
    #     all_tables[date] = sorted(list(set(tuple(row) for row in all_tables[date])), key=lambda x: int(x[0]))
    
    print("Extracted Tables:")
    for date, rows in all_tables.items():
        print(f"Date: {date}")
        for row in rows:
            print(row)
    
    return header, all_tables


def save_tables_to_excel(header, all_tables, output_path):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for date, rows in all_tables.items():
            df = pd.DataFrame(rows, columns=header)
            sheet_name = date.replace(" ", "_").replace("-", "_")
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# Extract and save the tables
header, all_tables = extract_tables_from_pdf(pdf_path)
save_tables_to_excel(header, all_tables, excel_output_path)


# Close the browser
browser.quit()


# def extract_tables_from_pdf(pdf_path):
#     all_tables = {}
#     header = ["Sr. No.", "Supplier Name", "Category Name", "Brand"]
#     current_date = None
    
#     with pdfplumber.open(pdf_path) as pdf:
#         for page_num, page in enumerate(pdf.pages, start=1):
#             text = page.extract_text()
#             lines = text.split('\n')
            
#             for line in lines:
#                 if "As on" in line:
#                     current_date = line.split("As on")[1].strip()
#                     if current_date not in all_tables:
#                         all_tables[current_date] = []
#                     print(f"New date found: {current_date}")
#                 elif current_date and line.strip() and line[0].isdigit():
#                     parts = line.split()
#                     if len(parts) >= 4:
#                         sr_no = parts[0]
#                         brand = parts[-1]
#                         category = ' '.join(parts[-2::-1])[::-1].strip()
#                         supplier = ' '.join(parts[1:-2])
#                         row = [sr_no, supplier, category, brand]
#                         if row not in all_tables[current_date]:
#                             all_tables[current_date].append(row)
#                             print(f"Added row: {row}")
    
    # # Remove duplicate entries and sort by Sr. No.
    # for date in all_tables:
    #     all_tables[date] = sorted(list(set(tuple(row) for row in all_tables[date])), key=lambda x: int(x[0]))
    
    # print("Extracted Tables:")
    # for date, rows in all_tables.items():
    #     print(f"Date: {date}")
    #     for row in rows:
    #         print(row)
    
    # return header, all_tables
            
# def save_tables_to_excel(header, all_tables, output_path):
#     with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#         for date, rows in all_tables.items():
#             df = pd.DataFrame(rows, columns=header)
#             sheet_name = date.replace(" ", "_").replace("-", "_")
#             df.to_excel(writer, sheet_name=sheet_name, index=False)         

# # Extract and save the tables
# header, all_tables = extract_tables_from_pdf(pdf_path)
# save_tables_to_excel(header, all_tables, excel_output_path)

# Close the browser
browser.quit()
