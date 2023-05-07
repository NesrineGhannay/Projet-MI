import copy

from Angluin import Angluin
from automata.fa.dfa import DFA


# def restriction(mot, alphabet):
#     motRestreint = ""
#     for caractere in mot:
#         if caractere in alphabet:
#             motRestreint += caractere
#     return motRestreint



def completedAutomata(states, alphabet, transitions, initial_state, final_states):
    """
    The automaton P (of property) is completed by a well state which is an error state (P_err = new automaton)

    :param states : the states of the automaton P
    :param alphabet: the alphabet of the automaton P
    :param transitions: the transitions of the automaton P
    :param initial_state: the initial states of the automaton P
    :param final_states: the finals states of the automaton P

    :return: DFA P in which the error status was added = P_err.

    """
    add_pi = False
    for dictionnary in transitions:
        for char in alphabet:
            if char not in transitions[dictionnary]:
                transitions[dictionnary][char] = "pi"
                add_pi = True
                if "pi" not in states:
                    states.add("pi")
    if add_pi:
        transitions["pi"] = {}
        for char in alphabet:
            transitions["pi"][char] = "pi"
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
               final_states=final_states)


# Produit parallele : Lidia
"""
Fonction print-transitions :
input : T : transitions
output : print ligne by ligne all transition one by one
"""
def print_transitions(T):
    print("T ", T)
    for source in T:
        for label in T[source]:
            target = T[source][label]
            print("Transition from", source, "to", target, "labelled by", label)


def synchronization(M1, M2):
    T = {}
    T1 = M1.transitions
    T2 = M2.transitions
    for q1 in T1:
        for q2 in T2:
            for a in T1[q1]:
                for b in T2[q2]:
                    if a == b:
                        if not ((q1, q2) in T):
                            T[(q1, q2)] = {}
                        target = (T1[q1][a], T2[q2][b])
                        T[(q1, q2)][a] = target
    return T


def interleaving(T, M1, M2):
    T1 = M1.transitions
    T2 = M2.transitions
    for q1 in T1:
        for q2 in T2:
            for a in T1[q1]:
                if a not in M2.input_symbols:
                    if not ((q1, q2) in T):
                        T[(q1, q2)] = {}
                    target = (T1[q1][a], q2)
                    T[(q1, q2)][a] = target
            for b in T2[q2]:
                if b not in M1.input_symbols:
                    if not ((q1, q2) in T):
                        T[(q1, q2)] = {}
                    target = (q1, T2[q2][b])
                    T[(q1, q2)][b] = target
    return T

def get_final_states(etats1, etats2):
    """
    Returns the final states set for the parallel composition of two DFAs.
    :param etats1: final states set for the first DFA
    :param etats2: final states set for the second DFA
    :return: A set of final states composed of
    """
    etats = set()
    for etat1 in etats1:
        for etat2 in etats2:
            etats.add((etat1, etat2))
    return etats


def parallel_composition(M1, M2):
    # Q : les etats (states)
    Q = set()
    Q1 = M1.states
    Q2 = M2.states
    for q1 in Q1:
        for q2 in Q2:
            Q.add((q1, q2))
    # q_0 : etat initial
    q1_0 = M1.initial_state
    q2_0 = M2.initial_state
    q_0 = (q1_0, q2_0)
    # aM : alphabet
    aM1 = M1.input_symbols
    aM2 = M2.input_symbols
    aM = aM1 | aM2
    # les transitons
    # si lettre dans intersection des alphabets de M1 et M2
    T = synchronization(M1, M2)
    # si lettre existante dans un seul des alphabet
    T_ = interleaving(T, M1, M2)
    # F : final and accepted states
    F = get_final_states(M1.final_states, M2.final_states)
    return DFA(states=Q, input_symbols=aM, transitions=T_, initial_state=q_0, final_states=F, allow_partial=True)
#Carla : Pourquoi les transitions de la synchronisation n'y sont pas ?


def assumption_garantee(alphabet, m1, m2, property):
    """
    Main program: Uses Compositional Model Checking approach to learn regular language
    :param alphabet: System alphabet
    :param m1:  First system component
    :param m2: Second system component
    :param property: Property to be verified
    :return: Return the automaton if the property is satisfied
    """
    angluin = Angluin(alphabet, m2)
    angluin.Lstar_Initialise()
    while not angluin.is_closed():
        angluin.lstar_close()
    assump = angluin.lstar_build_automaton()
    assumption = completedAutomata(assump.states, assump.input_symbols, assump.transitions, assump.initial_state, assump.final_states)
    answer = learning(m1, m2, assumption, property, angluin, alphabet)
    if answer == False:
        print("ERROR")
    else:
        print("Automate trouvé : ")
        return answer


