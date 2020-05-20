# vary thruster speed to determine stable speed range 

 

include <Servo.h> 

 

byte servoPinLeft = 9; 

byte servoPinRight = 10; 

Servo servoLeft; 

Servo servoRight; 

 

void setup() { 

 

  servoLeft.attach(servoPinLeft); 

  servoRight.attach(servoPinRight); 

 

  servoLeft.writeMicroseconds(1500); // send "stop" signal to ESC. 

  servoRight.writeMicroseconds(1500); 

 

  delay(120000); // delay to allow the ESC to recognize the stopped signal 

} 

 

void loop() { 

 

  int signal = 1550; // Set signal value, which should be between 1100 and 1900 

 

  servoLeft.writeMicroseconds(signal); // Send signal to ESC. 

  servoRight.writeMicroseconds(signal); 

 

delay(30000); 

 

servoLeft.writeMicroseconds(1650); 

servoRight.writeMicroseconds(1650); 

 

delay(20000); 

 

servoLeft.writeMicroseconds(1500); 

servoRight.writeMicroseconds(11500); 

 

delay(60000); 

} 