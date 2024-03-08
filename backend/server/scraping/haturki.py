from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time


def scrape(wine_name) :
    url = "https://www.haturki.com/?s="

    url += wine_name

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)


    # Navigate to the URL
    driver.get(url)
    time.sleep(2)
    # Assuming your HTML content is stored in the variable html_content
    html_content = driver.page_source
    # Parse the HTML content
    soup = BeautifulSoup(html_content , 'html.parser')
    # Find the first prod-price class inside the body divider
    prod_price_element = soup.select_one("body div.prod-price")

    # Find the first span element inside the prod-price div
    first_span_element = prod_price_element.find("span")

    # Extract the price value from the text inside the span element
    price_value = first_span_element.nextSibling.strip()

    # Close the WebDriver
    driver.quit()

    return price_value

