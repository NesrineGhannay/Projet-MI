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
        red = [""]
        blue = []
        for letter in self.alphabet:
            blue.append(letter)

        self.exp.append("")

        for r in red:
            self.pref[r] = "red"
        for b in blue:
            self.pref[b] = "blue"

        # STA = red + blue
        for e in self.exp:
            for word in self.pref:
                self.fill_the_table(str(word + e))

    def compareOT(self, word1, word2):
        """
        Compares the lines in the Observation Table given two words belonging to RED or BLUE.
        :param word1: first word to compare
        :param word2: second word to compare
        :return: True if the lines are equals, False if not
        """
        for e in self.exp:
            if self.mq[str(word1 + e)] != self.mq[str(word2 + e)]:
                return False
        return True

    def blue(self):
        """
        Returns all the words from BLUE, representing the current states' successors which are not in RED.
        :return: a list containing prefixes from the BLUE category
        """
        blue = []
        for i in self.pref:
            if self.pref[i] == "blue":
                blue.append(i)
        return blue

    def red(self):
        """
        Returns all the words from RED, representing the current DFA set of states.
        :return: a list containing prefixes from the RED category
        """
        red = []
        for i in self.pref:
            if self.pref[i] == "red":
                red.append(i)
        return red

    def is_closed(self):
        """
        Determine if the table is closed
        :return: True if it's closed
        -- uses function blue
        -- uses function red
        """
        elts_blue = self.blue()
        elts_red = self.red()
        lignes_red = set()
        for u in elts_red :
            lignes_red.add(str(self.line(u)))
        for s in elts_blue :
            if not str(self.line(s)) in lignes_red:
                return False
        return True

    def line(self, s):
        """
        Retrieve the values of a line from the table
        :param s:  The word for which we want to retrieve the line
        :return: Return the values in a list
        """
        values = []
        for e in self.exp:
            values.append(self.mq[s + e])
        return values

    def different(self, s):
        """
        Check if the line s is different from all lines of red
        :param s: Line of the table we want to compare
        :return: True if there's different False else
        -- uses function red
        -- uses function line
        """
        for u in self.red():
            if self.line(s) == self.line(u):
                return False
        return True

    def fill_the_table(self, u):
        """
        Fills the empty gaps in the observation table with membership tests.
        :param u : the word whose belonging to the language of the self automaton is tested

        -- uses function accepts_input
        """
        if self.automate.accepts_input(u):
            self.mq[u] = 1
        else:
            self.mq[u] = 0

    def lstar_close(self):
        """
        Updates the observation table to make it closed.
        -- uses function blue
        -- uses function different
        -- uses function fill_the_table
        """
        for s in self.blue():
            if self.different(s):
                self.pref[s] = "red"
                for a in self.alphabet:
                    for e in self.exp:
                        self.fill_the_table(str(s + a + e))
                        self.pref[str(s + a)] = "blue"
    def find_consistency_problem(self):
        """
        Finds the example making the table not consistent if it is not.

        :return: [False, (a,e)] if the word (a+e) make the table not consistent,
                  [True] if the table is consistent

        -- uses function compareOT
            """
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
        Makes the automaton's table consistent.

        -- uses function find_consistency_problem & fill_the_table
        """
        letter, e = self.find_consistency_problem()[1]
        self.exp.append(str(letter + e))
        for line in self.pref:
            for e in self.exp:
                if str(line + e) not in self.mq:
                    self.fill_the_table(str(line + e))

    def get_prefixes(self, word):
        """
        Returns the word's prefixes in a list.
        :param word: the word to get prefixes from
        :return: a list containing the word's prefixes
        """
        prefixes = []
        for i in range(len(word) + 1):
            prefixes.append(word[0:i])
        return prefixes

    def LSTAR_USEEQ(self, answer):
        """
        Modifies the observation table in order to correct the false assumption, by using the counter-example returned.
        :param answer: the counter-example returned after the equivalence query
        """
        prefixes = self.get_prefixes(answer)
        for p in prefixes:
            self.pref[p] = "red"
            for a in self.alphabet:
                if str(p + a) not in prefixes and str(p + a) not in self.pref:
                    self.pref[str(p + a)] = "blue"
        for line in self.pref:
            for e in self.exp:
                if str(line + e) not in self.mq:
                    self.fill_the_table(str(line+e))

    def lstar_build_automaton(self):
        """
        Build the automaton thanks mq, pref and exp.

        :return: the automaton built

        -- uses functions red, compareOT
        """
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

    def lstar(self, count_failures = False):
        """
        Main program: Uses Angluin’s algorithm (L*) to learn a regular language.

        :param count_failures: optional variable to check how often the algorithm is wrong (used for tests)
        :return: the automaton guessed at the end of learning with Angluin

        -- uses functions Lstar_Initialise, is_closed, is_consistent, lstar_close, lstar_consistent, lstar_build_automaton, dfa.__eq__, LSTAR_USEEQ
        """
        self.Lstar_Initialise()
        first_iteration = True # to enter the while loop
        count = 0
        while first_iteration or not answer :
            if count_failures:
                if count == 10:
                    return False
            first_iteration = False
            while not self.is_closed() or not self.is_consistent():
                if not self.is_closed():
                    self.lstar_close()

                if not self.is_consistent():
                    self.lstar_consistent()

            assumption = self.lstar_build_automaton()
            answer = assumption.__eq__(self.automate, witness=True) # equivalence query

            if not answer :
                self.LSTAR_USEEQ(answer)
            else:
                return assumption
            count += 1
        return assumption