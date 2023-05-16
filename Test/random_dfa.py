import copy
import random

import pytest

from automata.fa.dfa import DFA


def set_accessible(alphabet, liste_states):
    """
    Makes reachable all states from the initial state "0".

    :param alphabet:
    :param liste_states:

    :return: the initial transitions
    """
    list_letters = list(alphabet)
    transitions = {0: {}}
    waited_list = copy.copy(liste_states)
    waited_list.remove(0)
    closed = [0]
    for target in waited_list :  # On peut prendre n'importe quel élément de Ouvert car tous les états isolés sont équivalents
        letter = random.choice(list_letters)
        root = random.choice(closed)
        while letter in transitions[root]:
            letter = random.choice(list_letters)
            root = random.choice(closed)
        transitions[root][letter] = target
        closed.append(target)
        transitions[target] = {}  # On initialise les transitions du nouvel état ajouté à Fermé
    return transitions


def complete_randomly(transitions, alphabet, liste_states, p):
    """
    Complete randomly and partially the DFA's transitions with the alphabet "alphabet" and the parameter p.

    :param alphabet:
    :param liste_states:
    :param transitions: the transitions to complete.
    :param p: it's used to create randomly transitions.

    :return: the completed transitions
    """
    for source in liste_states:  # Pour que l'automate soit complet
        for letter in alphabet:
            if not letter in transitions[source]:
                if random.random() < p :
                    target = random.choice(liste_states)
                    transitions[source][letter] = target
    return transitions


def random_dfa(alphabet, number_states, all_final = False, p=1):
    """
    Build randomly a DFA with the alphabet "alphabet", number_states.

    :param alphabet:
    :param number_states:
    :param all_final: if this parameter is True, so all states are final, else the final states are random.
    :param p: it's used to create randomly transitions.

    :return: the random DFA
    """
    list_states = [i for i in range(number_states)]
    states = set(copy.copy(list_states))
    transitions = set_accessible(alphabet, list_states)
    transitions = complete_randomly(transitions, alphabet, list_states, p)
    if all_final :
        final = copy.deepcopy(states)
    else :
        final = set(random.sample(list_states, random.randint(1, number_states)))
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=0, final_states=final, allow_partial=True)


@pytest.mark.parametrize("nombre", range(100))
def test_random_dfa(nombre):
    """
    Check that all states are reachable
    """
    number_states = random.randint(1, 100000)
    result = random_dfa({"a", "b"}, number_states)
    assert len(result._compute_reachable_states()) == number_states
