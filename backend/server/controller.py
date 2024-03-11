import crud_api 
import scraping_script


def updatePrices():
    products_list = crud_api.get_all_products();
    list = {}
    for i , name in enumerate(products_list):
        data = scraping_script.get_prices(name[0])
        list[name] = data
        
    
    for l in list:
        print(l , " ---------> ",list[l])


def test():
    email = "wine@gmail.com"
    password = "123456"
    print(crud_api.get_user_login_details(email,password))

def main():
    test()
    
    # get prices
    # insert data with name to table 
    
    
    
    

main()