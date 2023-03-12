from automata.fa.dfa import DFA


class Angluin:

    def __init__(self, alphabet, automate_a_apprendre):
        self.alphabet = alphabet
        self.automate = automate_a_apprendre

    def Lstar_Initialise(self):
        red = []
        red.append('epsilon')
        blue = []
        for l in self.alphabet:
            blue.append(l)
        exp = []
        exp.append('epsilon')
        n = len(red)  # nombre de lignes
        m = len(exp)  # nombre de colonnes
        M = 'teste d equivalence'
        table = [['' for j in range(m)] for i in range(n)]
        print(table)
        table['epsilon']['epsilon'] = M('epsilon')
        for lettre in self.alphabet:
            table[lettre]['epsilon'] = M(lettre)
        return table

    print(Lstar_Initialise())

    def compareOT(self, mq, exp, u, v):
        for e in exp:
            if mq[str(u + e)] != mq[str(v + e)]:
                return False
        return True

    """
    Allows to make our automaton's table close ?
    input = the table corresponding to the actual automaton
    output = the updating table corresponding to the new actual automaton
    -- uses function membership_test
    """
    def blue(self, pref):
        blue = []
        for i in pref:
            if pref[i] == "blue":
                blue.append(i)
        return blue

    def red(self, pref):
        red = []
        for i in pref:
            if pref[i] == "red":
                red.append(i)
        return red

    def is_closed(self, mq, pref, exp):
        for s in self.blue(pref):
            for u in self.red(pref):
                if not self.compareOT(mq, exp, s, u):
                    return False
        return True

    def is_consistent(self, mq, pref, exp):
        for s1 in self.red(pref):
            for s2 in self.red(pref):
                if self.compareOT(mq, exp, s1, s2):
                    for a in self.alphabet:
                        if not self.compareOT(mq, exp, str(s1 + a), str(s2 + a)):
                            return False
        return True

    def different(self, mq, pref, exp, s):
        dernier = exp[len(exp) - 1]
        for u in self.red(pref):
            if mq[s + dernier] == mq[u + dernier]:
                return False
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
        return mq, pref, T"""  # j'ai fais bordel mais je le laisse lol
    def membership_test(self, u):
        return 0

    def lstar_close(self, mq, pref, exp, alphabet):
        dernier = exp[len(exp) - 1]
        for s in self.blue(pref):
            if self.different(mq, pref, exp, s):
                pref[s] = "red"
                for a in alphabet:
                    mq[s + a + dernier] = self.membership_test(s + a + dernier)
                    pref[s + a] = "blue"
        return mq, pref, exp

    """
    Allows to make our automaton's table consistent 
    input = the table corresponding to the actual automaton
    output = the updating table corresponding to the new actual automaton
    -- uses function membership_test
    """
    def find_consistency_problem(self, mq, pref, exp):
        for s1 in pref:
            for s2 in pref:
                if pref[s1] == "red" and pref[s2] == "red":
                    if self.compareOT(mq, exp, s1, s2):
                        for e in exp:
                            for a in self.alphabet:
                                if mq[str(s1 + a + e)] != mq[str(s2 + a + e)]:
                                    return a, e
        return False

    # on a pas eu le temps de modifier mais peut etre que ça sert à rien de faire deux fois tout
    # le parcours : on peut fusionner find_consistency_problem et is_consistent

    def lstar_consistent(self, mq, pref, exp):
        a, e = self.find_consistency_problem(mq, pref, exp)
        exp.add(str(a + e))
        for line in pref:
            for e in exp:
                if str(line + e) not in mq:
                    mq[str(line + e)] = '*'  # membership_test(mq, pref, exp)


    def equivalence_test(self, mq, pref, exp):
        return True

    """
    Renvoie les préfixes d'un mot sous forme de liste. dsl je sais pas faire la documentation python propre je regarde après, j'ai mis ça pour pas oublier
    """
    def get_prefixes(self, word):
        prefixes = []
        for i in range(len(word) + 1):
            prefixes.append(word[0:i])
        return prefixes

    def LSTAR_USEEQ(self, mq, pref, exp, answer):
        prefixes = self.get_prefixes(answer)
        for p in prefixes:
            pref[p] = "red"
            for a in self.alphabet:
                if str(p + a) not in prefixes:
                    pref[str(p + a)] = "blue"
        # for line in pref.keys():
        # for line in list(pref.keys()):
        for line in [*pref]:
            for e in exp:
                if str(line + e) not in mq:
                    mq[str(line + e)] = self.membership_test(
                        str(line + e))  # nom temporaire selon comment on fait pour les requetes d'appartenance
        # return mq, pref, exp # j'allais le mettre mais enft ça modifie direct je pense (j'espère)

    """
    Create the automaton
    """
    def lstar_buildautomaton(self, mq, pref, exp):
        Q = set()
        rouge = self.red(pref)
        for u in rouge:
            etat = True
            for v in Q:
                if self.compareOT(mq, exp, u, v):
                    etat = False
                    break
            if etat:
                Q.add(u)
        F_a = set()
        delta = {}
        for q_u in Q:
            if mq[str(q_u)] == 1:
                F_a.add(q_u)
            delta[q_u] = {}
            for a in self.alphabet:
                x = q_u + a
                for y in Q:
                    if self.compareOT(mq, exp, x, y):
                        delta[q_u][a] = y
                        break
        return DFA(states=Q, input_symbols=self.alphabet, transitions=delta, initial_state="", final_states=F_a)

    # Carla : je ne sais pas à quelle méthode cela correspond
    epsilon = 0
    alphabet = {'a', 'b'}

    def lstar(self):
        mq, pref, exp = self.Lstar_Initialise()
        a = True
        while a or self.answer:
            a = False
            while not self.is_closed(mq, pref, exp) or not self.is_consistent(mq, pref, exp):
                if not self.is_closed(mq, pref, exp):
                    mq, pref, exp = self.lstar_close(mq, pref, exp, self.alphabet)
                if not self.is_consistent(mq, pref, exp):
                    mq, pref, exp = self.lstar_consistent(mq, pref, exp)  # Carla :cette méthode ne retourne rien...
            answer = self.equivalence_test(mq, pref, exp)
            if answer != True:
                mq, pref, exp = self.LSTAR_USEEQ(mq, pref, exp)  # Carla :cette méthode ne retourne rien pour l'instant
        return self.lstar_buildautomaton(mq, pref, exp)
