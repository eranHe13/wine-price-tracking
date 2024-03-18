import crud_api 
import scraping_script 

DATABASE_PATH = "..\\data\\pricetracking.db"


def update_prices():
   wine_list = crud_api.get_all_products()
   wines = {}
   for wine in wine_list:
      print(f"----    {wine} ")
      wine_data = scraping_script.get_prices(wine[1])
      wines[wine[1]] = [wine[0] ,wine[1] ,  wine_data["prices"]]
   for wine in wines:
      crud_api.update_products(wines[wine][0] , wines[wine][1],wines[wine][2])
      
   
def main():
   update_prices()
main()




