import copy

from Angluin import Angluin
from automata.fa.dfa import DFA


# def restriction(mot, alphabet):
#     motRestreint = ""
#     for caractere in mot:
#         if caractere in alphabet:
#             motRestreint += caractere
#     return motRestreint


"""
On complète l'automate de base par un état puits qui est un état d'erreur (P_err = nouvel automate)
input = Automate de la propriété à compléter P
output = Automate P dans lequel on a ajouté l'état d'erreur = P_err.
"""
def completedAutomata(states, alphabet, transitions, initial_state, final_states):
    ajouter_pi = False
    for dico in transitions:
        for char in alphabet:
            if char not in transitions[dico]:
                transitions[dico][char] = "pi"
                ajouter_pi = True
                if "pi" not in states:
                    states.add("pi")
    if ajouter_pi:
        transitions["pi"] = {}
        for char in alphabet:
            transitions["pi"][char] = "pi"
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
               final_states=final_states)


# TEST
# etats ={"0", "1"}
# input_symbols={"b", "a"}
# transition={"0" : {"b" : "1"}, "1" : {"a" : "0", "b" : "1"}}
# ini_state="0"
# fin_states={"1"}
#
# print(completedAutomata(etats, input_symbols, transition, ini_state, fin_states))

# Modele Cheking

# Produit parallele : Lidia
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
                        # for t1 in T1[q1][a]:
                        #     print("T1[q1][a] ", T1[q1][a])
                        #     for t2 in T2[q2][b]:
                        #         print(t1, " ", t2)
                        #         target.add((t1, t2))
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
                    # target = set()
                    # for t1 in T1[q1][a]:
                    #     print("(t1, q2) ", (t1, q2))
                    #     target.add((t1, q2))
                    T[(q1, q2)][a] = target
            for b in T2[q2]:
                if b not in M1.input_symbols:
                    if not ((q1, q2) in T):
                        T[(q1, q2)] = {}
                    target = (q1, T2[q2][b])
                    # target = set()
                    # for t2 in T2[q2][b]:
                    #     print("(q1, t2) ", (q1, t2))
                    #     target.add((q1, t2))
                    T[(q1, q2)][b] = target
    return T


def recupetatsfinaux(etats1, etats2):  # METHODE TEMPORAIRE !!!
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
    # ATTENTION ETAT FINAL PAS FAIT
    final = recupetatsfinaux(M1.final_states, M2.final_states)
    # return DFA(states=Q, input_symbols=aM, transitions=T_, initial_state=q_0, final_states=M1.final_states)
    print("Q ", Q)
    print("aM ", aM)
    print("T_ ", T_)
    print("q0 ", q_0)
    print("final ", final)
    return DFA(states=Q, input_symbols=aM, transitions=T_, initial_state=q_0, final_states=final, allow_partial=True)
#Carla : Pourquoi les transitions de la synchronisation n'y sont pas ?


def assumption_garantee(alphabet, m1, m2, property):
    prop = Angluin(alphabet, m2)
    proposition = prop.Lstar_Initialise()
    while not proposition.is_closed(): #Carla : C'est la même chose que while not m1.is_closed() ? Réponse : Oui c'est vrai
        proposition.lstar_close()
    proposition = proposition.lstar_build_automaton()
    answer = learning(m1, m2, proposition, property, prop)
    if answer == False:
        print("ERROR")
    else:
        print("Automate trouvé : ")
        return answer


def learning(m1, m2, proposition, property, prop, alphabet):
    answer = False
    while answer != True:
        if satisfies(parallel_composition(m1, proposition), property):
            cex = satisfies(m2, proposition)
            if cex == True:
                answers = True
            elif real_error(cex, m2, property, alphabet):
                return False
            else :
                proposition = prop.LSTAR_USEEQ()
    return proposition

'''
Les deux méthodes ci dessous sont à implémenter
'''

def real_error(m1, cex, propriete, alphabet):
    cex = trace(cex, alphabet)
    if satisfies(parallel_composition(m1, cex), propriete):
        return False
    return True

def trace(cex, alphabet):
    states = {""}
    transition = {}
    state = ""
    for i in cex:
        state_avant = state
        state += str(i)
        transition[state_avant] = {}
        transition[state_avant][i] = state
        states.add(state)
    return DFA(states, alphabet, transition, "", state, True)



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
