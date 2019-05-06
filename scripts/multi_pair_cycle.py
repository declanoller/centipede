import path_utils
from LegPair import LegPair
from DriverBoard import DriverBoard
import argparse
from time import time
from math import pi
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('--N_pairs', type=int, default='1')
parser.add_argument('--runtime', type=int, default='4')
parser.add_argument('--addr', type=int, default='41')
args = parser.parse_args()

b = DriverBoard(args.addr, 16)

if args.N_pairs > 4:
    b_front = DriverBoard(40, 8)

sleep(0.5)
pairs = []
for i in range(args.N_pairs):
    if i < 4:
        lp = LegPair(b, i)
    else:
        lp = LegPair(b_front, i-4)

    if i%2 == 1:
        lp.set_phase_offset(pi)
    pairs.append(lp)

start = time()
time_limit = args.runtime

while True:
    for p in pairs:
        p.increment()

    if time()-start > time_limit:
        break

for p in pairs:
    p.reset_pair()








#
