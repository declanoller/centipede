from utils import HipKneeIndices, LeftOrRight, FrontOrBack
from Leg import Leg
from math import pi


class LegPair:

    def __init__(self, driver_board, front_or_back: FrontOrBack, 
                left_hip_knee_indices: HipKneeIndices, 
                right_hip_knee_indices: HipKneeIndices, **kwargs):

        # Here, pair_index N will correspond to Leg's 2*N and 2*N+1.
        # Since a Leg has 2 Servo obj's, and a Pair has 2 Leg obj's,
        # it has 4 Servo obj's, and therefore there are only 4 Pair's
        # to a driver_board.

        self.leg_left = Leg(driver_board, LeftOrRight.LEFT, front_or_back=front_or_back, 
                            hip_knee_indices=left_hip_knee_indices, **kwargs)
        self.leg_right = Leg(driver_board, LeftOrRight.RIGHT, front_or_back=front_or_back, 
                            hip_knee_indices=right_hip_knee_indices, **kwargs)
        self.legs = [self.leg_left, self.leg_right]

        self.phase_offset = 0
        self.phase_incr = 0.05 * 2 * pi
        self.phase = 0. if front_or_back==FrontOrBack.FRONT else pi
        self.leg_left_phase_offset = 0.
        self.leg_right_phase_offset = pi / 1.


    def increment_phase_and_move(self):
        self.phase = (self.phase + self.phase_incr) % (2 * pi)
        self.move_to_phase(self.phase)
        # sleep(self.incr_pause)


    def move_to_phase(self, phase):
        self.phase = phase
        self.leg_left.move_to_phase(self.phase + self.leg_left_phase_offset)
        self.leg_right.move_to_phase(self.phase + self.leg_right_phase_offset)


    def reset_pair(self):
        for l in self.legs:
            l.reset_leg()











#
