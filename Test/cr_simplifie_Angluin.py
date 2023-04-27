from Angluin import *
import matplotlib.pyplot as plt

alphabet = {"a", "b"}
states = {0, "puits"}
transitions = {0 : {"a" : "puits", "b" : "puits"}, "puits" : {"a" : "puits", "b" : "puits"}}
initial_state = 0
final_states = {0}


abscisse = []
ordonnee = []

for i in range(1, 100):
    abscisse.append(i+1)
    automate = DFA(states=states, input_symbols= alphabet, transitions=transitions, initial_state=initial_state, final_states=final_states)
    a = time.time()
    angluin = Angluin(alphabet=alphabet, automate_a_apprendre=automate, mq={}, pref={}, exp=[])
    angluin.lstar()
    b = time.time()
    ordonnee.append(b-a)
    states.add(i)
    transitions[i - 1] = {"a": i, "b": i}
    transitions[i] = {"a": "puits", "b": "puits"}
    final_states = {i}


plt.figure()
plt.plot(abscisse, ordonnee)
plt.xlabel("Nombre d\'états")
plt.ylabel('Temps d\'exécution d\'Angluin en secondes')
plt.title('Complexité de temps d\'Angluin')
plt.legend()
plt.show()
