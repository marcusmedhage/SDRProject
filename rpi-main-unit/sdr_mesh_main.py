import sys
import time
import argparse
import struct
from enum import Enum
import random
from pyrf24 import RF24, RF24Network, RF24Mesh, RF24NetworkHeader, RF24_2MBPS, MESH_DEFAULT_ADDRESS
from pyrf24 import RF24_PA_LOW, RF24_PA_MIN, RF24_PA_HIGH

start = time.monotonic()

def millis():
    return int((time.monotonic() - start) * 1000) % (2**32)

radio = RF24(17, 0) # CSN and CE PIN integers
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)

mesh.setNodeID(0)

previousMillis = 0

# Number representing the different message types from RF24Network
SENSOR_DATA = 1
CONFIG_COMMAND = 2


address_self = 0o0 # Node 0 is always the main node.
default_channel = 85

nodes = [5]


if not radio.begin():
    raise OSError("Radio hardware not responding")
radio.set_pa_level(RF24_PA_HIGH, False)

if not mesh.begin(default_channel):
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

def checkIncomingData():

    has_payload, pipe_number = radio.available_pipe()
    has_payload = radio.available()
    if has_payload:
        print(pipe_number)
        msg = radio.read(32)
        print(repr(msg))

    while network.available():
        print("network available")
        header, payload = network.read()
        print(header.to_string())
        
        if header.type == SENSOR_DATA:
            C, H = struct.unpack("BB",payload)
            senderID = mesh.get_node_id(header.from_node)
            print(f"Package from: {senderID}")
            print(f"C: {C}      H: {H}")

            #radio.print_pretty_details()


def sendChannelSwitch(new_channel, node, debug = False):
    msg = struct.pack("B", new_channel)
    radio.stopListening()
    ok = mesh.write(msg, CONFIG_COMMAND, node)
    radio.startListening()
    if not ok and debug:
        print("Problem sending switch command to node: " + str(node))
    elif debug:
        print("Switch command received by node: " + str(node))
    return ok

def sendChannelSwitchAll(new_channel, debug = False):
    oks = [False]*len(nodes)
    for i, node in enumerate(nodes):
        oks[i] = sendChannelSwitch(new_channel, node, debug)
    return oks

try:
    while True:
        # Call mesh.update to keep the network updated
        mesh.update()
        mesh.DHCP()
        checkIncomingData()
        time.sleep(0.001)  # delay 1 ms
except KeyboardInterrupt:
    print("Powering down.")
    radio.power = False