def learning(m1, m2, assumption, property, angluin, alphabet):
    """
    Model Checking Program
    :param m1: First system component
    :param m2: Second sustem component
    :param assumption: The determined automaton
    :param property: Property to be verified
    :param angluin: Input that allows to retrieve the methods of Angluin
    :param alphabet: System aphabet
    :return: the correct assumption or False if it's not possible to generate it

    """
    answer = False
    while answer != True:
        print("parallel_composition(m1, assumption) ", parallel_composition(m1, assumption))
        print("property", property)
        compo = parallel_composition(m1, assumption)
        if satisfies(completedAutomata(compo.states, compo.input_symbols, compo.transitions, compo.initial_state, compo.final_states), property):
            cex = satisfies(m2, assumption)
            if cex == True:
                answer = True
            elif real_error(cex, m2, property, alphabet):
                return False
            else :
                assumption = angluin.LSTAR_USEEQ()
    return assumption

def real_error(m1, cex, proprety, alphabet):
    """
    Determine if the property is satisfable

    :param m1: First system component
    :param cex: Conter-example
    :param proprety: Proprety that we want to satisfy
    :param alphabet: Conter-example alphabet
    :return: True if the conter_example not satisfies the property

    -- uses function trace
    -- uses function satisfies
    -- uses function parallel_composition
    """
    cex = trace(cex, alphabet)
    if satisfies(parallel_composition(m1, cex), proprety):
        return False
    return True

def trace(cex, alphabet):
    """
    Determine the trace of a word
    :param cex: The word tha we want to determine the trace
    :param alphabet: Conter-example alphabet
    :return: Return the trace
    """
    states = {""}
    transition = {}
    state = ""
    for i in cex:
        state_avant = state
        state += str(i)
        transition[state_avant] = {}
        transition[state_avant][i] = state
        states.add(state)
    return DFA(states=states, input_symbols=alphabet, transitions=transition, initial_state="", final_states=state, allow_partial=True)



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

def satisfies(M, P):
    """
    Returns True if the system M satisfies property P.
    :param M: DFA representing the system
    :param P: error LTS representing the property
    :return: True if M satisfies P, False if not
    """
    restricted_symbols = set()
    for symbol in M.input_symbols:
        if symbol not in P.input_symbols:
            restricted_symbols.add(symbol)
    if len(restricted_symbols) > 0:
        P_complete = extend_alphabet(P, restricted_symbols)
        P = P_complete
        print("aaaaa ", P.input_symbols)
    # P is now able to read words from the M alphabet
    return M.__le__(P, witness=True)

def extend_alphabet(A, symbols_to_add):
    """
    Extends the alphabet and adds a simple transition loop on each state for each symbol to add. It produces a DFA
    with the same behaviour, but which will be able to read words from its alphabet extended with the symbols given
    in parameter.
    :param A: DFA to which the symbols will be added
    :param symbols_to_add: list of symbols to be added to the DFA
    :return: the completed DFA
    """
    # we are not using copy() to get the original alphabet because it is represented by a frozenset (immutable)
    completed_alphabet = set()
    for symbol in A.input_symbols:
        completed_alphabet.add(symbol)

    # we are not using copy() to get the original transition set because it is represented by a frozendict (immutable)
    completed_transitions = {}
    for state in A.transitions:
        completed_transitions[state] = {}
        for symbol in A.transitions[state]:
            completed_transitions[state][symbol] = A.transitions[state][symbol]

    for symbol in symbols_to_add:
        completed_alphabet.add(symbol)
        for state in A.states:
            completed_transitions[state][symbol] = state
    automate_complete = DFA(states=A.states.copy(), input_symbols=completed_alphabet, transitions=completed_transitions,
                            initial_state=A.initial_state, final_states=A.final_states.copy())
    return automate_complete


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

# exemple diapo assume guarantee
Input = DFA(
    states={"0", "1", "2"},
    input_symbols={"a", "i", "s"},
    transitions={
        "0" : {"i" : "1"},
        "1" : {"s" : "2"},
        "2" : {"a" : "0"}
    },
    initial_state="0",
    final_states={"0", "1", "2"},
    allow_partial=True
)
Output = DFA(
    states={"0", "1", "2"},
    input_symbols={"a", "o", "s"},
    transitions={
        "0" : {"s" : "1"},
        "1" : {"o" : "2"},
        "2" : {"a" : "0"}
    },
    initial_state="0",
    final_states={"0", "1", "2"},
    allow_partial=True
)
P = completedAutomata(
    states={"0", "1"},
    alphabet={"i", "o"},
    transitions={
        "0" : {"i" : "1"},
        "1" : {"o" : "0"}
    },
    initial_state="0",
    final_states={"0", "1"}
)
#alphabet = (Input.input_symbols.union(P.input_symbols)).intersection(Output.input_symbols)
alphabet = Output.input_symbols
assumption_garantee(alphabet, Input, Output, P)


# Exemple doc 2
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
#     final_states={"0", "1", "2", "3", "4"},
#     allow_partial=True
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
#     final_states={"0", "1", "2"},
#     allow_partial=True
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
#     final_states={"0", "1", "2"},
#     allow_partial=True
# )

# Exemple crane de Nazrine : Vérifier que tout b est suivi d'un c
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

assumption_garantee({"a", "b", "c", "d"}, M1, M2, P_1_2)