import sqlite3
import sqlite3

# Function to log errors
def log_error(f, e):
    with open('sqlLogs.txt', 'a') as file:
        file.write(f"{f} --> {e}\n")

# Function to add a user
def add_user(name, password, email):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
    try:
        cursor.execute(sql, (name, password, email))
        conn.commit()
    except sqlite3.Error as e:
        log_error("add_user error : ( " + name + " "+ password + " "+ email + " )", e)
    finally:
        conn.close()

# Function to get user by username
def get_user_by_username(username):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        log_error("get_user_by_username error : ( " + username + " )", e)
        return None
    finally:
        conn.close()

# Function to add a user-product alert
def add_user_product_alert(user_id, product_id, desired_price):
    '''
    --- check if allready exist
    
    '''
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    sql = "INSERT INTO user_product_alerts (user_id, product_id, desired_price) VALUES (?, ?, ?)"
    try:
        cursor.execute(sql, (user_id, product_id, desired_price))
        conn.commit()
    except sqlite3.Error as e:
        log_error("add_user_product_alert error : ( " + str(user_id) + ", " + str(product_id) + ", " + str(desired_price) + " )", e)
    finally:
        conn.close()

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



# Example usage
def test():
    product_id = add_product("Example Product", "http://example.com/product")
    if product_id:
        user_id = 1  # Assuming you have a user ID
        desired_price = 100.00  # Example desired price
        add_user_product_alert(user_id, product_id, desired_price)


test()