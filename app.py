#!/usr/bin/env python3

import json

from flask import Flask, render_template, request

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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/handle-button', methods=['POST'])
def handle_button():
    data = json.loads(request.data)
    current_outlet = outletCodes[data['name']][data['lightSetting']]
    print(current_outlet)
    send_code(current_outlet['code'], current_outlet['protocol'], current_outlet['pulse_length'])

    return render_template('home.html')


@app.route('/turn-off-all-lights', methods=['GET'])
def turn_all_lights_off():
    for outlet in outletCodes:
        current_outlet = outletCodes[outlet]['off']
        send_code(current_outlet['code'], current_outlet['protocol'], current_outlet['pulse_length'])

    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
