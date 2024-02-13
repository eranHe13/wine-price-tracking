import requests
from bs4 import BeautifulSoup


def get_product_price(url):
    try:
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # You'll need to update the selector based on the actual page structure
            price_element = soup.find('span', class_='price-class')  # Example selector
            if price_element:
                price = price_element.text.strip()
                return price
            else:
                print("Price element not found.")
                return None
        else:
            print(f"Failed to retrieve the web page: Status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching the web page: {e}")
        return None
