from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Luxury AI Agent API is working!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)