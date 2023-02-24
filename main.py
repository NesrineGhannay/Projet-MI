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
def lstar_consistent(Mq, Pref, T, alphabet):
    for s1 in Pref:
        for s2 in Pref:
            for a in alphabet:
                for e in T:
                    if Pref[s1] == "RED" and Pref[s2] == "RED" and Mq[str(s1 + e)] == Mq[str(s2 + e)] and Mq[str(s1 + a + e)] != Mq[str(s2 + a + e)]:
                        T.add(str(a + e))
                        for x in alphabet:
                            Mq[str(x + a + e)] = '*'

    membership_test(Mq, Pref, T) # ça c'est la sauce
    return Mq, Pref, T #je me demande est-ce que c'est pas mieux de renvoyer table où table = [Mq, Pref, T]


"""
Allows to fill the table's automat with a membership test for all empty gaps
input = the table corresponding to the actual automaton
output = the updating table corresponding to the same automaton but filled
"""
"""def membership_test(automate, Mq, Pref, T, alphabet):
    for x in alphabet:
        for y in alphabet:
            if Mq[x+y] == '*':
                res = automate.accepts(x+y)
                Mq[x+y] = res
    return Mq, Pref, T""" # j'ai fais bordel mais je le laisse lol



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

