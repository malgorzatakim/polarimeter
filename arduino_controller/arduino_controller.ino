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
const int voltageCheckPin = 1; // analog pin
boolean voltageOk = false; // start false because it hasn't been checked yet

// need to keep track of gimbal status because if it's already on
// and you try and turn it on it will stop and then restart.
boolean gimbalOn = false;

// keep track of laser
boolean laserOn = false;

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
      
      voltageOk = voltageCheck();
        
      if (voltageOk == true) {     
        if (msg == 76) {          // L = laser on
          laserStart();
          Serial.print("1");
        } else if (msg == 108) {  // l = laser off
          laserStop();
          Serial.print("1");
        } else if (msg == 71) {   // G = start
          // only switch it on if it's not running
          if (gimbalOn == false) {
            startGimbal();
            gimbalOn = true;
          }
          Serial.print("1");
        } else if (msg = 103) {   // g = stop
          stopGimbal();
          Serial.print("1");
        }
      } else {
        // Arduino isn't connected to the power supply; respond to all
        // commands with V
        Serial.print("V");
      }
  }
  
  // check if the power has gone off
  voltageOk = voltageCheck();
  
  // if power has gone off and stuff is on, switch it off
  if (voltageOk == false && gimbalOn == true) {
    stopGimbal();
  } else if (voltageOk == false && laserOn == true) {
    laserStop();
  }
}

void laserStart() {
  analogWrite(laser,255);
  laserOn = true;
}

void laserStop() {
  analogWrite(laser,0);
  laserOn = false;
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

void stopGimbal() {
  gimbal.write(0);
  digitalWrite(gimbalPower, LOW);
  gimbalOn = false;
}

bool voltageCheck() {
  // do voltage check
  int val = analogRead(voltageCheckPin);
  // through fiddling/debugging, val around 520 means that it's powered off
  // the power supply. Around 300, means it's on the USB.
  if (val > 500) {
    return true;
  } else {
    return false;
  }
}
