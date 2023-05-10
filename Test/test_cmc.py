from automata.fa.dfa import DFA
import Compositional_Model_Checking


M1 = DFA(
    states={"0", "1", "2", "3", "4"},
    input_symbols={"a", "b", "c", "d"},
    transitions={
        "0": {"a": "1", "c": "3"},
        "1": {"b": "2", "c": "1"},
        "3": {"d": "4"},
        "4": {"a": "1"}
    },
    initial_state="0",
    final_states={"0", "1", "2", "3", "4"}
)

M2 = DFA(
    states={"0", "1", "2"},
    input_symbols={"a", "b", "c"},
    transitions={
        "0": {"c": "1"},
        "1": {"a": "2"},
        "2": {"b": "1"}
    },
    initial_state="0",
    final_states={"0", "1", "2"}
)

P_1_2 = DFA(
    states={"0", "1", "2"},
    input_symbols={"a", "b"},
    transitions={
        "0": {"a": "1"},
        "1": {"a": "2"},
        "2": {"a": "1", "b": "0"}
    },
    initial_state="0",
    final_states={"0", "1", "2"}
)

