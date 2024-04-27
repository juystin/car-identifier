import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True
}

class Database():
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        
    def insert(self, car_count, timestamp, color, car_type, in_out):        
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO car_tracking (timestamp, car_count, color, car_type, in_out) VALUES ('{}', {}, '{}', '{}', '{}');".format(timestamp, car_count, color, car_type, in_out))
        self.conn.commit()
        cursor.close()
        
    def get_latest_count(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT car_count FROM car_tracking ORDER BY timestamp DESC LIMIT 1;")
        row = cursor.fetchone()

        if row is not None:
            car_count = row[0]
        else:
            car_count = None

        return car_count
        
    def close(self):
        self.conn.close()