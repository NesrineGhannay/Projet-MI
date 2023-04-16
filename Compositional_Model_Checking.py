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
    for source in T:
        for label in T[source]:
            for target in T[source][label]:
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
                        target = set()
                        for t1 in T1[q1][a]:
                            for t2 in T2[q2][b]:
                                target.add((t1, t2))
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
                    target = set()
                    for t1 in T1[q1][a]:
                        target.add((t1, q2))
                    T[(q1, q2)][a] = target
            for b in T2[q2]:
                if b not in M1.input_symbols:
                    if not ((q1, q2) in T):
                        T[(q1, q2)] = {}
                    target = set()
                    for t2 in T2[q2][b]:
                        target.add((q1, t2))
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
    return completedAutomata(Q, aM, T_, q_0, final)

A = completedAutomata(
        states = {"0", "1", "2"},
        alphabet = {"in", "send", "ack"},
        transitions = {
            "0": {"in" : "1"},
            "1": {"send" : "2"},
            "2": {"ack" : "0"}
                        },
        initial_state = "0",
        final_states = {"2"}
        )

B = completedAutomata(
        states = {"a", "b", "c"},
        alphabet = {"out", "send", "ack"},
        transitions = {
            "a": {"send" : "b"},
            "b": {"out" : "c"},
            "c": {"ack" : "a"}
                        },
        initial_state = "a",
        final_states = {"c"}
        )

print_transitions(A.transitions)
print(A)
print(B)
print(parallel_composition(A, B))