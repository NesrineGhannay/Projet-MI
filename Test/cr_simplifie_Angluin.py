from Angluin import *
import matplotlib.pyplot as plt

alphabet = {"a", "b"}
states = {0, "puits"}
transitions = {0 : {"a" : "puits", "b" : "puits"}, "puits" : {"a" : "puits", "b" : "puits"}}
initial_state = 0
final_states = {0}


abscisse = []
ordonnee = []


for i in range(0, 2000001, 250000):
    abscisse.append(i+2)
    automate = DFA(states=states, input_symbols= alphabet, transitions=transitions, initial_state=initial_state, final_states=final_states)
    a = time.time()
    angluin = Angluin(alphabet=alphabet, automate_a_apprendre=automate, mq={}, pref={}, exp=[])
    angluin.lstar()
    b = time.time()
    ordonnee.append(b-a)
    for j in range(250000):
        states.add(i+j+1)
        transitions[i+j] = {"a": i+j+1, "b": i+j+1}
        transitions[i+j+1] = {"a": "puits", "b": "puits"}
        final_states = {i+j+1}

plt.figure()
plt.plot(abscisse, ordonnee)
plt.xlabel("Nombre d\'états")
plt.ylabel('Temps d\'exécution d\'Angluin en secondes')
plt.title('Complexité de temps d\'Angluin')
plt.legend()
plt.show()
