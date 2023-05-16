import time
from random_dfa import random_dfa
from Angluin import *
import matplotlib.pyplot as plt


abscissa = []
ordinate = []


def add_abs_ord(beginning, ending, step):
    """
    Add abscissa and ordinate. The abscissa are the number of states of the DFA and ordinate are the average time of
    Angluin's execution.

    :param beginning: the number of states of first built DFA's
    :param ending: the number of states of last built DFA's
    :param step: for each loop, we increase the number of states of "step" states.
    """
    for i in range(beginning, ending, step):
        abscissa.append(i)
        result = 0
        print(i)
        for j in range(1000):
            A = random_dfa({"a", "b"}, i)
            a = time.time()
            angluin = Angluin({"a", "b"}, A, mq={}, pref={}, exp=[])
            angluin.lstar()
            b = time.time()
            result += b-a
        ordinate.append(result/1000)


add_abs_ord(1, 10002, 1000)

plt.figure()
plt.plot(abscissa, ordinate)
plt.xlabel("Nombre d\'états")
plt.ylabel('Temps')
plt.title('Complexité de temps d\'Angluin')
plt.legend()
plt.show()
