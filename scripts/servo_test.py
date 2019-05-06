import path_utils
from Servo import Servo
from DriverBoard import DriverBoard
import argparse
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, default='0')
args = parser.parse_args()

b = DriverBoard(41, 16)

s = Servo(b, args.index, 1)

start = time()
time_limit = 2

while True:
    s.increment()
    print('cur phase: {:.2f}'.format(s.get_phase()))
    if time()-start > time_limit:
        break



s.reset_to_middle()













#
