from automata.fa.dfa import DFA
from Compositional_Model_Checking import *

# Exemple diapo assume guarantee
Input = DFA(
    states={"0", "1", "2"},
    input_symbols={"a", "i", "s"},
    transitions={
        "0": {"i": "1"},
        "1": {"s": "2"},
        "2": {"a": "0"}
    },
    initial_state="0",
    final_states={"0", "1", "2"},
    allow_partial=True
)
Output = DFA(
    states={"0", "1", "2"},
    input_symbols={"a", "o", "s"},
    transitions={
        "0": {"s": "1"},
        "1": {"o": "2"},
        "2": {"a": "0"}
    },
    initial_state="0",
    final_states={"0", "1", "2"},
    allow_partial=True
)
P = completedAutomata(
    states={"0", "1"},
    alphabet={"i", "o"},
    transitions={
        "0": {"i": "1"},
        "1": {"o": "0"}
    },
    initial_state="0",
    final_states={"0", "1"}
)

alphabet = (Input.input_symbols.union(P.input_symbols)).intersection(Output.input_symbols)
print(assumption_garantee(alphabet, Input, Output, P))

# Problème rencontré :
# M1_P DFA(states={('1', '1'), 'pi', ('2', '0'), ('2', '1'), ('0', '0'), ('1', '0'), ('0', '1')}, input_symbols={'o', 'i', 's', 'a'}, transitions={('0', '0'): {'i': ('1', '1'), 'o': 'pi'}, ('0', '1'): {'i': 'pi', 'o': ('0', '0')}, ('1', '0'): {'s': ('2', '0'), 'o': 'pi'}, ('1', '1'): {'s': ('2', '1'), 'o': ('1', '0')}, ('2', '0'): {'a': ('0', '0'), 'o': 'pi'}, ('2', '1'): {'a': ('0', '1'), 'o': ('2', '0')}, 'pi': {'o': 'pi', 'a': 'pi', 'i': 'pi', 's': 'pi'}}, initial_state=('0', '0'), final_states={('1', '1'), ('2', '0'), ('2', '1'), ('0', '0'), ('1', '0'), ('0', '1')}, allow_partial=True)
# mq {'': 1, 'o': 0, 's': 1, 'a': 1, 'oo': 0, 'os': 0, 'oa': 0, 'so': 1, 'ss': 1, 'sa': 1, 'sao': 1, 'sas': 1, 'saa': 1, 'ao': 1, 'ooo': 0, 'oso': 0, 'oao': 0, 'soo': 1, 'sso': 1, 'saoo': 1, 'saso': 1, 'saao': 1}
# pref {'': 'red', 'o': 'red', 's': 'red', 'a': 'blue', 'oo': 'blue', 'os': 'blue', 'oa': 'blue', 'so': 'blue', 'ss': 'blue', 'sa': 'red', 'sao': 'blue', 'sas': 'blue', 'saa': 'blue'}
# exp ['', 'o']
# A_i DFA(states={'', 's'}, input_symbols={'o', 's', 'a'}, transitions={'': {'s': 's', 'a': 's'}, 's': {'o': 's', 's': 's', 'a': 's'}}, initial_state='', final_states={'', 's'}, allow_partial=True)
# A_i || M1 DFA(states={('s', '1'), ('', '0'), ('', '1'), ('s', '2'), ('s', '0')}, input_symbols={'o', 'i', 's', 'a'}, transitions={('', '1'): {'s': ('s', '2')}, ('s', '1'): {'s': ('s', '2'), 'o': ('s', '1')}, ('s', '2'): {'a': ('s', '0'), 'o': ('s', '2')}, ('', '0'): {'i': ('', '1')}, ('s', '0'): {'o': ('s', '0'), 'i': ('s', '1')}}, initial_state=('', '0'), final_states={('s', '1'), ('', '0'), ('', '1'), ('s', '2'), ('s', '0')}, allow_partial=True)
# restricted symbols {'s', 'a'}
# first result isoo

# -------------------------------------------------------------------------------------------------------------


# Exemple doc 2 (pas encore testé)
# M1 = DFA(
#     states={"0", "1", "2", "3", "4"},
#     input_symbols={"a", "b", "c", "d"},
#     transitions={
#         "0": {"a": "1", "c": "3"},
#         "1": {"b": "2", "c": "1"},
#         "3": {"d": "4"},
#         "4": {"a": "1"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2", "3", "4"}
# )
#
# M2 = DFA(
#     states={"0", "1", "2"},
#     input_symbols={"a", "b", "c"},
#     transitions={
#         "0": {"c": "1"},
#         "1": {"a": "2"},
#         "2": {"b": "1"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2"}
# )
#
# "Après un nombre impair de a, il est possible de faire un b"
# P_1_2 = DFA(
#     states={"0", "1", "2"},
#     input_symbols={"a", "b"},
#     transitions={
#         "0": {"a": "1"},
#         "1": {"a": "2"},
#         "2": {"a": "1", "b": "0"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2"}
# )



