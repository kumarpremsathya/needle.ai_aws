import time
import docx
import requests
import pdf2docx
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome()

url = "https://www.pfrda.org.in"


# PDF and Word file paths
pdf_path = r'C:\Users\Premkumar.8265\Desktop\Pfrda_aggregators-demo\Pfrda_aggregators-demo\Aggregaters_PFRDA\Aggregators_PFRDA.pdf'

word_output_path = 'converted_word_document.docx'


def convert_pdf_to_word(pdf_path, output_path):
    pdf2docx.parse(pdf_path, output_path)


def extract_tables_from_docx(docx_path):
    doc = docx.Document(docx_path)
    tables = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text.strip())
            table_data.append(row_data)
        tables.append(pd.DataFrame(table_data))
    return tables


def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("PDF file downloaded successfully!")
    else:
        print("Failed to download PDF file. Status code:", response.status_code)


browser.get(url)
browser.maximize_window()

close = browser.find_element(By.ID, "close_modal")
time.sleep(2)
close.click()


intermediaries = browser.find_element(By.XPATH, "//a[@title='Intermediaries']")
ActionChains(browser).move_to_element(intermediaries).perform()
time.sleep(2)

Aggregators = browser.find_element(By.XPATH, "//a[@title='Aggregators']")
ActionChains(browser).move_to_element(Aggregators).perform()
time.sleep(2)

List_Aggregators = browser.find_element(By.XPATH, "//a[@title='List of Registered Aggregators ']")
List_Aggregators.click()
time.sleep(2)


List_Aggregators_pdf = browser.find_element(By.XPATH, "//*[@id='cmscontent']/ul/li/a")
time.sleep(2)
link = List_Aggregators_pdf.get_attribute('href')
List_Aggregators_pdf.click()
time.sleep(2)


# pdf_url = "https://www.pfrda.org.in/myauth/admin/showimg.cshtml?ID=2803"
pdf_filename = 'Aggregators_PFRDA.pdf'
time.sleep(10)
download_pdf(link, pdf_filename)


# Convert PDF to Word
convert_pdf_to_word(pdf_path, word_output_path)

# Extract tables from Word
tables = extract_tables_from_docx(word_output_path)
# Concatenate tables into a single DataFrame
combined_df = pd.concat(tables, ignore_index=True)

# Save the combined DataFrame to an Excel file
excel_path = 'final_excel_sheet.xlsx'
combined_df.to_excel(excel_path, index=False)

print("Excel file has been created successfully.")
