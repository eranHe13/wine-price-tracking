from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_and_extract(url):
    print("start test")

    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get(url)

    try:
        # Wait for the flashy-popup element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.flashy-popup')))
    except:
        print("Flashy popup not found or timed out.")

    # Write the HTML page to a file
    with open('./paneco.txt', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

    # Quit the WebDriver session
    driver.quit()

    print("HTML page saved to 'paneco.txt'")
    print("Test completed.")

# Example usage
url = 'https://www.paneco.co.il/wine'
search_and_extract(url)
