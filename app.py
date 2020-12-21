#!/usr/bin/env python3

import json
import traceback

from flask import Flask, request, make_response, jsonify

from static.services.outlet_handler import handle_transmission

app = Flask(__name__)


@app.route('/api/handle-button', methods=['POST'])
def handle_button():
    data = json.loads(request.data)

    try:
        handle_transmission(data)

        message = 'Transmission successful'
        successful = True
        status = 200
    except Exception:
        message = f'There was an error during the transmission: {traceback.format_exc()}'
        successful = False
        status = 500

    return make_response(jsonify({'message': message, 'successful': successful}), status)


@app.route('/api/all-lights', methods=['POST'])
def all_lights():
    data = json.loads(request.data)

    try:
        for outlet in data:
            handle_transmission(outlet)

        message = 'Transmission successful'
        successful = True
        status = 200
    except Exception:
        message = f'There was an error during the transmission: {traceback.format_exc()}'
        successful = False
        status = 500

    return make_response(jsonify({'message': message, 'successful': successful}), status)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
