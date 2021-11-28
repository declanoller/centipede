
from Servo import Servo
from math import pi
from time import sleep
from utils import LeftOrRight, FrontOrBack, LegPart

class Leg:

    def __init__(self, driver_board, left_or_right, front_or_back, hip_servo_index, knee_servo_index, **kwargs):

        assert left_or_right in LeftOrRight, 'Leg side must be in LeftOrRight! Val : {}'.format(left_or_right)
        assert front_or_back in FrontOrBack, 'front_or_back must be in FrontOrBack! Val : {}'.format(front_or_back)

        self.left_or_right = left_or_right
        self.front_or_back = front_or_back
        self.driver_board = driver_board

        self.hip_servo_index = hip_servo_index
        self.knee_servo_index = knee_servo_index

        self.incr_pause = kwargs.get('incr_pause', 0.005)
        self.phase_incr = 0.05 * 2 * pi
        self.direction = -1  # should determine this from left_or_right etc

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

        # Also, I DEFINITELY need to set their phases separately here. I think
        # it'll probably be another top-down thing where the leg gets a phase,
        # and then uses that to set the phases of the servos.
        self.servos = [self.hip, self.knee]
        self.phase = 0.
        self.hip_phase_offset = 0.

        if self.front_or_back == FrontOrBack.FRONT:
            self.knee_phase_offset = 3 * pi/2
        else:
            self.knee_phase_offset = 1 * pi/2


    def reset_leg(self):
        for s in self.servos:
            s.reset_to_middle()


    def increment(self):
        self.phase = (self.phase + self.direction * self.phase_incr) % (2 * pi)
        
        self.hip.move_to_phase(self.phase + self.hip_phase_offset)
        self.knee.move_to_phase(self.phase + self.knee_phase_offset)

        # sleep(self.incr_pause)










#
