from time import sleep
# from pca9685_driver import Device
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import busio
from board import SCL, SDA

class DriverBoard:


    def __init__(self, addr, N_servos):

        # I don't want to deal with passing hex shit, so just pass addr
        # as an int.
        self.addr = addr
        self.N_servos = N_servos

        assert addr in [40, 41], 'Invalid I2C addr! : {}'.format(addr)
        assert (N_servos >= 1) and (N_servos <=16), ('N_servos out of bds in DriverBoard.__init__!' +
                                                    'Val is {}, must be >=1, <={}'.format(N_servos, N_servos))

        '''if addr == 40:
            self.dev = Device(0x40)
        if addr == 41:
            self.dev = Device(0x41)

        self.dev.set_pwm_frequency(50)'''
        i2c = busio.I2C(SCL, SDA)

        # Create a simple PCA9685 class instance.
        self.dev = PCA9685(i2c, address = 65)
        self.dev.frequency = 50

        self.servos = [servo.Servo(self.dev.channels[i]) for i in range(16)]


    def set_servo_pwm(self, servo_index, pwm):
        assert (servo_index >= 0) and (servo_index < self.N_servos), ('servo_index out of bds in DriverBoard.set_servo_pwm!' +
                    'Val is {}, must be >=0, <{}'.format(servo_index, self.N_servos))

        self.dev.set_pwm(servo_index, pwm)


    def set_servo_angle(self, servo_index, angle):
        self.servos[servo_index].angle = angle

























#
