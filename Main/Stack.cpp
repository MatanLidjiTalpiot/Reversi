#include "Stack.h"

void Stack::move_steps_stack(int steps_to_move) {
  digitalWrite(enable_pin_stack, LOW); //enable
  digitalWrite(dir_pin_stack, LOW);
  delay(10);
  for (int x = 0; x < steps_to_move; x++) {
    digitalWrite(step_pin_stack, HIGH);
    delayMicroseconds(interval);
    digitalWrite(step_pin_stack, LOW);
    delayMicroseconds(interval);
  }
  digitalWrite(enable_pin_stack, HIGH); //disable
  delay(10);
}

void Stack::init() {
  pinMode(step_pin_stack, OUTPUT);
  pinMode(dir_pin_stack, OUTPUT);
  pinMode(enable_pin_stack, OUTPUT);
  digitalWrite(enable_pin_stack, HIGH); //disable
}

void Stack::spin() {
  move_steps_stack(50);
  delay(100);
}
