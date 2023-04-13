from Angluin import *
from automata.fa.dfa import DFA

from automata.fa.dfa import DFA
from Angluin import *

# automate qui accepte "a" et "ab"
AB = DFA(states={"0", "1", "2", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0" : {"a": "1", "b": "puits"},
            "1" : {"a": "puits", "b": "2"},
            "2" : {"a": "puits", "b": "puits"},
            "puits" : {"a" : "puits", "b" : "puits"}},
        initial_state="0",
        final_states={"1", "2"}
        )

# automate qui accepte "a"
A = DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0" : {"a": "1", "b": "puits"},
            "1" : {"a": "puits", "b": "puits"},
            "puits" : {"a" : "puits", "b" : "puits"}},
        initial_state="0",
        final_states={"1"}
        )

print(AB.__le__(A, True))