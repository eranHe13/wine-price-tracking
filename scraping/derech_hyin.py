from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

def exit_from_popup(driver):
    # Function to handle popup by pressing ESC key
    time.sleep(5)  # Wait for the popup to appear
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def scrap(url, query):
    # Function to scrap product details
    
    # Initialize WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Navigate to the URL with the search query
        url += query
        driver.get(url)
        
        # Exit from popup
        exit_from_popup(driver)
        
        # Wait for search results to load and find the first product
        search_element = driver.find_element(By.CLASS_NAME, "thumbnail")
        
        # Extract the outer HTML of the product
        outer_html = driver.execute_script("return arguments[0].outerHTML;", search_element)
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(outer_html, 'html.parser')
        
        # Find the anchor tag within the product
        a = soup.find('a')
        
        # Construct the URL of the product
        product_url = "https://www.wineroute.co.il/Product/" + a['data-product-id']
        
        # Navigate to the product page
        driver.get(product_url)
        
        # Exit from popup
        exit_from_popup(driver)
        
        # Find the price element on the product page
        price = driver.find_element(By.XPATH , "/html/body/div[3]/div/div/div[2]/div/div[3]/div/div[2]/span")
        
        # Extract the outer HTML of the price element
        price_outer_html = driver.execute_script("return arguments[0].outerHTML;", price)
        
        # Parse the price HTML using BeautifulSoup
        price_html = BeautifulSoup(price_outer_html , 'html.parser')
        
        # Print the price HTML (you might want to extract specific information here)
        print("Price HTML: " , price_html)
        
    finally:
        # Close the WebDriver session
        driver.quit()

# Call the scrap function with the search URL and query
scrap('https://www.wineroute.co.il/search?keyword=', 'בוגל אסנשיאל בלנד')
