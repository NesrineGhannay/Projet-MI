import time

from Angluin import *
import matplotlib.pyplot as plt

alphabet = {"a", "b"}
states = {0, "puits"}
transitions = {0 : {"a" : "puits", "b" : "puits"}, "puits" : {"a" : "puits", "b" : "puits"}}
initial_state = 0
final_states = {0}


abscissa = []
ordinate = []


for i in range(0, 101, 10):
    abscissa.append(i+2)
    automaton = DFA(states=states, input_symbols= alphabet, transitions=transitions, initial_state=initial_state, final_states=final_states)
    print(automaton)
    a = time.time()
    angluin = Angluin(alphabet=alphabet, DFA_to_learn=automaton, mq={}, pref={}, exp=[])
    result = angluin.lstar()
    b = time.time()
    print(result)
    ordinate.append(b-a)
    print(i)
    for j in range(10):
        states.add(i+j+1)
        transitions[i+j] = {"a": i+j+1, "b": i+j+1}
        transitions[i+j+1] = {"a": "puits", "b": "puits"}
        final_states = {i+j+1}

plt.figure()
plt.plot(abscissa, ordinate)
plt.xlabel("Nombre d\'états")
plt.ylabel('Temps d\'exécution d\'Angluin en secondes')
plt.title('Complexité de temps d\'Angluin')
plt.legend()
plt.show()
