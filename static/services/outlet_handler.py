from static.repository.outlet_transmitter import send_code


def handle_transmission(outlet):
    current_outlet = outlet['outlet']
    return send_code(current_outlet['code'], current_outlet['protocol'], current_outlet['pulse_length'])
