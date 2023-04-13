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

# Some initialisations
angluin_A = Angluin({"a", "b"}, A)


#Some tables :

# TABLE NON CONSISTENTE
mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0,'bba': 0, 'bbb': 0}
pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp0 = ['']

# TABLE QUI DEVIENT CONSISTENTE AVEC L'APPEL DE lstar_consistent()
mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1, 'bbb': 0, 'bbba': 0}
pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp = ['', 'a']


table_non_consistente = Angluin({"a", "b"}, A, mq0, pref0, exp0)      #TODO : Quels sont les automates qui pourraient convenir à ces tables ? (Ici j'ai mis A par défaut : n'impacte pas les résultats de compare_OT)
table_consistente = Angluin({"a", "b"}, A, mq, pref, exp)


def test_fill_the_table():
    angluin_A.fill_the_table("")
    angluin_A.fill_the_table("a")
    angluin_A.fill_the_table("b")
    angluin_A.fill_the_table("ab")
    angluin_A.fill_the_table("ba")
    angluin_A.fill_the_table("abba")
    angluin_A.fill_the_table("aaa")
    assert angluin_A.mq == {"" : 0, "a" : 1, "b" : 0, "ab" : 0, "ba" : 1, "abba": 0, "aaa" : 1}


def test_lstar_initialise():
    angluin_A.Lstar_Initialise()
    assert angluin_A.alphabet == {"a","b"}
    assert angluin_A.automate == A
    assert angluin_A.mq == {"" : 0, "a": 1, "b" : 0}
    assert angluin_A.pref == {"" : "red", "a" : "blue", "b" : "blue"}
    assert angluin_A.exp == [""]


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
    angluin_A.Lstar_Initialise()
    assert angluin_A.ligne("") == [0]
    assert angluin_A.ligne("a") == [1]
    assert angluin_A.ligne("b") == [0]
    assert table_consistente.ligne("") == [1, 0]
    assert table_consistente.ligne("a") == [0, 1]
    assert table_consistente.ligne("b") == [0, 0]
    assert table_consistente.ligne("ab") == [0, 0]


def test_different():
    angluin_A.Lstar_Initialise()
    assert angluin_A.different("a") == True     #la ligne correspondante à "a" est différente de toutes les lignes correspondantes à red
    assert angluin_A.different("b") == False
    assert table_consistente.different("ab") == False


def test_is_closed():
    assert table_non_consistente.is_closed() == True
    assert table_consistente.is_closed() == True
    angluin_A.Lstar_Initialise()
    assert angluin_A.is_closed() == False


def test_lstar_close():
    angluin_A.Lstar_Initialise()
    angluin_A.lstar_close()
    assert angluin_A.alphabet == {"a", "b"}
    assert angluin_A.automate == A
    assert angluin_A.mq == {"" : 0, "a": 1, "b" : 0, "ab" : 0, "aa" : 1}
    assert angluin_A.pref == {"" : "red", "a" : "red", "b" : "blue", "aa" : "blue", "ab" : "blue"}
    assert angluin_A.exp == [""]


def test_find_consistency_problem():
    assert False


def test_is_consistent():
    assert False


def test_lstar_consistent():
    assert False


def test_get_prefixes():
    assert False


def test_lstar_useeq():
    assert False


def test_lstar_build_automaton():
    assert False


def test_lstar():
    assert False
