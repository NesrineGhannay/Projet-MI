import time

from automata.fa.dfa import DFA


class Angluin:

    def __init__(self, alphabet, automate_a_apprendre, mq={}, pref={}, exp=[]):
        self.alphabet = alphabet
        self.automate = automate_a_apprendre
        self.mq = mq
        self.pref = pref
        self.exp = exp

    def set_mq(self, mq):
        self.mq = mq

    def set_pref(self, pref):
        self.pref = pref

    def set_exp(self, exp):
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
                #print("# ", str(u + e) , " et ", str(v + e) , "COMPARER")
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
        # for s in self.blue():
        #     for u in self.red():
        #         if not self.compareOT(s, u):
        #             return False
        # return True
        elts_blue = self.blue()
        elts_red = self.red()
        lignes_red = set()
        for u in elts_red :
            lignes_red.add(str(self.ligne(u)))
        #print("Lignes rouges : ",lignes_red )
        for s in elts_blue :
            if not str(self.ligne(s)) in lignes_red:
                #print("NON, closed")
                return False
        #print("OUI, closed")
        return True

    def ligne(self, s):
        list = []
        for e in self.exp:
            list.append(self.mq[s + e])
        return list


    """
    Vérifie si la ligne correspondant à s est différente de toutes les lignes correspondantes à red
    """
    def different(self, s):
        for u in self.red():
            if self.ligne(s) == self.ligne(u):
                return False
        return True


    def fill_the_table(self, u):
        """
        Allows to fill the table's automat with a membership test for all empty gaps

        :param u: the word whose belonging to the language of the self automaton is tested
        :return : the updating table corresponding to the same automaton but filled

        -- uses function accepts_input
        """
        if self.automate.accepts_input(u):
            self.mq[u] = 1
        else:
            self.mq[u] = 0

    def lstar_close(self):
        for s in self.blue():
            if self.different(s):
                self.pref[s] = "red"
                #print("---> on fait passer ", s, " dans red")
                for a in self.alphabet:
                    for e in self.exp:
                        # self.mq[s + a + e] = self.fill_the_table(s + a + e)
                        self.fill_the_table(str(s + a + e))
                        self.pref[str(s + a)] = "blue"
                #print("****", self.red(), "\n", "**", self.blue())

    """
    Allows to find the example who make the table not consistency if she is not
    
    :return : [False, (a,e)] if the word (a+e) make the table not consistent
              [True] if the table is consistent
              
    -- uses function compareOT 
    """
    def find_consistency_problem(self):
        for word1 in self.red():
            for word2 in self.red():
                if self.compareOT(word1, word2):
                    for e in self.exp:
                        for letter in self.alphabet:
                            if self.mq[str(word1 + letter + e)] != self.mq[str(word2 + letter + e)]:
                                return [False, (letter, e)]
        return [True]



    def is_consistent(self):
        """
        Allows to know if the table is consistent or not, thanks to find_consistency_problem

        :return: False (if find_consistency_problem return [False, (a,e)] the table is not consistent)
        True  (if find_consistency_problem return only [True] the table is consistent)
        """
        res = self.find_consistency_problem()
        if res[0]:
            return True
        return False


    def lstar_consistent(self):
        """
        Allows to make our automaton's table consistent

        :return : the updating table corresponding to the new actual automaton

        -- uses function find_consistency_problem & fill_the_table
        """
        letter, e = self.find_consistency_problem()[1]
        self.exp.append(str(letter + e))
        for line in self.pref:
            for e in self.exp:
                if str(line + e) not in self.mq:
                    self.fill_the_table(str(line + e))

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
                # if str(p + a) not in prefixes :
                if str(p + a) not in prefixes and str(p + a) not in self.pref:
                    self.pref[str(p + a)] = "blue"
        # for line in pref.keys():
        # for line in list(pref.keys()):
        # for line in [*self.pref]:
        for line in self.pref:
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
    Main program: Uses Angluin’s algorithm (L*) to learn a regular language
    
    :param echec : optional variable to check how often the algorithm is wrong (parameters needed for tests)
    :return : the automaton guessed at the end of learning with Angluin
    
    -- uses functions Lstar_Initialise, is_closed, is_consistent, lstar_close, lstar_consistent, lstar_build_automaton, __eq__, LSTAR_USEEQ
    """
    def lstar(self, echec = False):
        self.Lstar_Initialise()
        #print("INITIALISER")
        #print("mq =", self.mq)
        #print("pref =", self.pref)
        #print("exp =", self.exp)
        a = True # pour rentrer dans le while car c'est un do until
        cpt = 0
        while a or answer != True:
            if echec:
                if cpt == 10:
                    return False
            a = False
            #print("BOUCLE WHILE  1")
            while not self.is_closed() or not self.is_consistent():
                #print("BOUCLE WHILE 2 : ", "clos : ",self.is_closed(), " consistent : ", self.is_consistent())
                # print("avant")
                # print("mq : ", self.mq)
                # print("pref : ", self.pref)
                # print("exp : ", self.exp)
                if not self.is_closed():
                    #print("pas fermé")
                    self.lstar_close()
                    #print("fermé ?", self.is_closed())
                    # print("mq : ", self.mq)
                    # print("pref : ", self.pref)
                    # print("exp : ", self.exp)

                if not self.is_consistent():
                    #print("pas consistant")
                    self.lstar_consistent()
                    #print("consistent ? ", self.is_consistent())
                    # print("mq : ", self.mq)
                    # print("pref : ", self.pref)
                    # print("exp : ", self.exp)

            # answer = self.equivalence_test()
            proposition = self.lstar_build_automaton() # automate construit par l'algo
            answer = proposition.__eq__(self.automate, witness=True) # test d'équivalence
            #print("answer: ", answer)

            if answer != True:
                #print("l'automate n'est pas bon")
                self.LSTAR_USEEQ(answer)
                # print("mq : ", self.mq)
                # print("pref : ", self.pref)
                # print("exp : ", self.exp)

            else:
                #print("Automate trouvé : ")
                return proposition
            cpt += 1
        # return self.lstar_build_automaton()
        return proposition