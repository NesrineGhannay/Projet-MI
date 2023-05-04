import copy
import random

import pytest

from automata.fa.dfa import DFA


def rendre_accessible(alphabet, liste_states):
    liste_letters = list(alphabet)
    transitions = {0: {}}
    Ouvert = copy.copy(liste_states)
    Ouvert.remove(0)
    Ferme = [0]
    for target in Ouvert :  # On peut prendre n'importe quel élément de Ouvert car tous les états isolés sont équivalents
        letter = random.choice(liste_letters)
        source = random.choice(Ferme)
        while letter in transitions[source]:
            letter = random.choice(liste_letters)
            source = random.choice(Ferme)
        transitions[source][letter] = target
        Ferme.append(target)
        transitions[target] = {}  # On initialise les transitions du nouvel état ajouté à Fermé
    return transitions


def complete_alea(transitions, alphabet, liste_states):
    for source in liste_states:  # Pour que l'automate soit complet
        for letter in alphabet:
            if not letter in transitions[source]:
                target = random.choice(liste_states)
                transitions[source][letter] = target
    return transitions


# construit un automate déterministe fini complet aléatoirement
def random_dfa(alphabet, number_states, tous_finaux = False):
    liste_states = [i for i in range(number_states)]
    states = set(copy.copy(liste_states))
    transitions = rendre_accessible(alphabet, liste_states)
    transitions = complete_alea(transitions, alphabet, liste_states)
    if tous_finaux :
        final = copy.deepcopy(states)
    else :
        final = set(random.sample(liste_states, random.randint(1, number_states)))
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=0, final_states=final)


@pytest.mark.parametrize("nombre", range(100))
def test_random_dfa(nombre):
    number_states = random.randint(1, 100000)
    result = random_dfa({"a", "b"}, number_states)
    assert len(result._compute_reachable_states()) == number_states
