from automata.fa.dfa import DFA


class Angluin:

    def __init__(self, alphabet, automate_a_apprendre, mq={}, pref={}, exp=[]):
        self.alphabet = alphabet
        self.automate = automate_a_apprendre
        self.mq = mq
        self.pref = pref
        self.exp = exp

    def Lstar_Initialise(self):
        red = []
        red.append("")
        blue = []
        for lettre in self.alphabet:
            blue.append(lettre)

        self.exp.append("")

        for r in red:
            self.pref[r] = "red"
        for b in blue:
            self.pref[b] = "blue"

        # STA = red + blue
        for colonne in self.exp:
            for ligne in self.pref:
                self.fill_the_table(str(ligne + colonne))


    def compareOT(self, u, v):
        for e in self.exp:
            if self.mq[str(u + e)] != self.mq[str(v + e)]:
                return False
        return True

    """
    Allows to make our automaton's table close ?
    input = the table corresponding to the actual automaton
    output = the updating table corresponding to the new actual automaton
    -- uses function membership_test
    """
    def blue(self):
        blue = []
        for i in self.pref:
            if self.pref[i] == "blue":
                blue.append(i)
        return blue

    def red(self):
        red = []
        for i in self.pref:
            if self.pref[i] == "red":
                red.append(i)
        return red

    def is_closed(self):
        for s in self.blue():
            for u in self.red():
                if not self.compareOT(s, u):
                    return False
        return True

    def ligne(self, s):
        list = []
        for e in self.exp:
            list.append(self.mq[s + e])
        return list

    def different(self, s):
        for u in self.red():
            if self.ligne(s) == self.ligne(u):
                return False
        return True

    """
    Allows to fill the table's automat with a membership test for all empty gaps
    input = the table corresponding to the actual automaton
    output = the updating table corresponding to the same automaton but filled
    """
    def fill_the_table(self, u):
        if self.automate.accepts_input(u):
            self.mq[u] = 1
        else:
            self.mq[u] = 0

    def lstar_close(self):
        for s in self.blue():
            if self.different(s):
                self.pref[s] = "red"
                for a in self.alphabet:
                    for e in self.exp:
                        # self.mq[s + a + e] = self.fill_the_table(s + a + e)
                        self.fill_the_table(s + a + e)
                        self.pref[s + a] = "blue"

    """
    Allows to find the example who make the table not consistency if she is not
    input = the table corresponding to the actual automaton
    output = [False, (a,e)] if the word (a+e) make the table not consistent
             [True] if the table is consistent
    """
    def find_consistency_problem(self):
        for s1 in self.red():
            for s2 in self.red():
                if self.compareOT(s1, s2):
                    for e in self.exp:
                        for a in self.alphabet:
                            if self.mq[str(s1 + a + e)] != self.mq[str(s2 + a + e)]:
                                return [False, (a, e)]
        return [True]


    """
    Allows to know if the table is consistent or not, thanks to find_consistency_problem
    input = the table corresponding to the actual automaton
    output = False (if find_consistency_problem return [False, (a,e)] the table is not consistent)
             True  (if find_consistency_problem return only [True] the table is consistent)
    """
    def is_consistent(self):
        res = self.find_consistency_problem()
        if res[0]:
            return True
        return False

    """
    Allows to make our automaton's table consistent 
    input = the table corresponding to the actual automaton
    output = the updating table corresponding to the new actual automaton
    -- uses function membership_test
    """
    def lstar_consistent(self):
        a, e = self.find_consistency_problem()[1]
        self.exp.append(str(a + e))
        for line in self.pref:
            for e in self.exp:
                if str(line + e) not in self.mq:
                    self.fill_the_table(str(line + e))

    def equivalence_test(self):
        return True

    """
    Renvoie les préfixes d'un mot sous forme de liste. dsl je sais pas faire la documentation python propre je regarde après, j'ai mis ça pour pas oublier
    """
    def get_prefixes(self, word):
        prefixes = []
        for i in range(len(word) + 1):
            prefixes.append(word[0:i])
        return prefixes

    def LSTAR_USEEQ(self, answer):
        prefixes = self.get_prefixes(answer)
        for p in prefixes:
            self.pref[p] = "red"
            for a in self.alphabet:
                if str(p + a) not in prefixes:
                    self.pref[str(p + a)] = "blue"
        # for line in pref.keys():
        # for line in list(pref.keys()):
        for line in [*self.pref]:
            for e in self.exp:
                if str(line + e) not in self.mq:
                    self.fill_the_table(str(line+e))

    """
    Allows to create the automaton
    Input = the table corresponding to the actual automaton
    Output = the automaton corresponding to the table
    """
    def lstar_build_automaton(self):
        states = set()
        red = self.red()
        for u in red:
            state = True
            for v in states:
                if self.compareOT(u, v):
                    state = False
                    break
            if state:
                states.add(u)
        final_states = set()
        transitions = {}
        for state in states:
            if self.mq[state] == 1:
                final_states.add(state)
            transitions[state] = {}
            for letter in self.alphabet:
                x = state + letter
                for other_state in states:
                    if self.compareOT(x, other_state):
                        transitions[state][letter] = other_state
                        break
        return DFA(states=states, input_symbols=self.alphabet, transitions=transitions,
                   initial_state="", final_states=final_states)

    """
    Programme principal
    """
    def lstar(self):
        self.Lstar_Initialise()
        print("initialisé")
        a = True
        while a or self.answer:
            a = False
            while not self.is_closed() or not self.is_consistent():
                if not self.is_closed():
                    print("pas fermé")
                    self.lstar_close()
                if not self.is_consistent():
                    print("pas consistant")
                    self.lstar_consistent()
            # answer = self.equivalence_test()
            proposition = self.lstar_build_automaton() # automate construit par l'algo
            answer = proposition.__eq__(self.automate, witness=True) # test d'équivalence
            if not answer:
                print("l'automate n'est pas bon")
                self.LSTAR_USEEQ()
        # return self.lstar_build_automaton()
        return proposition
