from time import sleep
from math import sin, pi
import os
import json

pwm_min = 400
pwm_max = 500
pwm_mid_list = [312, 452, 452, 462, 292, 345, 302, 332, 202, 292, 302, 312, 312, 282, 322, 342]
pwm_amplitude = 35

class Servo:

    def __init__(self, driver_board, driver_index, direction, type=None):

        # driver_board is the DriverBoard object with the pca driver object you
        # have to pass to it, so it can do things.
        # driver_index is which index of the driver_board corresponds
        # to this servo.
        # type is whether it's an "ankle" (attached directly to the foot for
        # U/D movement) or "hip" (attached to the body for L/R movement). Right
        # now I don't think I'll use it but it could be useful in the future.
        self.driver_board = driver_board
        self.driver_index = driver_index
        assert (driver_index >= 0) and (driver_index <=15), 'Driver index out of bds in Servo.__init__! Val is {}'.format(driver_index)

        self.load_center_pwm(self.driver_board.addr)

        self.direction = direction
        self.phase = 0
        self.phase_offset = 0
        self.phase_incr = 0.05*2*pi
        self.reset_pause = 0.4
        self.incr_pause = 0.0005
        self.type = type

        assert direction in [1, -1], 'Direction must be 1 or -1! Val is {}'.format(direction)
        assert type in [None, 'ankle', 'hip', 'bend'], 'type arg in Servo.__init__ must be in [None, ankle, hip, bend]! Val is {}'.format(type)


    def get_phase(self):
        return(self.phase)


    def servo_setup(self):

        # Does necessary setup for the servo.
        # Necessary at all?
        pass


    def reset_to_middle(self):
        # Sets the servo to the middle of its range.
        print('Setting index {} to pwm {}'.format(self.driver_index, self.pwm_mid))
        self.driver_board.set_index_pwm(self.driver_index, self.pwm_mid)
        sleep(self.reset_pause)


    def set_phase_offset(self, phase_offset):
        # This should be passed in terms of pi. It's up to a higher
        # level class to determine the relation between the diff phase_offsets.
        self.phase_offset = phase_offset


    def set_pause(self, pause):
        # I'm not sure we need the pause. There might need to be a couple
        # of them actually. One might be so the board doesn't get confused if it
        # gets too many commands too quickly, but another might be so that the movements
        # of the servos actually happen (i.e., if you tell it to go one way and then
        # the other way immediately after, it might just do nothing cause it doesn't
        # have time to do either).
        self.pause = pause


    def increment(self):

        # Increments only the phase, depending on the direction.
        # Note: does NOT include phase_offset here.
        self.phase += self.direction*self.phase_incr
        self.phase = self.phase%(2*pi)
        self.update_angle()


    def update_angle(self):
        # This sets the servo to the angle specified by phase and phase_offset.

        # So this is doing it in a way I might want to change in the future.
        # self.phase will always be between 0 and 2*pi, but the angle it gets set to
        # will be phase + phase_offset. This will hopefully have the nice feature that
        # many servos will have the same phase, but their diff positions will only be
        # det'd by their phase_offsets.

        # The servo will oscillate around self.pwm_mid, so the max/min should be self.pwm_mid +- pwm_amplitude.

        pwm = int(self.pwm_mid + pwm_amplitude*sin(self.phase + self.phase_offset))

        #assert (pwm >= pwm_min) and (pwm <= pwm_max), 'pwm out of bds: {}. Must be between {} and {}.'.format(pwm, pwm_min, pwm_max)

        self.driver_board.set_index_pwm(self.driver_index, pwm)
        sleep(self.incr_pause)



    def load_center_pwm(self, board_addr):

        self.pwm_mid = pwm_mid_list[self.driver_index]

        addr_str = str(board_addr)
        center_file = '../parameters/servo_center_pwm.json'

        if os.path.exists(center_file):

            with open(center_file, 'r') as f:
                servo_center_dict = json.load(f)

            if addr_str in servo_center_dict.keys():
                pwm_dict = servo_center_dict[addr_str]
                pwm_dict = {int(k):v for k,v in pwm_dict.items()}
                self.pwm_mid = pwm_dict[self.driver_index]

#
