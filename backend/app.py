# Importing the necessary libraries and modules including the Flask class
from flask import Flask, request, jsonify
# Importing CORS to allow cross-origin requests
from flask_cors import CORS
# Importing the qrCodeAnalyser funtion from the detectionAlgorithm.py file
from detectionAlgorithm import qrCodeAnalyser

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
    qrCode = data['url']
    # Assigning the result of the qrCodeAnalyser function (with the qrCode as an argument) to the variable result
    result = urlAnalyser(url)
    # Returning the result as a JSON object
    return jsonify(result)

# Running the Flask app (with debugging enabled)
if __name__ == '__main__':
    app.run(debug=True)