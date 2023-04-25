from random_dfa import random_dfa


def boucle(debut, fin, pas):
    alphabet = set()
    for i in range(10):
        alphabet.add(str(i))
        for j in range(debut, fin, pas):
            file = open("samples/" + str(j) + "etats_" + str(i+1) + ".txt", "+w")
            file.write(str(random_dfa(alphabet, j)) + "\n")
            file.close()


boucle(1, 100, 10)
boucle(100, 1000, 100)
boucle(1000, 10000, 1000)
boucle(10000, 100000, 10000)