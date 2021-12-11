import path_utils
from Servo import Servo
from DriverBoard import DriverBoard
import argparse
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('--n_servos', type=int, default='1')
parser.add_argument('--board_addr', type=int, default='41')
args = parser.parse_args()

b = DriverBoard(args.board_addr, 16)

board_limit = 16

if args.n_servos > board_limit:
    b_front = DriverBoard(40, 8)

sleep(0.5)
pairs = []
for i in range(args.n_servos):
    print(f'resetting servo index {i}')
    if i < board_limit:
        s = Servo(b, i, 1)
    else:
        s = Servo(b_front, i-board_limit, 1)
    s.reset_to_middle()
    sleep(0.1)





#




#
