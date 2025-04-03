# Importing the necessary libraries and modules including the Flask class
from flask import Flask, make_response, request, jsonify
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

        response = make_response(jsonify({'exists': bool(user)}))
        # if the username exists, return a JSON object with the key 'exists' set to True
        if user:
            return jsonify({'exists': True})
        # if the username does not exist, insert the username into the database and return a JSON object with the key 'exists' set to False
        else:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            db.commit()
            response = make_response(jsonify({'exists': False}))

        response.set_cookie('username', username, httponly=True, samesite='Lax') 
        return response
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
    # Getting username from cookies incase url is not already in database
    username = request.cookies.get('username')

    if not username:
        return jsonify({'error': 'Username not found in request or cookies'}), 400

    print("Received username from cookie:", repr(username))
    # Assigning the value of the 'url' key in the JSON to the variable url
    data = request.get_json() 
    url = data.get('url')
    # Attempting to connect to the database
    try:
        db = createDbConnection()
        cursor = db.cursor(dictionary=True)
        # Select the database
        cursor.execute("USE Quishing")
        # Fetching userId
        cursor.execute("SELECT userId FROM users WHERE username = %s", (username,)) 
        user = cursor.fetchone() 
        cursor.close()

        # Initialise userId to None
        userId = None

        # In case issue with fetching username
        if user:
            userId = user['userId']
        else:
            userId = None
        cursor = db.cursor(dictionary=True)
        # Assigning the result of the urlAnalyser function (with the url as an argument) to the variable result
        result = urlAnalyser(url)
        # Checking if url is in the database and if not, storing the it and user_id that found it (in the database) if the result is 'bad'
        if result['result'] == 'bad':
            cursor.execute("SELECT linkId FROM links WHERE url = (%s)", (url,))
            existingLink = cursor.fetchone()

            if not existingLink:
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

# Creating a route to fetch the leaderboard
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    # Attempting to connect to the database
    try:
        db = createDbConnection()
        cursor = db.cursor(dictionary=True)
        # Select the database
        cursor.execute("USE Quishing")
        # Query to count the number of bad links each user has reported
        cursor.execute("""
            SELECT u.username, COUNT(l.userId) AS num_of_links 
            FROM users u
            LEFT JOIN links l ON u.userId = l.userId
            GROUP BY u.userId
            ORDER BY num_of_links DESC
        """)
        # Fetch all the results and save them to the variable leaderboard
        leaderboard = cursor.fetchall()
        
        # Close database connection
        cursor.close()
        db.close()
        # Return the leaderboard
        return jsonify(leaderboard)  
    # Handle errors
    except Exception as e:
        print("Error fetching leaderboard:", str(e))
        return jsonify({'error': str(e)}), 500

# Creating a route to fetch the user data (for the leaderboard) using the username
@app.route('/userData/<username>', methods=['GET'])
def userData(username):
    # Attempting to connect to the database
    try:
        db = createDbConnection()
        cursor = db.cursor(dictionary=True)
        # Select the database
        cursor.execute("USE Quishing")
        # Query to get the leaderboard with ranks
        cursor.execute("""
            SELECT u.username, COUNT(l.userId) AS num_links, RANK() OVER (ORDER BY COUNT(l.userId) DESC) AS ranking
            FROM users u
            LEFT JOIN links l ON u.userId = l.userId
            GROUP BY u.userId
        """)
        
        # Fetch all the results
        leaderboard = cursor.fetchall()

        # Find the user's rank and phishing attempt count
        usersData = next((user for user in leaderboard if user["username"] == username), None)

        # Close database connection
        cursor.close()
        db.close()

        # Return the user data if found
        if usersData:
            return jsonify(usersData)  
        else:
            return jsonify({'error': 'User not found'}), 404
    # Handle errors
    except Exception as e:
        print("Error fetching user stats:", str(e))
        return jsonify({'error': str(e)}), 500

# Running the Flask app (with debugging enabled)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)