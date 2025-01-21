# Importing the necessary libraries and modules including the Flask class
from flask import Flask, request, jsonify
# Importing CORS to allow cross-origin requests
from flask_cors import CORS
# Importing the qrCodeAnalyser funtion from the detectionAlgorithm.py file
from detectionAlgorithm import qrCodeAnalyser
# Importing the mysql.connector library
import mysql.connector

# Creating and naming the instance of the Flask class
app = Flask(__name__)

# Passing the app instance to CORS
CORS(app)

# Defining the URL to trigger the validate function via a POST request
@app.route('/validate', methods=['POST'])

# Creating the validate function to receive the POST request
def validate():
    # Assigning the JSON (retrieved from the POST request) to the variable data
    data = request.json
    # Assigning the value of the 'url' key in the JSON to the variable qrCode
    url = data['url']
    # Assigning the result of the qrCodeAnalyser function (with the qrCode as an argument) to the variable result
    result = urlAnalyser(url)
    # Returning the result as a JSON object
    return jsonify(result)

# Running the Flask app (with debugging enabled)
if __name__ == '__main__':
    app.run(debug=True)

# Database connection
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=""
    )
    # Check if the connection was successful
    print("Successfully connected to the database server.")

    # Creating a cursor from the cursor() method of the db object
    cursor = db.cursor()
    # Using the cursor to execute SQL queries
    # Creating the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS Quishing")
    cursor.execute("USE Quishing")

    # Creating the tables
    cursor.execute("CREATE TABLE IF NOT EXISTS users (userId INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS links (linkId INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), userId INT, FOREIGN KEY (userId) REFERENCES users(userId))")

    # Committing the changes to the database
    db.commit()
    print("Successfully created the database and tables.")

except Error as e: 
    print("Error while connecting to MySQL", e)
finally:
    if (db.is_connected()):
        cursor.close()
        db.close()
        print("MySQL connection is closed.")





