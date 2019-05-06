from pca9685_driver import Device
from time import sleep

import curses
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--N_servos', type=int, default='1')
parser.add_argument('--addr', type=int, default='40')
args = parser.parse_args()


max_servo_index = args.N_servos - 1
print('Running with {} servos'.format(args.N_servos))

# 0x40 from i2cdetect -y 1 (1 if Raspberry pi 2)

print('i2c hex addr:', args.addr, type(args.addr))

if args.addr == 40:
    dev = Device(0x40)
if args.addr == 41:
    dev = Device(0x41)


dev.set_pwm_frequency(50)

max_pwm_val = 4097
min_pwm = 110
max_pwm = 515
mid_pwm = int((min_pwm + max_pwm)/2)
delta_pwm = 10

cur_servo = 0
pwm_mid_list = [452, 452, 472, 412, 302, 342, 312, 342, 312, 282, 292, 312, 312, 272, 332, 342]
pwm_dict = {i:pwm_mid_list[i] for i in range(args.N_servos)}
#init_pwm = mid_pwm
#pwm_dict = {i:init_pwm for i in range(args.N_servos)}
[dev.set_pwm(k, v) for k,v in pwm_dict.items()]


def moveCursorRefresh(stdscr):
    stdscr.move(curses.LINES - 1, curses.COLS - 1)
    stdscr.refresh() #Do this after addstr




def DCloop(stdscr):
    #https://docs.python.org/3/howto/curses.html
    #https://docs.python.org/3/library/curses.html#curses.window.clrtobot
    global cur_servo, pwm_dict, delta_pwm, mid_pwm
    move_str_pos = [2, 6]
    cur_servo_str_pos = [4, 6]
    pwm_str_pos = [6, 6]

    stdscr.erase()
    stdscr.addstr(*cur_servo_str_pos, 'Current servo: {}'.format(cur_servo))
    stdscr.addstr(*pwm_str_pos, 'Current pwm val: {}'.format(pwm_dict[cur_servo]))
    moveCursorRefresh(stdscr)

    while True:
        c = stdscr.getch()


        if c in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, 'r', 'm']:
            stdscr.erase()


        if c == curses.KEY_LEFT:
            pwm_dict[cur_servo] += delta_pwm
            stdscr.addstr(*move_str_pos, 'Pressed Left key, turning CCW')


        if c == curses.KEY_RIGHT:
            pwm_dict[cur_servo] -= delta_pwm
            stdscr.addstr(*move_str_pos, 'Pressed Right key, turning CW')


        if c == curses.KEY_UP:
            cur_servo = max(0, min(max_servo_index, cur_servo + 1))
            stdscr.addstr(*move_str_pos, 'Pressed Up key, switching servo +1')


        if c == curses.KEY_DOWN:
            cur_servo = max(0, min(max_servo_index, cur_servo - 1))
            stdscr.addstr(*move_str_pos, 'Pressed Down key, switching servo -1')


        if c == ord('r'):
            stdscr.addstr(*move_str_pos, 'Pressed r, refreshing')


        if c == ord('m'):
            pwm_dict[cur_servo] = mid_pwm
            stdscr.addstr(*move_str_pos, 'Pressed m, moving to middle position')


        if c in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ord('r'), ord('m')]:
            pwm_dict[cur_servo] = max(min_pwm, min(max_pwm, pwm_dict[cur_servo]))
            dev.set_pwm(cur_servo, pwm_dict[cur_servo])
            stdscr.addstr(*cur_servo_str_pos, 'Current servo: {}'.format(cur_servo))
            stdscr.addstr(*pwm_str_pos, 'Current pwm val: {}'.format(pwm_dict[cur_servo]))
            moveCursorRefresh(stdscr)


        if c == ord('q'):
            break  # Exit the while loop



def directControl():
    print('entering curses loop')
    curses.wrapper(DCloop)
    print('exited curses loop.')




directControl()













'''
        if c == curses.KEY_UP:
            stdscr.erase()

            stdscr.addstr(*move_str_pos, 'Pressed Up key, going straight')
            moveCursorRefresh(stdscr)


        if c == curses.KEY_DOWN:
            stdscr.erase()

            stdscr.addstr(*move_str_pos, 'Pressed Down key, going backwards')
            moveCursorRefresh(stdscr)
'''





















#
