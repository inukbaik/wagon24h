import sqlite3


def connect_database(db_path):
    return sqlite3.connect(db_path)


def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS car_prices 
                     (car_name TEXT, current_bid TEXT, location TEXT, mileage TEXT, link TEXT, timestamp TIMESTAMP)''')
    conn.commit()


def insert_car_data(conn, car_name, current_bid, location, mileage, link):
    c = conn.cursor()
    c.execute("INSERT INTO car_prices (car_name, current_bid, location, mileage, link, timestamp) VALUES (?, ?, ?, ?, ?, datetime('now'))",
              (car_name, current_bid, location, mileage, link))
    conn.commit()