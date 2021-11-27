from Leg import Leg

class LegPair:

    def __init__(self, driver_board, pair_index, **kwargs):

        # Here, pair_index N will correspond to Leg's 2*N and 2*N+1.
        # Since a Leg has 2 Servo obj's, and a Pair has 2 Leg obj's,
        # it has 4 Servo obj's, and therefore there are only 4 Pair's
        # to a driver_board.
        assert (pair_index >= 0) and (pair_index <=3), 'pair_index out of bds in Pair.__init__! Val : {}'.format(pair_index)

        self.pair_index = pair_index
        self.leg_L_index = 2*pair_index
        self.leg_R_index = 2*pair_index + 1

        self.leg_L = Leg(driver_board, 'L', self.leg_L_index, **kwargs)
        self.leg_R = Leg(driver_board, 'R', self.leg_R_index, **kwargs)
        self.legs = [self.leg_L, self.leg_R]

        self.phase_offset = 0



    def set_phase_offset(self, phase_offset):
        # This should be passed in terms of pi. It's up to a higher
        # level class to determine the relation between the diff phase_offsets.
        self.phase_offset = phase_offset
        self.leg_L.set_phase_offset(-self.phase_offset)
        self.leg_R.set_phase_offset(self.phase_offset)


    def increment(self):

        # Increments each segment of the leg.
        for leg in self.legs:
            leg.increment()



    def increment_ankles(self):

        # Increments each segment of the leg.
        for leg in self.legs:
            leg.increment_ankle()



    def reset_pair(self):
        for l in self.legs:
            l.reset_leg()











#
