#include <String>
#include "Board.h"

int in[16] = {53, 51, 49, 47, 45, 43, 41, 39, 38, 40, 42, 44, 46, 48, 50, 52};
int switchx[8] = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]};
int switchy[8] = {in[8], in[9], in[10], in[11], in[12], in[13], in[14], in[15]};
int length1 = 100;
char buffer1[100];

bool starts_with_flip(String str) {
  return str.substring(0, 4) == "flip");
}

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
  Serial.write("serial connected\n");
  Board::init();
  Serial.write("finished initialization\n");
}

void loop() {
  Serial.readBytes(buffer1, length1);
  int len = 0;
  for (int i = 0; i < 100; i++) {
    if (buffer1[i] == '\0') {
      len = i + 1;
      break;
    }
  }
  Serial.write(len);
  Serial.write("\n");
  Serial.write(buffer1);
  Serial.write("\n");
  if (len > 5 && starts_with_flip(buffer1)) { //assume that if we want to flip the string is flip12
    Serial.write("flip square");
    Board::flip_square(buffer1[4] - '0', buffer1[5] - '0');
  }
  else if (len > 3 && buffer1[0] == 'c') { //assume that if we want to flip the string is col3
    Serial.write("flip column");
    Board::flip_column(buffer1[3] - '0');
  }
  else if (len > 3 && buffer1[0] == 'r') { //assume that if we want to flip the string is row5
    Serial.write("flip row");
    Board::flip_row(buffer1[3] - '0');
  }
  else {

  }
  buffer1[0] = '\0';
}
