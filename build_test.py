from Angluin import *
from automata.fa.dfa import DFA

#On teste la méthode lstar_build_automaton() en supposant que l'automate à deviner est A
A = DFA(states={"0", "1", "puits"},
    input_symbols={"b", "a"},
    transitions={"0" : {"a" : "1", "b" : "0"}, "1" : {"a" : "1", "b" : "puits"}, "puits" : {"a" : "puits", "b" : "puits"}},
    initial_state="0",
    final_states={"1"}
    )

#et qu'avec les méthodes de l'algo d'Angluin, on ait obtenu mq, pref et exp tels que :
testA = Angluin({"a", "b"}, A,
                mq={"" : 0, "a" : 1, "b" : 0, "aa" : 1, "ab" : 0},
               pref={"" : "red", "a" : "red", "b": "blue", "aa": "blue", "ab": "blue"}, exp=[""])

print(testA.lstar_build_automaton())


#On teste la méthode lstar_build_automaton() en supposant que l'automate à deviner est B
B = DFA(states={"0", "1"},
    input_symbols={"b", "a"},
    transitions={"0" : {"a" : "0", "b" : "1"}, "1" : {"a" : "0", "b" : "1"}},
    initial_state="0",
    final_states={"1"}
    )

#et qu'avec les méthodes de l'algo d'Angluin, on ait obtenu mq, pref et exp tels que :
testB = Angluin({"a", "b"}, B,
                mq={"" : 0, "a" : 0, "b" : 1, "aa" : 0, "ab" : 1, "aab": 1, "aaba": 0, "aabb" : 1, "aaa": 0, "ba" : 0, "aba": 0, "aabaa" : 0, "aabba" :0},
               pref={"" : "red", "a" : "red", "b": "blue", "aa": "red", "ab": "blue", "aab" : "red", "aaba" : "blue", "aabb": "blue"},
                exp=[""])


print(testB.lstar_build_automaton())