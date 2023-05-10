import copy
import pytest
from Angluin import *
from samples import samples
from automata.fa.dfa import DFA

alphabet_ab = {"a", "b"}
alphabet_01 = {"0", "1"}


# List of initial instances of Angluin with the automaton to guess:
@pytest.fixture
def list_angluin():
    result = []
    for automaton in samples.liste:
        result.append(
            Angluin(
                alphabet_01 if automaton == samples.odd_number_of_1 else alphabet_ab,
                automaton, mq={}, pref={}, exp=[]))
    return result


# Instance of an Angluin in which the table is not consistent (the automaton is A2)
@pytest.fixture
def no_consistent():
    mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0, 'bba': 0, 'bbb': 0}
    pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
             'bbb': 'blue'}
    exp0 = ['']
    return Angluin(alphabet_ab, samples.A2, mq0, pref0, exp0)


# Two instances of the Angluin in which the table has become consistent
# The first with the counterexample of '' and 'a' are red but 'a' and 'aa' are different
@pytest.fixture
def consistent_a():
    mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1,
          'bbb': 0, 'bbba': 0}
    pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
            'bbb': 'blue'}
    exp = ['', 'a']
    return Angluin(alphabet_ab, samples.A2, mq, pref, exp)


# The second with the counterexample of '' and 'a' are red but 'b' and 'ab' are different
@pytest.fixture
def consistent_b():
    mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0, 'bba': 0, 'bbb': 0, "aab": 0, "abb": 1, "bab": 1,
          "bbab": 0, "bbbb": 1}
    pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue',
            'bbb': 'blue'}
    exp = ['', 'b']
    return Angluin(alphabet_ab, samples.A2, mq, pref, exp)


@pytest.mark.parametrize("automaton, expected_mq",
                         [(samples.A, {"": 0, "a": 1, "b": 0, "ab": 0, "ba": 1, "abba": 0, "aaa": 1}),
                          (samples.B, {"": 0, "a": 0, "b": 1, "ab": 1, "ba": 0, "abba": 0, "aaa": 0}),
                          (samples.C, {"": 0, "a": 0, "b": 0, "ab": 0, "ba": 0, "abba": 0, "aaa": 1}),
                          (samples.odd_number_of_1, {"": 0, "0": 0, "1": 1, "00": 0, "01": 1, "10": 1, "11": 0}),
                          (samples.A2, {"": 1, "a": 0, "b": 0, "ab": 0, "ba": 0, "abba": 0, "aaa": 0}),
                          (samples.automate, {"": 1, "a": 0, "b": 0, "ab": 0, "ba": 0, "abba": 1, "aaa": 0}),
                          (samples.automate2, {"": 0, "a": 0, "b": 1, "ab": 1, "ba": 0, "abba": 0, "aaa": 0})])
def test_fill_the_table(automaton, expected_mq):
    if automaton == samples.odd_number_of_1:
        angluin = Angluin(alphabet_01, automaton, mq={}, pref={}, exp=[])
        angluin.fill_the_table("")
        angluin.fill_the_table("0")
        angluin.fill_the_table("1")
        angluin.fill_the_table("00")
        angluin.fill_the_table("01")
        angluin.fill_the_table("10")
        angluin.fill_the_table("11")
    else:
        angluin = Angluin(alphabet_ab, automaton, mq={}, pref={}, exp=[])
        angluin.fill_the_table("")
        angluin.fill_the_table("a")
        angluin.fill_the_table("b")
        angluin.fill_the_table("ab")
        angluin.fill_the_table("ba")
        angluin.fill_the_table("abba")
        angluin.fill_the_table("aaa")
    assert angluin.mq == expected_mq


@pytest.mark.parametrize("automaton, expected_mq",
                         [(samples.A, {"": 0, "a": 1, "b": 0}),
                          (samples.B, {"": 0, "a": 0, "b": 1}),
                          (samples.C, {"": 0, "a": 0, "b": 0}),
                          (samples.odd_number_of_1, {"": 0, "0": 0, "1": 1}),
                          (samples.A2, {"": 1, "a": 0, "b": 0}),
                          (samples.automate, {"": 1, "a": 0, "b": 0}),
                          (samples.automate2, {"": 0, "a": 0, "b": 1})])
def test_lstar_initialise(automaton, expected_mq):
    if automaton == samples.odd_number_of_1:
        angluin = Angluin(copy.deepcopy(alphabet_01), automaton.copy(), mq={}, pref={}, exp=[])
        angluin.Lstar_Initialise()
        assert angluin.alphabet == alphabet_01
        assert angluin.automate == automaton
        assert angluin.mq == expected_mq
        assert angluin.pref == {"": "red", "0": "blue", "1": "blue"}
        assert angluin.exp == [""]
    else:
        angluin = Angluin(copy.deepcopy(alphabet_ab), automaton.copy(), mq={}, pref={}, exp=[])
        angluin.Lstar_Initialise()
        assert angluin.alphabet == alphabet_ab
        assert angluin.automate == automaton
        assert angluin.mq == expected_mq
        assert angluin.pref == {"": "red", "a": "blue", "b": "blue"}
        assert angluin.exp == [""]


