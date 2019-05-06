from pca9685_driver import Device
from time import sleep
from math import sin, cos, pi

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--N_pairs', type=int, default='1')
parser.add_argument('--addr', type=int, default='40')
parser.add_argument('--delta', default='0.05')
args = parser.parse_args()


if args.addr == 40:
    dev = Device(0x40)
if args.addr == 41:
    dev = Device(0x41)




#dev = Device(0x41)
dev.set_pwm_frequency(50)

# This is assuming you have the pairs set up as (0,1), (2,3), etc.
# Keep in mind that they legs on opp sides will obviously be going
# in diff directions
# Also assumes that the pairs are counting sequentially in one direction
# Assumes there's two servos per leg, the first is the body one, the second
# is the leg one
N_pairs = args.N_pairs
N_legs = 2*N_pairs
N_servos = 2*N_legs

leg_servos_dict = {i:[2*i, 2*i+1] for i in range(N_legs)} # Servo indices for each leg
pairs_legs_dict = {i:[2*i, 2*i+1] for i in range(N_pairs)} # Leg indices for each pair

min_pwm = 400
max_pwm = 500

'''mid_pwm = int(0.5*(min_pwm + max_pwm))
diff_pwm = max_pwm - mid_pwm'''
mid_pwm = 312
diff_pwm = 50

for servo_pair in leg_servos_dict.values():
    for servo in servo_pair:
        dev.set_pwm(servo, mid_pwm)

# I guess I'll do the phase per leg for now, since I assume the 2
# servos for a leg should be in phase
legs_phase_dict = {i:pi*(i//2) for i in range(N_legs)}
legs_direction_dict = {i:(-1)**i for i in range(N_legs)}

i = 0
delta = float(args.delta)
delta_i = 0.05*2*pi

space_delay_sleep = 0.00
pos_sleep = 0.01

try:
    while True:
        i = (i + delta_i)%(2*pi)
        for leg, servo_pair in leg_servos_dict.items():
            sleep(space_delay_sleep)
            dev.set_pwm(servo_pair[0], int(mid_pwm + diff_pwm*sin(i*legs_direction_dict[leg] + legs_phase_dict[leg]) ))
            sleep(space_delay_sleep)
            dev.set_pwm(servo_pair[1], int(mid_pwm + diff_pwm*cos(i + legs_phase_dict[leg]) ))

        print('cur phase: {:.3f}'.format(i))
        sleep(pos_sleep)


except:
    print('exited loop')

    for servo_pair in leg_servos_dict.values():
        for servo in servo_pair:
            dev.set_pwm(servo, mid_pwm)











#
