import mysql.connector
from mysql.connector import Error

# Try database connection
def createDbConnection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="Quishing"
        )
        return db
        # Catch failed connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return e
    
def createDb():
    # Creating databse and tables if they do not already exist 
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
        cursor.execute("CREATE TABLE IF NOT EXISTS users (userId INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) UNIQUE")
        cursor.execute("CREATE TABLE IF NOT EXISTS links (linkId INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), userId INT DEFAULT NULL, FOREIGN KEY (userId) REFERENCES users(userId))")

        # Committing the changes to the database
        db.commit()
        print("Successfully created the database and tables.")
    # Catch errors
    except Error as e:
        print("Error setting up the database:", e)
        raise e
    # Always close the connection
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()
