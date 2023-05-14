from Angluin import *

# Some DFA :

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

odd_number_of_1 = DFA(
    states={'0', '1', '2'},
    input_symbols={'0', '1'},
    transitions={
        '0': {'0': '0', '1': '1'},
        '1': {'0': '1', '1': '2'},
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

odd_number_of_1_version2 = DFA(states={0, 1},
                               input_symbols={"0", "1"},
                               transitions={0: {"0": 0, "1": 1}, 1: {"0": 1, "1": 0}},
                               initial_state=0,
                               final_states={1})


A_with_c = DFA(states={"0", "1", "puits"},
        input_symbols={"b", "a", "c"},
        transitions={
            "0": {"a": "1", "b": "0", "c" : "puits"},
            "1": {"a": "1", "b": "puits", "c" : "puits"},
            "puits": {"a": "puits", "b": "puits", "c" : "puits"}},
        initial_state="0",
        final_states={"1"}
        )

# List of DFA with whom we test our functions :
liste = [A, B, C, odd_number_of_1, A2, automate, automate2, A_with_c]
