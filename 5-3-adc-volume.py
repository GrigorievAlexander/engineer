import RPi.GPIO as GPIO
import time

def dec2bin(x):
    binary = bin(x)[2::].zfill(8)
    return list(map(lambda x: int(x), binary))

def adc_simple(dac):
    n = len(dac)
    for i in range(2 ** n):
        signal = dec2bin(i)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            return i
    return 255

def adc_sar(dac):
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

def set_leds(leds, value):
    GPIO.output(leds, dec2bin(value))

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
leds = [2, 3, 4, 17, 27, 22, 10, 9]


GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(leds, GPIO.HIGH)
time.sleep(1)
GPIO.output(leds, GPIO.LOW)

max_voltage = 3.3
sampling = 2 ** len(dac)

try:
    while True:
        digit_volt_simple = adc_simple(dac)
        voltage = max_voltage * digit_volt_simple / sampling
        print(f'1) curr volt: {"{:.3f}".format(voltage)}; curr digit volt: {"{:.3f}".format(digit_volt_simple)}')
        
        digit_volt_sar = adc_sar(dac)
        voltage = max_voltage * digit_volt_sar / sampling
        print(f'2) curr volt: {"{:.3f}".format(voltage)}; curr digit volt: {"{:.3f}".format(digit_volt_sar)}')
        set_leds(leds, digit_volt_simple)
        time.sleep(0.001)

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup()