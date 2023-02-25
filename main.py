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
Allows to make our automaton's table more consistent ?
input = the table corresponding to the actual automaton
output = the updating table corresponding to the new actual automaton
-- uses function membership_test
"""
def lstar_consistent(mq, pref, exp, alphabet):
    for s1 in pref:
        for s2 in pref:
            for a in alphabet:
                for e in exp:
                    if pref[s1] == "RED" and pref[s2] == "RED" and mq[str(s1 + e)] == mq[str(s2 + e)] and mq[str(s1 + a + e)] != mq[str(s2 + a + e)]:
                        exp.add(str(a + e))
                        for x in alphabet:
                            mq[str(x + a + e)] = '*'

    membership_test(mq, pref, exp) # ça c'est la sauce
    return mq, pref,exp #je me demande est-ce que c'est pas mieux de renvoyer table où table = [mq, pref, exp]


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
                mq[str(line+e)] # = membership_query(str(line+e)) # nom temporaire selon comment on fait pour les requetes d'appartenance
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
    V = set()
    for u in pref:
        etat = True
        if pref[u] == "red":
            for v in V:
                if mq[v] == mq[u]:  #Dois-je le faire pour tous les "v + exp" ???
                    etat = False
                    break
            if etat:
                V.add(u)
    F_a = set()
    F_r = set()
    delta = {}
    for q_u in Q :
        if mq[str(q_u + "lambda")] == 1:
            F_a.add(q_u)
        else:
            F_r.add(q_u)
        delta[q_u] = {}
        for a in alphabet:
            for y in Q:
                if mq[str(q_u + a)] == mq[y]:
                    w = y
                    break
            delta[q_u][a] = w
    return DFA(Q, alphabet, delta, "lambda", F_a)

#On pourrait écrire pref = {"red" : ["lambda", "a", "aa", "aab"], "blue" : [...]} ?
#On pourra donc accéder directement à red, au lieu de tester pour chaque mot (ligne 92/94)...