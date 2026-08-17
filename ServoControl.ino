#include <servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist;
Servo gripper;

void setup(){
    Serial.begin(9600)

    base.attach(3);
    shoulder.attach(5);
    elbow.attach(6);
    wrist.attach(9);
    gripper.attach(10);
}

void loop(){

}