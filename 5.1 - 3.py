import math
import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
troyka = 13
comp = 14
leds = [2,3,4,17,27,22,10,9]
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)


def f(x):
    s = str(bin(x)[2::])
    X = [0]*(8-len(s))
    for i in s: X.append(int(i))
    return X

def adc():
    x = 0
    for i in [128, 64, 32, 16, 8, 4, 2, 1]:
        x += i
        GPIO.output(dac, f(x))
        time.sleep(0.005)
        if GPIO.input(comp) == 1:
            x -= i
    
    return x

try:
    while True:
        x = adc()
        print("Выходное напряжение: ", x*3.3/256, "В")
        y = int(8*x/256)+1
        S = [0]*8
        for i in range(y): S[i] = 1
        GPIO.output(leds, S)
        
        

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()