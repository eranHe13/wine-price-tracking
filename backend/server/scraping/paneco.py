from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException

def scrape(name):
    url = 'https://www.paneco.co.il/catalogsearch/result/?q='
    url += name

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    driver.get(url)

    try:
        # Find the first <li> element with class "item product product-item"
        first_product = driver.find_element(By.CSS_SELECTOR, "li.item.product.product-item")

        # Get the image link
        try:
            image_element = first_product.find_element(By.CSS_SELECTOR, "img.product-image-photo")
            image_link = image_element.get_attribute("src")
        except NoSuchElementException:
            print("Image not found")
            image_link = None

        # Find the price container
        try:
            price_container = first_product.find_element(By.CSS_SELECTOR,
                                                         "span.price-container.price-final_price.tax.weee.rewards_earn")
        except NoSuchElementException:
            print("Price container not found")
            return None

        # Get the price
        try:
            price_span = price_container.find_element(By.CSS_SELECTOR, "span[data-price-amount]")
            price = price_span.get_attribute("data-price-amount")
        except NoSuchElementException:
            print("Price not found")
            return None

        # Close the WebDriver
        driver.quit()

        return price, image_link

    except NoSuchElementException:
        print("Product not found")
        driver.quit()
        return None


