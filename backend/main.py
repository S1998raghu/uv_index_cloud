import os
from flask_cors import CORS
from flask import Flask, request, jsonify
import requests
from datetime import datetime



ENDPOINT = 'https://api.openuv.io/api/v1/uv'
print("Received a request..")
app = Flask(__name__)
CORS(app, origins=['*'], allow_headers=['Content-Type', 'x-access-token'])
@app.route('/UV', methods=['POST', 'OPTIONS'])
def uv():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        api_key = request.headers['x-access-token']
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')

        parameters = {
            'lat': lat,
            'lng': lng,
            'alt': 0,  # Default altitude
            'dt': datetime.now()  # Default date-time
        }
        if not lat or not lng:
            return jsonify({'error': 'Latitude and Longitude are required'}), 400
        if not api_key:
            return jsonify({'error': 'API key is required'}), 401
        headers = {
            'x-access-token': api_key
        }        
        response  = requests.get(ENDPOINT, params=parameters, headers=headers)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch UV data'}), response.status_code
        uv_data = response.json()
        uv_value = uv_data.get('result', {}).get('uv', None)
        return jsonify({'uv': uv_value}), 200
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
   
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
# This code is a Flask application that provides an endpoint to fetch UV index data based on latitude and longitude.
# It uses the OpenUV API to get the UV index and requires an API key for access. The endpoint is designed to handle POST requests with JSON data containing latitude and longitude.
