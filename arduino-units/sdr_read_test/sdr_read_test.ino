#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_HIGH);
  radio.startListening();
  radio.setDataRate(RF24_2MBPS);
  radio.setChannel(85);
}

void loop() {
  if (radio.available()) {
    Serial.println("a");
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);
  }
}