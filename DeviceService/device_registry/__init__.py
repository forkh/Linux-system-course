from flask import Flask, jsonify
from flask_restful import reqparse, Resource, Api
import kasa
import asyncio
import json
import threading
import time
import sys

app = Flask(__name__)
api = Api(app)

DEVICES = []

UPDATE_INTERVAL = 5

#loop = asyncio.get_event_loop()
#loop.run_until_complete()

ASYNC_LOOP = asyncio.new_event_loop()
ASYNC_LOOP = asyncio.get_event_loop()
#ASYNC_LOOP.run_forever()
#LOOPY = asyncio.set_event_loop(ASYNC_LOOP)

parser = reqparse.RequestParser()
parser.add_argument('ip_address')
parser.add_argument('state')


class KasaExtended:
    def __init__(self):
        print("Started")

    #async def scan(self):
    def scan(self):
        devices = asyncio.run(kasa.Discover.discover())
        #loop = asyncio.get_running_loop()
        temporary_devices = []
        global DEVICES
        for ip_addr, dev in devices.items():
            asyncio.run(dev.update())
            #ASYNC_LOOP.run_until_complete(dev.update())
            #await asyncio.run(dev.update())
            #asyncio.run(dev.update())
            #loop.run(dev.update())
            #ASYNC_LOOP.run_until_complete(dev.update())
            #await ASYNC_LOOP.create_task(dev.update())
            #t asyncio.ensure_future(dev.update(), loop=ASYNC_LOOP)
            temporary_devices.append((ip_addr, dev.mac[-2:]))

        DEVICES = temporary_devices
        return 'Ok', 200

    def get_info(self, ip_address):
        plug = kasa.SmartPlug(ip_address)
        print(type(plug))
        sys.stdout.flush()
        asyncio.run(plug.update())
        daily_stats = asyncio.run(plug.get_emeter_daily(year=2021, month=2))
        ret = {ip_address:
            {
            'is_on': plug.is_on,
            'on_since': str(plug.on_since),
            'model': str(plug.model),
            'led_state': plug.state_information['LED state'],
            'emeter_realtime': plug.emeter_realtime,
            'emeter_statistics_daily': daily_stats,
            'alias': plug.alias
            }
        }
        return ret

    def get_info_all(self):
        ret = []
        for dev in DEVICES:
            dev_info = self.get_info(dev[0])
            item = [dev[0], dev[1], dev_info[dev[0]]['is_on']]
            print(type(dev_info[dev[0]]['is_on']))
            sys.stdout.flush()
            #dev_info['ip'] = dev[0]
            ret.append(item)
        return ret

    async def turn_on(self, ip_address):
        plug = kasa.SmartPlug(ip_address)
        await plug.turn_on()
        return 'Ok', 200

    async def turn_off(self, ip_address):
        plug = kasa.SmartPlug(ip_address)
        await plug.turn_off()
        return 'Ok', 200


KASA = KasaExtended()

class DeviceList(Resource):
    def get(self):
        return json.dumps(DEVICES), 200

class RefreshList(Resource):
    def get(self):
    #async def get(self):
        #ASYNC_LOOP.run_until_complete(KASA.scan())
        #await asyncio.ensure_future(KASA.scan(), loop=ASYNC_LOOP)
        KASA.scan()
        return "Ok", 200

class Terje(Resource):
    def get(self):
        for dev in DEVICES:
            if dev[1] == '7E':
                return dev[0], 200
        return 404

class NameLookup(Resource):
    def get(self, ip_address):
        for t in DEVICES:
            if t[0] == ip_address:
                plug = kasa.SmartPlug(ip_address)
                asyncio.run(plug.update())
                return plug.mac[-2:], 200
        else:
            return f"Device with IP: {ip_address} not found", 404

class DeviceName(Resource):
    def get(self, name):
        for dev in DEVICES:
            #print(f"Name: {name}, in DEVICES: {dev[1]}, IP: {dev[0]}")
            #sys.stdout.flush()
            if dev[1].lower() == name.lower():
                return KASA.get_info(dev[0]), 200
        else:
            return 404

class Device(Resource):
    def get(self, ip_address):
        for t in DEVICES:
            if t[0] == ip_address:
                return KASA.get_info(ip_address), 200
        else:
            return 404
    def post(self, ip_address):
        for t in DEVICES:
            if t[0] == ip_address:
                args = parser.parse_args()
                state = args['state']
                if state == "on":
                    ASYNC_LOOP.run_until_complete(KASA.turn_on(ip_address))
                elif state == "off":
                    ASYNC_LOOP.run_until_complete(KASA.turn_off(ip_address))
                return 'Ok', 200
        else:
            return 'Not found', 404

class DevIP(Resource):
    def get(self, alias):
        alias = alias.lower()
        for dev in DEVICES:
            if alias == dev[1].lower():
                return dev[0]
        else:
            return 404

class GetDeviceInfoAll(Resource):
    def get(self):
        return KASA.get_info_all(), 200

class GetAliasIp(Resource):
    def get(self):
        ret = dict()
        for dev in DEVICES:
            ret[dev[1]] = dev[0]
        print(ret)
        sys.stdout.flush()
        return ret, 200

api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<ip_address>')
api.add_resource(NameLookup, '/name/<ip_address>')
api.add_resource(RefreshList, '/refresh')
api.add_resource(Terje, '/terje')
api.add_resource(DeviceName, '/dev/<name>')
api.add_resource(DevIP, '/ip/<alias>')
api.add_resource(GetDeviceInfoAll, '/device_info_all')
api.add_resource(GetAliasIp, '/alias_ip')

#if __name__ == '__main__':
#    app.run(debug=True)

