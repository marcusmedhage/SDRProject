#include <RF24.h>
#include <RF24Network.h>
#include "RF24Mesh.h"
#include <SPI.h>
#include <EduIntro.h>

DHT11 dht11(D6);

RF24 radio(7, 8);
RF24Network network(radio);
RF24Mesh mesh(radio, network);

// nodeID, similar to a machine address, constant and unique for each device.
const byte nodeID = 5;
const byte mainNode = 0;
byte channel = 85;
bool QUIET = false;

unsigned long previousMillis = 0;

byte C;   // temperature C readings are integers
byte H;   // humidity readings are integers


byte SENSOR_DATA = 1;
byte CONFIG_COMMAND = 2;
byte SDR_COMMAND = 3;
byte QUIET_COMMAND = 4;

typedef struct {
  byte C;
  byte H;
} SensorReading;

typedef struct {
  byte newChannel;
} ConfigCommand;

typedef struct {
  byte quiet;
} QuietCommand;

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
  if (!mesh.begin(channel)) {
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
  s.H = 50 + random(20);
  return s;
}

SensorReading readSensor(void) {
  // Usage: SensorReading s = readSensor()
  SensorReading s;
  dht11.update();
  s.C = dht11.readCelsius();
  s.H = dht11.readHumidity();
  return s;
}

void transmitData(SensorReading s, uint16_t node = 0) {
  // Usage: transmitData(SensorReading s, uint16_t to_node)
  // Sends sensor data to the desired node. By default it sends to the main node.

  Serial.print("About to send sensor data with C = ");
  Serial.println(s.C);
  radio.stopListening();
  bool ok = mesh.write(&s, SENSOR_DATA,  sizeof(s), node); // Send the data
  if (!ok) { // if error sending message
      if (!mesh.checkConnection()) { // First check connection
        Serial.println("Renewing Address"); // Refresh address if not
        if (mesh.renewAddress() == MESH_DEFAULT_ADDRESS) {
          //If address renewal fails, reconfigure the radio and restart the mesh
          //This allows recovery from most if not all radio errors
          mesh.begin(channel);
        }
      } else {
        Serial.println("Send fail, Test OK");
      }
    } else {
      Serial.print("Send OK: ");
    }
  radio.startListening();
  if (ok == true) {
    Serial.println("SUCCESS SENDING DATA. ");
    //Serial.println(radio.getARC());
  }
  else {
    Serial.println("ERROR SENDING DATA. ");
  }
  }

void readAndSendData(long dataIntervalMillis) {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= dataIntervalMillis) { // transmits in intervals
    previousMillis = currentMillis;
    SensorReading s = simulateSensor();
    transmitData(s, mainNode);
    }
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
    if (header.type == QUIET_COMMAND) {
      QuietCommand msg;
      network.read(header, &msg, sizeof(msg)); // Read the incoming data
      QUIET = msg.quiet;
    }; // end if

  } // end while network available
} // end check incoming commands

void switchChannel(uint8_t newChannel) {
  channel = newChannel;
  Serial.print("NEW CHANNEL: ");
  Serial.println(newChannel);
  mesh.setChannel(newChannel);
}

void loop() {

  mesh.update();
  checkIncomingCommands();
  if(!QUIET){
    readAndSendData(5000);
  }
  
}





