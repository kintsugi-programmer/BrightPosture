SoftwareSerial#include <SoftwareSerial.h>

#define TRIG 9
#define ECHO 10
#define LDR A0
#define BT_TX 2
#define BT_RX 3

SoftwareSerial BT(BT_TX, BT_RX);

void setup() {
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    pinMode(LDR, INPUT);
    
    BT.begin(9600);
    Serial.begin(9600);
}

long getDistance() {
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    return pulseIn(ECHO, HIGH) * 0.034 / 2;
}

void loop() {
    long distance = getDistance();
    int lightIntensity = analogRead(LDR);

    String data = String(distance) + "," + String(lightIntensity);
    
    BT.println(data);  // Send data to MIT App Inventor
    Serial.println(data);  // Debugging in Serial Monitor

    delay(1000);  // Wait for a second
}