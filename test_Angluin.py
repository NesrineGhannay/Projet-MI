import pytest

from Angluin import *
from automata.fa.dfa import DFA

from automata.fa.dfa import DFA
from Angluin import *

# TODO :
# 1 : faire fonctionner lstar_consistent
# 2 : simplifier le code un maximum avec les fixture
# 3 : Utiliser parametrize
# 4 : comprendre le beug avec le mq, exp, pref
# 5 : l'appliquer aussi avec odd_number

#TODO : utiliser les fixture et parametrize
# Là on a fait le test seulement pour A.
# Or on veut le faire pour tous les autres.
# On va donc faire des tests paramétriques

alphabet = {"a", "b"}

# Quelques DFA initialisés avec Angluin:

@pytest.fixture
def A():
    automate = DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "1", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"1"}
        )
    return Angluin(alphabet, automate, mq={}, pref={}, exp=[])


@pytest.fixture
def B():
    automate = DFA(states={"0", "1"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "0", "b": "1"},
            "1": {"a": "0", "b": "1"}},
        initial_state="0",
        final_states={"1"}
        )
    return Angluin(alphabet, automate, mq={}, pref={}, exp=[])

@pytest.fixture
def C():
    a = DFA(states={"0", "1", "2", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "2", "b": "puits"},
            "2": {"a": "2", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"2"}
        )
    return Angluin(alphabet, a, mq={}, pref={}, exp=[])

@pytest.fixture
def odd_number_of_1():
    a = DFA(
    states={'0', '1', '2'},
    input_symbols={'0', '1'},
    transitions={
        '0': {'0': '0', '1': '1'},
        '1': {'0': '0', '1': '2'},
        '2': {'0': '2', '1': '1'}
    },
    initial_state='0',
    final_states={'1'})
    return Angluin({"0", "1"}, a,  mq={}, pref={}, exp=[])

@pytest.fixture
def automate_test_A2():
    a = DFA(
    states={'0', '1', '2', '3'},
    input_symbols={'a', 'b'},
    transitions={
        '0': {'a': '1', 'b': '3'},
        '1': {'a': '2', 'b': '3'},
        '2': {'a': '1', 'b': '3'},
        '3': {'a': '3', 'b': '2'}
    },
    initial_state='0',
    final_states={'0', '2'})
    return Angluin(alphabet, a, mq={}, pref={}, exp=[])

# AUTOMATE LSTAR
@pytest.fixture
def automate():
    a = DFA(states={"0", "1", "2", "3"},
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
    return Angluin(alphabet, a, mq={}, pref={}, exp=[])

@pytest.fixture
def automate2():
    a = DFA(states={"0", "1", "2"},
                input_symbols={"a", "b"},
                transitions={
                    "0": {"a": "0", "b": "1"},
                    "1": {"a": "0", "b": "2"},
                    "2": {"a": "2", "b": "2"}
                },
                initial_state="0",
                final_states={"1"}
                )  # exemple du document Learning_with_Queries.pdf
    return Angluin(alphabet, a,  mq={}, pref={}, exp=[])

# List of DFA with whom we test our functions :
@pytest.fixture
def liste(A, B, C, automate_test_A2, automate, automate2): #TODO : faire fonction odd_number aussi !!!
    return [A, B, C, automate_test_A2, automate, automate2]


#Some tables :

# TABLE NON CONSISTENTE correspond au dfa automate_test_A2
mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0,'bba': 0, 'bbb': 0}
pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp0 = ['']

# TABLE QUI DEVIENT CONSISTENTE AVEC L'APPEL DE lstar_consistent()
mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1, 'bbb': 0, 'bbba': 0}
pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp = ['', 'a']

# TABLE QUI DEVIENT CONSISTENTE AVEC L'APPEL DE lstar_consistent() en choisissant le contre exemple avec b
mqb = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0,'bba': 0, 'bbb': 0, "aab" : 0, "abb" : 1, "bab" : 1, "bbab" : 0, "bbbb" : 1}
prefb = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
expb = ['', 'b']


#TODO : trouver la solution pour accéder à l'automate de automate_test_A2
table_non_consistente = Angluin({"a", "b"}, automate_test_A2, mq0, pref0, exp0)     #correspond à before_automate de test_pytest
table_consistente = Angluin({"a", "b"}, automate_test_A2, mq, pref, exp)            #correspond à learned_automate de test_pytest
table_consistente_b = Angluin({"a", "b"}, automate_test_A2, mqb, prefb, expb)


testA = Angluin({"a", "b"}, A,
                mq={"" : 0, "a" : 1, "b" : 0, "aa" : 1, "ab" : 0, "aba": 0, "abaa": 0, "abaaa" : 0, "abab" : 0, "ababa" : 0, "aaa" : 1, "ba" : 1},
                pref={"" : "red", "a" : "red", "b": "blue", "aa": "blue", "ab": "blue", "aba" : "red", "abaa":"blue", "abab":"blue"},
                exp=["", "a"])

testB = Angluin({"a", "b"}, B,
                mq={"" : 0, "a" : 0, "b" : 1, "aa" : 0, "ab" : 1, "aab": 1, "aaba": 0, "aabb" : 1},
               pref={"" : "red", "a" : "red", "b": "blue", "aa": "red", "ab": "blue", "aab" : "red", "aaba" : "blue", "aabb": "blue"},
                exp=[""])


