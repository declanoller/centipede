
from Servo import Servo
from math import pi


class Leg:

    def __init__(self, driver_board, side, leg_index):

        assert side in ['L', 'R'], 'Leg side must be L or R! Val : {}'.format(side)

        self.side = side
        self.driver_board = driver_board
        # Okay, so decision to make... It might get tricky with how to assign
        # the indices for everything in a top-down way. I think I'm gonna say,
        # leg_index N corresponds to Servo indices 2*N and 2*N+1, where 2*N is the "hip"
        # (conn'd directly to body) and 2*N+1 is the "ankle" (conn'd to foot).

        # Therefore, leg_index can only go from only 0-7, because it will map to
        # servos 0-15.
        assert (leg_index >= 0) and (leg_index <=7), 'leg_index out of bds in Leg.__init__! Val is {}'.format(leg_index)

        self.leg_index = leg_index
        self.hip_index = 2*leg_index
        self.ankle_index = 2*leg_index + 1

        # I have to think about this side/direction stuff. Maybe it's a bad
        # way of thinking about it, when it's really just 1D anyway (so really
        # just diff phases, which I already have).
        self.hip = Servo(self.driver_board, self.hip_index, 1, type='hip')
        self.ankle = Servo(self.driver_board, self.ankle_index, 1, type='ankle')

        self.set_phase_offset(0)
        # Also, I DEFINITELY need to set their phases separately here. I think
        # it'll probably be another top-down thing where the leg gets a phase,
        # and then uses that to set the phases of the servos.
        self.servos = [self.hip, self.ankle]



    def reset_leg(self):
        for s in self.servos:
            s.reset_to_middle()


    def set_phase_offset(self, phase_offset):
        # This should be passed in terms of pi. It's up to a higher
        # level class to determine the relation between the diff phase_offsets.
        self.phase_offset = phase_offset

        if self.side == 'L':
            self.hip.set_phase_offset(self.phase_offset + 0)
            self.ankle.set_phase_offset(self.phase_offset + pi/2)
        else:
            self.hip.set_phase_offset(self.phase_offset + pi)
            self.ankle.set_phase_offset(self.phase_offset + -pi/2)


    def increment(self):

        # Increments each segment of the leg.
        for s in self.servos:
            s.increment()


    def increment_ankle(self):
        self.ankle.increment()













#
