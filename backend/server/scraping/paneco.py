from bs4 import BeautifulSoup
from selenium import webdriver
import re

def scrape(name):
    url = 'https://www.paneco.co.il/catalogsearch/result/?q='
    url += name

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    driver.get(url)
    try :
        # Assuming your HTML content is stored in the variable html_content
        html_content = driver.page_source
        # Parse the HTML content
        soup = BeautifulSoup(html_content , 'html.parser')

        # Extract the wine name
        # Find the element by ID and extract the data-name attribute
        product_details_element = soup.find("div" , class_="product details product-item-details")
        WINE_NAME = product_details_element.contents[1].contents[1].contents[0][2:]
        # Find the span element with the class "product-image-wrapper"
        image_wrapper = soup.find("span" , class_="product-image-wrapper")
        # Get the img tag inside the span element
        image_tag = image_wrapper.find("img")
        # Get the src attribute of the img tag
        WINE_IMG_URL = image_tag["src"]
        # Get the url to the product
        url_product = product_details_element.contents[1].contents[1].attrs['href']


        # Get the price
        try:
            reg_price_text = product_details_element.contents[len(product_details_element.contents)-6].contents[0].contents[1].contents[1].contents[0].text
            REGULAR_PRICE = float(re.search(r'(\d+\.\d+)' , reg_price_text).group(1))
        except:
            REGULAR_PRICE = 0
        try:
            club_price_text = product_details_element.contents[len(product_details_element.contents)-6].contents[2].contents[1].contents[3].contents[0].contents[0].text
            CLUB_PRICE = float(re.search(r'(\d+\.\d+)' , club_price_text).group(1))
        except:
            CLUB_PRICE = 0
        try :
            # Find the SALE_PRICE element using soup
            product_sale_element = soup.find("div" , class_="product details product-item-details")
            sale_price_lst  = product_sale_element.contents[len(product_details_element.contents)-4].contents[1].contents[0]
            numbers_only = re.findall(r'\d+' , sale_price_lst)
            numbers_only = [float(num) for num in numbers_only]
            SALE_PRICE = [numbers_only[0] , numbers_only[-1]]
            SALE_PRICE.append(SALE_PRICE[1] / SALE_PRICE[0])
        except:
            print("Sale price not found")
            SALE_PRICE = []

    except Exception as e :
        driver.quit()
        WINE_NAME = ""
        WINE_IMG_URL = ""
        url_product = ""
        REGULAR_PRICE = 0
        CLUB_PRICE = 0
        SALE_PRICE = 0

    # Close the WebDriver
    driver.quit()

    wine = {
        "id" : None ,
        "name" : WINE_NAME ,
        "regular_price" : REGULAR_PRICE ,
        "club_price" : CLUB_PRICE ,
        "sale_price" : SALE_PRICE ,
        "url" : url_product ,
        "image_url" : WINE_IMG_URL
    }
    driver.quit()
    return wine







