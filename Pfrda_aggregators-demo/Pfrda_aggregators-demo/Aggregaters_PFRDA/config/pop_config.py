from selenium import webdriver
import mysql.connector

source_status = "Active"

download_folder = r"C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})

browser = webdriver.Chrome(options=chrome_options)

url = "https://www.pfrda.org.in"

log_list = [None] * 10
no_data_avaliable = 0
no_data_scraped = 0
deleted_sources = ""
deleted_source_count = 0
source_name = "pfrda_aggregators"

host = 'localhost'
user = 'root'
password = 'root'
database = 'pfrda'
auth_plugin = 'mysql_native_password'


connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    auth_plugin=auth_plugin
)

cursor = connection.cursor()
