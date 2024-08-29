from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Setup WebDriver
browser = webdriver.Chrome()

# URL to scrape
# url = "https://www.rnz.co.nz/news/business"
# browser.get(url)
# browser.maximize_window()
# time.sleep(10)  # Allow time for the page to load

# # Find the main container with the topics
# main_container = browser.find_element(By.CLASS_NAME, "o-feature-set__primary")

# # Find all articles within the main container
# articles = main_container.find_elements(By.CLASS_NAME, "o-digest")

# # Initialize a list to hold the scraped data
# data = []

# for article in articles:
#     # Extract the title
#     title_element = article.find_element(By.CLASS_NAME, "o-digest__headline")
#     title = title_element.text
    
#     # Extract the link
#     link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    
#     # Extract the image URL
#     image_url = article.find_element(By.CLASS_NAME, "thumb-container").find_element(By.TAG_NAME, "img").get_attribute("src")
    
#     # Extract the time
#     time_element = article.find_element(By.CLASS_NAME, "o-kicker__time")
#     time_posted = time_element.text
    
#     # Store the data in the list
#     data.append({
#         "title": title,
#         "link": link,
#         "image_url": image_url,
#         "time_posted": time_posted
#     })

# # Print the scraped data
# for item in data:
#     print(f"Title: {item['title']}")
#     print(f"Link: {item['link']}")
#     print(f"Image URL: {item['image_url']}")
#     print(f"Time Posted: {item['time_posted']}")
#     print("-" * 50)

# # Close the browser
# browser.quit()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# # Setup WebDriver
# browser = webdriver.Chrome()

# # URL to scrape
# url = "https://www.rnz.co.nz/news/business"
# browser.get(url)
# browser.maximize_window()
# time.sleep(10)  # Allow time for the page to load

# # Find the main container with the list of articles
# articles = browser.find_elements(By.CLASS_NAME, "o-digest")

# # Initialize a list to hold the scraped data
# data = []

# for article in articles:
#     # Extract the title
#     title_element = article.find_element(By.CLASS_NAME, "o-digest__headline")
#     title = title_element.text
    
#     # Extract the link
#     link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    
#     # Extract the image URL
#     image_container = article.find_element(By.CLASS_NAME, "thumb-container")
#     image_url = image_container.find_element(By.TAG_NAME, "img").get_attribute("src")
    
#     # Extract the time
#     time_element = article.find_element(By.CLASS_NAME, "o-kicker__time")
#     time_posted = time_element.text
    
#     # Store the data in the list
#     data.append({
#         "title": title,
#         "link": link,
#         "image_url": image_url,
#         "time_posted": time_posted
#     })

# # Print the scraped data
# for item in data:
#     print(f"Title: {item['title']}")
#     print(f"Link: {item['link']}")
#     print(f"Image URL: {item['image_url']}")
#     print(f"Time Posted: {item['time_posted']}")
#     print("-" * 50)

# # Close the browser
# browser.quit()


# import os
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# # Setup WebDriver
# browser = webdriver.Chrome()

# # URL to scrape
# url = "https://www.rnz.co.nz/news/business"
# browser.get(url)
# browser.maximize_window()
# time.sleep(10)  # Allow time for the page to load

# # Find the main container with the list of articles
# articles = browser.find_elements(By.CLASS_NAME, "o-digest")

# # Initialize a list to hold the scraped data
# data = []

# # Specify the folder to save the images
# image_folder = "downloaded_images"
# os.makedirs(image_folder, exist_ok=True)

# for idx, article in enumerate(articles):
#     # Extract the title
#     title_element = article.find_element(By.CLASS_NAME, "o-digest__headline")
#     title = title_element.text
    
#     # Extract the link
#     link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    
#     # Extract the image URL
#     image_container = article.find_element(By.CLASS_NAME, "thumb-container")
#     image_url = image_container.find_element(By.TAG_NAME, "img").get_attribute("src")
    
#     # Extract the time
#     time_element = article.find_element(By.CLASS_NAME, "o-kicker__time")
#     time_posted = time_element.text
    
#     # Store the data in the list
#     data.append({
#         "title": title,
#         "link": link,
#         "image_url": image_url,
#         "time_posted": time_posted
#     })

#     # Download the image and save it to the specified folder
#     image_data = requests.get(image_url).content
#     image_name = f"image_{idx + 1}.jpg"
#     image_path = os.path.join(image_folder, image_name)
#     with open(image_path, 'wb') as file:
#         file.write(image_data)

#     print(f"Downloaded {image_name}")

# # Print the scraped data
# for item in data:
#     print(f"Title: {item['title']}")
#     print(f"Link: {item['link']}")
#     print(f"Image URL: {item['image_url']}")
#     print(f"Time Posted: {item['time_posted']}")
#     print("-" * 50)

# # Close the browser
# browser.quit()




import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdfkit

# Setup WebDriver
browser = webdriver.Chrome()

# URL to scrape
url = "https://www.rnz.co.nz/news/business"
browser.get(url)
browser.maximize_window()
time.sleep(10)  # Allow time for the page to load

# Create folders to save images and PDFs
image_folder = "rnz_business_images"
pdf_folder = "rnz_business_pdfs"

os.makedirs(image_folder, exist_ok=True)
os.makedirs(pdf_folder, exist_ok=True)

# Find the main containers with the topics
main_containers = [
    browser.find_element(By.CLASS_NAME, "content__primary"),
    browser.find_element(By.CLASS_NAME, "o-feature-set__primary")
]

# Initialize a list to hold the scraped data
data = []

for container in main_containers:
    # Find all articles within the main container
    articles = container.find_elements(By.CLASS_NAME, "o-digest")

    for idx, article in enumerate(articles):
        # Extract the title
        title_element = article.find_element(By.CLASS_NAME, "o-digest__headline")
        title = title_element.text
        
        # Extract the link
        link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        # Extract the image URL
        image_url = article.find_element(By.CLASS_NAME, "thumb-container").find_element(By.TAG_NAME, "img").get_attribute("src")
        
        # Extract the time
        time_element = article.find_element(By.CLASS_NAME, "o-kicker__time")
        time_posted = time_element.text
        
        # Store the data in the list
        data.append({
            "title": title,
            "link": link,
            "image_url": image_url,
            "time_posted": time_posted
        })
        
        # Download the image
        image_name = f"image_{len(data)}.jpg"
        image_path = os.path.join(image_folder, image_name)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download image {image_name}. Status code:", response.status_code)
        
        # If wkhtmltopdf is not in PATH, specify the full path
        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

        # Save the page as a PDF
        pdf_name = f"article_{len(data)}.pdf"
        pdf_path = os.path.join(pdf_folder, pdf_name)
        pdfkit.from_url(link, pdf_path, configuration=config)
        print(f"Saved {pdf_name}")

# Close the browser
browser.quit()

# Print the scraped data
for item in data:
    print(f"Title: {item['title']}")
    print(f"Link: {item['link']}")
    print(f"Image URL: {item['image_url']}")
    print(f"Time Posted: {item['time_posted']}")
    print("-" * 50)

