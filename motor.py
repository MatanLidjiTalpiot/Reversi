from image_control_xy_movement import get_move_and_dist

def left(steps):
    pass
def right(steps):
    pass
def up(steps):
    pass
def down(steps):
    pass
# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# print("found %d devices" % len(nearby_devices))
#
# for addr, name in nearby_devices:
#     print("  %s - %s" % (addr, name))

# region ---CONSTANST---
BLUETOOTH_ADDRESS = '00:16:53:0E:0B:F5'
MAX_POWER = 127
INPUT_ERROR = "input error please enter a direction (u,d,r,l) and than a " \
              "number in degrees"
SLOPE = 0.0111  # degrees = cm/SLOPE
LEFT_SLOPE = 0.0093

MIN_DIST_REQUIRED_MOVE = 1 #CM
MAX_CM_MOVMENT = 56
# the system is being dragd up when moving left by this ratio
UP_DRAG_LEFT_SLOPE = 0.0017  # DRAG_UP = cm_left/UP_DRAG_LEFT_SLOPE
# endregion ---CONSTANST---

# region ---INITIALIZE---
"""initialize the program variabels"""
brick = blue.BlueSock(BLUETOOTH_ADDRESS).connect()
print("connected")

m_left = Motor(brick, PORT_A)
m_right = Motor(brick, PORT_C)
both_same = nxt.SynchronizedMotors(m_left, m_right, 0)
both_oposite_A = nxt.SynchronizedMotors(m_right, m_left, MAX_POWER)
both_oposite_B = nxt.SynchronizedMotors(m_left, m_right, MAX_POWER)


# endregion ---INITIALIZE---

def move_XY(y, x):
    if x > 0:
        left(x)
    else:
        right(-x)
    if y > 0:
        up(y)
    else:
        down(-y)

def move_to_xy_with_monitoring(move):
    x_y_dist = get_move_and_dist(move)
    y_dist = x_y_dist[0]
    x_dist = x_y_dist[1]
    dist = x_y_dist[2]
    print(y_dist, x_dist, dist)
    while dist > MIN_DIST_REQUIRED_MOVE:
        move_XY(y_dist, x_dist)
        x_y_dist = get_move_and_dist(move)
        y_dist = x_y_dist[0]
        x_dist = x_y_dist[1]
        dist = x_y_dist[2]



# region ---MOVMENTS---
def check_movment_vality(cm):
    if cm > MAX_CM_MOVMENT:
        return False


def down(cm):
    degrees = cm / SLOPE
    both_same.turn(-MAX_POWER, degrees)


def up(cm):
    degrees = cm / SLOPE
    both_same.turn(MAX_POWER, degrees)


def left(cm):
    degrees = cm / LEFT_SLOPE
    both_oposite_A.turn(100, degrees)
    up_drag_cm = degrees * UP_DRAG_LEFT_SLOPE
    print(up_drag_cm)
    down(up_drag_cm)


def right(cm):
    degrees = cm / SLOPE
    both_oposite_B.turn(100, degrees)


# endregion ---MOVMENTS---

def manual_commands():
    try:
        print("enter direction: ", end='')
        command = input()
        if command == 'du':  # make a small adjusment up
            up(120 * SLOPE)
            down(90 * SLOPE)
        elif command == 'dd':  # make a small adjusment down
            up(90 * SLOPE)
            down(120 * SLOPE)
        elif command == 'dr':  # make a small adjusment right
            left(90 * LEFT_SLOPE)
            right(120 * SLOPE)
        elif command == 'dl':  # make a small adjusment left
            right(90 * SLOPE)
            left(120 * LEFT_SLOPE)
        else:
            print("enter centimeters: ", end='')
            degrees = int(input())
            if degrees < 0:
                print("degrees < 0 please enter a positive number")
            elif command == "up" or command == 'u':
                up(degrees)
            elif command == "down" or command == 'd':
                down(degrees)
            elif command == "left" or command == 'l':
                left(degrees)
            elif command == "right" or command == 'r':
                right(degrees)
            else:
                print("direction must be one of u,d,l,r")
    except Exception as e:
        # print("cast exception if the input enter again")
        print("Exception: ", end='')
        print(e)


if __name__ == '__main__':
    while True:
        manual_commands()
