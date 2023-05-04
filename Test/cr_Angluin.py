import time
from random_dfa import random_dfa
from Angluin import *
import matplotlib.pyplot as plt


abscissa = []
ordinate = []


def add_abs_ord(beginning, ending, step):
    for i in range(beginning, ending, step):
        abscissa.append(i)
        result = 0
        print(i)
        for j in range(100):
            A = random_dfa({"a", "b"}, i)
            a = time.time()
            angluin = Angluin({"a", "b"}, A, mq={}, pref={}, exp=[])
            angluin.lstar()
            b = time.time()
            result += b-a
        ordinate.append(result/100)

add_abs_ord(1, 100002, 10000)

plt.figure()
plt.plot(abscissa, ordinate)
plt.xlabel("Nombre d\'états")
plt.ylabel('Temps')
plt.title('Complexité de temps d\'Angluin')
plt.legend()
plt.show()
