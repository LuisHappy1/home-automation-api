#!/usr/bin/env python3

from flask import Flask, render_template
from rpi_rf import RFDevice

app = Flask(__name__)

rfdevice = RFDevice(17)
rfdevice.enable_tx()


@app.route('/')
def home():
    return render_template('home.html')


# on
# python3 rfrx_send.py 9407996 -p 163 -t 1
# off
# python3 rfrx_send.py 9407988 -p 71 -t 31
@app.route('/lamp')
def lamp():
    print('lamp will be turned on')
    rfdevice.tx_code(9407996, 1, 163, 24)
    rfdevice.cleanup()
    return render_template('home.html')


if __name__ == "__main__":
    print('here in the main')
    app.run(host='0.0.0.0')
