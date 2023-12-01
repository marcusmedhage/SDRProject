#include <RF24.h>
#include <RF24Network.h>
#include "RF24Mesh.h"
#include <SPI.h>

RF24 radio(7, 8);
RF24Network network(radio);
RF24Mesh mesh(radio, network);

// User Configuration: nodeID - A unique identifier for each radio. Allows addressing
// to change dynamically with physical changes to the mesh.
const byte nodeID = 4;
const byte mainNode = 0;
const byte defaultChannel = 65;

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

  Serial.begin(115200);
  mesh.setNodeID(nodeID);

  // Set the PA Level to MIN and disable LNA for testing & power supply related issues
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);

  mesh.renewAddress();
  Serial.println("Starting...");
  // Connect to the mesh
  Serial.println(F("Connecting to the mesh..."));
  if (!mesh.begin(defaultChannel)) {
    if (radio.isChipConnected()) {
      do {
        // mesh.renewAddress() will return MESH_DEFAULT_ADDRESS on failure to connect
        Serial.println(F("Could not connect to network.\nConnecting to the mesh..."));
      } while (mesh.renewAddress() == MESH_DEFAULT_ADDRESS);
    } else {
      Serial.println(F("Radio hardware not responding."));
      while (1) {
        // hold in an infinite loop
      }
    }
  }
}


SensorReading simulateSensor(void) {
  // Usage: SensorReading s = simualteSensor()
  SensorReading s;
  s.C = 20 + random(5);
  s.H = 50 + random(49);
  return s;
}

void transmitData(SensorReading s, uint16_t node = 0) {
  Serial.println(s.C);
  radio.stopListening();
  bool ok = mesh.write(&s, CONFIG_COMMAND,  sizeof(s), node); // Send the data
  if (!ok) { // if error sending message
      if (!mesh.checkConnection()) { // First check connection
        Serial.println("Renewing Address"); // Refresh address if not
        if (mesh.renewAddress() == MESH_DEFAULT_ADDRESS) {
          //If address renewal fails, reconfigure the radio and restart the mesh
          //This allows recovery from most if not all radio errors
          mesh.begin();
        }
      } else {
        Serial.println("Send fail, Test OK");
      }
    } else {
      Serial.print("Send OK: ");
    }
  radio.startListening();
  if (ok == true) {
    Serial.println("SUCCESS SENDING DATA WITH id: ");
  }
  else {
    Serial.println("ERROR SENDING DATA WITH id: ");
  }
  }

void readAndSendData(long dataIntervalMillis) {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= dataIntervalMillis) { // transmits in intervals
    previousMillis = currentMillis;
    SensorReading s = simulateSensor();
    //Serial.println(s.H);
    transmitData(s, mainNode);
    }
}


void loop() {

  mesh.update();
  readAndSendData(2000);

    /*RF24NetworkHeader header;
    payload_t payload;
    network.read(header, &payload, sizeof(payload));*/
}





