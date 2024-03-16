from concurrent.futures import ThreadPoolExecutor, as_completed
import scraping.derech_hyin as derech_hyin
import scraping.haturki as haturki
import scraping.paneco as paneco
import openai

import crud_api as data_api

openai.api_key = "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"

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
    
    prices = [dict_results["scraping.derech_hyin"], dict_results["scraping.paneco"][0], dict_results["scraping.haturki"]]
    image_link = dict_results["scraping.paneco"][1]  
    wine = {}
    if dict_results["scraping.derech_hyin"]:
        wine = {
            "name": wine_name,
            "price_derech_hyein" : [dict_results["scraping.derech_hyin"]["regular_price"] , dict_results["scraping.derech_hyin"]["club_price"] , dict_results["scraping.derech_hyin"]["sale_price"]],
            "price_paneco": dict_results["scraping.paneco"][0],
            "price_haturki": dict_results["scraping.haturki"],
            "image_link": image_link
        }
    else:
        wine = {
            "name": wine_name,
            "price_derech_hyein" : 0,
            "price_paneco": dict_results["scraping.paneco"][0],
            "price_haturki": dict_results["scraping.haturki"],
            "image_link": image_link
        }    
    for k in wine:
        print(f'{k} : {wine[k]}')
    return prices, image_link


def get_details(prompt , model="gpt-3.5-turbo"):
    response = openai.Completion.create(
        engine="text-davinci-004",  # Or another model name
        prompt=prompt,
        temperature=0.7,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    print(response.choices[0].text.strip())
    
    
    
#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
def main():
    wine_name = "גליל כרם משגב עם 2020"
    promot = '''
    עם התבנית הזאת - תן לי מידע על היין {wine_name} , כל קטגוריה מהתבנית אמורה להיות שורה 
הרכב זני: 
אזור גידול: 
על היין: 
'''
    get_prices(wine_name)
    print(get_details(promot))
main()