import pytest
from Angluin import *

alphabet = {"a", "b"}

# Quelques DFA initialisés avec Angluin:

A = DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "1", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"1"}
        )

B = DFA(states={"0", "1"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "0", "b": "1"},
            "1": {"a": "0", "b": "1"}},
        initial_state="0",
        final_states={"1"}
        )

C = DFA(states={"0", "1", "2", "puits"},
        input_symbols={"b", "a"},
        transitions={
            "0": {"a": "1", "b": "0"},
            "1": {"a": "2", "b": "puits"},
            "2": {"a": "2", "b": "puits"},
            "puits": {"a": "puits", "b": "puits"}},
        initial_state="0",
        final_states={"2"}
        )

odd = DFA(
    states={'0', '1', '2'},
    input_symbols={'0', '1'},
    transitions={
        '0': {'0': '0', '1': '1'},
        '1': {'0': '0', '1': '2'},
        '2': {'0': '2', '1': '1'}
    },
    initial_state='0',
    final_states={'1'})

A2 = DFA(
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

automate = DFA(states={"0", "1", "2", "3"},
               input_symbols={"a", "b"},
               transitions={
                   "0": {"a": "1", "b": "3"},
                   "1": {"a": "0", "b": "2"},
                   "2": {"a": "3", "b": "1"},
                   "3": {"a": "2", "b": "0"}
               },
               initial_state="0",
               final_states={"0"}
               )

automate2 = DFA(states={"0", "1", "2"},
                input_symbols={"a", "b"},
                transitions={
                    "0": {"a": "0", "b": "1"},
                    "1": {"a": "0", "b": "2"},
                    "2": {"a": "2", "b": "2"}
                },
                initial_state="0",
                final_states={"1"}
                )  # exemple du document Learning_with_Queries.pdf

# List of DFA with whom we test our functions :
liste = [A, B, C, odd, A2, automate, automate2]


testA = Angluin({"a", "b"}, A,
                mq={"": 0, "a": 1, "b": 0, "aa": 1, "ab": 0, "aba": 0, "abaa": 0, "abaaa": 0, "abab": 0, "ababa": 0,
                    "aaa": 1, "ba": 1},
                pref={"": "red", "a": "red", "b": "blue", "aa": "blue", "ab": "blue", "aba": "red", "abaa": "blue",
                      "abab": "blue"},
                exp=["", "a"])

testB = Angluin({"a", "b"}, B,
                mq={"": 0, "a": 0, "b": 1, "aa": 0, "ab": 1, "aab": 1, "aaba": 0, "aabb": 1},
                pref={"": "red", "a": "red", "b": "blue", "aa": "red", "ab": "blue", "aab": "red", "aaba": "blue",
                      "aabb": "blue"},
                exp=[""])
