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


#Instances de tables pour tester la consistence

# Pour A2 :
@pytest.fixture
def non_consistent_A2():
    mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0, 'bba': 0, 'bbb': 0}
    pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
             'bbb': 'blue'}
    exp0 = ['']
    return Angluin(alphabet, samples.A2, mq0, pref0, exp0)


@pytest.fixture
def consistent_a_A2():
    mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1,
      'bbb': 0, 'bbba': 0}
    pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
        'bbb': 'blue'}
    exp = ['', 'a']
    return Angluin(alphabet, samples.A2, mq, pref, exp)


@pytest.fixture
def consistent_b_A2():
    mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0, 'bba': 0, 'bbb': 0, "aab": 0, "abb": 1, "bab": 1,
       "bbab": 0, "bbbb": 1}
    pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
         'bbb': 'blue'}
    exp = ['', 'b']
    return Angluin(alphabet, samples.A2, mq, pref, exp)


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


def test_compare_ot(non_consistent_A2):
    assert non_consistent_A2.compareOT("", "a") == False
    assert non_consistent_A2.compareOT("", "b") == False
    assert non_consistent_A2.compareOT("a", "b") == True
    assert non_consistent_A2.compareOT("aa", "ba") == False
    assert non_consistent_A2.compareOT("ab", "bb") == False


def test_blue(non_consistent_A2):
    assert non_consistent_A2.blue() == ["aa", "ab", "ba", "bba", "bbb"]


def test_red(non_consistent_A2):
    assert non_consistent_A2.red() == ["", "a", "b", "bb"]


def test_ligne(consistent_a_A2):
    A = Angluin(alphabet, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.ligne("") == [0]
    assert A.ligne("a") == [1]
    assert A.ligne("b") == [0]
    assert consistent_a_A2.ligne("") == [1, 0]
    assert consistent_a_A2.ligne("a") == [0, 1]
    assert consistent_a_A2.ligne("b") == [0, 0]
    assert consistent_a_A2.ligne("ab") == [0, 0]


def test_different(consistent_a_A2):
    A = Angluin(alphabet, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.different("a") == True     #la ligne correspondante à "a" est différente de toutes les lignes correspondantes à red
    assert A.different("b") == False
    assert consistent_a_A2.different("ab") == False


def test_is_closed(non_consistent_A2):
    A = Angluin(alphabet, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.is_closed() == False
    assert non_consistent_A2.is_closed() == True


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
def test_find_consistency_problem(non_consistent_A2, consistent_a_A2):
    assert consistent_a_A2.find_consistency_problem() == [True]
    result = non_consistent_A2.find_consistency_problem()
    assert result == [False, ("a", "")] or result == [False, ("b", "")]


def test_is_consistent(non_consistent_A2, consistent_a_A2, consistent_b_A2):
    assert non_consistent_A2.is_consistent() == False
    assert consistent_a_A2.is_consistent() == True
    assert consistent_b_A2.is_consistent() == True


def test_lstar_consistent(non_consistent_A2, consistent_a_A2, consistent_b_A2):
    non_consistent_A2.lstar_consistent()
    assert non_consistent_A2.alphabet == consistent_a_A2.alphabet
    assert non_consistent_A2.automate == samples.A2
    assert non_consistent_A2.mq == consistent_a_A2.mq or non_consistent_A2.mq == consistent_b_A2.mq
    assert non_consistent_A2.pref == consistent_a_A2.pref
    assert non_consistent_A2.exp == consistent_a_A2.exp or non_consistent_A2.exp == consistent_b_A2.exp


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
