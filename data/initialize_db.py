import sqlite3

def initialize_db():
    conn = sqlite3.connect('../data/pricetracking.db')
    cursor = conn.cursor()

    create_usersANDproducts_table = """
    CREATE TABLE IF NOT EXISTS user_product_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        desired_price REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """

    create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
"""


    create_products_table = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE
    );
    """

    create_price_history_table = """
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        date TEXT NOT NULL,
        price REAL NOT NULL,
        store TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    );
    """

    #cursor.execute(create_users_table)
    #cursor.execute(create_products_table)
    #cursor.execute(create_price_history_table)
    cursor.execute(create_usersANDproducts_table)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
