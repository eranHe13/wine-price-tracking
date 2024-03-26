from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from .similarity import compute_similarity


def scrape(name):
    # Function to scrape product details
    url_serach = 'https://www.wineroute.co.il/search?keyword=' + name
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url_serach)

    try :
        # SEARCH WINE IN THE SITE IF EXISTS EXTRACT HIS ID
        WINE_ELEMENT  = driver.find_element(By.XPATH ,'/html/body/div[4]/div/div/div[1]/div/div[2]/div')
        WINE_ELEMENT_OH = driver.execute_script("return arguments[0].outerHTML;" , WINE_ELEMENT)
        SOUP = BeautifulSoup(WINE_ELEMENT_OH, 'html.parser')
        WINE_ID_STRING = SOUP.find('a', class_='thumbnail')['data-product-id']
        WINE_NAME = SOUP.find('h3', class_='name').text
        if(compute_similarity(WINE_NAME ,name ) < 0.85):
            raise ValueError

        ## add - check similary of search name and product name if not return None
        

    
    
        # GET WINE PAGE
        url_product = "https://www.wineroute.co.il/Product/" + WINE_ID_STRING
        driver.get(url_product)

        '''
        #DETAILS ABOUT THE WINE
        WINE_DETAILS_ELEMENT = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]")
        WINE_DETAILS_ELEMENT_OH = driver.execute_script("return arguments[0].outerHTML;" , WINE_DETAILS_ELEMENT)
        WINE_DETAILS_SOUP = BeautifulSoup(WINE_DETAILS_ELEMENT_OH, 'html.parser')
        '''

        # GET PRICES REGULAR AND CLUB
        WINE_PRICE = driver.find_element(By.XPATH ,"/html/body/div[3]/div/div/div[2]/div/div[3]/div" )
        WINE_PRICE_ELEMENT_OH = driver.execute_script("return arguments[0].outerHTML;" , WINE_PRICE)
        WINE_PRICE_SOUP = BeautifulSoup(WINE_PRICE_ELEMENT_OH, 'html.parser')
        REGULAR_PRICE = WINE_PRICE_SOUP.find('div', class_='price red').find('span').text.replace("₪", "")
        REGULAR_PRICE = float(REGULAR_PRICE)
        try:
            CLUB_PRICE = WINE_PRICE_SOUP.find('div', class_='price club').find('span').text.replace("₪", "")
            CLUB_PRICE = float(CLUB_PRICE.replace("₪", ""))
        except Exception as e:
            print("Error not founed CLUB_PRICE - " , e)
            CLUB_PRICE = 0

        # GET SALE PRICE
        try:
            SALE_PRICE_ELEM = driver.find_element(By.XPATH ,"/html/body/div[3]/div/div/div[2]/div/div[1]/img" ).get_attribute("alt")
            SALE_PRICE = re.findall(r'\d+\.\d+|\d+', SALE_PRICE_ELEM)
            SALE_PRICE = [float(x) for x in SALE_PRICE]
            SALE_PRICE.append(SALE_PRICE[1] / SALE_PRICE[0])
        except Exception as e:
            print("Error not founed SALE_PRICE - " , e)
            SALE_PRICE = []

        #GET IMAGE URL
        WINE_IMG_ELEM = driver.find_element(By.XPATH ,"/html/body/div[3]/div/div/div[2]/div/div[1]/a/img" )
        WINE_IMG_URL = WINE_IMG_ELEM.get_attribute('src')

    except Exception as e:
        print("Error not founed wine in the site derech_hyin - " , e)
        WINE_ID_STRING = ""
        WINE_NAME = ""
        WINE_IMG_URL = ""
        url_product = ""
        REGULAR_PRICE = 0
        CLUB_PRICE = 0
        SALE_PRICE = 0

    wine = {
        "id": WINE_ID_STRING,
        "name": WINE_NAME,
        "regular_price": REGULAR_PRICE,
        "club_price": CLUB_PRICE,
        "sale_price": SALE_PRICE,
        "url": url_product,
        "image_url":WINE_IMG_URL
    }
    driver.quit()
    return wine




    















































# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import re

# def scrape(name):
#     # Function to scrape product details
#     url = 'https://www.wineroute.co.il/search?keyword='
#     url += name

#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)

#     try :
#         # Find the price element of the first product
#         price_element = driver.find_element(By.XPATH ,'/html/body/div[4]/div/div/div[1]/div/div[2]/div[1]/a/div/div[1]')

#         # Extract the outer HTML of the price element
#         price_outer_html = driver.execute_script("return arguments[0].outerHTML;" , price_element)

#         # Parse the price HTML using BeautifulSoup
#         price_html = BeautifulSoup(price_outer_html , 'html.parser')

#         # Get the text inside the price element
#         price_text = price_html.get_text()

#         # Use regular expression to extract numeric value
#         price_numeric = re.search(r'\d+\.\d+' , price_text).group()

#         # Convert the extracted numeric value to float
#         price_numeric = float(price_numeric)

#         # Close the WebDriver session
#         driver.quit()

#         # Return the price
#         return price_numeric

#     except Exception as e :
#         print("Error while extracting price:" , e)
#         driver.quit()
#         return 0



# def main():
#     scrape("דרך ארץ רוזה")
# main()
    