import sqlite3
import bcrypt  # for password hashing
import datetime
from contextlib import closing
import scraping_script
import json

DATABASE_PATH = "..\\data\\pricetracking.db"

# Function to hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to verify a password
def verify_password(plain_password, hashed_password):
    print(f"plain_password: {plain_password}")
    print(f"hashed_password: {hashed_password}")
    return bcrypt.checkpw(plain_password, hashed_password)

def get_user_login_details(email, password):
    print("---------get_user_login_details function-----------\ninput --> ", email, password)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE users.email=?", (email,))
        user = cursor.fetchone()
        if user:
            stored_password = user[2]  # Assuming password is stored at index 2 in the database
            if verify_password(password.encode('utf-8'), stored_password):
                print("Login successful!")
                
                return (user[0] , user[1] , user[3])
            else:
                print("Incorrect password!")
                return None
        else:
            print("User not found in DB")
            return None
    except sqlite3.Error as e:
        print("Error User Not Found In DB: ", e)
        return None
    finally:
        conn.close()
        print("EXIT FROM get_user_login_details function")


def get_user_wine_list(user_id):
    print("---------get_user_wine_list function-----------\ninput --> ", user_id)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        query = "SELECT current_price.* , user_product_alerts.desired_price FROM current_price JOIN user_product_alerts ON user_product_alerts.product_id = current_price.id WHERE  user_product_alerts.user_id = ? ;"
        cursor.execute(query , (user_id,))
        user_wines = cursor.fetchall()
        if user_wines:
            print("user_wines---> ", user_wines)
            return user_wines
        # cursor.execute("SELECT product_id FROM user_product_alerts WHERE user_product_alerts.user_id =? ", (str(user_id),))
        # products_id = cursor.fetchall()
        # print("products_id---> ", products_id)
        # if products_id:
        #     numbers_list = [item[0] for item in products_id]
        #     questions_marks = ','.join("?" for _ in numbers_list)
        #     query = f"SELECT * FROM price_history WHERE price_history.id IN ({questions_marks})"
        #     cursor.execute(query, numbers_list)
        #     products = cursor.fetchall()
        #     return products
        else:
            return None
    except sqlite3.Error as e:
        print("Error User Wines Not Found: ", e)
        return None
    finally:
        print("EXIT FROM get_user_login_details function")
        conn.close()

# Function to add a user with hashed password
def add_user(name, password, email):
    print("---------add_user-----------\ninput --> ", name, password, email )
    hashed_password = hash_password(password)
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        try:
            cursor.execute(sql, (name, hashed_password, email))
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
            cursor.execute("SELECT current_price.id FROM current_price WHERE wine_name=?", (wine_name,))
            product = cursor.fetchone()

            if product:
                product_id = product[0]
                cursor.execute("UPDATE current_price SET counter = counter + 1 WHERE id = ?;", (product_id , ))

                
                print("wine exists in the price_history table", wine_name)
            else:
                # If the wine doesn't exist, scrape the prices
                print("wine doesnt exist in the price_history table", wine_name)
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                wine = scraping_script.get_prices(wine_name)
                urls_json = json.dumps(wine["urls"])
                sp_derech_json = json.dumps(wine["prices"]["derech_hyin"]["sale_price"])
                sp_haturki_json = json.dumps(wine["prices"]["haturki"]["sale_price"])
                sp_paneco_json = json.dumps(wine["prices"]["paneco"]["sale_price"])

                # Insert scraped prices into the price_history table
                query = '''INSERT INTO current_price (wine_name , date ,counter, product_image , details , rp_derech , cp_derech , sp_derech , rp_haturki , cp_haturki , sp_haturki , rp_paneco , cp_paneco , sp_paneco) 
                        VALUES (?, ?, ?,? , ?, ?, ? , ?, ?, ? , ?, ?, ? ,?)'''
                
                cursor.execute(
                    query,
                    (wine["name"], date ,1,wine["img"], urls_json,
                     wine["prices"]["derech_hyin"]["regular_price"] , wine["prices"]["derech_hyin"]["club_price"] ,sp_derech_json,
                     wine["prices"]["haturki"]["regular_price"] , wine["prices"]["haturki"]["club_price"] ,sp_haturki_json,
                     wine["prices"]["paneco"]["regular_price"] , wine["prices"]["paneco"]["club_price"] ,sp_paneco_json
                     ))
                
                
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


def remove_wine_for_user_by_user_id(user_id, product_id):
    print("---------remove_wine_for_user_by_user_id-----------\ninput --> ", user_id, ", ", product_id)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        # Remove the wine from the user's alerts
        cursor.execute("DELETE FROM user_product_alerts WHERE user_id=? AND product_id=?", (user_id, product_id))
        conn.commit()
        print(f"{product_id} removed for user with ID {user_id}")

    except sqlite3.Error as e:
        print("Error removing wine for user:", e)
    finally:
        conn.close()
        print("EXIT FROM remove_wine_for_user_by_user_id function")



def get_all_products():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT id , wine_name FROM current_price ")
        temp = cursor.fetchall()
        return temp
    

    except sqlite3.Error as e:
        print(e)
        return None
    finally:
        conn.close()
        
################################



# # Function to add a user
# def add_user(name, password, email):
#     print("---------add_user-----------\ninput --> ", name, password, email )
#     hashed_password = hash_password(password)
#     with sqlite3.connect(DATABASE_PATH) as conn:
#         cursor = conn.cursor()
#         sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
#         try:
#             cursor.execute(sql, (name, hashed_password, email))
#             conn.commit()
#             last_id = cursor.lastrowid
#             cursor.execute("SELECT * FROM users WHERE id = ?", (last_id,))
#             user = cursor.fetchone()
#             print("newUser -- > ", user )
#             return user
#         except sqlite3.Error as e:
#             print(f"add_user error: ({name}, {email})", str(e))
#             return "user email exists"


# Add the rest of your functions here