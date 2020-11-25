import sys, os

from flask import Flask, jsonify, request

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json

import asyncio
import uuid
import argparse

CONFIG_FILE = "tradfri_keys.conf"

app = Flask(__name__)
gateway = None
api = None
loop = asyncio.get_event_loop()

async def init():
    global gateway
    global api

    conf = load_json(CONFIG_FILE)

    identity = conf["192.168.50.30"].get("identity")
    psk = conf["192.168.50.30"].get("key")
    api_factory = await APIFactory.init(host="192.168.50.30", psk_id=identity, psk=psk)

    api = api_factory.request

    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = await api(devices_command)
    devices = await api(devices_commands)

    print(f"Detected devices: {devices}")

def get_future(future):
    return loop.run_until_complete(future)

def get_command(cmd):
    return get_future(api(get_future(api(cmd))))

get_future(init())

#
# Device operator/getter
# Input:
# {
#   "state": 1,
#   "color": "#FFF"
# }
#
# Output:
# {
#   "selected": ["Office spot", ...]
# }
#

@app.route("/tradfri/<select>", methods=["GET", "POST"])
def tradfri(select):
    data = request.get_json()
    lights = get_command(gateway.get_devices())
    target = [light for light in lights if light.name == select and light.has_light_control]
    
    if not target:
        return jsonify({"status": "ERROR", "code": 404})

    for k, v in data.items():
        if k == "state":
            [get_future(api(x.light_control.set_state(True if v == 1 else False))) for x in target]
        elif k == "color":
            [get_future(api(x.light_control.set_color(v))) for x in target]


    return jsonify({
            "status": "OK",
            "data": {"selected": [x.name for x in target]},
        })

