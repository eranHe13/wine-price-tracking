import sqlite3
import bcrypt  # for password hashing
import scraping.scraping_script
import datetime

from contextlib import closing

# Function to log errors
DATABASE_PATH = '../data/pricetracking.db'

def log_error(context, error):
    # Implement your error logging mechanism here
    pass

# Function to add a user
def add_user(name, password, email):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        try:
            cursor.execute(sql, (name, hashed_password, email))
            conn.commit()
        except sqlite3.Error as e:
            log_error(f"add_user error: ({name}, {email})", str(e))

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

#add wine to user_product and price_history table. scrapes prices if needed.
def add_new_product_for_user( user_name ,wine_name , desired_price) :
    with sqlite3.connect(DATABASE_PATH) as conn :
        cursor = conn.cursor()
        try :
            # Check if the wine exists in the price_history table
            cursor.execute("SELECT id FROM price_history WHERE wine_name=?" , (wine_name ,))
            product = cursor.fetchone()

            if product :
                product_id = product[0]
            else :
                # If the wine doesn't exist, scrape the prices
                wine_prices = scraping.scraping_script.get_prices(wine_name)  # Call your scraping script
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Insert scraped prices into the price_history table
                cursor.execute(
                    "INSERT INTO price_history (wine_name,date, price_wine_rout, price_paneco, price_haturki) VALUES (?, ?, ?, ?,?)" ,
                    (wine_name ,date, wine_prices[0] , wine_prices[1] , wine_prices[2]))
                conn.commit()
                product_id = cursor.lastrowid  # Get the product ID

            # Add the product ID to the user_product_alerts table
            cursor.execute(
                "INSERT INTO user_product_alerts (user_id, product_id, desired_price) VALUES ((SELECT id FROM users WHERE username=?), ?, ?)" ,
                (user_name , product_id , desired_price))
            conn.commit()
        except sqlite3.Error as e :
            log_error(f"add_product_alert error: ({wine_name}, {user_name}, {desired_price})" , str(e))

def get_user_id_by_username(username) :
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try :
        cursor.execute("SELECT id FROM users WHERE username=?" , (username ,))
        user = cursor.fetchone()
        if user :
            return user[0]
        else :
            return None
    except sqlite3.Error as e :
        print("Error getting user ID by username:" , e)
        return None
    finally :
        conn.close()

def remove_wine_for_user_by_username(username , wine_name) :
    user_id = get_user_id_by_username(username)
    if user_id is not None :
        remove_wine_for_user_by_user_id(user_id , wine_name)
    else :
        print("User not found")

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


# Example usage
def test():
    add_user("eran","123","eran@gmail.com")
    # add_new_product_for_user( "ilan" ,"לוינסון אדום",90)
    # add_new_product_for_user( "eran" ,"יפו שרדונה",75)
    # remove_wine_for_user_by_username("ilan","יפו שרדונה")
test()