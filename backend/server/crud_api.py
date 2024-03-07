import sqlite3
import bcrypt  # for password hashing
import datetime
from contextlib import closing
import scraping_script

DATABASE_PATH = "..\\data\\pricetracking.db"

def get_user_login_details(email , password) : 
    print("---------get_user_login_details fucntion-----------\ninput --> " , email , password)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try :
        cursor.execute("SELECT * FROM users WHERE users.email=? and users.password=?" , (email,password ))
        user = cursor.fetchone()
        if user :
            print("user found in db " ,user)
            return user
        else:
            return None 
    except sqlite3.Error as e :
        print("Error User Not Found In DB: " , e)
        return None
    finally :
        conn.close()
        print("EXIT FROM get_user_login_details fucntion")
    
def get_user_wine_list(user_id):
    print("---------get_user_wine_list fucntion-----------\ninput --> " , user_id )
    conn = sqlite3.connect(DATABASE_PATH)  
    cursor = conn.cursor()
    try :
        cursor.execute("SELECT product_id FROM user_product_alerts WHERE user_product_alerts.user_id =? " , (str(user_id),))
        products_id = cursor.fetchall()
        print("products_id---> " , products_id)
        if products_id  : 
            numbers_list = [item[0] for item in products_id]
            questions_marks = ','.join("?" for _ in numbers_list)
            query = f"SELECT * FROM price_history WHERE price_history.id IN ({questions_marks})"
            cursor.execute(query , numbers_list)
            products = cursor.fetchall()
            return products
        else :
            return None
        
        
    except sqlite3.Error as e :
        print("Error User Wines Not Founds: " , e)
        return None
    finally :
        print("EXIT FROM get_user_login_details fucntion")
        conn.close()

# Function to add a user
def add_user(name, password, email):
    print("---------add_user-----------\ninput --> " , name, password, email )
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        try:
            cursor.execute(sql, (name, password, email))
            conn.commit()
            last_id = cursor.lastrowid
            cursor.execute("SELECT * FROM users WHERE id = ?", (last_id,))
            user = cursor.fetchone()
            print("newUser -- > ", user )
            return user
        except sqlite3.Error as e:
            print(f"add_user error: ({name}, {email})", str(e))
            return "user email exists" 


def add_new_product_for_user(user_id, wine_name, desired_price):
    print("---------add_new_product_for_user-----------\ninput --> ", user_id, ", ", wine_name, ", ", desired_price)
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        try:
            # Check if the wine exists in the price_history table
            cursor.execute("SELECT id FROM price_history WHERE wine_name=?", (wine_name,))
            product = cursor.fetchone()

            if product:
                product_id = product[0]
                print("wine exists in the price_history table", wine_name)
            else:
                # If the wine doesn't exist, scrape the prices
                print("wine *doesnt* exist in the price_history table", wine_name)
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                wine_prices = scraping_script.get_prices(wine_name)
                # Insert scraped prices into the price_history table
                cursor.execute(
                    "INSERT INTO price_history (wine_name, date, price_wine_rout, price_paneco, price_haturki) VALUES (?, ?, ?, ?, ?)",
                    (wine_name, date, wine_prices[0], wine_prices[1], wine_prices[2]))
                conn.commit()
                product_id = cursor.lastrowid  # Get the product ID

            # Add the product ID to the user_product_alerts table
            cursor.execute(
                "INSERT INTO user_product_alerts (user_id, product_id, desired_price) VALUES (?, ?, ?)",
                (user_id, product_id, desired_price))
            conn.commit()
        except sqlite3.Error as e:
            print(f"add_product_alert error: ({wine_name}, {user_id}, {desired_price})", str(e))
        finally:
            print("EXIT FROM add_new_product_for_user function")


################################

'''
def add_new_product_for_user( user_id ,wine_name , desired_price ) :
    print("---------add_new_product_for_user-----------\ninput --> " , user_id ,", ",wine_name ,", ", desired_price )
    with sqlite3.connect(DATABASE_PATH) as conn :
        cursor = conn.cursor()
        try :
            # Check if the wine exists in the price_history table
            cursor.execute("SELECT id FROM price_history WHERE wine_name=?" , (wine_name ,))
            product = cursor.fetchone()

            if product :
                product_id = product[0]
                print("wine exists in the price_history table " , wine_name)
            else :
                # If the wine doesn't exist, scrape the prices
                print("wine *doesnt* exists in the price_history table " , wine_name)
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                wine_prices = scraping_script.get_prices(wine_name)
                # Insert scraped prices into the price_history table
                cursor.execute(
                    "INSERT INTO price_history (wine_name,date, price_wine_rout, price_paneco, price_haturki) VALUES (?, ?, ?, ?,?)" ,
                    (wine_name ,date, wine_prices[0] , wine_prices[1] , wine_prices[2]))
                conn.commit()
                product_id = cursor.lastrowid  # Get the product ID

            # Add the product ID to the user_product_alerts table
            cursor.execute(
                "INSERT INTO user_product_alerts (user_id, product_id, desired_price) VALUES (?, ?, ?)" ,
                (user_id , product_id , desired_price))
            conn.commit()
        except sqlite3.Error as e :
            print(f"add_product_alert error: ({wine_name}, {user_id}, {desired_price})" , str(e))
        finally:
            print("EXIT FROM add_new_product_for_user fucntion")
            conn.close()

'''



'''
# Function to get user by username
def get_user_by_username(username):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            log_error(f"get_user_by_username error: ({username})", str(e))
            return None

# Function to change user's password
def change_user_password(username, new_password):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    sql = "UPDATE users SET password=? WHERE username=?"
    try:
        cursor.execute(sql, (new_password, username))
        conn.commit()
    except sqlite3.Error as e:
        log_error("change_user_password error : ( " + username + ", " + new_password + " )", e)
    finally:
        conn.close()


def remove_wine_for_user_by_user_id(user_id , wine_name) :
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try :
        # Get the product_id of the wine
        cursor.execute("SELECT id FROM price_history WHERE wine_name=?" , (wine_name ,))
        product = cursor.fetchone()

        if product :
            product_id = product[0]
            # Remove the wine from the user's alerts
            cursor.execute("DELETE FROM user_product_alerts WHERE user_id=? AND product_id=?" , (user_id , product_id))
            conn.commit()
            print(f"{wine_name} removed for user with ID {user_id}")
        else :
            print(f"{wine_name} not found in price history")
    except sqlite3.Error as e :
        print("Error removing wine for user:" , e)
    finally :
        conn.close()

'''