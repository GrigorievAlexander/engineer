import math
import RPi.GPIO as GPIO
import time as time
from matplotlib import pyplot

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
troyka = 13
comp = 14
leds = [2,3,4,17,27,22,10,9]
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

#Перевод в двоичную систему
def f(x):
    s = str(bin(x)[2::])
    X = [0]*(8-len(s))
    for i in s: X.append(int(i))
    return X

#Функция снятия показаний с компоратора
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
    #x - напряжение (от 0 до 256) на компораторе
    #X - массив напряжений
    #s - счетчик, считающий количество периодов измерения
    x=0
    X=[]
    start=time.time()
    s=0

    print('Зарядка')
    GPIO.output(troyka, 1)

    while x<207:
        x=adc()
        print(x)
        X.append(x)
        time.sleep(0.005)
        s+=1
        GPIO.output(leds, f(x))



    print('Разрядка')
    GPIO.output(troyka, 0)
    while x>176:
        x=adc()
        print(x)
        X.append(x)
        time.sleep(0.005)
        s+=1
        GPIO.output(leds, f(x))

    time = time.time()-start

    #Запись данных в файлы
    print('Запись данных')
    with open('data.txt', 'w') as f:
        for i in X:
            f.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write(str(1/(time/s)) + '\n')
        f.write(str(3.3/255))
    print('Общая продолжительность эксперимента: ',time)
    print('Период одного измерения: ', time/s)
    print('Средняя частота дискретизации: ', 1/(time/s))
    print('Шаг квантования АЦП:', 3.3/255)

    #Графики
    print('Построение графиков')
    y=[i/256*3.3 for i in X]
    x=[i*time/s for i in range(len(X))]
    pyplot.plot(x, y)
    pyplot.xlabel('t, с')
    pyplot.ylabel('U, В')
    pyplot.show()

        
        

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()