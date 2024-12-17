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

def validate():
    data = request.json
    qrCode = data['qrCode']
    result = qrCodeAnalyser(qrCode)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)