# Exemple supplémentaire : Vérifier que tout b est suivi d'un c (pas encore testé)
# M3 = DFA(
#     states={"0", "1"},
#     input_symbols={"b", "c"},
#     transitions={
#         "0": {"b": "1"},
#         "1": {"c": "0"}
#     },
#     initial_state="0",
#     final_states={"0", "1"}
# )
#
# M4 = DFA(
#     states={"0", "1", "2"},
#     input_symbols={"a", "b", "c"},
#     transitions={
#         "0": {"a": "1", "c": "1"},
#         "1": {"b": "2"},
#         "2": {"c": "0"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2"}
# )
#
# P_3_4 = DFA(
#     states={"0", "1", "2"},
#     input_symbols={"a", "b", "c"},
#     transitions={
#         "0" : {"a": "0", "c": "0", "b": "0"},
#         "1" : {"c": "1"},
#         "2": {"b": "1", "a": "0", "c": "0"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2"}
# )


# M1 = DFA(
#     states={"0", "1", "2", "3", "4"},
#     input_symbols={"a", "b", "c", "d"},
#     transitions={
#         "0": {"a": "1", "c": "3"},
#         "1": {"b": "2", "c": "1"},
#         "3": {"d": "4"},
#         "4": {"a": "1"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2", "3", "4"}
# )

# M2 = DFA(
#     states={"0", "1", "2"},
#     input_symbols={"a", "b", "c"},
#     transitions={
#         "0": {"c": "1"},
#         "1": {"a": "2"},
#         "2": {"b": "1"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2"}
# )
#
# P_1_2 = DFA(
#     states={"0", "1", "2"},
#     input_symbols={"a", "b"},
#     transitions={
#         "0": {"a": "1"},
#         "1": {"a": "2"},
#         "2": {"a": "1", "b": "0"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2"}
# )





# TEST UNITAIRES


# Composition Parralèlle Lidia
# A = DFA(
#         states = {"0", "1", "2"},
#         input_symbols = {"in", "send", "ack"},
#         transitions = {
#             "0": {"in" : "1"},
#             "1": {"send" : "2"},
#             "2": {"ack" : "0"}
#                         },
#         initial_state = "0",
#         final_states = {"2"},
#         allow_partial=True
#         )
#
# B = DFA(
#         states = {"a", "b", "c"},
#         input_symbols = {"out", "send", "ack"},
#         transitions = {
#             "a": {"send" : "b"},
#             "b": {"out" : "c"},
#             "c": {"ack" : "a"}
#                         },
#         initial_state = "a",
#         final_states = {"c"},
#         allow_partial=True
#         )
#
# # print_transitions(A.transitions)
# # print(A)
# # print(B)
# print(parallel_composition(A, B))

# tests pauline
# M = DFA(
#     states={"0", "1", "2", "3"},
#     input_symbols={"i", "o", "s"},
#     transitions={
#         "0": {"i": "1", "o": "2", "s": "2"},
#         "1": {"i": "1", "o": "0", "s": "3"},
#         "2": {"i": "0", "o": "2", "s": "2"},
#         "3": {"i": "1", "o": "0", "s": "2"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "3"}
# )
#
# # exemple diapo 28 doit satisfaire P
# IO_ok = completedAutomata(
#     states={"0", "1", "2", "3"},
#     alphabet={"i", "s", "o", "a"},
#     transitions={
#         "0": {"i": "1"},
#         "1": {"s": "2"},
#         "2": {"o": "3"},
#         "3": {"a": "0"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2", "3"}
# )
#
# # exemple diapo 29 ne doit pas satisfaire P
# IO_pas_ok = completedAutomata(
#     states={"0", "1", "2", "3"},
#     alphabet={"i", "s", "o", "a"},
#     transitions={
#         "0": {"i": "1"},
#         "1": {"s": "2", "i": "3"},
#         "2": {"o": "3"},
#         "3": {"a": "0"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "2", "3"}
# )
#
# # automate Order_err dans le diapo
# P = DFA(
#     states={"0", "1", "2"},
#     input_symbols={"i", "o"},
#     transitions={
#         "0": {"i": "1", "o": "2"},
#         "1": {"i": "2", "o": "0"},
#         "2": {"i": "2", "o": "2"}
#     },
#     initial_state="0",
#     final_states={"0", "1"}
# )
#
# print("ok?", satisfies(M, P)) # False
# print("ok?", satisfies(IO_ok, P)) # True
# print("ok?", satisfies(IO_pas_ok, P)) # False



# Test d'inclusion
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

# print(AB.__le__(A, True))

# TEST: rendre automate complet
# etats ={"0", "1"}
# input_symbols={"b", "a"}
# transition={"0" : {"b" : "1"}, "1" : {"a" : "0", "b" : "1"}}
# ini_state="0"
# fin_states={"1"}
#
# print(completedAutomata(etats, input_symbols, transition, ini_state, fin_states))