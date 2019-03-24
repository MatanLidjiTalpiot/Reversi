#ifndef _STACK_H
#define _STACK_H

class Stack //todo: may need to change to namespace
//todo: may need to change void to int
{
  public:
    void init();
    void spin();
    void move_steps_stack(int steps_to_move);
  private:
    // defines pins numbers
    const int step_pin_stack = 13;
    const int dir_pin_stack = 12;
    const int enable_pin_stack = 24;
    const int interval = 3000;
}

#endif // _STACK_H
