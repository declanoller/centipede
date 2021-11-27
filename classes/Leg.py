
from Servo import Servo
from math import pi
from time import sleep
from utils import Side, FrontOrBack, LegPart

class Leg:

    def __init__(self, driver_board, side, front_or_back, hip_servo_index, knee_servo_index, **kwargs):

        assert side in Side, 'Leg side must be in Side! Val : {}'.format(side)
        assert front_or_back in FrontOrBack, 'front_or_back must be in FrontOrBack! Val : {}'.format(front_or_back)

        self.side = side
        self.front_or_back = front_or_back
        self.driver_board = driver_board

        self.hip_servo_index = hip_servo_index
        self.knee_servo_index = knee_servo_index

        self.incr_pause = kwargs.get('incr_pause', 0.0005)

        # I have to think about this side/direction stuff. Maybe it's a bad
        # way of thinking about it, when it's really just 1D anyway (so really
        # just diff phases, which I already have).
        self.hip = Servo(
            self.driver_board,
            self.hip_servo_index,
            direction=1,
            type='hip',
            **kwargs
        )
        self.knee = Servo(
            self.driver_board,
            self.knee_servo_index,
            direction=1,
            type='knee',
            **kwargs
        )

        self.set_phase_offset(0)
        # Also, I DEFINITELY need to set their phases separately here. I think
        # it'll probably be another top-down thing where the leg gets a phase,
        # and then uses that to set the phases of the servos.
        self.servos = [self.hip, self.knee]
        self.whole_leg_phase = 0



    def reset_leg(self):
        for s in self.servos:
            s.reset_to_middle()


    def set_phase_offset(self, phase_offset):
        # This should be passed in terms of pi. It's up to a higher
        # level class to determine the relation between the diff phase_offsets.
        self.phase_offset = phase_offset
        print(self.side, self.front_or_back)
        if self.side == Side.LEFT:
            if self.front_or_back == FrontOrBack.FRONT:
                self.hip.set_phase_offset(self.phase_offset + 0)
                self.knee.set_phase_offset(self.phase_offset + 3 * pi/2)  # have to fix
            else:
                self.hip.set_phase_offset(self.phase_offset + 0)  # back left is good
                self.knee.set_phase_offset(self.phase_offset + pi/2)
        else:
            self.hip.set_phase_offset(self.phase_offset + pi)
            self.knee.set_phase_offset(self.phase_offset + -pi/2)


    def increment(self):

        # Increments each segment of the leg.
        for s in self.servos:
            s.increment()


    def increment_knee(self):
        self.knee.increment()


    def manual_increment(self):
        self.hip.set_pwm_from_phase(self.whole_leg_phase)

        if self.front_or_back == FrontOrBack.FRONT:
            self.knee.set_pwm_from_phase(self.whole_leg_phase + 3 * pi/2)
        else:
            self.knee.set_pwm_from_phase(self.whole_leg_phase + 1 * pi/2)

        
        
        self.whole_leg_phase = (self.whole_leg_phase + 0.05 * 2 * pi) % (2 * pi)
        sleep(self.incr_pause)










#
