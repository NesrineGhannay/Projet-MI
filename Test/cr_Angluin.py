import time
from random_dfa import random_dfa
from Angluin import *
import matplotlib.pyplot as plt


abscisse = []
ordonnee = []

def add_abs_ord(debut, fin, pas):
    for i in range(debut, fin, pas):
        abscisse.append(i)
        a = time.time()
        A = random_dfa({"a", "b"}, i)
        angluin = Angluin({"a", "b"}, A, mq={}, pref={}, exp=[])
        angluin.lstar()
        b = time.time()
        ordonnee.append(b-a)

add_abs_ord(1, 10001, 1000)

plt.figure()
plt.plot(abscisse, ordonnee)
plt.xlabel("Nombre d\'états")
plt.ylabel('Temps')
plt.title('Complexité de temps d\'Angluin')
plt.legend()
plt.show()
