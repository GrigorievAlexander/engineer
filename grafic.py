import matplotlib.pyplot as plt
import numpy as np

Z = []
with open('settings.txt', 'r', encoding='utf-8') as f:
    for line in f:
        Z.append(float(line))

Y = []
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        Y.append(int(line)*Z[1])

T = []
for i in range(len(Y)):
    T.append(i/Z[0])

fig, ax = plt.subplots()
ax.plot(T, Y)


ax.set_title('Зависимость напряжения на конденсаторе от времени')
ax.set_xlabel('Время t, с')
ax.set_ylabel('Напряжение U, В')
ax.grid()

plt.xlim(0, 12)
plt.ylim(0, 3.3)

plt.savefig('grafic.svg')
plt.show()