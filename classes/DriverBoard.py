from time import sleep
from pca9685_driver import Device



class DriverBoard:


    def __init__(self, addr, N_servos):

        # I don't want to deal with passing hex shit, so just pass addr
        # as an int.
        self.addr = addr
        self.N_servos = N_servos

        assert addr in [40, 41], 'Invalid I2C addr! : {}'.format(addr)
        assert (N_servos >= 1) and (N_servos <=16), ('N_servos out of bds in DriverBoard.__init__!' +
                                                    'Val is {}, must be >=1, <={}'.format(N_servos, N_servos))

        if addr == 40:
            self.dev = Device(0x40)
        if addr == 41:
            self.dev = Device(0x41)

        self.dev.set_pwm_frequency(50)



    def set_index_pwm(self, index, pwm):
        assert (index >= 0) and (index < self.N_servos), ('index out of bds in DriverBoard.set_index_pwm!' +
                    'Val is {}, must be >=0, <{}'.format(index, self.N_servos))

        self.dev.set_pwm(index, pwm)

























#
