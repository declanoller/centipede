from pca9685_driver import Device
from time import sleep



# 0x40 from i2cdetect -y 1 (1 if Raspberry pi 2)
dev = Device(0x40)

# set the duty cycle for LED05 to 50%
dev.set_pwm(0, 204)

# set the pwm frequency (Hz)
dev.set_pwm_frequency(50)

lb = int(0.01*4097)
ub = int(0.12*4097)
for i in range(lb, ub):
    dev.set_pwm(0, i)
    print(i)
    sleep(0.01)
