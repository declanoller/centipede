import path_utils

from pca9685_driver import Device
from time import sleep

from pathlib import Path
import curses
import argparse
import json
import os

from Servo import keys_to_int

'''
This is to create a servo_center_pwm.json file
that the servos will look at to get their center
values. It will overwrite any that's there.

It will be first indexed by the I2C board_addr (40 or 41)
and then the board index.
'''


parser = argparse.ArgumentParser()
parser.add_argument('--board_addr', type=int, default='41')
args = parser.parse_args()

backup_pwm_mid_list = [190, 312, 442, 292, 292, 305, 282, 192, 312, 282, 292, 312, 312, 272, 332, 342]
pwm_dict = {i:val for i,val in enumerate(backup_pwm_mid_list)}

board_addr = args.board_addr
center_pwm_file = Path(__file__).resolve().parent.parent / 'parameters' / 'servo_center_pwm.json'
print('Attempting to load center_pwm_file from {}'.format(center_pwm_file))
if center_pwm_file.exists():
    print('\nOpening {} and reading dict...'.format(center_pwm_file))
    with center_pwm_file.open('r') as f:
        servo_center_dict = json.load(f, object_hook=keys_to_int)

    print('center pwm file keys: ', servo_center_dict.keys())
    if board_addr in servo_center_dict:
        print('\nBoard addr {} in center file, setting pwm_dict to it'.format(board_addr))
        pwm_dict = servo_center_dict[board_addr]
        print('pwm_dict:')
        [print('{}  :  {}'.format(k, v)) for k,v in pwm_dict.items()]
    else:
        print('\nBoard addr {} NOT in center file, using default.'.format(board_addr))
else:
    print('\nFile {} does not exist, using default pwm list.'.format(center_pwm_file))
    servo_center_dict = {}




# 0x40 from i2cdetect -y 1 (1 if Raspberry pi 2)
print('i2c hex board_addr:', args.board_addr, type(args.board_addr))
if args.board_addr == 40:
    dev = Device(0x40)
if args.board_addr == 41:
    dev = Device(0x41)

dev.set_pwm_frequency(50)


min_pwm = 110
max_pwm = 515
mid_pwm = int((min_pwm + max_pwm)/2)
delta_pwm = 10

cur_servo = 0
#[dev.set_pwm(k, v) for k,v in pwm_dict.items()]


def moveCursorRefresh(stdscr):
    stdscr.move(curses.LINES - 1, curses.COLS - 1)
    stdscr.refresh() #Do this after addstr


def DCloop(stdscr):
    #https://docs.python.org/3/howto/curses.html
    #https://docs.python.org/3/library/curses.html#curses.window.clrtobot
    global cur_servo, pwm_dict, delta_pwm, mid_pwm
    max_servo_index = 16 - 1
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

print('\n\nWriting new pwm_dict for board_addr {} to file.'.format(board_addr))
servo_center_dict[board_addr] = pwm_dict
print(servo_center_dict)
print(pwm_dict[0], type(board_addr), type(pwm_dict[0]))
with center_pwm_file.open('w+') as f:
    json.dump(servo_center_dict, f, indent=4)



exit()






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
