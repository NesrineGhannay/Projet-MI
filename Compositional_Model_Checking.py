import copy

from automata.fa.dfa import DFA


def restriction(mot, alphabet):
    motRestreint = ""
    for caractere in mot:
        if caractere in alphabet:
            motRestreint += caractere
    return motRestreint


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
    if ajouter_pi :
        transitions["pi"] = {}
        for char in alphabet :
            transitions["pi"][char] = "pi"
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=initial_state, final_states=final_states)


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

def recupetatsfinaux(etats1, etats2):           #METHODE TEMPORAIRE !!!
  etats = set()
  for etat1 in etats1 :
    for etat2 in etats2 :
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
    final = recupetatsfinaux(M1.final_states,M2.final_states)
    #return DFA(states=Q, input_symbols=aM, transitions=T_, initial_state=q_0, final_states=M1.final_states)
    print("Q ", Q)
    print("aM ", aM)
    print("T_ ", T_)
    print("q0 ", q_0)
    print("final ", final)
    return DFA(states=Q, input_symbols=aM, transitions=T_, initial_state=q_0, final_states=final, allow_partial=True)

def assumption_garantee(m1):
    m1.Lstar_Initialise()
    while not m1.is_closed():
        if not m1.is_closed():
            m1.lstar_close()
    proposition = m1.lstar_build_automaton()
    answer = learning(m1, proposition)
    if answer != True:
        print("ERROR")
    else:
        print("Automate trouvé : ")
        return proposition

def learning(m1, proposition):
    answer = False
    while answer != True :
        if consequences(parallel_composition(m1, proposition)):
            proposition = consequences(proposition) # c'est censé etre le contre exemple mise a part ca je sais pas comment on pourrait le recuperer
            if proposition == True:
                return True
            elif real_error(proposition, m1):
                return False
    return True

'''
Les deux méthodes ci dessous sont à implémenter
'''
def consequences(m1):
    return True

def real_error(m1, m2):
    return False

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

def satisfies(M, P):  # pauline
    """Renvoie True si ce DFA satisfait un automate d'erreur représentant une propriété P"""
    restreints = set()
    for symbol in M.input_symbols :
        if symbol not in P.input_symbols :
            restreints.add(symbol)
    if len(restreints) > 0:
        P_complete = etendre_alphabet(P, restreints)
    # P peut maintenant lire des mots de l'aphabet de M
    return M.__le__(P_complete, witness=True)

def etendre_alphabet(A, symboles_a_ajouter):
    """Ajoute des boucles simples sur tous les états pour transformer l'alphabet et ajoute les lettres manquantes à
    l'alphabet de A. Cela permet d'avoir un automate qui a le même comportement et qui peut lire les lettres qui
    n'appartenaient pas à son alphabet"""
    alphabet_complete = A.input_symbols.copy()
    transitions_completees = copy.deepcopy(A.transitions)
    for symbole in symboles_a_ajouter:
        alphabet_complete.add(symbole)
        for etat in A.states:
            transitions_completees[etat][symbole] = etat
    automate_complete = DFA(states=A.states, input_symbols=alphabet_complete, transitions=transitions_completees, initial_state=A.initial_state, final_states=A.final_states)
    print(automate_complete)
    return automate_complete

# tests pauline
# M = DFA(
#     states = {"0", "1", "2", "3"},
#     input_symbols={"i", "o", "s"},
#     transitions={
#         "0" : {"i" : "1", "o" : "2", "s" : "2"},
#         "1" : {"i" : "1", "o" : "0", "s" : "3"},
#         "2" : {"i" : "0", "o" : "2", "s" : "2"},
#         "3" : {"i" : "1", "o" : "0", "s" : "2"}
#     },
#     initial_state="0",
#     final_states={"0", "1", "3"}
# )
#
# P = DFA(
#     states = {"0", "1", "2"},
#     input_symbols={"i", "o"},
#     transitions={
#         "0" : {"i" : "1", "o" : "2"},
#         "1" : {"i" : "2", "o" : "0"},
#         "2" : {"i" : "2", "o" : "2"}
#     },
#     initial_state="0",
#     final_states={"0", "1"}
# )
#
# print(satisfies(M,P))