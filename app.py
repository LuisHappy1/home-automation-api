#!/usr/bin/env python3

import json
from flask import Flask, request, make_response, jsonify

from static.actions.outlet_transmitter import send_code

app = Flask(__name__)

outletCodes = {
    "lamp": {
        "on": {
            "code": 9407996,
            "protocol": 1,
            "pulse_length": 163
        },
        "off": {
            "code": 9407988,
            "protocol": 3,
            "pulse_length": 71
        }
    },
    "christmas_tree": {
        "on": {
            "code": 9407994,
            "protocol": 1,
            "pulse_length": 185
        },
        "off": {
            "code": 9407986,
            "protocol": 1,
            "pulse_length": 170
        }
    }
}


@app.route('/handle-button', methods=['POST'])
def handle_button():
    data = json.loads(request.data)
    try:
        current_outlet = outletCodes[data['name']][data['lightSetting']]
        send_code(current_outlet['code'], current_outlet['protocol'], current_outlet['pulse_length'])
        message = f'Lights were successfully turned {data["lightSetting"]}'
        return make_response(jsonify({'message': message, 'successful': True}), 200)

    except RuntimeError:
        message = f'There was an error trying to turn on the {data["name"]}'
        return make_response(jsonify({'message': message, 'successful': False}), 500)


@app.route('/all-lights', methods=['POST'])
def all_lights():
    data = json.loads(request.data)

    for outlet in outletCodes:
        current_outlet = outletCodes[outlet][data['lightSetting']]
        send_code(current_outlet['code'], current_outlet['protocol'], current_outlet['pulse_length'])

    return make_response(200)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