def test_fill_the_table(A):
    A.fill_the_table("")
    A.fill_the_table("a")
    A.fill_the_table("b")
    A.fill_the_table("ab")
    A.fill_the_table("ba")
    A.fill_the_table("abba")
    A.fill_the_table("aaa")
    assert A.mq == {"" : 0, "a" : 1, "b" : 0, "ab" : 0, "ba" : 1, "abba": 0, "aaa" : 1}

def test_lstar_initialise(A):
    A.Lstar_Initialise()
    assert A.alphabet == {"a","b"}
    assert A.automate == DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "1", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"1"}
        )
    assert A.mq == {"" : 0, "a": 1, "b" : 0}
    assert A.pref == {"" : "red", "a" : "blue", "b" : "blue"}
    assert A.exp == [""]


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


def test_ligne(A):
    A.Lstar_Initialise()
    assert A.ligne("") == [0]
    assert A.ligne("a") == [1]
    assert A.ligne("b") == [0]
    assert table_consistente.ligne("") == [1, 0]
    assert table_consistente.ligne("a") == [0, 1]
    assert table_consistente.ligne("b") == [0, 0]
    assert table_consistente.ligne("ab") == [0, 0]


def test_different(A):
    A.Lstar_Initialise()
    assert A.different("a") == True     #la ligne correspondante à "a" est différente de toutes les lignes correspondantes à red
    assert A.different("b") == False
    assert table_consistente.different("ab") == False


def test_is_closed(A):
    assert table_non_consistente.is_closed() == True
    assert table_consistente.is_closed() == True
    A.Lstar_Initialise()
    assert A.is_closed() == False


def test_lstar_close(A):
    A.Lstar_Initialise()
    A.lstar_close()
    assert A.alphabet == {"a", "b"}
    assert A.automate == DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "1", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"1"}
        )
    assert A.mq == {"" : 0, "a": 1, "b" : 0, "ab" : 0, "aa" : 1}
    assert A.pref == {"" : "red", "a" : "red", "b" : "blue", "aa" : "blue", "ab" : "blue"}
    assert A.exp == [""]


def test_find_consistency_problem():
    assert table_consistente.find_consistency_problem() == [True]
    assert table_non_consistente.find_consistency_problem() == [False, ("a", "")] or table_non_consistente.find_consistency_problem() == [False, ("b", "")]
    #pour le 2nd assert c'est juste mais voir s'il y a moyen de simplifier


def test_is_consistent():
    assert table_non_consistente.is_consistent() == False       #correspond à ligne 112 de test_pytest
    assert table_consistente.is_consistent() == True
    assert table_consistente_b.is_consistent() == True



def test_lstar_consistent():
    table_non_consistente.lstar_consistent()
    assert table_non_consistente.alphabet == table_consistente.alphabet
    assert table_non_consistente.automate == table_consistente.automate
    assert table_non_consistente.mq == table_consistente.mq or table_non_consistente.mq == table_consistente_b.mq
    assert table_non_consistente.pref == table_consistente.pref
    assert table_non_consistente.exp == table_consistente.exp or table_non_consistente.exp == table_consistente_b.exp


def test_get_prefixes(A):
    mot = "abaabbb"
    assert A.get_prefixes(mot) == ["", "a", "ab", "aba", "abaa", "abaab", "abaabb", "abaabbb"]


#TODO : on admet que la méthode __eq__ est vérifiée


def test_lstar_useeq():
    A_apres = Angluin({"a", "b"},
                DFA(states={"0", "1", "puits"},
                    input_symbols={"b", "a"},
                    transitions=
                    {
                    "0": {"a": "1", "b": "0"},
                    "1": {"a": "1", "b": "puits"},
                    "puits": {"a": "puits", "b": "puits"}},
                    initial_state="0",
                    final_states={"1"}),
                mq={"": 0, "a": 1, "b":0, "aa":1, "ab":0},
                pref={"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "blue"},
                exp=[""])
    answer = "aba"
    final_A = Angluin({"a", "b"},
                      DFA(states={"0", "1", "puits"},
                          input_symbols={"b", "a"},
                          transitions=
                          {
                              "0": {"a": "1", "b": "0"},
                              "1": {"a": "1", "b": "puits"},
                              "puits": {"a": "puits", "b": "puits"}},
                          initial_state="0",
                          final_states={"1"}),
                      mq={"": 0, "a": 1, "aba" : 0, "b":0, "aa":1, "ab":0, "abb" : 0, "abaa":0, "abab":0},
                      pref={"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "red", "aba":"red", "abb":"blue", "abaa": "blue", "abab":"blue"},
                      exp=[""])
    A_apres.LSTAR_USEEQ(answer)
    assert A_apres.alphabet == final_A.alphabet
    assert A_apres.automate == final_A.automate
    assert A_apres.mq == final_A.mq
    assert A_apres.pref == final_A.pref
    assert A_apres.exp == final_A.exp


def test_lstar_build_automaton():
    resultA = testA.lstar_build_automaton()
    resultB = testB.lstar_build_automaton()
    assert resultA.__eq__(A)
    assert resultB.__eq__(B)


def test_lstar(liste):
    for a in liste:
        assert a.lstar().__eq__(a.automate)
    #TODO : ne pas oublier de le tester sur odd_number_of_1 aussi
