import path_utils
from Servo import Servo
from DriverBoard import DriverBoard
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, default='0')
args = parser.parse_args()


b = DriverBoard(41, 16)

s = Servo(b, args.index, 1)

s.reset_to_middle()













#
