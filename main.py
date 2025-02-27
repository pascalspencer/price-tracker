# import the required libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv

# set up Chrome options
options = webdriver.ChromeOptions()

# run Chrome in headless mode
options.add_argument("--headless=new")

# install ChromeDriver and set up the driver instance
driver = webdriver.Chrome(
    options=options, service=Service(ChromeDriverManager().install())
)

# specify the target URL
target_url = (
    "https://www.amazon.com/Logitech-G502-Performance-Gaming-Mouse/dp/B07GBZ4Q68/"
)

# visit the target URL
driver.get(target_url)

# extract the product name
product_name = driver.find_element(By.ID, "title").text

# find the price element with JavaScript's querySelector
price_element = driver.execute_script(
    'return document.querySelector(".a-price.a-text-price span.a-offscreen")'
)

# get the text of the listing price
price = driver.execute_script("return arguments[0].textContent", price_element)

# extract the description list
description_list = driver.find_element(
    By.CSS_SELECTOR, "ul.a-unordered-list.a-vertical.a-spacing-mini"
)

# find all list items within the description list
description_items = description_list.find_elements(By.TAG_NAME, "li")

# create an empty list to collect the descriptions
description_data = []

# collect and store all product description texts
for item in description_items:
    # get the text content of the span within the li
    description_text = item.find_element(By.TAG_NAME, "span").text.strip()
    description_data.append(description_text)

# extract the rating score
ratings = driver.find_element(By.ID, "acrPopover").text

# select the div element containing the featured image
image_element = driver.find_element(By.ID, "imgTagWrapperId")

# scrape the image tag from its parent div
product_image = image_element.find_element(By.TAG_NAME, "img")

# get the image src attribute
product_image_url = product_image.get_attribute("src")

# create a dictionary to store scraped product data
data = {
    "Name": product_name,
    "Price": price,
    "Description": description_data,
    "Rating": ratings,
    "Featured Image": product_image_url,
}

# define the CSV file name for storing scraped data
csv_file = "product.csv"

# open the CSV file in write mode with proper encoding
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    # create a CSV writer object
    writer = csv.writer(file)

    # write the header row to the CSV file
    writer.writerow(data.keys())

    # write the data row to the CSV file
    writer.writerow(data.values())

# print a confirmation message after successful data extraction and storage
print("Scraping completed and data written to CSV")

# quit the driver instance
driver.quit()
