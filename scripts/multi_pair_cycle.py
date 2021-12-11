import path_utils
from LegPair import LegPair
from DriverBoard import DriverBoard
from utils import FrontOrBack, HipKneeIndices
import argparse
from time import time, sleep
from math import pi

parser = argparse.ArgumentParser()
parser.add_argument('--runtime', type=int, default='2')
parser.add_argument('--addr', type=int, default='41')
parser.add_argument('--pause', type=float, default='0.01')
args = parser.parse_args()

b = DriverBoard(args.addr, 16)

# in the format of [left leg indices, right leg indices]
leg_pair_infos = [
    ([(4, 3), (6, 1)], FrontOrBack.FRONT),
    ([(5, 0), (7, 2)], FrontOrBack.BACK),
]

# Create all leg pairs
leg_pairs = []
for leg_pair_indices, front_or_back in leg_pair_infos:
    leg_pairs.append(
                    LegPair(
                        b,
                        front_or_back,
                        HipKneeIndices(*leg_pair_indices[0]),
                        HipKneeIndices(*leg_pair_indices[1]),
                        incr_pause=args.pause,
                    )
    )


# Start loop
start = time()
while True:
    for leg_pair in leg_pairs:
        leg_pair.increment_phase_and_move()
    if time() - start > args.runtime:
        break

for leg_pair in leg_pairs:
    leg_pair.reset_pair()

#
