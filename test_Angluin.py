import pytest
from Angluin import *
import samples

alphabet = {"a", "b"}

# List of DFA with whom we test our functions :
@pytest.fixture
def liste_angluin():
    result = []
    for a in samples.liste:
        if a == samples.odd:
            result.append(Angluin({"0", "1"}, a, mq={}, pref={}, exp=[]))
        else:
            result.append(Angluin(alphabet, a, mq={}, pref={}, exp=[]))
    return result



@pytest.mark.parametrize("nom, expected",
                         [(samples.A, {"" : 0, "a" : 1, "b" : 0, "ab" : 0, "ba" : 1, "abba": 0, "aaa" : 1}),
                          (samples.B, {"" : 0, "a" : 0, "b" : 1, "ab" : 1, "ba" : 0, "abba": 0, "aaa" : 0}),
                          (samples.C, {"" : 0, "a" : 0, "b" : 0, "ab" : 0, "ba" : 0, "abba": 0, "aaa" : 1}),
                          (samples.A2, {"" : 1, "a" : 0, "b" : 0, "ab" : 0, "ba" : 0, "abba": 0, "aaa" : 0}),
                          (samples.automate, {"" : 1, "a" : 0, "b" : 0, "ab" : 0, "ba" : 0, "abba": 1, "aaa" : 0}),
                          (samples.automate2, {"" : 0, "a" : 0, "b" : 1, "ab" : 1, "ba" : 0, "abba": 0, "aaa" : 0})])
def test_fill_the_table(nom, expected):
    a = Angluin(alphabet, nom, mq={}, pref={}, exp=[])
    a.fill_the_table("")
    a.fill_the_table("a")
    a.fill_the_table("b")
    a.fill_the_table("ab")
    a.fill_the_table("ba")
    a.fill_the_table("abba")
    a.fill_the_table("aaa")
    assert a.mq == expected


@pytest.mark.parametrize("nom, expected_mq",
                        [(samples.A, {"" : 0, "a" : 1, "b" : 0}),
                          (samples.B, {"" : 0, "a" : 0, "b" : 1}),
                          (samples.C, {"" : 0, "a" : 0, "b" : 0}),
                          (samples.A2, {"" : 1, "a" : 0, "b" : 0}),
                          (samples.automate, {"" : 1, "a" : 0, "b" : 0}),
                          (samples.automate2, {"" : 0, "a" : 0, "b" : 1})])
def test_lstar_initialise(nom, expected_mq):
    a = Angluin(alphabet, nom, mq={}, pref={}, exp=[])
    a.Lstar_Initialise()
    assert a.alphabet == {"a", "b"}
    assert a.automate == a.automate
    assert a.mq == expected_mq
    assert a.pref == {"" : "red", "a" : "blue", "b" : "blue"}
    assert a.exp == [""]

#TODO
def test_compare_ot():
    assert samples.table_non_consistente.compareOT("", "a") == False
    assert samples.table_non_consistente.compareOT("", "b") == False
    assert samples.table_non_consistente.compareOT("a", "b") == True
    assert samples.table_non_consistente.compareOT("aa", "ab") == False
    assert samples.table_non_consistente.compareOT("", "aa") == True
    assert samples.table_consistente.compareOT("", "a") == False
    assert samples.table_consistente.compareOT("a", "b") == False
    assert samples.table_non_consistente.compareOT("", "aa") == True


def test_blue():
    assert samples.table_non_consistente.blue() == ["aa", "ab", "ba", "bba", "bbb"]
    #même blue pour samples.table_consistente


def test_red():
    assert samples.table_non_consistente.red() == ["", "a", "b", "bb"]
    #même red pour samples.table_consistente


def test_ligne():
    A = Angluin(alphabet, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.ligne("") == [0]
    assert A.ligne("a") == [1]
    assert A.ligne("b") == [0]
    assert samples.table_consistente.ligne("") == [1, 0]
    assert samples.table_consistente.ligne("a") == [0, 1]
    assert samples.table_consistente.ligne("b") == [0, 0]
    assert samples.table_consistente.ligne("ab") == [0, 0]


def test_different():
    A = Angluin(alphabet, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.different("a") == True     #la ligne correspondante à "a" est différente de toutes les lignes correspondantes à red
    assert A.different("b") == False
    assert samples.table_consistente.different("ab") == False


def test_is_closed():
    A = Angluin(alphabet, samples.A, mq={}, pref={}, exp=[])
    assert samples.table_non_consistente.is_closed() == True
    assert samples.table_consistente.is_closed() == True
    A.Lstar_Initialise()
    assert A.is_closed() == False

@pytest.mark.parametrize("nom, mq0, pref0, exp0, expected_mq, expected_pref",
                         [(samples.A, {"" : 0, "a" : 1, "b" : 0}, {"" : "red", "a": "blue", "b" : "blue"}, [""],
                           {"" : 0, "a" : 1, "b" : 0, "aa" : 1, "ab" : 0},
                           {"" : "red", "a": "red", "b" : "blue", "aa":"blue", "ab":"blue"}),
                          (samples.B, {"": 0, "a": 0, "b": 1}, {"": "red", "a": "blue", "b": "blue"},[""],
                           {"": 0, "a": 0, "b": 1, "ba": 0, "bb": 1},
                           {"": "red", "b": "red", "a": "blue", "ba": "blue", "bb": "blue"})
                          ])
def test_lstar_close(nom, mq0, pref0, exp0, expected_mq, expected_pref):
    a = Angluin(alphabet, nom, mq0, pref0, exp0.copy())
    a.lstar_close()
    assert a.alphabet == {"a", "b"}
    assert a.automate == nom
    assert a.mq == expected_mq
    assert a.pref == expected_pref
    assert a.exp == exp0


#TODO
def test_find_consistency_problem():
    assert samples.table_consistente.find_consistency_problem() == [True]
    assert samples.table_non_consistente.find_consistency_problem() == [False, ("a", "")] or samples.table_non_consistente.find_consistency_problem() == [False, ("b", "")]
    #pour le 2nd assert c'est juste mais voir s'il y a moyen de simplifier


def test_is_consistent():
    assert samples.table_non_consistente.is_consistent() == False       #correspond à ligne 112 de test_pytest
    assert samples.table_consistente.is_consistent() == True
    assert samples.table_consistente_b.is_consistent() == True



def test_lstar_consistent():
    samples.table_non_consistente.lstar_consistent()
    assert samples.table_non_consistente.alphabet == samples.table_consistente.alphabet
    assert samples.table_non_consistente.automate == samples.table_consistente.automate
    assert samples.table_non_consistente.mq == samples.table_consistente.mq or samples.table_non_consistente.mq == samples.table_consistente_b.mq
    assert samples.table_non_consistente.pref == samples.table_consistente.pref
    assert samples.table_non_consistente.exp == samples.table_consistente.exp or samples.table_non_consistente.exp == samples.table_consistente_b.exp


def test_get_prefixes():
    a = Angluin(alphabet, samples.A, mq={}, pref={}, exp=[])
    mot = "abaabbb"
    assert a.get_prefixes(mot) == ["", "a", "ab", "aba", "abaa", "abaab", "abaabb", "abaabbb"]


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
    resultA = samples.testA.lstar_build_automaton()
    resultB = samples.testB.lstar_build_automaton()
    assert resultA.__eq__(samples.A)
    assert resultB.__eq__(samples.B)


def test_lstar(liste_angluin):
    for a in liste_angluin:
        assert a.lstar().__eq__(a.automate)
