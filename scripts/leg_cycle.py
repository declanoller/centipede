import path_utils
from Leg import Leg
from DriverBoard import DriverBoard
import argparse
from time import time
from utils import LeftOrRight, FrontOrBack

parser = argparse.ArgumentParser()
parser.add_argument('--hip_index', type=int, required=True)
parser.add_argument('--knee_index', type=int, required=True)
parser.add_argument('--side', type=LeftOrRight, required=True, choices=list(LeftOrRight))
parser.add_argument('--front_or_back', type=FrontOrBack, required=True, choices=list(FrontOrBack))

parser.add_argument('--runtime', type=int, default='2')
parser.add_argument('--addr', type=int, default='41')
parser.add_argument('--pause', type=float, default='0.005')
args = parser.parse_args()

b = DriverBoard(args.addr, 16)

leg = Leg(b, args.side, args.front_or_back, args.hip_index, args.knee_index, incr_pause=args.pause)

start = time()

while True:
    leg.increment()
    if time() - start > args.runtime:
        break

leg.reset_leg()







#
