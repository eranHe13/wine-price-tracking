import crud_api 
import scraping_script 
import ast 
DATABASE_PATH = "..\\data\\pricetracking.db"
from product import Product
import mail_sender


def update_prices():
   wine_list = crud_api.get_all_products()
   products = {}
   for wine in wine_list:
      wine_data = scraping_script.get_prices(wine[1])
      products[wine[0]] = Product(wine[0] ,wine[1] ,  wine_data["prices"])
   # for p in products:
   #    print(f"{products[p].id} , {products[p].name } ----> {products[p].min_price()}")
   for product in products:
     crud_api.update_products(product , products[product].name ,products[product].prices)
      
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
         #print(f"product_id {product_id} ,  user_price  {user_price} ,   min_price  {min_price} , store  {store}")

         if (min_price <= user_price) :
            mail_data = f"USER - {user_id} the wine  {products[product_id].name} with the price -- {min_price} is selling in {store} the price is lower then users\n "
            user_email = crud_api.get_user_email(user_id)
            #print(f"USER - {user_id} the wine  {products[product_id].name} with the price -- {min_price} is selling in {store} the price is lower then users\n ")
            mail_sender.email_controller(user_email , mail_data)
         else:
            print(f"NONE----")

def test_email_controller():
   users_products = crud_api.get_user_product_alerts()
   users_products_set = {}
   for d in users_products:
      if d[1] in users_products_set:
         users_products_set[d[1]].append((d[2], d[3]))
      else:
         users_products_set[d[1]] = [(d[2], d[3])]
   print(users_products_set)
   product_data = crud_api.get_all_products_test()
   products = {}
   for p in product_data:
      prices = {"derech":{"regular_price":p[6],"club_price":p[7],"sale_price":p[8]} ,
                "haturky":{"regular_price":p[9],"club_price":p[10],"sale_price":p[11]} ,
                "paneco":{"regular_price":p[12],"club_price":p[13],"sale_price":p[14]}} 
      products[p[0]] = Product(p[0], p[1],prices )   
   for user_id in users_products_set:
      for product_alert in users_products_set[user_id]:
         product_id   = product_alert[0]
         user_price = product_alert[1]
         store , min_price  = products[product_id].min_price()

         if (min_price <= user_price) :
            mail_data = f"USER - {user_id} the wine  {products[product_id].name} with the price -- {min_price} is selling in {store} the price is lower then your price\n "
            user_email = crud_api.get_user_email(user_id)[0][0]
            print(user_email)
            print(mail_data)
            mail_sender.email_controller(user_email , mail_data)


def main(): 
   test_email_controller()
   #print(crud_api.get_user_email("14"))
   #products = update_prices()
   #check_user_prices(products)
main()



#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
