# Importing the necessary libraries and modules including the Flask class
from flask import Flask, request, jsonify
# Importing CORS to allow cross-origin requests
from flask_cors import CORS
# Importing the urlAnalyser function from the detectionAlgorithm.py file
from detectionAlgorithm import urlAnalyser
# Importing database functions
from database import createDbConnection, createDb

# Creating and naming the instance of the Flask class
app = Flask(__name__)

# Passing the app instance to CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Creating a connection to the MySQL database and set up if not already
createDb()

# Creating a route to check if the username exists in the database
@app.route('/check-username', methods=['POST'])
def checkUsername():
    # Assigning the JSON (retrieved from the POST request) to the variable data
    data = request.json
    username = data.get('username')
    try:
        db = createDbConnection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("USE Quishing")
        cursor.execute("SELECT userId FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        # if the username exists, return a JSON object with the key 'exists' set to True
        if user:
            return jsonify({'exists': True})
        # if the username does not exist, insert the username into the database and return a JSON object with the key 'exists' set to False
        else:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            db.commit()
            return jsonify({'exists': False})
    # Error handling
    except Exception as e:
        # DEBUGGING PRINT STATEMENT
        print("Error checking username:", str(e))  # Log the actual error
        return jsonify({'error': str(e)}), 501
    # Always close the connection
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
# Defining the URL to trigger the validate function via a POST request
@app.route('/validate', methods=['POST'])
def validate():
    # Assigning the JSON (retrieved from the POST request) to the variable data
    data = request.json
    # DEBUGGING PRINT STATEMENT
    print("Received data:", data)
    # Assigning the value of the 'url' key in the JSON to the variable url
    url = data.get('url')
    # Assigning the value of the 'username' key in the JSON to the variable username
    username = data.get('username', None)

    # Attempting to connect to the database
    try:
        db = createDbConnection()
        cursor = db.cursor(dictionary=True)
        # Select the database
        cursor.execute("USE Quishing")

        # Initialize userId to None
        userId = None

        # Checking if the username exists in the database 
        if username:
            cursor.execute("SELECT userId FROM users WHERE username = %s", (username,)) 
            user = cursor.fetchone()  
            # If the username exists, assign the userId to the variable userId
            cursor.close()
            if user:
                userId = user['userId']
            # If the username does not exist, insert the username into the database and assign the userId to the variable userId
            else:
                cursor = db.cursor(dictionary=True)
                cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
                db.commit()
                userId = cursor.lastrowid

        # Assigning the result of the urlAnalyser function (with the url as an argument) to the variable result
        result = urlAnalyser(url)
        # Storing the url and user_id in the database if the result is 'bad'
        if result['result'] == 'bad':
            cursor.execute("INSERT INTO links (url, userId) VALUES (%s, %s)", (url, userId))
            db.commit()
        # DEBUGGING PRINT STATEMENT
        print("Validation result:", result)
        # closing the cursor
        cursor.close()  
        # closing the database connection
        db.close()      
        # Returning the result as a JSON object
        return jsonify(result)
    except Exception as e:
        # DEBUGGING PRINT STATEMENT
        print("Error handling validation:", str(e))  # Log the actual error
        return jsonify({'result': 'error', 'message': str(e)})

    # Always close the connection
    finally:
        if db.is_connected():
            db.close()

# Running the Flask app (with debugging enabled)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)