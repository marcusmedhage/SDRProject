import sys
import time
import argparse
import struct
from enum import Enum
import random
from pyrf24 import RF24, RF24Network, RF24Mesh, RF24NetworkHeader, RF24_PA_LOW, RF24_2MBPS, MESH_DEFAULT_ADDRESS

start = time.monotonic()

def millis():
    """:Returns: Delta time since started example in milliseconds. Wraps value around
    the width of a ``long`` integer."""
    return int((time.monotonic() - start) * 1000) % (2**32)

radio = RF24(17, 0) # CSN and CE PIN integers
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)

mesh.setNodeID(0)

previousMillis = 0

# Number representing the different message types from RF24Network
SENSOR_DATA = 0
CONFIG_COMMAND = 1


address_self = 0o0 # Node 0 is always the main node.
default_channel = 85

if not radio.begin():
    raise OSError("Radio hardware not responding")
radio.set_pa_level(RF24_PA_LOW)

if not mesh.begin():
    if radio.is_chip_connected:
        try:
            print("Could not connect to network. Attempting to reconnect...")
            while mesh.renew_address() == MESH_DEFAULT_ADDRESS:
                print("Could not connect to network. Attempting to reconnect...")
        except KeyboardInterrupt:
            radio.power = False
            sys.exit()
    else:
        raise OSError("Radio hardware not responding.")
radio.print_pretty_details()



TIMER = 0

try:
    while True:
        # Call mesh.update to keep the network updated
        mesh.update()

        if (millis() - TIMER) >= 1000:
            TIMER = millis()

            if not mesh.write(struct.pack("L", TIMER), ord("M")):
                # If a write fails, check connectivity to the mesh network
                if not mesh.checkConnection():
                    # The address could be refreshed per a specified time frame
                    # or only when sequential writes fail, etc.
                    print("Send fail. Renewing Address...")
                    while mesh.renewAddress() == 0o4444:
                        print("Renewing Address...")
                else:
                    print("Send fail, Test OK")
            else:
                print("Send OK:", TIMER)
        time.sleep(0.001)  # delay 1 ms
except KeyboardInterrupt:
    print("Powering down.")
    radio.power = False