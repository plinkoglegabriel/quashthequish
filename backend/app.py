from flask import Flask, request, jsonify
from flask_cors import CORS
from detectionAlgorithm import qrCodeAnalyser

app = Flask(__name__)

CORS(app)
@app.route('/validate', methods=['POST'])

def validate():
    data = request.json
    qrCode = data['qrCode']
    result = qrCodeAnalyser(qrCode)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)