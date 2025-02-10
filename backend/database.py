# filepath: /Users/pollyluisa/Desktop/quashthequish/backend/database.py
import mysql.connector
from mysql.connector import Error

def createDbConnection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Theoc123'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def createDb():
    # Creating database and tables if they do not already exist 
    try:
        db = createDbConnection()
        # Checking if the connection is successful
        if db is None:
            raise Exception("Failed to connect to the database")
        # Creating a cursor from the cursor() method of the db object
        cursor = db.cursor()
        # Using the cursor to execute SQL queries
        # Creating the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS Quishing")

        # Creating the tables
        cursor.execute("USE Quishing")
        cursor.execute("CREATE TABLE IF NOT EXISTS users (userId INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) UNIQUE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS links (linkId INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), userId INT DEFAULT NULL, FOREIGN KEY (userId) REFERENCES users(userId))")

        # Committing the changes to the database
        db.commit()
        print("Successfully created the database and tables.")
    # Catch errors
    except Error as e:
        print("Error setting up the database:", e)