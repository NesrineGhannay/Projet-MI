from Angluin import *
from automata.fa.dfa import DFA

from automata.fa.dfa import DFA
from Angluin import *

# Some DFA :

A = DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "1", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"1"}
        )

B = DFA(states={"0", "1"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "0", "b": "1"},
            "1": {"a": "0", "b": "1"}},
        initial_state="0",
        final_states={"1"}
        )

C = DFA(states={"0", "1", "2", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "2", "b": "puits"},
            "2": {"a": "2", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"2"}
        )

# DFA which matches all binary strings ending in an odd number of '1's
odd_number_of_1 = DFA(
    states={'0', '1', '2'},
    input_symbols={'0', '1'},
    transitions={
        '0': {'0': '0', '1': '1'},
        '1': {'0': '0', '1': '2'},
        '2': {'0': '2', '1': '1'}
    },
    initial_state='0',
    final_states={'1'}
)

automate_test_A2 = DFA(
    states={'0', '1', '2', '3'},
    input_symbols={'a', 'b'},
    transitions={
        '0': {'a': '1', 'b': '3'},
        '1': {'a': '2', 'b': '3'},
        '2': {'a': '1', 'b': '3'},
        '3': {'a': '3', 'b': '2'}
    },
    initial_state='0',
    final_states={'0', '2'}
)

# AUTOMATE LSTAR
automate = DFA(states={"0", "1", "2", "3"},
               input_symbols={"a", "b"},
               transitions={
                   "0": {"a": "1", "b": "3"},
                   "1": {"a": "0", "b": "2"},
                   "2": {"a": "3", "b": "1"},
                   "3": {"a": "2", "b": "0"}
               },
               initial_state="0",
               final_states={"0"}
               )  # exemple du document L_STAR_ALGO.pdf

automate2 = DFA(states={"0", "1", "2"},
                input_symbols={"a", "b"},
                transitions={
                    "0": {"a": "0", "b": "1"},
                    "1": {"a": "0", "b": "2"},
                    "2": {"a": "2", "b": "2"}
                },
                initial_state="0",
                final_states={"1"}
                )  # exemple du document Learning_with_Queries.pdf

# List of DFA with whom we test our functions :
dfa_to_test = [A, B, C, odd_number_of_1, automate_test_A2, automate, automate2]


#Some tables :

# TABLE NON CONSISTENTE
mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0,'bba': 0, 'bbb': 0}
pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp0 = ['']

# TABLE QUI DEVIENT CONSISTENTE AVEC L'APPEL DE lstar_consistent()
mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1, 'bbb': 0, 'bbba': 0}
pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp = ['', 'a']


table_non_consistente = Angluin({"a", "b"}, automate_test_A2, mq0, pref0, exp0)     #correspond à before_automate de test_Angluin_pytest
table_consistente = Angluin({"a", "b"}, automate_test_A2, mq, pref, exp)            #correspond à learned_automate de test_Angluin_pytest


def test_fill_the_table():
    angluin_A = Angluin({"a", "b"}, A)
    angluin_A.fill_the_table("")
    angluin_A.fill_the_table("a")
    angluin_A.fill_the_table("b")
    angluin_A.fill_the_table("ab")
    angluin_A.fill_the_table("ba")
    angluin_A.fill_the_table("abba")
    angluin_A.fill_the_table("aaa")
    assert angluin_A.mq == {"" : 0, "a" : 1, "b" : 0, "ab" : 0, "ba" : 1, "abba": 0, "aaa" : 1}

def test_lstar_initialise():    #apparemment test_fill_the_table modifie aussi angluin_B... ?
    angluin_B = Angluin({"a", "b"}, A)
    angluin_B.Lstar_Initialise()
    assert angluin_B.alphabet == {"a","b"}
    assert angluin_B.automate == A
    assert angluin_B.mq == {"" : 0, "a": 1, "b" : 0}
    assert angluin_B.pref == {"" : "red", "a" : "blue", "b" : "blue"}
    assert angluin_B.exp == [""]


