#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <RF24Network.h>

RF24 radio(7, 8); // CE, CSN/CS 

const byte address[3] = "666";
const int intervalMillis = 10000;
unsigned long previousMillis = millis();

/*

RF24_PA_MIN (0) 	-18 dBm 	-6 dBm 	-12 dBm
RF24_PA_LOW (1) 	-12 dBm 	-0 dBm 	-4 dBm
RF24_PA_HIGH (2) 	-6 dBm 	3 dBm 	1 dBm
RF24_PA_MAX (3) 	0 dBm 	7 dBm 	4 dBm 

*/

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.setPALevel(RF24_PA_HIGH);  // change PA level here
  radio.openWritingPipe(address);
  radio.setDataRate(RF24_250KBPS);
  int newChannel = 90;
  radio.setChannel(newChannel);
}

void loop() {
  // put your main code here, to run repeatedly:
  //int newChannel = 18;

  const char text[] = "Hello World";
  for (int i = 0; i < 100; i++) {
    radio.write(&text, sizeof(text));
  }
  
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= intervalMillis) { // transmits in intervals
    previousMillis = currentMillis;
    int newChannel = 84 + random(5);
    radio.setChannel(newChannel);
    Serial.println("Using channel: " + newChannel);
  } // end if internal

}
