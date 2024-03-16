from concurrent.futures import ThreadPoolExecutor, as_completed
import scraping.derech_hyin as derech_hyin
import scraping.haturki as haturki
import scraping.paneco as paneco

import crud_api as data_api

# openai.api_key = "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"

def scrape_price(source, wine_name):
    # Function to scrape price from a given source
    return source.scrape(wine_name)


def get_prices(wine_name) :
    # Scrape prices and image links from multiple sources concurrently
    with ThreadPoolExecutor() as executor :
        # Submit scraping tasks for each source
        futures = [executor.submit(scrape_price , source , wine_name) for source in [paneco , haturki , derech_hyin]]
        # Retrieve results as they become available
        dict_results = {source.__name__ : future.result() for source , future in
                        zip([paneco , haturki , derech_hyin] , futures)}

    # Extract prices from each source
    prices = {
        "derech_hyin" : dict_results.get("scraping.derech_hyin" ,
                                         {"regular_price" : None , "club_price" : None , "sale_price" : None}) ,
        "paneco" : dict_results.get("scraping.paneco" ,
                                    {"regular_price" : None , "club_price" : None , "sale_price" : None}) ,
        "haturki" : dict_results.get("scraping.haturki" ,
                                     {"regular_price" : None , "club_price" : None , "sale_price" : None})
    }
    ############################ for printing ###################################
    # Extract image link from paneco source
    image_links = {
        "derech_hyin" : dict_results.get("scraping.derech_hyin" , {}).get("image_url" , None) ,
        "paneco" : dict_results.get("scraping.paneco" , {}).get("image_url" , None) ,
        "haturki" : dict_results.get("scraping.haturki" , {}).get("image_url" , None)
    }

    # Extract URLs from each source
    urls = {
        "derech_hyin" : dict_results.get("scraping.derech_hyin" , {}).get("url" , None) ,
        "paneco" : dict_results.get("scraping.paneco" , {}).get("url" , None) ,
        "haturki" : dict_results.get("scraping.haturki" , {}).get("url" , None)
    }

    # Create wine dictionary
    wine = {
        "name" : wine_name ,
        "prices" : prices ,
        "image_links" : image_links ,
        "urls" : urls
    }

    # Print wine details
    print("Wine Name:" , wine_name)
    print("Prices:")
    for source , price in prices.items() :
        print(
            f"- {source.capitalize()} Price: {price['regular_price']}, Club Price: {price['club_price']}, Sale Price: {price['sale_price']}")
    print("Image Links:")
    for source , link in image_links.items() :
        print(f"- {source.capitalize()}: {link}")
    print("URLs:")
    for source , url in urls.items() :
        print(f"- {source.capitalize()}: {url}")
    ############################ end printing ###################################

    return dict_results


# def get_details(prompt , model="gpt-3.5-turbo"):
#     response = openai.Completion.create(
#         engine="text-davinci-004",  # Or another model name
#         prompt=prompt,
#         temperature=0.7,
#         max_tokens=60,
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=0.0
#         )
#
#     print(response.choices[0].text.strip())
#
    
    
#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
def main():
    wine_name = "תשבי מלבק "
    promot = '''
    עם התבנית הזאת - תן לי מידע על היין {wine_name} , כל קטגוריה מהתבנית אמורה להיות שורה 
הרכב זני: 
אזור גידול: 
על היין: 
'''
    get_prices(wine_name)
    # print(get_details(promot))
main()