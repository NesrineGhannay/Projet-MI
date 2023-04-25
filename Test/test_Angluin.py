import copy

import pytest
from Angluin import *
from samples import samples

alphabet_ab = {"a", "b"}
alphabet_01 = {"0", "1"}


# Liste de tous les Angluins formées avec les DFA de sample :
@pytest.fixture
def liste_angluin():
    result = []
    for a in samples.liste:
        if a == samples.odd:
            result.append(Angluin(alphabet_01, a, mq={}, pref={}, exp=[]))
        else:
            result.append(Angluin(alphabet_ab, a, mq={}, pref={}, exp=[]))
    return result


# Instances de tables pour tester la consistence

# Pour A2 :
@pytest.fixture
def non_consistent_a2():
    mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0, 'bba': 0, 'bbb': 0}
    pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
             'bbb': 'blue'}
    exp0 = ['']
    return Angluin(alphabet_ab, samples.A2, mq0, pref0, exp0)


@pytest.fixture
def consistent_a_a2():
    mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1,
          'bbb': 0, 'bbba': 0}
    pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
            'bbb': 'blue'}
    exp = ['', 'a']
    return Angluin(alphabet_ab, samples.A2, mq, pref, exp)


@pytest.fixture
def consistent_b_a2():
    mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0, 'bba': 0, 'bbb': 0, "aab": 0, "abb": 1, "bab": 1,
          "bbab": 0, "bbbb": 1}
    pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
            'bbb': 'blue'}
    exp = ['', 'b']
    return Angluin(alphabet_ab, samples.A2, mq, pref, exp)

odd_number_of_1_version2 = DFA(input_symbols= alphabet_01, states= {0, 1},
                               transitions={0: {"0" : 0, "1" : 1}, 1:{"0" : 1, "1" : 0}}, initial_state=0, final_states={1})


@pytest.mark.parametrize("nom, expected",
                         [(samples.A, {"": 0, "a": 1, "b": 0, "ab": 0, "ba": 1, "abba": 0, "aaa": 1}),
                          (samples.B, {"": 0, "a": 0, "b": 1, "ab": 1, "ba": 0, "abba": 0, "aaa": 0}),
                          (samples.C, {"": 0, "a": 0, "b": 0, "ab": 0, "ba": 0, "abba": 0, "aaa": 1}),
                          (samples.odd, {"": 0, "0": 0, "1": 1, "00": 0, "01" : 1, "10": 1, "11": 0}),
                          (samples.A2, {"": 1, "a": 0, "b": 0, "ab": 0, "ba": 0, "abba": 0, "aaa": 0}),
                          (samples.automate, {"": 1, "a": 0, "b": 0, "ab": 0, "ba": 0, "abba": 1, "aaa": 0}),
                          (samples.automate2, {"": 0, "a": 0, "b": 1, "ab": 1, "ba": 0, "abba": 0, "aaa": 0})])
def test_fill_the_table(nom, expected):
    if nom == samples.odd:
        a = Angluin(alphabet_01, nom, mq={}, pref={}, exp=[])
        a.fill_the_table("")
        a.fill_the_table("0")
        a.fill_the_table("1")
        a.fill_the_table("00")
        a.fill_the_table("01")
        a.fill_the_table("10")
        a.fill_the_table("11")
    else :
        a = Angluin(alphabet_ab, nom, mq={}, pref={}, exp=[])
        a.fill_the_table("")
        a.fill_the_table("a")
        a.fill_the_table("b")
        a.fill_the_table("ab")
        a.fill_the_table("ba")
        a.fill_the_table("abba")
        a.fill_the_table("aaa")
    assert a.mq == expected


@pytest.mark.parametrize("nom, expected_mq",
                         [(samples.A, {"": 0, "a": 1, "b": 0}),
                          (samples.B, {"": 0, "a": 0, "b": 1}),
                          (samples.C, {"": 0, "a": 0, "b": 0}),
                          (samples.odd, {"": 0, "0": 0, "1": 1}),
                          (samples.A2, {"": 1, "a": 0, "b": 0}),
                          (samples.automate, {"": 1, "a": 0, "b": 0}),
                          (samples.automate2, {"": 0, "a": 0, "b": 1})])
