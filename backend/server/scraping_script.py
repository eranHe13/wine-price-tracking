from concurrent.futures import ThreadPoolExecutor, as_completed
import scraping.derech_hyin as derech_hyin
import scraping.haturki as haturki
import scraping.paneco as paneco
import crud_api as data_api

def scrape_price(source, wine_name):
    # Function to scrape price from a given source
    return source.scrape(wine_name)

def get_prices(wine_name):
    # Scrape prices and image links from multiple sources concurrently
    with ThreadPoolExecutor() as executor:
        # Submit scraping tasks for each source
        futures = [executor.submit(scrape_price, source, wine_name) for source in [paneco, haturki, derech_hyin]]
        # Retrieve results as they become available
        dict_results = {source.__name__: future.result() for source, future in zip([paneco, haturki, derech_hyin], futures)}
    print(dict_results)
    prices = [dict_results["scraping.derech_hyin"], dict_results["scraping.paneco"][0], dict_results["scraping.haturki"]]
    image_link = dict_results["scraping.paneco"][1]  # Only Paneco returns an image link

    return prices, image_link