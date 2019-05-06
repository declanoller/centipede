import path_utils
from LegPair import LegPair
from DriverBoard import DriverBoard
import argparse
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, default='0')
args = parser.parse_args()

b = DriverBoard(41, 16)

leg_pair = LegPair(b, args.index)
leg_pair.set_phase_offset(0)

start = time()
time_limit = 4

while True:
    leg_pair.increment()
    if time()-start > time_limit:
        break

leg_pair.reset_pair()







#
