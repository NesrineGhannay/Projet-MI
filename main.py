from automata.fa.dfa import DFA

# j'ai mis les tests de la documentation apparemment ça marche
# j'ai mis aussi frozendict et networkx et pydot parceque automata en a besoin

# DFA which matches all binary strings ending in an odd number of '1's
dfa = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)

print(dfa.read_input('01'))

if dfa.accepts_input('0'):
    print('accepted')
else:
    print('rejected')


"""
Allows to make our automaton's table consistent 
input = the table corresponding to the actual automaton
output = the updating table corresponding to the new actual automaton
-- uses function membership_test
"""
def lstar_consistent(mq, pref, exp):
    for s1 in pref:
        for s2 in pref:
            if pref[s1] == "RED" and pref[s2] == "RED":
                if compareOT(mq, exp, s1, s2):
                    for e in exp:
                        for a in alphabet:
                            if mq[str(s1 + a + e)] != mq[str(s2 + a + e)]:
                                exp.add(str(a + e))
                                break
    for line in pref:
        for e in exp:
            if str(line+e) not in mq:
                mq[str(line+e)] = '*' # membership_test(mq, pref, exp)


def compareOT(mq, exp, u, v):
    for e in exp:
        if mq[str(u+e)] != mq[str(v+e)] :
            return Falfor v in Q:
                etat = False
                for e in exp :
                    if mq[v + e] != mq[u + e]:
                        etat = True
                        break
                if not etat:
                    breakse
    return True



"""
Allows to fill the table's automat with a membership test for all empty gaps
input = the table corresponding to the actual automaton
output = the updating table corresponding to the same automaton but filled
"""
"""def membership_test(automate, mq, pref, T, alphabet):
    for x in alphabet:
        for y in alphabet:
            if mq[x+y] == '*':
                res = automate.accepts(x+y)
                mq[x+y] = res
    return mq, pref, T""" # j'ai fais bordel mais je le laisse lol



alphabet = [] # j'ai mis pour que ma fonction me fasse pas la tête mais on peut changer ou enlever

def LSTAR_USEEQ(mq, pref, exp, answer):
    prefixes = get_prefixes(answer)
    for p in prefixes:
        pref[p] = "red"
        for a in alphabet:
            if str(p+a) not in prefixes:
                pref[str(p+a)] = "blue"
    # for line in pref.keys():
    # for line in list(pref.keys()):
    for line in [*pref]:
        for e in exp:
            if str(line+e) not in mq:
                mq[str(line+e)] = membership_test(str(line+e)) # nom temporaire selon comment on fait pour les requetes d'appartenance
    # return mq, pref, exp # j'allais le mettre mais enft ça modifie direct je pense (j'espère)


"""
Renvoie les préfixes d'un mot sous forme de liste. dsl je sais pas faire la documentation python propre je regarde après, j'ai mis ça pour pas oublier
"""
def get_prefixes(word):
    prefixes = []
    for i in range(len(word)+1):
        prefixes.append(word[0:i])
    return prefixes


def lstar_buildautomaton(mq, pref, exp, alphabet):
    Q = set()
    for u in pref:
        if pref[u] == "red":
            etat = False  # pauline : je rajoute hors du for pour éviter l'erreur
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
        if mq[str(q_u + "lambda")] == 1:
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
    return DFA(Q, alphabet, delta, "lambda", F_a) # pauline : ici pareil je me demande si il faut pas mettre "" au lieu de "lambda"

#On pourrait écrire pref = {"red" : ["lambda", "a", "aa", "aab"], "blue" : [...]} ?
#On pourra donc accéder directement à red, au lieu de tester pour chaque mot (ligne 92/94)...

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
def different(mq, pref, exp, s):
    dernier = exp[len(exp) - 1]
    for u in red(pref):
        if mq[s + dernier] == mq[u + dernier]:
            return False
    return True

def membership_test(u):
    return 0

def lstar_close(mq, pref, exp, alphabet):
    dernier = exp[len(exp) - 1]
    for s in blue(pref):
        if different(mq, pref, exp, s): # pauline : dsl j'ai pas trop compris cette partie
            # different ça teste si la dernière colonne de s est differente de toutes les
            # dernières colonnes de red ? jsp si il faut pas tester sur tous les exp pour que
            # toute la "ligne" soit identique (jsp si c clair) comme dans la fonction compareOT
            pref[s] = "red"
            for a in alphabet : # pauline : est ce que c'est pas for e in exp plutot ?
                # ou alors j'ai mal compris
                mq[s + a + dernier] = membership_test(s + a + dernier)
                pref[s + a] = "blue"
    return mq, pref, exp