def test_lstar_initialise(nom, expected_mq):
    if nom == samples.odd:
        a = Angluin(copy.deepcopy(alphabet_01), nom.copy(), mq={}, pref={}, exp=[])
        a.Lstar_Initialise()
        assert a.alphabet == alphabet_01
        assert a.automate == nom
        assert a.mq == expected_mq
        assert a.pref == {"": "red", "0": "blue", "1": "blue"}
        assert a.exp == [""]
    else:
        a = Angluin(copy.deepcopy(alphabet_ab), nom.copy(), mq={}, pref={}, exp=[])
        a.Lstar_Initialise()
        assert a.alphabet == alphabet_ab
        assert a.automate == nom
        assert a.mq == expected_mq
        assert a.pref == {"": "red", "a": "blue", "b": "blue"}
        assert a.exp == [""]


def test_compare_ot(non_consistent_a2):
    assert non_consistent_a2.compareOT("", "a") == False
    assert non_consistent_a2.compareOT("", "b") == False
    assert non_consistent_a2.compareOT("a", "b") == True
    assert non_consistent_a2.compareOT("aa", "ba") == False
    assert non_consistent_a2.compareOT("ab", "bb") == False


def test_blue(non_consistent_a2):
    assert non_consistent_a2.blue() == ["aa", "ab", "ba", "bba", "bbb"]


def test_red(non_consistent_a2):
    assert non_consistent_a2.red() == ["", "a", "b", "bb"]


def test_ligne(consistent_a_a2):
    A = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.ligne("") == [0]
    assert A.ligne("a") == [1]
    assert A.ligne("b") == [0]
    assert consistent_a_a2.ligne("") == [1, 0]
    assert consistent_a_a2.ligne("a") == [0, 1]
    assert consistent_a_a2.ligne("b") == [0, 0]
    assert consistent_a_a2.ligne("ab") == [0, 0]


def test_different(consistent_a_a2):
    A = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.different(
        "a") == True  # la ligne correspondante à "a" est différente de toutes les lignes correspondantes à red
    assert A.different("b") == False
    assert consistent_a_a2.different("ab") == False


def test_is_closed(non_consistent_a2):
    A = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    A.Lstar_Initialise()
    assert A.is_closed() == False
    assert non_consistent_a2.is_closed() == True


