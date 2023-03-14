from automata.fa.dfa import DFA
from Angluin import *

# j'ai mis les tests de la documentation apparemment ça marche
# j'ai mis aussi frozendict et networkx et pydot parce que automata en a besoin

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

# print(dfa.read_input('01'))
#
# if dfa.accepts_input('0'):
#     print('accepted')
# else:
#     print('rejected')


automate_test = DFA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a':'q0', 'b': 'q3'},
        'q1': {'a':'q2', 'b': 'q3'},
        'q2': {'a': 'q1', 'b': 'q3'},
        'q3': {'a': 'q3', 'b': 'q2'}
    },
    initial_state='q0',
    final_states={'q0', 'q2'}
)


mq2 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0,'bba': 0, 'bbb': 0}
pref2 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
exp2 = ['']



mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1, 'bbb': 0, 'bbba': 0}
pref = {'': 'RED', 'a': 'RED', 'b': 'RED', 'bb': 'RED', 'aa': 'BLUE', 'ab': 'BLUE', 'ba': 'BLUE', 'bba': 'BLUE', 'bbb': 'BLUE'}
exp = ['', 'a']

before_automate = Angluin(automate_test.input_symbols, automate_test, mq2, pref2, exp2)
learned_automate = Angluin(automate_test.input_symbols, automate_test, mq, pref, exp)
# print(learned_automate.is_consistent())
# print(before_automate.is_consistent())
before_automate.lstar_consistent()
print("mq : ", mq, "pref : ", pref, "exp : ", exp)



