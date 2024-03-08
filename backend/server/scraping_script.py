from concurrent.futures import ThreadPoolExecutor, as_completed
import scraping.derech_hyin as derech_hyin
import scraping.haturki as haturki
import scraping.paneco as paneco
import crud_api as data_api

def scrape_price(source, wine_name):
    # Function to scrape price from a given source
    return source.scrape(wine_name)

def get_prices(wine_name):
    # Scrape prices from multiple sources concurrently
    with ThreadPoolExecutor() as executor:
        # Submit scraping tasks for each source
        futures = [executor.submit(scrape_price, source, wine_name) for source in [paneco, haturki, derech_hyin]]
        # Retrieve results as they become available
        prices = {source.__name__: future.result() for source, future in zip([paneco, haturki, derech_hyin], futures)}

    # Print and return prices
    for source, price in prices.items():
        print(f"{source}: {price}")
    return prices

