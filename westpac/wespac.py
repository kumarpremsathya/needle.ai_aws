
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from sqlalchemy import create_engine


# Configure ChromeOptions
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()  # Maximize the browser window

# Navigate to the URL
url = 'https://www.westpac.com.au/about-westpac/investor-centre/events-and-presentations/presentations-agm/'
browser.get(url)

# Wait for the element to be present
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div'))
)

# Find all elements based on the XPath
elements = browser.find_elements(By.XPATH, '//*[@id="content"]/div[2]/div')

# # Extract details from each element
# data = []
# for element in elements:
#     text = element.text
#     data.append(text)

# # Print or save the data
# df = pd.DataFrame(data, columns=["Details"])
# print(df)

# # Optionally save to a CSV file
# df.to_csv('westpac_details.csv', index=False)
# df.to_excel('westpac_details.xlsx', index=False)


# # Close the browser
# browser.quit()


# Extract HTML content from these elements
html_content = ""
for element in elements:
    html_content += element.get_attribute('outerHTML')

# Close the browser
browser.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')  # or 'html.parser'
print("soup", soup.prettify())
 

# New parsing logic
data = {}
current_section = None

for element in soup.find_all(['h2', 'a']):
    if element.name == 'h2':
        current_section = element.text.strip()
        data[current_section] = []
    elif element.name == 'a' and current_section:
        href = element.get('href', '')
        if href.endswith('.pdf'):
            pdf_name = element.text.strip()
            data[current_section].append((href, pdf_name))

# Convert to DataFrame
df = pd.DataFrame({k: pd.Series(v) for k, v in data.items()})

# Separate PDF links and names
for column in df.columns:
    df[f'{column}_link'] = df[column].apply(lambda x: x[0] if isinstance(x, tuple) else None)
    df[f'{column}_pdf_name'] = df[column].apply(lambda x: x[1] if isinstance(x, tuple) else None)
    df = df.drop(columns=[column])

print(df)

# Save the DataFrame to an Excel file
df.to_excel('westpac_pdfs_with_names.xlsx', index=False)

# Function to download PDF
def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

# Create a directory for PDFs if it doesn't exist
if not os.path.exists('westpac_pdfs'):
    os.makedirs('westpac_pdfs')

# Download all PDFs
for column in df.columns:
    if column.endswith('_link'):
        for url, name in zip(df[column].dropna(), df[column.replace('_link', '_pdf_name')].dropna()):
            if url.startswith('/'):
                url = 'https://www.westpac.com.au' + url
            # Use the PDF name for the filename, replacing spaces with underscores
            filename = os.path.join('westpac_pdfs', name.replace(' ', '_') + '.pdf')
            download_pdf(url, filename)

print("All PDFs have been downloaded.")



# MySQL database connection using SQLAlchemy
# Replace these with your actual database credentials
DATABASE_TYPE = 'mysql'
DBAPI = 'pymysql'
HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'wespac_db'
PORT = 3306

# Create a connection string
connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

# Store the DataFrame in MySQL
df.to_sql('westpac_pdfs', engine, if_exists='replace', index=False)

print("DataFrame has been stored in MySQL database.")