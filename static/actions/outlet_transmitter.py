from rpi_rf import RFDevice

rfdevice = RFDevice(17)
rfdevice.enable_tx()
rfdevice.tx_repeat = 10


def send_code(code, protocol, pulse_length, length=24):
    rfdevice.tx_code(code, protocol, pulse_length, length)
    # pass
