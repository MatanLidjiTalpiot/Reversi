#include "Plotter.h"

void Plotter::move_motors(int steps_to_move, int dir)
{
  digitalWrite(enable_pin_plotter, LOW); //enable todo: maybe move after dir

  if (dir == UP) {
    digitalWrite(dir_pin_motor1, HIGH);
    digitalWrite(dir_pin_motor2, LOW);
  }
  else if (dir == DOWN) {
    digitalWrite(dir_pin_motor1, LOW);
    digitalWrite(dir_pin_motor2, HIGH);
  }
  else if (dir == LEFT) {
    digitalWrite(dir_pin_motor1, HIGH);
    digitalWrite(dir_pin_motor2, HIGH);
  }
  else { //(dir == RIGHT)
    digitalWrite(dir_pin_motor1, LOW);
    digitalWrite(dir_pin_motor2, LOW);
  }
  for (int x = 0; x < steps_to_move; x++) {
    digitalWrite(step_pin_motor1, HIGH);
    delayMicroseconds(interval_motors);
    digitalWrite(step_pin_motor1, LOW);
    delayMicroseconds(interval_motors);

    digitalWrite(step_pin_motor2, HIGH);
    delayMicroseconds(interval_motors);
    digitalWrite(step_pin_motor2, LOW);
    delayMicroseconds(interval_motors);
  }
  digitalWrite(enable_pin_plotter, HIGH); //disable
}

void Plotter::init()
{
  pinMode(step_pin_motor1, OUTPUT);
  pinMode(dir_pin_motor1, OUTPUT);
  pinMode(step_pin_motor2, OUTPUT);
  pinMode(dir_pin_motor2, OUTPUT);
  pinMode(enable_pin_plotter, OUTPUT);
  digitalWrite(enable_pin_plotter, HIGH); //disable
}

void Plotter::drop(String square)
{
  int y = sequence[0] - '0'; //yCor
  int x = sequence[1] - '0'; //xCor

  // magnetic field
  digitalWrite(switchx[x], LOW);
  digitalWrite(switchy[y], LOW);
  delay(500);

  myservo.write(servoLiftPoint);
  delay(500);
  myservo.write(servoStartPoint);
  delay(500);

  digitalWrite(switchx[x], HIGH);
  digitalWrite(switchy[y], HIGH);
  delay(100);
}
