#include <String.h>
#include <Servo.h> 

//general variables
int switchx[4] = {6,7,8,9};//arduino inputs
int switchy[4] = {2,3,4,5};//arduino inputs
int length = 100;
char buffer[100];
Servo myservo;
int servoInput = 10;//pwm arduino input connected to servo
int servoStartPoint = 195;//servo deafault start point
int servoLiftPoint = 120;//servo correct point to lift up to
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
//  Serial.println("serial set up finish");
  for(int i = 0; i< 4; i++){
    pinMode(switchx[i], OUTPUT);
    digitalWrite(switchx[i], HIGH);
  }
  for(int i = 0; i< 4; i++){
    pinMode(switchy[i], OUTPUT);
    digitalWrite(switchy[i], HIGH);
  }
//  Serial.println("cylonoids set up finish");
  myservo.attach(servoInput);//connect servo to input
  myservo.write(servoStartPoint);  // set servo to mid-point
//  Serial.println("servo drop set up finish");

  
}
void loop() {
  if(Serial.available()>0){//if we didnt get something dont enter
      //now we get something and execute the actual program
    String myBuffer = "";
    myBuffer = Serial.readString();
//    Serial.println("I got: "+myBuffer+ "\n");

    if(myBuffer.indexOf("flip")!=-1) {//assume that if we want to flip the string is flip12
      int len = myBuffer.length();
      for(int i = 0; i< (len-4)/2.0; i++){
        int str_index_1 = 4+i*2;
        int str_index_2 = 4+i*2+1;
        //got command to flip    
        char loc[2];
        loc[0] = myBuffer[str_index_1];//yCor
        loc[1] = myBuffer[str_index_2];//xCor
        int xyLoc[2];
        xyLoc[0] = loc[0]-'0'-2;//yCor
        xyLoc[1] = loc[1]-'0'-2;//xCor
        digitalWrite(switchx[xyLoc[1]], LOW);
        digitalWrite(switchy[xyLoc[0]], LOW);
    
        delay(500);
        digitalWrite(switchx[xyLoc[1]], HIGH);
        digitalWrite(switchy[xyLoc[0]], HIGH);
        delay(100);
        
      }
      
    }else if(myBuffer.indexOf("drop")!=-1){
    //drop magnet
//        Serial.println("in drop");
        char loc[2];
        loc[0] = myBuffer[4];//yCor
        loc[1] = myBuffer[5];//xCor
        int xyLoc[2];
        xyLoc[0] = loc[0]-'0'-2;//yCor
        xyLoc[1] = loc[1]-'0'-2;//xCor
        digitalWrite(switchx[xyLoc[1]], LOW);
        digitalWrite(switchy[xyLoc[0]], LOW);
        delay(500);
    
        myservo.write(servoLiftPoint);
        delay(500);

        myservo.write(servoStartPoint);    
        delay(500);
        Serial.print("ended drop");
        digitalWrite(switchx[xyLoc[1]], HIGH);
        digitalWrite(switchy[xyLoc[0]], HIGH);
        delay(500);
    }else if(myBuffer.indexOf("moveXY")!=-1){
      //got command to move the xy
//            Serial.println("No commands yet - in moveXY");
    }else if(myBuffer.indexOf("getDisk")!=-1){
      //got command to move the xy to deafault position
//            Serial.println("No commands yet - in getDisk");

    }else if (myBuffer.indexOf("loop")!=-1){
      for(int i=0; i<4; i++){
        for(int j = 0; j<4; j++){
          digitalWrite(switchx[i], LOW);
        digitalWrite(switchy[j], LOW);
    
        delay(500);
        digitalWrite(switchx[i], HIGH);
        digitalWrite(switchy[j], HIGH);
        delay(20);
        }
      }
    }
    else if(myBuffer.length()!=0){
//        Serial.println("Error - Bad input format");
    }
  }
  
}
