import sqlite3

def insert_car_data(conn, c, car_name, current_bid, location, mileage, link):
    insert_query = '''INSERT INTO car_prices (car_name, current_bid, location, mileage, link, timestamp) VALUES (?, ?, ?, ?, ?, datetime('now'))'''
    c.execute(insert_query, (car_name, current_bid, location, mileage, link,))
    conn.commit()

# Define other database functions here...
