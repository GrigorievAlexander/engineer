import math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)

def f(x):
    s = str(bin(x)[2::])
    return '0'*(8-len(s)) + s

try:
    while True:
        a = input()
        if a == 'q':
            break
        else:
            print("Выходное напряжение: ", float(a)*3.3/256, "В")
            y = f(round(float(a)))
            for i in range(8):
                GPIO.output(dac[i], int(y[i]))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
