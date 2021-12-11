from time import sleep
from math import sin, pi
import os
import json
from pathlib import Path


def keys_to_int(x):
    new_dict = {}
    for k, v in x.items():
        if isinstance(v, dict):
            new_dict[int(k)] = keys_to_int(v)
        else:
            new_dict[int(k)] = v
    return new_dict

def load_center_pwm_from_file(board_addr, servo_index):

    center_pwm_file = Path(__file__).resolve().parent.parent / 'parameters' / 'servo_center_pwm.json'
    print('Loading center_pwm_file from {}'.format(center_pwm_file))
    assert center_pwm_file.exists(), 'servo_center_pwm.json must exist to run! If it does not, run calibrate_centers.py'

    with center_pwm_file.open('r') as f:
        servo_center_dict = json.load(f, object_hook=keys_to_int)

    assert board_addr in servo_center_dict, 'address {} not in servo_center_pwm.json! Run calibrate_centers.py'.format(board_addr)
    
    pwm_dict = servo_center_dict[board_addr]

    assert servo_index in pwm_dict, 'index {} not in servo_center_pwm.json! Run calibrate_centers.py'.format(servo_index)
    pwm_mid = pwm_dict[servo_index]

    return pwm_mid


class Servo:

    def __init__(self, driver_board, driver_index, direction, servo_type=None, **kwargs):

        # driver_board is the DriverBoard object with the pca driver object you
        # have to pass to it, so it can do things.
        # driver_index is which index of the driver_board corresponds
        # to this servo.
        # servo_type is whether it's an "knee" (attached directly to the foot for
        # U/D movement) or "hip" (attached to the body for L/R movement). Right
        # now I don't think I'll use it but it could be useful in the future.
        assert (driver_index >= 0) and (driver_index <=15), 'Driver index out of bds in Servo.__init__! Val is {}'.format(driver_index)
        assert direction in [1, -1], 'Direction must be 1 or -1! Val is {}'.format(direction)
        assert servo_type in [None, 'knee', 'hip', 'bend'], 'servo_type arg in Servo.__init__ must be in [None, knee, hip, bend]! Val is {}'.format(servo_type)
        
        self.driver_board = driver_board
        self.driver_index = driver_index

        # self.pwm_mid = load_center_pwm_from_file(self.driver_board.addr, self.driver_index)
        # print('Set self.pwm_mid to {} from file'.format(self.pwm_mid))
        self.pwm_mid = 90

        self.direction = direction
        self.phase = 0
        self.phase_offset = 0
        self.phase_incr = 0.05 * 2 * pi
        self.reset_pause = 0.05
        self.pwm_amplitude = 15  # originally 35
        self.incr_pause = kwargs.get('incr_pause', 0.005)
        self.servo_type = servo_type


        self.amp_mod = 1.0
        if self.servo_type == 'knee':
            self.amp_mod = 2.8


    def reset_to_middle(self):
        # Sets the servo to the middle of its range.
        # print('Setting index {} to pwm {}'.format(self.driver_index, self.pwm_mid))
        self.move_to_phase(0)
        sleep(self.reset_pause)


    def increment_phase_and_move(self):

        self.phase = (self.phase + self.direction * self.phase_incr) % (2 * pi)
        self.move_to_phase(self.phase)


    def move_to_phase(self, phase):
        pwm = int(self.pwm_mid + self.amp_mod * self.pwm_amplitude * sin(phase))
        self.phase = phase
        # Actually set the pwm of the servo
        # self.driver_board.set_servo_pwm(self.driver_index, pwm)
        self.driver_board.set_servo_angle(self.driver_index, pwm)
        sleep(self.incr_pause)


#
