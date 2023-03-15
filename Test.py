from automata.fa.dfa import DFA
from Angluin import *


# DFA which matches all binary strings ending in an odd number of '1's
dfa = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)


# TEST CONSISTENCE
automate_test_A2 = DFA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a':'q1', 'b': 'q3'},
        'q1': {'a':'q2', 'b': 'q3'},
        'q2': {'a': 'q1', 'b': 'q3'},
        'q3': {'a': 'q3', 'b': 'q2'}
    },
    initial_state='q0',
    final_states={'q0', 'q2'}
)


# TABLE NON CONSISTENTE
mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0,'bba': 0, 'bbb': 0}
pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp0 = ['']

# TABLE QUI DEVIENT CONSISTENTE AVEC L'APPEL DE lstar_consistent()
mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1, 'bbb': 0, 'bbba': 0}
pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp = ['', 'a']

# before_automate = Angluin(automate_test_A2.input_symbols, automate_test, mq0, pref0, exp0)
# learned_automate = Angluin(automate_test_A2.input_symbols, automate_test, mq, pref, exp)
# print(learned_automate.is_consistent())
# print(before_automate.is_consistent())
# before_automate.lstar_consistent()
# print("mq0 : ", mq0, "pref0 : ", pref0, "exp0 : ", exp0)





# TEST D'ÉQUIVALENCE
A = DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a"},
        transitions={"0" : {"a" : "1", "b" : "0"}, "1" : {"a" : "1", "b" : "puits"}, "puits" : {"a" : "puits", "b" : "puits"}},
        initial_state="0",
        final_states={"1"}
        )
C = DFA(states={"0", "1", "2","puits"},
        input_symbols={"b", "a"},
        transitions={"0" : {"a" : "1", "b" : "0"}, "1" : {"a" : "2", "b" : "puits"}, "2" : {"a" : "2", "b" : "puits"}, "puits" : {"a" : "puits", "b" : "puits"}},
        initial_state="0",
        final_states={"2"}
        )

# A.__eq__(C, witness=True)


# AUTOMATE LSTAR
automate = DFA(states={"0", "1", "2", "3"},
               input_symbols={"b","a"},
               transitions={
                   "0" : {"a" : "1", "b" : "3"},
                   "1" : {"a" : "0", "b" : "2"},
                   "2" : {"a" : "3", "b" : "1"},
                   "3" : {"a" : "2", "b" : "0"}
               },
               initial_state="0",
               final_states={"0"}
)

angluin = Angluin({"a","b"}, automate)
resultat = angluin.lstar()