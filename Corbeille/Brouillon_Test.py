# from Angluin import *
# from automata.fa.dfa import DFA
#
# from automata.fa.dfa import DFA
# from Angluin import *
#
#
# #Some DFA :
#
# A = DFA(states={"0", "1", "puits"},
#         input_symbols={"b", "a"},
#         transitions={
#             "0" : {"a" : "1", "b" : "0"},
#             "1" : {"a" : "1", "b" : "puits"},
#             "puits" : {"a" : "puits", "b" : "puits"}},
#         initial_state="0",
#         final_states={"1"}
#         )
#
#
# B = DFA(states={"0", "1"},
#     input_symbols={"b", "a"},
#     transitions={
#         "0" : {"a" : "0", "b" : "1"},
#         "1" : {"a" : "0", "b" : "1"}},
#     initial_state="0",
#     final_states={"1"}
#     )
#
#
# C = DFA(states={"0", "1", "2","puits"},
#         input_symbols={"b", "a"},
#         transitions={
#             "0" : {"a" : "1", "b" : "0"},
#             "1" : {"a" : "2", "b" : "puits"},
#             "2" : {"a" : "2", "b" : "puits"},
#             "puits" : {"a" : "puits", "b" : "puits"}},
#         initial_state="0",
#         final_states={"2"}
#         )
#
# # DFA which matches all binary strings ending in an odd number of '1's
# odd_number_of_1 = DFA(
#     states={'0', '1', '2'},
#     input_symbols={'0', '1'},
#     transitions={
#         '0': {'0': '0', '1': '1'},
#         '1': {'0': '0', '1': '2'},
#         '2': {'0': '2', '1': '1'}
#     },
#     initial_state='0',
#     final_states={'1'}
# )
#
#
# automate_test_A2 = DFA(
#     states={'0', '1', '2', '3'},
#     input_symbols={'a', 'b'},
#     transitions={
#         '0': {'a':'1', 'b': '3'},
#         '1': {'a':'2', 'b': '3'},
#         '2': {'a': '1', 'b': '3'},
#         '3': {'a': '3', 'b': '2'}
#     },
#     initial_state='0',
#     final_states={'0', '2'}
# )
#
#
# # AUTOMATE LSTAR
# automate = DFA(states={"0", "1", "2", "3"},
#                input_symbols={"a","b"},
#                transitions={
#                    "0" : {"a" : "1", "b" : "3"},
#                    "1" : {"a" : "0", "b" : "2"},
#                    "2" : {"a" : "3", "b" : "1"},
#                    "3" : {"a" : "2", "b" : "0"}
#                },
#                initial_state="0",
#                final_states={"0"}
# ) # exemple du document L_STAR_ALGO.pdf
#
#
# automate2 = DFA(states={"0", "1", "2"},
#                 input_symbols={"a", "b"},
#                 transitions={
#                     "0" : {"a" : "0", "b" : "1"},
#                     "1" : {"a" : "0", "b" : "2"},
#                     "2" : {"a" : "2", "b" : "2"}
#                 },
#                 initial_state="0",
#                 final_states={"1"}
# ) # exemple du document Learning_with_Queries.pdf
#
#
# #List of DFA with whom we test our functions :
# dfa_to_test = [A, B, C, odd_number_of_1, automate_test_A2, automate, automate2]
#
#
# # TABLE NON CONSISTENTE
# mq0 = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'bb': 1, 'ab': 0, 'ba': 0,'bba': 0, 'bbb': 0}
# pref0 = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
# exp0 = ['']
#
# # TABLE QUI DEVIENT CONSISTENTE AVEC L'APPEL DE lstar_consistent()
# mq = {'': 1, 'a': 0, 'aa': 1, 'b': 0, 'ba': 0, 'bb': 1, 'bba': 0, 'aaa': 0, 'ab': 0, 'aba': 0, 'baa': 0, 'bbaa': 1, 'bbb': 0, 'bbba': 0}
# pref = {'': 'red', 'a': 'red', 'b': 'red', 'bb': 'red', 'aa': 'blue', 'ab': 'blue', 'ba': 'blue', 'bba': 'blue', 'bbb': 'blue'}
# exp = ['', 'a']
#
# # before_automate = Angluin(automate_test_A2.input_symbols, automate_test, mq0, pref0, exp0)
# # learned_automate = Angluin(automate_test_A2.input_symbols, automate_test, mq, pref, exp)
# # print(learned_automate.is_consistent())
# # print(before_automate.is_consistent())
# # before_automate.lstar_consistent()
# # print("mq0 : ", mq0, "pref0 : ", pref0, "exp0 : ", exp0)
#
# # A.__eq__(C, witness=True)
#
#
# angluin = Angluin({"a","b"}, automate)
# resultat = angluin.lstar()
# print("RESULTAT : ", resultat)
#
#
# angluin2 = Angluin({"a", "b"}, automate2)
# resultat2 = angluin2.lstar()
# print("RESULTAT2 : ", resultat2)
#
#
# #Carla : Tables d'observation à tester sur les DFA
#
# testA = Angluin({"a", "b"}, A,
#                 mq={"" : 0, "a" : 1, "b" : 0, "aa" : 1, "ab" : 0, "aba": 0, "abaa": 0, "abaaa" : 0, "abab" : 0, "ababa" : 0, "aaa" : 1, "ba" : 1},
#                pref={"" : "red", "a" : "red", "b": "blue", "aa": "blue", "ab": "blue", "aba" : "red", "abaa":"blue", "abab":"blue"}, exp=["", "a"])
#
# testB = Angluin({"a", "b"}, B,
#                 mq={"" : 0, "a" : 0, "b" : 1, "aa" : 0, "ab" : 1, "aab": 1, "aaba": 0, "aabb" : 1},
#                pref={"" : "red", "a" : "red", "b": "blue", "aa": "red", "ab": "blue", "aab" : "red", "aaba" : "blue", "aabb": "blue"},
#                 exp=[""])
#
#
#
#
#
# def test_lstar_build_automaton():
#     resultA = testA.lstar_build_automaton()
#     resultB = testB.lstar_build_automaton()
#     assert resultA.__eq__(A)
#     assert resultB.__eq__(B)
