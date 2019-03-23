#include "Board.h"

void Board::init()
{
  for (int i = 0; i < 8; i++) {
    pinMode(switchx[i], OUTPUT);
    digitalWrite(switchx[i], HIGH);
    pinMode(switchy[i], OUTPUT);
    digitalWrite(switchy[i], HIGH);
  }
}

void Board::flip_square(int row, int col)
{
  //todo: check if that actually works
  digitalWrite(switchx[row], LOW);
  digitalWrite(switchy[col]], LOW);
  delay(1000);
  digitalWrite(switchx[row], HIGH);
  digitalWrite(switchx[col], HIGH);
  delay(1000);
}

void Board::flip_row(int row)
{
  for (int i = 0; i < 8; i++)
  {
    flip_square(row, i);
  }
}

void Board::flip_column(int col)
{
  for (int i = 0; i < 8; i++)
  {
    flip_square(i, col);
  }
}

void Board::flip_board()
{
  for (int i = 0; i < 8; i++)
  {
    for (int j = 0; j < 8; j++)
    {
      flip_square(i, j);
    }
  }
}
