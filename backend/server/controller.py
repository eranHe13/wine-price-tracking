import crud_api 
import scraping_script 
import ast 
DATABASE_PATH = "..\\data\\pricetracking.db"
from product import Product


def update_prices():
   wine_list = crud_api.get_all_products()
   products = {}
   for wine in wine_list:
      wine_data = scraping_script.get_prices(wine[1])
      products[wine[0]] = Product(wine[0] ,wine[1] ,  wine_data["prices"])
   for p in products:
      print(f"{products[p].id} , {products[p].name } ----> {products[p].min_price()}")
   # for product in products:
   #   crud_api.update_products(product , products[product].name ,products[product].prices)
      
   return products
   
def check_user_prices(products):
   
   users_products = crud_api.get_user_product_alerts()
   users_products_set = {}
   for d in users_products:
      if d[1] in users_products_set:
         users_products_set[d[1]].append((d[2], d[3]))
      else:
         users_products_set[d[1]] = [(d[2], d[3])]
   print(users_products_set)
   
   for user_id in users_products_set:
      for product_alert in users_products_set[user_id]:
         product_id   = product_alert[0]
         user_price = product_alert[1]
         store , min_price  = products[product_id].min_price()
         print(f"product_id {product_id} ,  user_price  {user_price} ,   min_price  {min_price} , store  {store}")

         if (min_price <= user_price) :
            print(f"USER - {user_id} the wine  {products[product_id].name} with the price -- {min_price} is selling in {store} the price is lower then users\n ")
      
         else:
            print(f"NONE----")
   
      

def main(): 
   
   products = update_prices()
   check_user_prices(products)
main()