def test_compare_ot():
    assert table_non_consistente.compareOT("", "a") == False
    assert table_non_consistente.compareOT("", "b") == False
    assert table_non_consistente.compareOT("a", "b") == True
    assert table_non_consistente.compareOT("aa", "ab") == False
    assert table_non_consistente.compareOT("", "aa") == True
    assert table_consistente.compareOT("", "a") == False
    assert table_consistente.compareOT("a", "b") == False
    assert table_non_consistente.compareOT("", "aa") == True


def test_blue():
    assert table_non_consistente.blue() == ["aa", "ab", "ba", "bba", "bbb"]
    #même blue pour table_consistente


def test_red():
    assert table_non_consistente.red() == ["", "a", "b", "bb"]
    #même red pour table_consistente


def test_ligne():
    angluin_A = Angluin({"a", "b"}, A)
    angluin_A.Lstar_Initialise()
    assert angluin_A.ligne("") == [0]
    assert angluin_A.ligne("a") == [1]
    assert angluin_A.ligne("b") == [0]
    assert table_consistente.ligne("") == [1, 0]
    assert table_consistente.ligne("a") == [0, 1]
    assert table_consistente.ligne("b") == [0, 0]
    assert table_consistente.ligne("ab") == [0, 0]


def test_different():
    angluin_A = Angluin({"a", "b"}, A)
    angluin_A.Lstar_Initialise()
    assert angluin_A.different("a") == True     #la ligne correspondante à "a" est différente de toutes les lignes correspondantes à red
    assert angluin_A.different("b") == False
    assert table_consistente.different("ab") == False


def test_is_closed():
    angluin_A = Angluin({"a", "b"}, A)
    assert table_non_consistente.is_closed() == True
    assert table_consistente.is_closed() == True
    angluin_A.Lstar_Initialise()
    assert angluin_A.is_closed() == False


def test_lstar_close():
    angluin_A = Angluin({"a", "b"}, A)
    angluin_A.Lstar_Initialise()
    angluin_A.lstar_close()
    assert angluin_A.alphabet == {"a", "b"}
    assert angluin_A.automate == A
    assert angluin_A.mq == {"" : 0, "a": 1, "b" : 0, "ab" : 0, "aa" : 1}
    assert angluin_A.pref == {"" : "red", "a" : "red", "b" : "blue", "aa" : "blue", "ab" : "blue"}
    assert angluin_A.exp == [""]


def test_find_consistency_problem():
    assert table_consistente.find_consistency_problem() == [True]
    assert table_non_consistente.find_consistency_problem() == [False, ("a", "")] or table_non_consistente.find_consistency_problem() == [False, ("b", "")]
    #pour le 2nd assert c'est juste mais voir s'il y a moyen de simplifier


def test_is_consistent():
    assert table_non_consistente.is_consistent() == False       #correspond à ligne 112 de test_Angluin_pytest
    assert table_consistente.is_consistent() == True



def test_lstar_consistent():    #TODO : fonctionne une fois sur 2 tout dépend s'il prend le contre-exemple a ou b
    table_non_consistente.lstar_consistent()
    assert table_non_consistente.alphabet == table_consistente.alphabet
    assert table_non_consistente.automate == table_consistente.automate
    assert table_non_consistente.mq == table_consistente.mq
    assert table_non_consistente.pref == table_consistente.pref
    assert table_non_consistente.exp == table_consistente.exp


def test_get_prefixes():
    angluin_A = Angluin({"a", "b"}, A)
    mot = "abaabbb"
    assert angluin_A.get_prefixes(mot) == ["", "a", "ab", "aba", "abaa", "abaab", "abaabb", "abaabbb"]


def test_lstar_useeq():
    assert False


def test_lstar_build_automaton():
    assert False


def test_lstar():
    assert False
