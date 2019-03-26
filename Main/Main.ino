#include <String.h>
#include <Servo.h>

//general variables
int length = 100;
char buffer[100];
Servo myservo;


/////////////
// General //
/////////////

int* string_to_xy(String str, int prefix_size)
{
  int* ret = new int[2];
  ret[0] = str.substring(prefix_size)[0] - '0';
  ret[1] = str.substring(prefix_size)[1] - '0';
  return ret;
}

/////////////
// Plotter //
/////////////

int servoInput = 7;//pwm arduino input connected to servo
int servoStartPoint = 60;//servo deafault start point 40
int servoLiftPoint = 30;//servo correct point to lift up to 75

int step_pin_motor1 = 9;
int dir_pin_motor1 = 8;
int step_pin_motor2 = 11;
int dir_pin_motor2 = 10;
int enable_pin_plotter = 25;

int plotter_interval = 500;
int LEFT = 3;
int RIGHT = 4;
int UP = 5;
int DOWN = 6;
int one_square = 338;
int PLOTTER_OFFSET = 220;


///////////
// Board //
///////////

int in[16] = {53, 51, 49, 47, 45, 43, 41, 39, 38, 40, 42, 44, 46, 48, 50, 52};
//todo: may need to swap x and y (row and col)
int switchx[8] = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]};
int switchy[8] = {in[8], in[9], in[10], in[11], in[12], in[13], in[14], in[15]};

///////////
// Stack //
///////////

int step_pin_stack = 13;
int dir_pin_stack = 12;
int enable_pin_stack = 24;
int stack_interval = 3000;

/////////////
// Plotter //
/////////////

void plotter_move_motors(int steps_to_move, int dir)
{
  digitalWrite(enable_pin_plotter, LOW); //enable todo: maybe move after dir

  if (dir == UP)
  {
    digitalWrite(dir_pin_motor1, HIGH);
    digitalWrite(dir_pin_motor2, LOW);
  }
  else if (dir == DOWN)
  {
    digitalWrite(dir_pin_motor1, LOW);
    digitalWrite(dir_pin_motor2, HIGH);
  }
  else if (dir == LEFT)
  {
    digitalWrite(dir_pin_motor1, HIGH);
    digitalWrite(dir_pin_motor2, HIGH);
  }
  else //(dir == RIGHT)
  {
    digitalWrite(dir_pin_motor1, LOW);
    digitalWrite(dir_pin_motor2, LOW);
  }
  for (int x = 0; x < steps_to_move; x++)
  {
    digitalWrite(step_pin_motor1, HIGH);
    delayMicroseconds(plotter_interval);
    digitalWrite(step_pin_motor1, LOW);
    delayMicroseconds(plotter_interval);

    digitalWrite(step_pin_motor2, HIGH);
    delayMicroseconds(plotter_interval);
    digitalWrite(step_pin_motor2, LOW);
    delayMicroseconds(plotter_interval);
  }
  digitalWrite(enable_pin_plotter, HIGH); //disable
}

void plotter_init()
{
  pinMode(step_pin_motor1, OUTPUT);
  pinMode(dir_pin_motor1, OUTPUT);
  pinMode(step_pin_motor2, OUTPUT);
  pinMode(dir_pin_motor2, OUTPUT);
  pinMode(enable_pin_plotter, OUTPUT);
  digitalWrite(enable_pin_plotter, HIGH); //disable
}

void plotter_drop(int x, int y)
{
  // magnetic field
  digitalWrite(switchx[x], LOW);
  digitalWrite(switchy[y], LOW);
  delay(500);

  myservo.write(servoLiftPoint);
  delay(1000);

  digitalWrite(switchx[x], HIGH);
  digitalWrite(switchy[y], HIGH);
  delay(100);
  Serial.println("ended drop");
}


void plotter_move_to_square(int x, int y)
{
  //the 910 if to leave origin
  //up down
  plotter_move_motors(910 + one_square * (7 - x), UP);
  plotter_move_motors(PLOTTER_OFFSET, LEFT);
  //right left
  if (y == 7)
  {
    plotter_move_motors(one_square, RIGHT);
  }
  else
  {
    plotter_move_motors(one_square * (6 - y), LEFT);
  }
  Serial.print("done moving to square");
  Serial.print(x);
  Serial.println(y);
}
void plotter_move_to_stack(int x, int y)
{
  //right left
  plotter_move_motors(PLOTTER_OFFSET, RIGHT);

  if (y == 7)
  {
    plotter_move_motors(one_square, LEFT);
  }
  else
  {
    plotter_move_motors(one_square * (6 - y), RIGHT);
  }
  //up down
  plotter_move_motors(910 + one_square * (7 - x), DOWN);
  Serial.println("done moving back to stack");
}


///////////
// Board //
///////////