def test_compare_ot(no_consistent):
    assert no_consistent.compareOT("", "a") == False
    assert no_consistent.compareOT("", "b") == False
    assert no_consistent.compareOT("a", "b") == True
    assert no_consistent.compareOT("aa", "ba") == False
    assert no_consistent.compareOT("ab", "bb") == False


def test_blue(no_consistent):
    assert no_consistent.blue() == ["aa", "ab", "ba", "bba", "bbb"]


def test_red(no_consistent):
    assert no_consistent.red() == ["", "a", "b", "bb"]


def test_ligne(consistent_a):
    angluin = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    angluin.Lstar_Initialise()
    assert angluin.line("") == [0]
    assert angluin.line("a") == [1]
    assert angluin.line("b") == [0]
    assert consistent_a.line("") == [1, 0]
    assert consistent_a.line("a") == [0, 1]
    assert consistent_a.line("b") == [0, 0]
    assert consistent_a.line("ab") == [0, 0]


def test_different(consistent_a):
    angluin = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    angluin.Lstar_Initialise()
    assert angluin.different("a") == True
    assert angluin.different("b") == False
    assert consistent_a.different("ab") == False


def test_is_closed(no_consistent):
    angluin = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    angluin.Lstar_Initialise()
    assert angluin.is_closed() == False
    assert no_consistent.is_closed() == True


@pytest.mark.parametrize("automaton, mq0, pref0, exp0, expected_mq, expected_pref",
                         [(samples.A, {"": 0, "a": 1, "b": 0}, {"": "red", "a": "blue", "b": "blue"}, [""],
                           {"": 0, "a": 1, "b": 0, "aa": 1, "ab": 0},
                           {"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "blue"}),

                          (samples.B, {"": 0, "a": 0, "b": 1}, {"": "red", "a": "blue", "b": "blue"}, [""],
                           {"": 0, "a": 0, "b": 1, "ba": 0, "bb": 1},
                           {"": "red", "b": "red", "a": "blue", "ba": "blue", "bb": "blue"})
                          ])
def test_lstar_close(automaton, mq0, pref0, exp0, expected_mq, expected_pref):
    angluin = Angluin(alphabet_ab, automaton, mq0, pref0, exp0.copy())
    angluin.lstar_close()
    assert angluin.mq == expected_mq
    assert angluin.pref == expected_pref
    assert angluin.exp == exp0


def test_find_consistency_problem(no_consistent, consistent_a):
    assert consistent_a.find_consistency_problem() == [True]
    result = no_consistent.find_consistency_problem()
    assert result == [False, ("a", "")] or result == [False, ("b", "")]


def test_is_consistent(no_consistent, consistent_a, consistent_b):
    assert no_consistent.is_consistent() == False
    assert consistent_a.is_consistent() == True
    assert consistent_b.is_consistent() == True


def test_lstar_consistent(no_consistent, consistent_a, consistent_b):
    no_consistent.lstar_consistent()
    assert no_consistent.alphabet == consistent_a.alphabet
    assert no_consistent.automate == samples.A2
    assert no_consistent.mq == consistent_a.mq or no_consistent.mq == consistent_b.mq
    assert no_consistent.pref == consistent_a.pref
    assert no_consistent.exp == consistent_a.exp or no_consistent.exp == consistent_b.exp


def test_get_prefixes():
    angluin = Angluin(alphabet_ab, samples.A, mq={}, pref={}, exp=[])
    word = "abaabbb"
    assert angluin.get_prefixes(word) == ["", "a", "ab", "aba", "abaa", "abaab", "abaabb", "abaabbb"]


# TODO : faire le test de __eq__


@pytest.mark.parametrize("automaton, mq0, pref0, exp0, answer, expected_mq, expected_pref",
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
def test_lstar_useeq(automaton, mq0, pref0, exp0, answer, expected_mq, expected_pref):
    a = Angluin(alphabet_ab, automaton, mq0, pref0, exp0.copy())
    a.Lstar_use_eq(answer)
    assert a.mq == expected_mq
    assert a.pref == expected_pref
    assert a.exp == exp0


@pytest.mark.parametrize("automaton, mq, pref, exp",
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
def test_lstar_build_automaton(automaton, mq, pref, exp):
    angluin = Angluin(alphabet_ab, automaton, mq, pref, exp)
    assert angluin.lstar_build_automaton().__eq__(automaton)


def test_lstar(list_angluin):
    for a in list_angluin:
        automaton_to_guess = a.automate.copy()
        assert a.automate == automaton_to_guess
        p = a.lstar()
        assert p.__eq__(a.automate)
        #en revanche assert a.__eq__(a.automate) fonctionne...
