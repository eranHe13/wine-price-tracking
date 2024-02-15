from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def search_and_extract(url, search_query): 
    print("start test")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    
    # Navigate to the URL
    driver.get(url)
    
    time.sleep(10)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.flashy-popup')))

    driver.execute_script("document.querySelector('flashy-popup').remove();")

    # Initialize WebDriverWait 
    element = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.sendToBtn")
    driver.execute_script("arguments[0].click();", element)

    # Wait for the search box to be ready and interactable
    time.sleep(5)

    serach_box = driver.find_element(By.XPATH, '//form[@action="/search" and @id="searchform" and @title="חיפוש באתר"]')
    #serach_box = driver.find_element(By.ID , "searchform")
    search_input = serach_box.find_element(By.XPATH, '//input[@class="form-control" and @name="keyword" and @placeholder="חיפוש" and @title="חיפוש כללי באתר" and @type="text"]')

    print("serach_box" , serach_box.get_attribute('innerHTML'))
    print("\nsearch_input" , search_input.get_attribute('innerHTML'))
    
    
    #search_input = serach_box.find_element(By.CLASS_NAME, "form-control")
    # time.sleep(5)
    # # Send the search query
    # search_input.send_keys(search_query)
    # time.sleep(5)
    # search_input.send_keys(Keys.ENTER)
    
    # Wait for the submit button to be clickable and then click it
    #submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sm[type="submit"]')
    #submit_button.click()
    
    
    
    # Print the HTML of the current page
    #print(driver.page_source)
    
    # Clean up
    driver.quit()
    
    print("test end")

# Example usage
url = 'https://www.wineroute.co.il/?gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgTZOKorQDjqnvDBqZf0KzJXeB0R0KbolJ98jBp8IOFJd-CmXyuOLMcaAqQmEALw_wcB'
search_query = "alon"
search_and_extract(url, search_query)
