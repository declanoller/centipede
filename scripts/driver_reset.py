import RPi.GPIO as GPIO
from time import sleep

def driver_reset():

    output_enable_pin = 11 # This is pin 11/GPIO 17.
    off_time = 1.5

    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(output_enable_pin, GPIO.OUT, initial=GPIO.LOW)

    print('\n\nSetting pin 11 (GPIO 17) to HIGH to reset...')
    GPIO.output(output_enable_pin, GPIO.HIGH)

    print('\nKeeping off for {} s...'.format(off_time))
    sleep(off_time)

    print('\nSetting pin 11 (GPIO 17) to LOW to turn back on...')
    GPIO.output(output_enable_pin, GPIO.LOW)

    print('\nDone!\n\n')


    GPIO.cleanup()



if __name__ == '__main__':

    driver_reset()







#
