import RPi.GPIO as GPIO
import time

def dec2bin(x):
    binary = bin(x)[2::].zfill(8)
    return list(map(lambda x: int(x), binary))

def adc(dac):
    n = len(dac)
    number = 0
    for i in range(n-1, 1, -1):
        number = number | (1 << i)
        signal = dec2bin(number)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            number = number & ~(1 << i)
    return number

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13


GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

max_voltage = 3.3
sampling = 2 ** len(dac)

try:
    while True:
        digit_volt = adc(dac)
        voltage = max_voltage * digit_volt / sampling
        print(f'curr volt: {"{:.3f}".format(voltage)}; curr digit volt: {"{:.3f}".format(digit_volt)}')
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()
    print('end.')