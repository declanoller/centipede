import path_utils
from Leg import Leg
from DriverBoard import DriverBoard
import argparse
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, default='0')
args = parser.parse_args()

b = DriverBoard(41, 16)

leg = Leg(b, 'L', args.index)

start = time()
time_limit = 2

while True:
    leg.increment()
    if time()-start > time_limit:
        break

leg.reset_leg()







#
