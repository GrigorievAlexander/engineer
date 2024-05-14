import math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
troyka = 17
comp = 4
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def f(x):
    s = str(bin(x)[2::])
    return int('0'*(8-len(s)) + s)

try:
    while True:
        for i in range(256):
            x = GPIO.input(comp)
            if x == 0:
                print("Выходное напряжение: ", float(a)*3.3/256, "В")
                break
        y = f(round(float(a)))
        for i in range(8):
            GPIO.output(dac[i], int(y[i]))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
