from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def get_price_hatoorki(url , wine_name) :
    url += wine_name

    # Initialize the WebDriver
    driver = webdriver.Chrome()

    try :
        # Navigate to the URL
        driver.get(url)
        time.sleep(2)
        # Assuming your HTML content is stored in the variable html_content
        html_content = driver.page_source
        # Parse the HTML content
        soup = BeautifulSoup(html_content , 'html.parser')

        # Find the first appearance of the div with class 'm-product-item'
        product_div = soup.find('div' , class_='m-product-item')

        if product_div :
            # Find the div with class 'ml-8 flex flex-1 flex-col mr-2 pt-4'
            ml_div = product_div.find('div' , class_='ml-8 flex flex-1 flex-col mr-2 pt-4')

            if ml_div :
                # Find the price inside the ml div
                price_div = ml_div.find('div' , class_='prod-price')

                if price_div :
                    # Find the div containing the price
                    price_text_div = price_div.find('div' , class_='font-bold text-blue-dark')

                    if price_text_div :
                        # Extract the price text
                        price_text = price_text_div.text.strip()
                        print("Price:" , price_text)
                    else :
                        print("No price text found in the price div")
                else :
                    print("No price div found in the ml div")

    finally :
        # Close the browser
        driver.quit()


url = "https://www.haturki.com/?s="
wine_name = "יין לבן רקנאטי כרם אודם"
get_price_hatoorki(url,wine_name)
