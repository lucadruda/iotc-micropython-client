import sys
import json
from utime import sleep
from random import randint
from iotc import IoTCClient, IoTCConnectType, IoTCLogLevel, IoTCEvents, Credentials

scope_id = ''
device_id = ''
key = ''
conn_type = IoTCConnectType.DEVICE_KEY


class FileStorage():
    def retrieve(self):
        try:
            f = open('creds.json')
            creds = Credentials.create_from_json_string(f.read())
            f.close()
            return creds
        except:
            return None

    def persist(self, credentials):
        f = open('creds.json', 'w')
        f.write(credentials.to_json_string())
        f.close()


def on_props(property_name, property_value, component_name):
    print("Received {}:{}".format(property_name, property_value))
    return True


def on_commands(command):
    print("Received command {} with value {}".format(command.name, command.value))
    command.reply()


def on_enqueued_commands(command):
    print("Received offline command {} with value {}".format(
        command.name, command.value))


# change connect type to reflect the used key (device or group)
client = IoTCClient(scope_id, device_id, conn_type, key, storage=FileStorage())

# client.set_log_level(IoTCLogLevel.ALL)
client.on(IoTCEvents.PROPERTIES, on_props)
client.on(IoTCEvents.COMMANDS, on_commands)
client.on(IoTCEvents.ENQUEUED_COMMANDS, on_enqueued_commands)


def main():
    client.connect()
    client.send_property({"propertyComponent": {"prop1": 50}})
    send_interval = 10
    x = 0
    while client.is_connected():
        x = x+1
        client.listen()
        if x == send_interval:
            data = {
                "temperature": str(randint(20, 45))
            }
            client.send_telemetry(
                data, {"$.sub": "firstcomponent"}
            )
            x = 0


main()
