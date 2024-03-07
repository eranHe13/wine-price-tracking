import scraping.derech_hyin as derech_hyin
import scraping.haturki as haturki
import scraping.paneco as paneco
import crud_api as data_api

def get_prices(wine_name ):
    paneco_price = paneco.scrape(wine_name)
    haturki_price = haturki.scrape(wine_name)
    derech_hyin_price = derech_hyin.scrape(wine_name)
    print(f"paneco_price: {paneco_price}")
    print(f"haturki_price: {haturki_price}")
    print(f"derech_hyin_price: {derech_hyin_price}")
    return([derech_hyin_price,paneco_price,haturki_price])



