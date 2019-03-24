#ifndef _PLOTTER_H
#define _PLOTTER_H

class Plotter
{
  public:
    void Plotter::move_motors(int steps_to_move, int dir);
    void Plotter::init();
    void Plotter::drop(String square);
  private:
    // defines pins numbers
    const int step_pin_motor1 = 9;
    const int dir_pin_motor1 = 8;
    const int step_pin_motor2 = 11;
    const int dir_pin_motor2 = 10;
    const int enable_pin_plotter = 25;

    const int interval = 500;
    const int LEFT = 3;
    const int RIGHT = 4;
    const int UP = 5;
    const int DOWN = 6;
}
#endif //_PLOTTER_H
