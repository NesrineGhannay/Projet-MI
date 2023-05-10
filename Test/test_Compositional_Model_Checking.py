from Compositional_Model_Checking import *
import pytest
from automata.fa.dfa import DFA


@pytest.mark.parametrize("word, alphabet, exp",
                         [("oiaubav", {"a", "b"}, "aba"),
                          ("", {"a", "b"}, ""),
                          ("zofjw", {}, "")])
def test_restriction(word, alphabet, exp):
    assert restriction(word, alphabet) == exp


@pytest.mark.parametrize("states, alphabet, transitions, initial_state, final_states, exp_s, exp_t",
                         [({"0", "1"}, {"i", "o"}, {"0": {"i": "1"}, "1": {"o": "0"}}, "0", {"0", "1"},
                           {"0", "1", "puits"}, {"0": {"i": "1", "o": "puits"}, "1": {"o": "0", "i": "puits"},
                                                 "puits" : {"o" : "puits", "i" : "puits"}})])
def test_completedAutomata(states, alphabet, transitions, initial_state, final_states, exp_s, exp_t):
    result = completedAutomata(states, alphabet, transitions, initial_state, final_states)
    assert result.__eq__(
        DFA(states=exp_s, input_symbols=alphabet, transitions=exp_t, initial_state=initial_state,
            final_states=final_states))

#TODO : je ne sais pas comment fr pour completedAutomataByDFA
#TODO : print transitions pas important
