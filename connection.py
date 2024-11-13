import mysql.connector
from mysql.connector import Error
import toml
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="supplychain"
        )
        print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def login(username, password):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user and user['password'] == password:
        return True 
    return False

def fetch_data(query):
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def insert_data(query, values):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return True
