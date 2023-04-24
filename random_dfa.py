import copy
import random

import pytest

from automata.fa.dfa import DFA


def cas_1(alphabet):
    transitions = {0: {}}
    for letter in alphabet:
        transitions[0][letter] = 0
    return DFA(states={0}, input_symbols=alphabet, transitions=transitions, initial_state=0, final_states={0})


# construit un automate déterministe fini complet aléatoirement
def random_dfa(alphabet, number_states):
    if number_states == 0:
        cas_1(alphabet)
    states = set()
    liste_letters = list(alphabet)
    for i in range(number_states):
        states.add(i)
    transitions = {}
    Ouvert = list(copy.deepcopy(states))
    Ouvert.remove(0)
    Ferme = [0]
    transitions[0] = {}
    while Ouvert:  # Pour que l'automate soit déterministe fini et tous les états sont accessibles depuis la source
        target = Ouvert[0]  # On peut prendre le premier élément de Ouvert car tous les états isolés sont équivalents
        letter = random.choice(liste_letters)
        source = random.choice(Ferme)
        while letter in transitions[source]:
            letter = random.choice(liste_letters)
            source = random.choice(Ferme)
        Ouvert.remove(target)
        transitions[source][letter] = target
        Ferme.append(target)
        transitions[target] = {}  # On initialise les transitions du nouvel état ajouté à Fermé
        print(transitions)
    print(transitions)
    for source in Ferme:  # Pour que l'automate soit complet
        for letter in alphabet:
            if not letter in transitions[source]:
                target = random.choice(Ferme)
                transitions[source][letter] = target
    final = set(random.sample(Ferme, random.randint(1, number_states)))
    print(transitions)
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=0, final_states=final)


print(random_dfa({"a", "b"}, 1000))


@pytest.mark.parametrize("nombre", range(100))
def test_random_dfa(nombre):
    number_states = random.randint(1, 5000)
    result = random_dfa({"a", "b"}, number_states)
    print(len(result._compute_reachable_states()))
    print(number_states)
    assert len(result._compute_reachable_states()) == number_states
