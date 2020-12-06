#!/usr/bin/env python3

import datetime
import json
import sched
import time

from flask import Flask, render_template, request

from static.actions.outlet_transmitter import send_code

s = sched.scheduler(time.time, time.sleep)

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


@app.route('/all-lights', methods=['POST'])
def all_lights():
    data = json.loads(request.data)

    control_all_lights(data)

    return render_template('home.html')


def control_all_lights(data):
    for outlet in outletCodes:
        current_outlet = outletCodes[outlet][data['lightSetting']]
        send_code(current_outlet['code'], current_outlet['protocol'], current_outlet['pulse_length'])


def check_time(sc):
    now = datetime.datetime.now()
    shutoff_time = "23:45"
    current_time = f"{now.hour}:{now.minute}"

    if current_time == shutoff_time:
        print("Will now shut off all lights")
        control_all_lights({'lightSetting': 'off'})
    else:
        print(f"Lights are still on {current_time}")
    s.enter(60, 1, check_time, (sc,))


s.enter(60, 1, check_time, (s,))
s.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