void board_init()
{
  for (int i = 0; i < 8; i++)
  {
    pinMode(switchx[i], OUTPUT);
    digitalWrite(switchx[i], HIGH);
    pinMode(switchy[i], OUTPUT);
    digitalWrite(switchy[i], HIGH);
  }
  Serial.println("Board set up finish");
}

void board_flip_square(int row, int col)
{
  //todo: check if that actually works, may need to swap x,y (row,col)
  digitalWrite(switchx[row], LOW);
  digitalWrite(switchy[col], LOW);
  delay(1000);
  digitalWrite(switchx[row], HIGH);
  digitalWrite(switchy[col], HIGH);
  delay(1000);
}

void board_flip_row(int row)
{
  for (int i = 0; i < 8; i++)
  {
    board_flip_square(row, i);
  }
}

void board_flip_column(int col)
{
  for (int i = 0; i < 8; i++)
  {
    board_flip_square(i, col);
  }
}

void board_flip_board()
{
  for (int i = 0; i < 8; i++)
  {
    for (int j = 0; j < 8; j++)
    {
      board_flip_square(i, j);
    }
  }
}

void board_flip_sequence(String sequence)
{
  int len = sequence.length(); // should be even
  for (int i = 0; i < len - 1; i += 2)
  {
    int y = sequence[i] - '0'; //yCor
    int x = sequence[i + 1] - '0'; //xCor
    board_flip_square(x, y);
    Serial.print("flipped ");
    Serial.print(x);
    Serial.println(y);
  }
}


///////////
// Stack //
///////////

void stack_move_steps(int steps_to_move)
{
  digitalWrite(enable_pin_stack, LOW); //enable
  digitalWrite(dir_pin_stack, LOW);
  delay(10);
  for (int x = 0; x < steps_to_move; x++)
  {
    digitalWrite(step_pin_stack, HIGH);
    delayMicroseconds(stack_interval);
    digitalWrite(step_pin_stack, LOW);
    delayMicroseconds(stack_interval);
  }
  digitalWrite(enable_pin_stack, HIGH); //disable
  delay(10);
}

void stack_init()
{
  pinMode(step_pin_stack, OUTPUT);
  pinMode(dir_pin_stack, OUTPUT);
  pinMode(enable_pin_stack, OUTPUT);
  digitalWrite(enable_pin_stack, HIGH); //disable
}

void stack_spin()
{
  digitalWrite(enable_pin_stack, LOW); //enable
  stack_move_steps(50);
  delay(100);
  Serial.println("stack ready");
  digitalWrite(enable_pin_stack, HIGH); //disable

}

//////////
// Main //
//////////

void setup()
{
  Serial.begin(9600);
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB
  }
  Serial.println("Serial set up finish");
  board_init();
  plotter_init(); //todo
  myservo.attach(servoInput); // connect servo to input
  myservo.write(servoStartPoint); // set servo to mid-point
  Serial.println("Plotter set up finish");
  stack_init(); //todo
}

void loop()
{
  if (Serial.available() <= 0)
  { //if we didnt get something dont enter
    return;
  }
  //now we get something and execute the actual program
  String myBuffer = "";
  myBuffer = Serial.readString();

  if (myBuffer.indexOf("move") != -1)
  {
    int* square = new int[2];
    square = string_to_xy(myBuffer, 3);
    int x = square[0] - '0';
    int y = square[1] - '0';
    Serial.println("before move to square");
    plotter_move_to_square(x, y);
    Serial.println("after move to square");
    plotter_drop(x, y);
    stack_spin();
  }

  else if (myBuffer.indexOf("flip") != -1) //assume that if we want to flip the string is flip121314
  {
    board_flip_sequence(myBuffer.substring(4));
  }

  else if (myBuffer.indexOf("back") != -1)
  {
    int* square = new int[2];
    square = string_to_xy(myBuffer, 4);
    plotter_move_to_stack(square[0], square[1]);
    delay(200);
    Serial.println("picked up disk");
    //todo: tell arduino we are done
  }

  else if (myBuffer.indexOf("u+") != -1)
  {
    plotter_move_motors(myBuffer.substring(2).toInt(), UP);
  }
  else if (myBuffer.indexOf("d+") != -1)
  {
    plotter_move_motors(myBuffer.substring(2).toInt(), DOWN);
  }
  else if (myBuffer.indexOf("l+") != -1)
  {
    plotter_move_motors(myBuffer.substring(2).toInt(), LEFT);
  }
  else if (myBuffer.indexOf("r+") != -1)
  {
    plotter_move_motors(myBuffer.substring(2).toInt(), RIGHT);
  }
  else if (myBuffer.indexOf("s+") != -1)
  {
    Serial.println("s+");
    stack_spin();
  }
  else if (myBuffer.length() != 0)
  {
    Serial.println("Error - Bad input format");
  }

  // todo: write a function that gets a place to put and a sequence of squares to flip and does everything automatically
}
