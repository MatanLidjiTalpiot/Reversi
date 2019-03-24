#include <String.h>
#include <Servo.h>

//general variables
int length = 100;
char buffer[100];
Servo myservo;
int servoInput = 10;//pwm arduino input connected to servo
int servoStartPoint = 195;//servo deafault start point
int servoLiftPoint = 120;//servo correct point to lift up to

void setup()
{
  Serial.begin(9600);
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB
  }
  Serial.println("Serial set up finish");
  Board::init()
  Serial.println("Board set up finish");
  Plotter::init() //todo
  myservo.attach(servoInput); // connect servo to input
  myservo.write(servoStartPoint); // set servo to mid-point
  Serial.println("Plotter set up finish");
  Stack::init() //todo
}

void loop() {
  if (Serial.available() <= 0) { //if we didnt get something dont enter
    return;
  }
  //now we get something and execute the actual program
  String myBuffer = "";
  myBuffer = Serial.readString();
  
  if (myBuffer.indexOf("move") != -1)
  {
    Plotter::move_to(myBuffer.substring(4));
  }

  else if (myBuffer.indexOf("flip") != -1) //assume that if we want to flip the string is flip12
  {
    Board::flip_sequnce(myBuffer.substring(4));
  }

  else if (myBuffer.indexOf("takedisk") != -1)
  {
    Plotter::move_to_stack(); // this function needs to get the current location?
    Stack::spin();
    //todo: tell arduino we are done
  }

  else if (myBuffer.indexOf("drop") != -1)
  {
    Plotter::drop(myBuffer.substring(4));
    Serial.print("ended drop");
  }

  else if (myBuffer.length() != 0) {
    //        Serial.println("Error - Bad input format");
  }
}
