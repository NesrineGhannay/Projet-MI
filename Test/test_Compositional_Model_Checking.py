from Compositional_Model_Checking import *
import pytest
from automata.fa.dfa import DFA


@pytest.fixture
def Input():
    return DFA(
        states={"0", "1", "2"},
        input_symbols={"a", "i", "s"},
        transitions={
            "0": {"i": "1"},
            "1": {"s": "2"},
            "2": {"a": "0"}
        },
        initial_state="0",
        final_states={"0", "1", "2"},
        allow_partial=True
    )


@pytest.fixture
def Output():
    return DFA(
        states={"0", "1", "2"},
        input_symbols={"a", "o", "s"},
        transitions={
            "0": {"s": "1"},
            "1": {"o": "2"},
            "2": {"a": "0"}
        },
        initial_state="0",
        final_states={"0", "1", "2"},
        allow_partial=True
    )


@pytest.fixture
def P():
    return completedAutomata(
        states={"0", "1"},
        alphabet={"i", "o"},
        transitions={
            "0": {"i": "1"},
            "1": {"o": "0"}
        },
        initial_state="0",
        final_states={"0", "1"}
    )


@pytest.mark.parametrize("word, alphabet, exp",
                         [("oiaubav", {"a", "b"}, "aba"),
                          ("", {"a", "b"}, ""),
                          ("zofjw", {}, "")])
def test_restriction(word, alphabet, exp):
    assert restriction(word, alphabet) == exp


@pytest.mark.parametrize("states, alphabet, transitions, initial_state, final_states, exp_s, exp_t",
                         [({"0", "1"}, {"i", "o"}, {"0": {"i": "1"}, "1": {"o": "0"}}, "0", {"0", "1"},
                           {"0", "1", "puits"}, {"0": {"i": "1", "o": "puits"}, "1": {"o": "0", "i": "puits"},
                                                 "puits": {"o": "puits", "i": "puits"}})])
def test_completedAutomata(states, alphabet, transitions, initial_state, final_states, exp_s, exp_t):
    result = completedAutomata(states, alphabet, transitions, initial_state, final_states)
    assert result.__eq__(
        DFA(states=exp_s, input_symbols=alphabet, transitions=exp_t, initial_state=initial_state,
            final_states=final_states))


#TODO : rendre l'automate complet Test.py
def test_completedAutomataByDFA(Input):
    assert completedAutomataByDFA(Input).__eq__(DFA(states={"0", "1", "puits"}, input_symbols={"i", "o"},
                                                    transitions={"0": {"i": "1", "o": "puits"},
                                                                 "1": {"o": "0", "i": "puits"},
                                                                 "puits": {"o": "puits", "i": "puits"}},
                                                    initial_state="0", final_states={"0", "1"}))


# print transitions pas necessaire


def test_synchronisation(Input, Output):
    assert synchronization(Input, Output) == {("1", "0"): {"s": ("2", "1")}, ("2", "2"): {"a": ("0", "0")}}


def test_interleaving(Input, Output):
    assert interleaving({("1", "0"): {"s": ("2", "1")}, ("2", "2"): {"a": ("0", "0")}}, Input, Output) == \
           {("1", "0"): {"s": ("2", "1")}, ("2", "2"): {"a": ("0", "0")}, ("0", "0"): {"i": ("1", "0")},
            ("2", "1"): {"o": ("2", "2")},
            ('0', '1'): {'i': ('1', '1'), 'o': ('0', '2')}, ('0', '2'): {'i': ('1', '2')},
            ('1', '1'): {'o': ('1', '2')}, }


def test_get_final_states(Input, Output):
    assert get_final_states(Input.states, Output.final_states) == {("0", "0"), ("0", "1"), ("0", "2"),
                                                                   ("1", "0"), ("1", "1"), ("1", "2"),
                                                                   ("2", "0"), ("2", "1"), ("2", "2")}


def test_parallel_composition(Input, Output):
    assert parallel_composition(Input, Output) == DFA(
        states={("0", "0"), ("1", "0"), ("2", "1"), ("2", "2")},
        input_symbols={"a", "o", "i", "s"},
        transitions={("0", "0"): {"i": ("1", "0")}, ("1", "0"): {"s": ("2", "1")}, ("2", "1"): {"o": ("2", "2")},
                     ("2", "2"): {"a": ("0", "0")}},
        initial_state=("0", "0"),
        final_states={("0", "0"), ("1", "0"), ("2", "1"), ("2", "2")},
        allow_partial=True)


def test_assumption_garantee(Input, Output, P):
    alphabet = (Input.input_symbols.union(P.input_symbols)).intersection(Output.input_symbols)
    assert assumption_garantee(alphabet, Input, Output, P) != "ERROR" #TODO :Vérifier d'abord que cela ne retourne pas erreur


def test_learning(Input, Output, P):
    alphabet = (Input.input_symbols.union(P.input_symbols)).intersection(Output.input_symbols)
    assumption = DFA(states={''}, input_symbols={'a', 's', 'o'}, transitions={'': {'a': '', 's': ''}}, initial_state='',
        final_states={''}, allow_partial=True)
    tables = [{'': 1, 'a': 1, 's': 1, 'o': 0, 'oa': 0, 'os': 0, 'oo': 0},
              {'': 'red', 'a': 'blue', 's': 'blue', 'o': 'red', 'oa': 'blue', 'os': 'blue', 'oo': 'blue'},
              ['']]
    assert learning(Input, Output, assumption, P, alphabet, tables) is not None  #TODO : à calculer à la main


@pytest.mark.parametrize("A_i, expected",
                         [(DFA(states={''}, input_symbols={'o', 'a', 's'}, transitions={'': {'a': '', 's': ''}}, initial_state='', final_states={''}, allow_partial=True),
                           "isai")])
def test_satisfies_with_composition_A_i_Input(A_i, expected, Input, P):
    compo = parallel_composition(A_i, Input)
    assert satisfies(compo, P) == expected


#TODO : tests Pauline
@pytest.mark.parametrize("M, P, expected",
                         [])
def test_satisfies_with_composition_A_i_Input(M, P, expected):
    assert satisfies(M, P) == expected


#TODO : tests unitaires de real_error, trace, copy_set, copy_transitions, extend_alphabet