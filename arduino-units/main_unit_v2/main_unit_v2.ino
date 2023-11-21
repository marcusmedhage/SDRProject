#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>
 // THIS IS THE MAIN UNIT
RF24 radio(7, 8); // CE, CSN/CS 
RF24Network network(radio); // RF24Network
const uint16_t selfAddress = 00; // MAIN UNIT

const byte defaultChannel = 76;

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
    network.peek(header); // to see type of message, maybe use &header

      if (header.type == SENSOR_DATA) {
        SensorReading s;
        network.read(header, &s, sizeof(s)); // Read the incoming data
        Serial.println(s.C);
      }; // end if
    } // end while network available
}

void switchChannel(uint8_t newChannel) {
  network.begin(newChannel, selfAddress); // change to new channel
}

void sendChannelSwitch(uint8_t newChannel, uint16_t address) {
  ConfigCommand msg;
  msg.newChannel = newChannel;
  RF24NetworkHeader header(address, CONFIG_COMMAND);
  radio.stopListening();
  network.write(header, &msg, sizeof(msg));
  radio.startListening();
}

