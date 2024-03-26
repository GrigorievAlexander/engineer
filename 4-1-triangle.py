import math
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)

def f(x):
    s = str(bin(x)[2::])
    return '0'*(8-len(s)) + s

try:
    while True:
        for i0 in range(0, 256):
            a = i0
            time.sleep(1/256)
            y = f(round(float(a)))
            for i in range(8):
                GPIO.output(dac[i], int(y[i]))
        for i0 in range(0, 256):
            a = 255 - i0
            time.sleep(1/256)
            y = f(round(float(a)))
            for i in range(8):
                GPIO.output(dac[i], int(y[i]))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
