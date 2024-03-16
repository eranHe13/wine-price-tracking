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
    try:
        # Assuming your HTML content is stored in the variable html_content
        html_content = driver.page_source
        # Parse the HTML content
        soup = BeautifulSoup(html_content , 'html.parser')

        # Extract the wine name
        wine_name_element = soup.select_one("#pageCategory section:nth-of-type(3) div:nth-of-type(1) a h2")
        WINE_NAME = wine_name_element.get_text(strip=True) if wine_name_element else None

        # Extract the image URL
        image_element = soup.select_one(
            "#pageCategory section:nth-of-type(3) div:nth-of-type(1) a div:nth-of-type(3) div img")
        WINE_IMG_URL = image_element.get("src") if image_element else None
        # Find the <a> element within the specified <div> class
        product_link_element = soup.find('div' , class_='m-product-item').find('a')
        # Extract the href attribute to get the URL
        url_product = "https://www.haturki.com"+product_link_element['href']

        # Find the first prod-price class inside the body divider
        prod_price_element = soup.select_one("body div.prod-price")
        try: # discount price
            # Find the first span element inside the prod-price div
            first_span_element = prod_price_element.find("span")
            # Extract the price value from the text inside the span element
            CLUB_PRICE = float(first_span_element.nextSibling.strip())
        except Exception as e :
            CLUB_PRICE = None
        try: # regular price
            # Extract the regular price using the provided XPath
            REGULAR_PRICE = prod_price_element.contents[0].contents[1].contents[0]
        except Exception as e :
            REGULAR_PRICE = 0
        try: # Sale price
            sale_price_element = prod_price_element.parent.contents[2]
            sale_price_tag = sale_price_element.contents[0]
            sale_price_lst = sale_price_tag.contents[0]
            numbers_only = re.findall(r'\d+' , sale_price_lst)
            numbers_only = [float(num) for num in numbers_only]
            SALE_PRICE = [numbers_only[0], numbers_only[-1]]
            SALE_PRICE.append(SALE_PRICE[1]/SALE_PRICE[0])

        except Exception as e :
            SALE_PRICE = []

    except Exception as e :
        driver.quit()
        WINE_NAME = ""
        WINE_IMG_URL = ""
        url_product = ""
        REGULAR_PRICE = 0
        CLUB_PRICE = 0
        SALE_PRICE = 0

    wine = {
        "id" : None ,
        "name" : WINE_NAME ,
        "regular_price" : REGULAR_PRICE ,
        "club_price" : CLUB_PRICE ,
        "sale_price" : SALE_PRICE,
        "url" : url_product ,
        "image_url" : WINE_IMG_URL
    }
    # Close the WebDriver
    driver.quit()

    return wine

