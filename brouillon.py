from automata.fa.dfa import DFA
"""
Allows to make our automaton's table close ?
input = the table corresponding to the actual automaton
output = the updating table corresponding to the new actual automaton
-- uses function membership_test
"""

def blue(pref):
    blue = []
    for i in pref:
        if pref[i] == "blue":
            blue.append(i)
    return blue

def red(pref):
    red = []
    for i in pref:
        if pref[i] == "red":
            red.append(i)
    return red
# def different(mq, pref, exp, s):
#     dernier = exp[len(exp) - 1]
#     for u in red(pref):
#         if mq[s + dernier] == mq[u + dernier]:
#             return False
#     return True

def ligne(mq, exp, s):
    list = []
    for e in exp:
        list.append(mq[s + e])
    return list

def different(mq, pref, exp, s):
    for u in red(pref):
        if ligne(mq, exp, s) == ligne(mq, exp, u):
            return False
    return True

def test_appartenance(u):
    return 0

# def lstar_close(mq, pref, exp, alphabet):
#     dernier = exp[len(exp) - 1]
#     for s in blue(pref):
#         if different(mq, pref, exp, s):
#             pref[s] = "red"
#             for a in alphabet :
#                 mq[s + a + dernier] = test_appartenance(s + a + dernier)
#                 pref[s + a] = "blue"
#     return mq, pref, exp

def lstar_close(mq, pref, exp, alphabet):
    for s in blue(pref):
        if different(mq, pref, exp, s):
            pref[s] = "red"
            for a in alphabet :
                for e in exp :
                    mq[s+a+e] = test_appartenance(s+a+e)
                    pref[s+a] = "blue"
    return mq, pref, exp


def lstar_buildautomaton(mq, pref, exp, alphabet):
    Q = set()
    for u in pref:
        if pref[u] == "red":
            etat = True  # pauline : je rajoute hors du for pour éviter l'erreur
            for v in Q:
                etat = False
                for e in exp :
                    if mq[v + e] != mq[u + e]:
                        etat = True
                        break
                if not etat:
                    break
            if etat:
                Q.add(u)
    F_a = set()
    F_r = set() # pauline : est ce que F_R est utilisé ?
                # Carla : Non je pense qu'on peut l'effacer. C'était seulement pour suivre le pseudo algo
    delta = {}
    for q_u in Q :
        # pauline : je pense que epsilon c'est le mot vide donc (si q_u
        # c'est bien le nom de l'état donc u) q_u + epsilon c'est juste q_u ?
        # Carla : Oui, on peut écrire seulement q_u je crois
        # pauline : je pense que si on met + "lambda" ça ne marchera pas
        if mq[str(q_u)] == 1:
            F_a.add(q_u)
        else:
            F_r.add(q_u)
        delta[q_u] = {}
        for a in alphabet:
            w = "" # pauline : je rajoute hors du for pour éviter l'erreur
            for y in Q:
                result = True
                for e in exp:
                    if mq[str(q_u + a + e)] != mq[y + e]:
                    # pauline : je pense que pareil il faut peut être regarder pour les exp ?
                    # car là si j'ai bien compris on renvoie vers le premier état tel que
                    # OT[ua][epsilon] = OT[w][epsilon] mais ça doit être égal sur toute la
                    # "ligne" je pense ? ou alors j'ai pas compris
                    # Carla : Oui c'est bien ça, je crois avoir corriger
                        result = False
                        break
                if result:
                    w = y
                    break
            delta[q_u][a] = w
    return DFA(states=Q, input_symbols=alphabet, transitions=delta, initial_state="", final_states=F_a) # pauline : ici pareil je me demande si il faut pas mettre "" au lieu de "lambda"


# TEST

mq = {"": 1, "a": 0, "b": 0}
pref = {"":"red", "a":"blue", "b":"blue"}
exp = [""]
alphabet = {"a","b"}

mq1 = {"": 0, "a":1, "b":1, "aa":0, "ab":1, "ba":0, "aaa":1, "aba":1}
pref1 = {"":"red", "a":"red", "b":"blue", "aa":"blue", "ab":"blue"}
exp1 = ["", "a"]

#print(lstar_buildautomaton(mq, pref, exp, alphabet))

print(lstar_close(mq, pref, exp, alphabet)[0], lstar_close(mq, pref, exp, alphabet)[1],lstar_close(mq, pref, exp, alphabet)[2])

print(lstar_close(mq1, pref1, exp1, alphabet)[0], lstar_close(mq1, pref1, exp1, alphabet)[1],lstar_close(mq1, pref1, exp1, alphabet)[2])