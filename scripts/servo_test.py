import path_utils
from Servo import Servo
from DriverBoard import DriverBoard
import argparse
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, default='0')
parser.add_argument('--runtime', type=int, default='2')
parser.add_argument('--addr', type=int, default='41')
parser.add_argument('--pause', type=float, default='0.005')
args = parser.parse_args()

b = DriverBoard(args.addr, 16)

s = Servo(b, args.index, 1, incr_pause=args.pause)

start = time()

while True:
    s.increment()
    print('cur phase: {:.2f}'.format(s.get_phase()))
    if time()-start > args.runtime:
        break



s.reset_to_middle()













#