@pytest.mark.parametrize("nom, mq0, pref0, exp0, expected_mq, expected_pref",
                         [(samples.A, {"": 0, "a": 1, "b": 0}, {"": "red", "a": "blue", "b": "blue"}, [""],
                           {"": 0, "a": 1, "b": 0, "aa": 1, "ab": 0},
                           {"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "blue"}),

                          (samples.B, {"": 0, "a": 0, "b": 1}, {"": "red", "a": "blue", "b": "blue"}, [""],
                           {"": 0, "a": 0, "b": 1, "ba": 0, "bb": 1},
                           {"": "red", "b": "red", "a": "blue", "ba": "blue", "bb": "blue"})
                          ])
def test_lstar_close(nom, mq0, pref0, exp0, expected_mq, expected_pref):
    a = Angluin(alphabet_ab, nom, mq0, pref0, exp0.copy())
    a.lstar_close()
    assert a.mq == expected_mq
    assert a.pref == expected_pref
    assert a.exp == exp0


def test_find_consistency_problem(non_consistent_a2, consistent_a_a2):
    assert consistent_a_a2.find_consistency_problem() == [True]
    result = non_consistent_a2.find_consistency_problem()
    assert result == [False, ("a", "")] or result == [False, ("b", "")]


def test_is_consistent(non_consistent_a2, consistent_a_a2, consistent_b_a2):
    assert non_consistent_a2.is_consistent() == False
    assert consistent_a_a2.is_consistent() == True
    assert consistent_b_a2.is_consistent() == True


def test_lstar_consistent(non_consistent_a2, consistent_a_a2, consistent_b_a2):
    non_consistent_a2.lstar_consistent()
    assert non_consistent_a2.alphabet == consistent_a_a2.alphabet
    assert non_consistent_a2.automate == samples.A2
    assert non_consistent_a2.mq == consistent_a_a2.mq or non_consistent_a2.mq == consistent_b_a2.mq
    assert non_consistent_a2.pref == consistent_a_a2.pref
    assert non_consistent_a2.exp == consistent_a_a2.exp or non_consistent_a2.exp == consistent_b_a2.exp


def test_get_prefixes():
    a = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    mot = "abaabbb"
    assert a.get_prefixes(mot) == ["", "a", "ab", "aba", "abaa", "abaab", "abaabb", "abaabbb"]


#TODO : faire le test de __eq__


@pytest.mark.parametrize("nom, mq0, pref0, exp0, answer, expected_mq, expected_pref",
                         [(samples.A, {"": 0, "a": 1, "b": 0, "aa": 1, "ab": 0},
                           {"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "blue"},
                           [""], "aba",
                           {"": 0, "a": 1, "aba": 0, "b": 0, "aa": 1, "ab": 0, "abb": 0, "abaa": 0, "abab": 0},
                           {"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "red", "aba": "red", "abb": "blue",
                            "abaa": "blue", "abab": "blue"}),

                          (samples.A, {"": 0, "a": 1, "b": 0, "aa": 1, "ab": 0, "aba": 0, "abaa": 0, "abab": 0, "ba": 0,
                                       "aaa": 1, "abaaa": 0, "ababa": 0, "abb": 0},
                           {"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "red", "aba": "red", "abaa": "blue",
                            "abab": "blue", "abb": "blue"},
                           ["", "a"], "ba",
                           {"": 0, "a": 1, "aba": 0, "b": 0, "aa": 1, "aaa": 1, "abaaa": 0, "ab": 0, "ba": 0, "bb": 0,
                            "abb": 0, "abaa": 0, "abab": 0, "baa": 1, "bab": 0, "ababa": 0, "bba": 1, "baaa": 1,
                            "baba": 0,
                            "abba": 0},
                           {"": "red", "a": "red", "b": "red", "ab": "red", "aba": "red", "ba": "red",
                            "aa": "blue", "abb": "blue", "abaa": "blue", "abab": "blue", "bb": "blue", "baa": "blue",
                            "bab": "blue"})
                          ])
def test_lstar_useeq(nom, mq0, pref0, exp0, answer, expected_mq, expected_pref):
    a = Angluin(alphabet_ab, nom, mq0, pref0, exp0.copy())
    a.LSTAR_USEEQ(answer)
    assert a.mq == expected_mq
    assert a.pref == expected_pref
    assert a.exp == exp0


@pytest.mark.parametrize("nom, mq, pref, exp",
                         [(samples.A,
                           {"": 0, "a": 1, "b": 0, "aa": 1, "ab": 0, "aba": 0, "abaa": 0, "abaaa": 0, "abab": 0,
                            "ababa": 0, "aaa": 1, "ba": 1},
                           {"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "blue", "aba": "red",
                            "abaa": "blue", "abab": "blue"},
                           ["", "a"]),

                          (samples.B,
                           {"": 0, "a": 0, "b": 1, "aa": 0, "ab": 1, "aab": 1, "aaba": 0, "aabb": 1},
                           {"": "red", "a": "red", "b": "blue", "aa": "red", "ab": "blue", "aab": "red", "aaba": "blue",
                            "aabb": "blue"},
                           [""])
                          ])
def test_lstar_build_automaton(nom, mq, pref, exp):
    a = Angluin(alphabet_ab, nom, mq, pref, exp)
    assert a.lstar_build_automaton().__eq__(nom)


def test_lstar(liste_angluin):
    for a in liste_angluin:
        automate_a_deviner = a.automate.copy()
        a.lstar()
        assert a.automate == automate_a_deviner
        assert a.__eq__(a.automate)
        assert a.__eq__(automate_a_deviner)
