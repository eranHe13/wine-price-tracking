from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def exit_from_popup(driver):
    # Function to handle popup by pressing ESC key
    time.sleep(5)  # Wait for the popup to appear
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def search_and_extract(url, name):
    print("start test")
    url+=name
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get(url)

    # Find the first <li> element with class "item product product-item"
    first_product = driver.find_element(By.CSS_SELECTOR , "li.item.product.product-item")

    try :
        # Find the span element with class 'price-container' for the discount price
        price_container = first_product.find_element(By.CSS_SELECTOR,
                                                     "span.price-container.price-register_price.tax.weee.rewards_earn")
    except NoSuchElementException :
        # If discount price container not found, try finding it for the final price
        try :
            price_container = first_product.find_element(By.CSS_SELECTOR ,
                                                         "span.price-container.price-final_price.tax.weee.rewards_earn")
        except NoSuchElementException :
            # If neither discount nor final price containers found, raise an error or handle as required
            print("Price container not found")

    # Print the price
    try :
        price_span = price_container.find_element(By.CSS_SELECTOR , "span[data-price-amount]")
        price = price_span.get_attribute("data-price-amount")
        print("Price:" , price)
    except NoSuchElementException :
        print("Price not found")


    # Close the WebDriver
    driver.quit()


    print("HTML page saved to 'paneco.txt'")
    print("Test completed.")

# Example usage
url = 'https://www.paneco.co.il/catalogsearch/result/?q='
name = 'וודקה חמוציות'
search_and_extract(url, name)
