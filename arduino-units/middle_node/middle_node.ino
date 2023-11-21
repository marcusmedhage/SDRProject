#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>

RF24 radio(7, 8); // CE, CSN/CS 
RF24Network network(radio); // RF24Network
const uint16_t selfAddress = 01; // 1st layer not base unit
const uint16_t mainAddress = 00; // address of main unit

const byte defaultChannel = 0;
const int dataIntervalMillis = 2000;


unsigned long previousMillis = millis();

typedef enum { // TYPE of Message
  SENSOR_DATA,
  CONFIG_COMMAND,
} MessageType;

typedef struct {
  byte C;
  byte H;
} SensorReading;

typedef struct {
  bool changeChannel;
  byte newChannel;
} ConfigCommand;

typedef union {
  SensorReading sensorData;
  ConfigCommand configCommand;
} MessageData;

// Define the message structure with a MessageType and MessageData union
typedef struct {
  MessageType type;
  MessageData data;
} Message;

void setup() {
  // put your setup code here, to run once:
  SPI.begin();
  radio.begin(); // initializes radio module to arduino
  network.begin(defaultChannel, selfAddress); //(channel, node address), preparing to network
  radio.setDataRate(RF24_2MBPS);
}

void loop() {

  network.update();
  while ( network.available() ) { // handles incoming data
    RF24NetworkHeader header;
    Message msg;
    network.read(header, &msg, sizeof(msg)); // Read the incoming data

    if (msg.type == CONFIG_COMMAND) {
      if (msg.data.configCommand.changeChannel == true) {
          switchChannel(msg.data.configCommand.newChannel);
      } // end if channel
    }; // end if
  } // end while network available

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= dataIntervalMillis) { // transmits in intervals
    previousMillis = currentMillis;
    SensorReading s = simulateSensor();
    transmitData(s, mainAddress);
  } // end if internal

} // end loop

void switchChannel(uint8_t newChannel) {
  network.begin(newChannel, selfAddress); // change to new channel
}

/*void sendChannelSwitchAll(uint8_t newChannel) {
  Message msg;
  msg.changeChannel = true;
  msg.newChannel = newChannel;
  
  // Send the control message to all units
  for (uint16_t nodeAddress : allNodeAddresses) {
    RF24NetworkHeader header(nodeAddress);
    network.write(header, &msg, sizeof(msg));
  }
}
*/

void sendChannelSwitch(uint8_t newChannel, uint16_t address) {
  Message msg;
  msg.type = CONFIG_COMMAND;
  msg.data.configCommand.changeChannel = true;
  msg.data.configCommand.newChannel = newChannel;
  RF24NetworkHeader header(address);
  radio.stopListening();
  network.write(header, &msg, sizeof(msg));
  radio.startListening();
}

void transmitData(SensorReading s, uint16_t address) {
  RF24NetworkHeader header(address); // sends to main address
  Message msg;
  msg.type = SENSOR_DATA;
  msg.data.sensorData = s;
  radio.stopListening();
  bool ok = network.write(header, &msg, sizeof(s)); // Send the data
  radio.startListening();
}

SensorReading simulateSensor(void) {
  // Usage: SensorReading s = simualteSensor()
  SensorReading s;
  s.C = 20 + random(5);
  s.H = 50 + random(49);
  return s;
}

