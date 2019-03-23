/*     Simple Stepper Motor Control Exaple Code

    by Dejan Nedelkovski, www.HowToMechatronics.com

*/
// defines pins numbers
const int stepPin1 = 9;
const int dirPin1 = 8;
const int stepPin2 = 11;
const int dirPin2 = 10;
const int stepPin3 = 13;
const int dirPin3 = 12;
const int enablePin12 = 25;
const int enablePin3 = 24;
const int interval_mahsanit = 3000;
const int interval_motors = 500;
const int LEFT = 3;
const int RIGHT = 4;
const int UP = 5;
const int DOWN = 6;
void move_steps_mahsanit(int steps_to_move) {
  digitalWrite(enablePin3, LOW); //enable
  digitalWrite(dirPin3, LOW);
  delay(10);
  for (int x = 0; x < steps_to_move; x++) {
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(interval_mahsanit);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(interval_mahsanit);
  }
  digitalWrite(enablePin3, HIGH); //disable
  delay(10);
}

void move_motors(int steps_to_move, int dir)
{
  digitalWrite(enablePin12, LOW); //enable

  if (dir == UP) {
    digitalWrite(dirPin1, HIGH);
    digitalWrite(dirPin2, LOW);
  }
  else if (dir == DOWN) {
    digitalWrite(dirPin1, LOW);
    digitalWrite(dirPin2, HIGH);
  }
  else if (dir == LEFT) {
    digitalWrite(dirPin1, HIGH);
    digitalWrite(dirPin2, HIGH);
  }
  else { //(dir == RIGHT)
    digitalWrite(dirPin1, LOW);
    digitalWrite(dirPin2, LOW);
  }
  for (int x = 0; x < steps_to_move; x++) {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(interval_motors);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(interval_motors);

    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(interval_motors);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(interval_motors);
  }
  digitalWrite(enablePin12, HIGH); //disable
}

void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(stepPin3, OUTPUT);
  pinMode(dirPin3, OUTPUT);
  pinMode(enablePin3, OUTPUT);
}
void loop() {
  //  digitalWrite(dirPin1,HIGH); // Enables the motor to move in a particular direction
  //  digitalWrite(dirPin2,HIGH);

  // Makes 200 pulses for making one full cycle rotation
  move_steps_mahsanit(50);
  //  move_motors(20,UP);

  delay(1000); // One second delay
  delay(1000);
}
