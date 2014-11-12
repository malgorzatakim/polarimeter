// Sketch to control the gimbal motor containing the polariser
// Gimbal controlled by Hobby King ESC. Connect black to ground
// and white to pin 10. (Note that you can only control servos
// on pin 9 and 10.) DO NOT CONNECT RED WIRE.
// Connect gate of transistor to pin 2.

// Run this sketch and then start the power to ESC when
// instructed by serial prompt. This needs to be replaced with
// a transistor/relay.

#include <Servo.h> 
Servo gimbal;
const int laser = 11; // PWM to control laser intensity
const int gimbalPower = 2; // to transistor to switch power to gimbal

void setup() 
{ 
  Serial.begin(9600);
  
  // laser off by default
  pinMode(laser, OUTPUT);
  analogWrite(laser, 0); 
  
  // power off to gimbal by default
  pinMode(gimbalPower,OUTPUT);
  digitalWrite(gimbalPower,LOW); 
  
  gimbal.attach(10);
  gimbal.write(0);
} 
 
void loop() 
{
  if (Serial.available() > 0) {
      int msg = Serial.read();
      
      if (msg == 76) {
        // L = laser on
        analogWrite(laser,255);
        Serial.print("1");
      } else if (msg == 108) {
        // l = laser off
        analogWrite(laser,0);
        Serial.print("1");
      } else if (msg == 71) {
        // G = start
        startGimbal();
        Serial.print("1");
      } else if (msg = 103) {
        // g = stop
        gimbal.write(0);
        digitalWrite(gimbalPower, LOW);
        Serial.print("1");
      }
  }
}

void startGimbal()
{
  digitalWrite(gimbalPower,HIGH); // Starts power 
  delay(1750);// picked this value by trial and error
  
  // have to ramp up the value like a joystick
  for (int i = 0; i < 181; i++) {
    gimbal.write(i);
    delay(25); // picked this value by trial and error
    //Serial.println(i);
  }
}
