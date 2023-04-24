import copy
import random
from automata.fa.dfa import DFA

#construit un automate déterministe fini complet aléatoirement
def random_dfa(alphabet, number_states):
    states = set()
    liste_letters = list(alphabet)
    for i in range(number_states):
        states.add(i)
    transitions = {}
    Ouvert = list(copy.deepcopy(states))
    Ouvert.remove(0)
    Ferme = [0]
    while Ouvert:   #Pour que l'automate soit déterministe fini et tous les états sont accessibles depuis la source
        target = Ouvert[0]  #On peut prendre le premier élément de Ouvert car tous les états isolés sont équivalents
        letter = random.choice(liste_letters)
        source = random.choice(Ferme)
        Ouvert.remove(target)
        transitions[source] = {letter : target}
        Ferme.append(target)
        transitions[target] = {}    #On initialise les transitions de la source au cas où si plus tard le choix aléatoire ne lui attribue aucune transition
    for source in Ferme:
        for letter in alphabet:
            if not letter in transitions[source]:
                target = random.choice(Ferme)
                transitions[source][letter] = target
    final = set(random.sample(Ferme, random.randint(1, number_states)))
    print(final)
    print(transitions)
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=0, final_states=final)

print(random_dfa({"a", "b"}, 1000))