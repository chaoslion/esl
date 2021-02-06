#include "Ultrasonic.h"
#include <Arduino.h>

int delayval = 500;

Ultrasonic ultrasonic(PIN_A6);

void setup() {
  Serial.begin(115200);
}

void loop() {
  long RangeInCentimeters;
  RangeInCentimeters = ultrasonic.MeasureInCentimeters(); // two measurements should keep an interval
  Serial.print(RangeInCentimeters);//0~400cm
  Serial.println(" cm");
  delay(100);
}
