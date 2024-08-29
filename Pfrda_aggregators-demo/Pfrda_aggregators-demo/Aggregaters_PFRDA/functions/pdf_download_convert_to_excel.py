import sys
import time
import docx
import shutil
import pdf2docx
import traceback
import requests
import pandas as pd
from datetime import datetime
from config import pop_config
from selenium.webdriver.common.by import By
from functions import check_increment_data, get_data_count_database, log, send_mail
from selenium.webdriver.common.action_chains import ActionChains

browser = pop_config.browser
url = pop_config.url
current_date = datetime.now().strftime("%Y-%m-%d")
cursor = pop_config.cursor


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


def download_pdf(pdf_url, filename):
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("PDF file downloaded successfully!")
        else:
            print("Failed to download PDF file. Status code:", response.status_code)
    except Exception as e:
        traceback.print_exc()
        pop_config.log_list[0] = "Failure"
        pop_config.log_list[4] = get_data_count_database.get_data_count_database(cursor)
        pop_config.log_list[5] = "Failed to download PDF file"
        log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        send_mail.send_email("PFRDA aggregators script error", e)
        pop_config.log_list = [None] * 8
        sys.exit()


def navigate_to_the_page():

    try:
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
        time.sleep(2)

        pdf_filename = f'Aggregators_PFRDA{current_date}.pdf'

        if link:
            List_Aggregators_pdf.click()
            time.sleep(10)
            download_pdf(link, pdf_filename)
        else:
            # redirected_url = browser.current_url # using browser.current_url to get link
            link = "https://www.pfrda.org.in/myauth/admin/showimg.cshtml?ID=2086"  # third way direct link
            List_Aggregators_pdf.click()
            time.sleep(10)
            download_pdf(link, pdf_filename)

        source_path = fr"C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA\{pdf_filename}"
        destination_path = r'C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA\data\pdf'
        shutil.move(source_path, destination_path)

        # PDF and Word file paths
        pdf_path = fr"C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA\data\pdf\{pdf_filename}"
        word_name = f'converted_word_document{current_date}.docx'
        word_output_path = fr"C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA\data\word\{word_name}"

        # Convert PDF to Word
        convert_pdf_to_word(pdf_path, word_output_path)

        # Extract tables from Word
        tables = extract_tables_from_docx(word_output_path)
        # Concatenate tables into a single DataFrame
        combined_df = pd.concat(tables, ignore_index=True)

        # Define the text values to remove
        text_to_remove = ["S.No", "Name of POP", "Registration No.", "Issued on", "Activity Registered for"]

        # Filter rows based on the absence of text_to_remove in any cell
        filtered_df = combined_df[~combined_df.apply(lambda row: row.astype(str).str.contains('|'.join(text_to_remove)).any(), axis=1)]

        # Reset index after removing rows
        filtered_df = filtered_df.reset_index(drop=True)

        # Save the filtered DataFrame to an Excel file
        excel_file_name = f"first_excel_sheet{current_date}.xlsx"
        excel_path = fr'C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA\data\first_excel_sheet\{excel_file_name}'
        filtered_df.to_excel(excel_path, index=False)

        print("Excel file has been created successfully.")

        check_increment_data.check_increment_data(excel_path)

    except Exception as e:
        traceback.print_exc()
        pop_config.log_list[1] = "Failure"
        pop_config.log_list[4] = get_data_count_database.get_data_count_database(cursor)
        pop_config.log_list[5] = "Failed to download PDF file"
        log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        send_mail.send_email("PFRDA aggregators script error", e)
        pop_config.log_list = [None] * 8
        sys.exit()
