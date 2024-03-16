import sqlite3


DATABASE_PATH = '../data/pricetracking.db'

def initialize_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """

    create_price_history_table = """
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wine_name TEXT,
        date TEXT NOT NULL,
        price_wine_rout REAL,
        price_paneco REAL,
        price_haturki REAL
    );
    """

    create_user_product_alerts_table = """
    CREATE TABLE IF NOT EXISTS user_product_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        desired_price REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES price_history(id)
    );
    """

    #cursor.execute(create_users_table)
    cursor.execute(create_price_history_table)
    #cursor.execute(create_user_product_alerts_table)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()