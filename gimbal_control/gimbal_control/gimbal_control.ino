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
 
void setup() 
{ 
  Serial.begin(9600);
  gimbal.attach(10);  
  gimbal.write(0);
  
  // Starts power 
  pinMode(2,OUTPUT);
  digitalWrite(2,HIGH);
  
  delay(2000);
  
  for (int i = 0; i < 181; i++) {
    gimbal.write(i);
    delay(20);
    Serial.println(i);
  }
} 
 
void loop() 
{ 
}
