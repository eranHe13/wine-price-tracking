import crud_api 
import scraping_script 
# import scraping_script
# import sqlite3
DATABASE_PATH = "..\\data\\pricetracking.db"



def update_prices():
   wine_list = crud_api.get_all_products()
   for wine in wine_list:
      tmp = scraping_script.get_prices(wine[1])
      
   print(tmp)
    
def main():
   update_prices()
   
main()




