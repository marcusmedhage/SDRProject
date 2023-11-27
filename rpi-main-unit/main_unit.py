import sys
import time
import argparse
import struct
from enum import Enum
import random
from pyrf24 import RF24, RF24Network, RF24NetworkHeader, RF24_PA_LOW, RF24_2MBPS, RF24_1MBPS


radio = RF24(17, 0) # CSN and CE PIN integers
network = RF24Network(radio)


previousMillis = int(time.time_ns()/1000000)

# Number representing the different message types from RF24Network
SENSOR_DATA = 0
CONFIG_COMMAND = 1


address_self = 0o0 # Node 0 is always the main node.
default_channel = 85

addresses = [0o5] # Address of other units

print("Starting!")
if not radio.begin():
    raise OSError("Radio hardware not responding")
#radio.set_pa_level(RF24_PA_LOW)

#radio.dynamic_payloads = True
#radio.ack_payloads = True

radio.channel = default_channel
network.begin(address_self)
radio.setDataRate(RF24_1MBPS)
radio.tx_delay = 200 # uS delay, needed since arduino slower
radio.set_auto_ack(True)


def checkIncomingData():
    while network.available():
        print("available")
        header, payload = network.read()
        print(header.to_string())

        if header.type == SENSOR_DATA:
            print("Test")
            C, H = struct.unpack("BB",payload)
            print(f"C: {C}      H: {H}")


def sendChannelSwitch(new_channel, address):
    header = RF24NetworkHeader(address, CONFIG_COMMAND)
    msg = struct.pack("B", new_channel)
    radio.stopListening()
    network.write(header, msg)
    radio.startListening()    

def sendChannelSwitchAll(new_channel):
    for address in addresses:
        sendChannelSwitch(new_channel, address)


def send_then_switch(intervalMillis):
    global previousMillis
    currentMillis = int(time.time_ns()/1000000)
    if (currentMillis - previousMillis >= intervalMillis):
        previousMillis = currentMillis
        new_channel = random.randint(60,90)
        sendChannelSwitchAll(new_channel)
        print("Switching Channel")
        print(f"old: {radio.channel}")
        radio.channel = new_channel
        print(f"new: {radio.channel}")


try:
    while True:
        network.update()
        checkIncomingData()
        #send_then_switch(1000000)
except KeyboardInterrupt:
    print("Shuttting down.")
    radio.power = False
