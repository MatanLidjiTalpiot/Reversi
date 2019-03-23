#ifndef _BOARD_H
#define _BOARD_H

class Board //todo: may need to change to namespace
{
  public:
    static void init();
    static void flip_square(int row, int col);
    static void flip_row(int row);
    static void flip_column(int col);
    static void flip_board();
  private:
    static int in[16] = {53, 51, 49, 47, 45, 43, 41, 39, 38, 40, 42, 44, 46, 48, 50, 52};
    //todo: may need to swap x and y (row and col)
    static int switchx[8] = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]};
    static int switchy[8] = {in[8], in[9], in[10], in[11], in[12], in[13], in[14], in[15]};
    Board() {} // disallow creating an object
}
#endif // _BOARD_H
