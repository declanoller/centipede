from DriverBoard import DriverBoard
from LegPair import LegPair
from Bend import Bend

class Centipede:

    def __init__(self, board_addrs, **kwargs):


        self.N_pairs = kwargs.get('N_pairs', 1)
        self.N_bends = kwargs.get('N_bends', 0)

        if len(board_addrs) == 0:
            board_addrs = [board_addrs]

        self.board_addrs = board_addrs
        self.driver_boards = []

        for b_a in self.board_addrs:
            self.driver_boards.append(DriverBoard(b_a, 16))


        for










#
