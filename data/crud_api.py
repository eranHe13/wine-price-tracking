import sqlite3

def log_error(f , e):
    with open('sqlLogs.txt', 'a') as file:
        file.write(f"{f} --> {e}\n")


def add_user(name, password , email):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    sql = "INSERT INTO users (username,  password , email) VALUES (?, ? ,?)"
    try:
        cursor.execute(sql, (name,  password , email))
        conn.commit()
    except sqlite3.Error as e:
        log_error( "add_user error : ( " + name + " "+ password + " "+ email + " )"  ,  e )
    finally:
        conn.close()



def add_product(name, url):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    sql = "INSERT INTO products (name, url) VALUES (?, ?)"
    try:
        cursor.execute(sql, (name, url))
        conn.commit()
    except sqlite3.Error as e:
            log_error( "add_user error : ( " + name + " "+ url + " )"  ,  e )
    finally:
        conn.close()

import sqlite3


def add_product(name, url):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    sql = "INSERT INTO products (name, url) VALUES (?, ?)"
    try:
        cursor.execute(sql, (name, url))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted product
    except sqlite3.Error as e:
        log_error("add_product error: (" + name + " " + url + ")", e)
        return None
    finally:
        conn.close()


def delete_product(product_id):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    sql = "DELETE FROM products WHERE id = ?"
    try:
        cursor.execute(sql, (product_id,))
        conn.commit()
    except sqlite3.Error as e:
            log_error( "delete_product error : ( " + product_id + " )"  ,  e )
    finally:
        conn.close()



def insert_user_product_alert(user_id, product_id, desired_price):
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()
    
    sql = "INSERT INTO user_product_alerts (user_id, product_id, desired_price) VALUES (?, ?, ?)"
    
    try:
        cursor.execute(sql, (user_id, product_id, desired_price))
        conn.commit()
        print("Alert added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Example usage
def test():
    product_id = add_product("Example Product", "http://example.com/product")
    if product_id:
        user_id = 1  # Assuming you have a user ID
        desired_price = 100.00  # Example desired price
        insert_user_product_alert(user_id, product_id, desired_price)


test()