from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

def scrape(name):
    # Function to scrape product details
    url = 'https://www.wineroute.co.il/search?keyword='
    url += name

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try :
        # Find the price element of the first product
        price_element = driver.find_element(By.XPATH ,
                                            '/html/body/div[4]/div/div/div[1]/div/div[2]/div[1]/a/div/div[1]')

        # Extract the outer HTML of the price element
        price_outer_html = driver.execute_script("return arguments[0].outerHTML;" , price_element)

        # Parse the price HTML using BeautifulSoup
        price_html = BeautifulSoup(price_outer_html , 'html.parser')

        # Get the text inside the price element
        price_text = price_html.get_text()

        # Use regular expression to extract numeric value
        price_numeric = re.search(r'\d+\.\d+' , price_text).group()

        # Convert the extracted numeric value to float
        price_numeric = float(price_numeric)

        # Close the WebDriver session
        driver.quit()

        # Return the price
        return price_numeric

    except Exception as e :
        print("Error while extracting price:" , e)
        driver.quit()
        return None



