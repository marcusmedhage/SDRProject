#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>
 // THIS IS THE MAIN UNIT
RF24 radio(7, 8); // CE, CSN/CS 
RF24Network network(radio); // RF24Network
const uint16_t selfAddress = 00; // MAIN UNIT

const byte defaultChannel = 0;

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

void setup() {
  SPI.begin();
  Serial.begin(115200);
  radio.begin(); // initializes radio module to arduino
  network.begin(defaultChannel, selfAddress); //(channel, node address), preparing to network
  radio.setDataRate(RF24_2MBPS);
}

void loop() {
  network.update();
  checkIncomingData();
}


void checkIncomingData(void) {
  while ( network.available() ) { // handles incoming data
      RF24NetworkHeader header;
      Message msg;
      network.read(header, &msg, sizeof(msg)); // Read the incoming data

      if (header.type == SENSOR_DATA) {
        SensorReading s = msg.data.sensorData;
        Serial.println(s.C);
      }; // end if
    } // end while network available
}

void switchChannel(uint8_t newChannel) {
  network.begin(newChannel, selfAddress); // change to new channel
}

void sendChannelSwitch(uint8_t newChannel, uint16_t address) {
  Message msg;
  msg.data.configCommand.changeChannel = true;
  msg.data.configCommand.newChannel = newChannel;
  RF24NetworkHeader header(address, CONFIG_COMMAND);
  radio.stopListening();
  network.write(header, &msg, sizeof(msg));
  radio.startListening();
}

