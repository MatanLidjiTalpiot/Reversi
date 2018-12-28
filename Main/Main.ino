#include <String.h>
#include <Servo.h> 

//general variables
int switchx[4] = {2,3,4,5};//arduino inputs
int switchy[4] = {6,7,8,9};//arduino inputs
int length = 100;
char buffer[100];
Servo myservo;
int servoInput = 10;//pwm arduino input connected to servo
int servostartPoint = 0;//servo deafault start point
int servoLiftPoint = 50;//servo correct point to lift up to
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
//  printf("serial set up finish");
  Serial.println("serial set up finish");
  for(int i = 0; i< 4; i++){
    pinMode(switchx[i], OUTPUT);
    digitalWrite(switchx[i], HIGH);
  }
  for(int i = 0; i< 4; i++){
    pinMode(switchy[i], OUTPUT);
    digitalWrite(switchy[i], HIGH);
  }
  Serial.println("cylonoids set up finish");
  myservo.attach(servoInput);//connect servo to input
  myservo.write(servostartPoint);  // set servo to mid-point
  Serial.println("servo drop set up finish");

  
}
void convertInputFlipToLoc4x4(char loc[2]){
  char x = loc[0];
  char y  = loc[1];
  int intY = y - 'a'+1;
  y = intY+'0';
  x = x-3;
  y = y-3;
  loc[0] = x;
  loc[1] = y;
}
void loop() {
  if(Serial.available()>0){//if we didnt get something dont enter
      //now we get something and execute the actual program
    String myBuffer = "";
    myBuffer = Serial.readString();
    Serial.println("I got: "+myBuffer+ "\n");

    if(myBuffer.indexOf("flip")!=-1) {//assume that if we want to flip the string is flip1b
      //got command to flip    
      char loc[2];
      loc[0] = myBuffer[4];//xCor
      loc[1] = myBuffer[5];//yCor
      convertInputFlipToLoc4x4(loc);
      int xyLoc[2];
      xyLoc[0] = loc[0]-'0';//xCor
      xyLoc[1] = loc[1]-'0';//yCor
      digitalWrite(switchx[xyLoc[0]], LOW);
      digitalWrite(switchy[xyLoc[1]], LOW);
  
      delay(500);
      digitalWrite(switchx[xyLoc[0]], HIGH);
      digitalWrite(switchy[xyLoc[1]], HIGH);
      delay(500);
      
    }else if(myBuffer.indexOf("drop")!=-1){
    //drop magnet
        myservo.write(servoLiftPoint);//move to point 50
        delay(500);
        myservo.write(servostartPoint);
    }else if(myBuffer.indexOf("move")!=-1){
      //got command to move the xy
            Serial.println("No commands yet - in moveXY");
    }else if(myBuffer.indexOf("getDisk")!=-1){
      //got command to move the xy to deafault position
            Serial.println("No commands yet - in getDisk");

    }else if(myBuffer.indexOf("LED")!=-1){
      
    }
  }
}
