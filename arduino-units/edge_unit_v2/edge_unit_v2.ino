#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>

RF24 radio(7, 8); // CE, CSN/CS 
RF24Network network(radio); // RF24Network

const uint16_t selfAddress = 05; // 1st layer not base unit
const uint16_t mainAddress = 00; // address of main unit

const byte defaultChannel = 85;
unsigned long previousMillis = 0;

typedef enum { // TYPE of Message
  SENSOR_DATA,
  CONFIG_COMMAND,
} MessageType;


typedef struct {
  byte C;
  byte H;
} SensorReading;

typedef struct {
  byte newChannel;
} ConfigCommand;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  SPI.begin();
  radio.begin(); // initializes radio module to arduino
  network.begin(defaultChannel, selfAddress); //(channel, node address), preparing to network
  radio.setDataRate(RF24_2MBPS);
  radio.setAutoAck(true);
}

void loop() {
  network.update();
  checkIncomingCommands();
  readAndSendData(2000); // argument sets interval between different readings.
}


void readAndSendData(long dataIntervalMillis) {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= dataIntervalMillis) { // transmits in intervals
    previousMillis = currentMillis;
    SensorReading s = simulateSensor();
    //Serial.println(s.H);
    transmitData(s, mainAddress);
  } // end if internal
}


void checkIncomingCommands(void) {
    while ( network.available() ) { // handles incoming data
    RF24NetworkHeader header;
    network.peek(header); // to see type of message, maybe use &header

    if (header.type == CONFIG_COMMAND) {
      ConfigCommand msg;
      network.read(header, &msg, sizeof(msg)); // Read the incoming data
      switchChannel(msg.newChannel);
    }; // end if
  } // end while network available
}

void switchChannel(uint8_t newChannel) {
  network.begin(newChannel, selfAddress); // change to new channel
  Serial.print("NEW CHANNEL: ");
  Serial.println(newChannel);
}

SensorReading simulateSensor(void) {
  // Usage: SensorReading s = simualteSensor()
  SensorReading s;
  s.C = 20 + random(5);
  s.H = 50 + random(49);
  return s;
}

void transmitData(SensorReading s, uint16_t address) {
  RF24NetworkHeader header(address, SENSOR_DATA); // sends to main address
  Serial.println(s.C);
  radio.stopListening();
  bool ok = network.write(header, &s, sizeof(s)); // Send the data
  radio.startListening();
  if (ok == true) {
    Serial.println("SUCCESS SENDING DATA WITH id: ");
    Serial.println(header.id);
  }
  else {
    Serial.println("ERROR SENDING DATA WITH id: ");
    Serial.println(header.id);

  }


}

