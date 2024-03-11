import crud_api 
import scraping_script
import sqlite3
DATABASE_PATH = "..\\data\\pricetracking.db"

def updatePrices():
    products_list = crud_api.get_all_products();
    list = {}
    for i , name in enumerate(products_list):
        data = scraping_script.get_prices(name[0])
        list[name] = data
        
    
    for l in list:
        print(l , " ---------> ",list[l])
    
    





