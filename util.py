from automata.fa.dfa import DFA


def fill_the_table(u, automate, mq=None):
    """
    Fills the empty gaps in the observation table with membership tests.
    :param u : the word whose belonging to the language of the self automaton is tested

    -- uses function accepts_input
    """
    if mq is None:
        mq = {}
    if automate.accepts_input(u):
        mq[u] = 1
    else:
        mq[u] = 0


def initialise(alphabet, automaton, mq=None, exp=None, pref=None):
    if mq is None:
        mq = {}
    if exp is None:
        exp = []
    if pref is None:
        pref = {}
    red = [""]
    blue = []
    for letter in alphabet:
        blue.append(letter)
    exp.append("")
    for r in red:
        pref[r] = "red"
    for b in blue:
        pref[b] = "blue"
    for e in exp:
        for word in pref:
            fill_the_table(str(word + e), automaton, mq)


def is_closed(pref, exp, mq):
    """
    Determine if the table is closed

    :return: True if it's closed

    -- uses function blue
    -- uses function red
    """
    elts_blue = blue(pref)
    elts_red = red(pref)
    lines_red = set()
    for u in elts_red:
        lines_red.add(str(line(u, exp, mq)))
    for s in elts_blue:
        if not str(line(s, exp, mq)) in lines_red:
            return False
    return True


def lstar_close(mq, pref, exp, alphabet, automaton):
    """
    Updates the observation table to make it closed.
    -- uses function blue
    -- uses function different
    -- uses function fill_the_table
    """
    for s in blue(pref):
        if different(s, mq, pref, exp):
            pref[s] = "red"
            for a in alphabet:
                for e in exp:
                    fill_the_table(str(s + a + e), automaton, mq)
                    pref[str(s + a)] = "blue"


def lstar_consistent(mq, pref, exp, automaton, alphabet):
    """
    Makes the automaton's table consistent.

    -- uses function find_consistency_problem & fill_the_table
    """
    letter, e = find_consistency_problem(pref, exp, mq, alphabet)[1]
    exp.append(str(letter + e))
    for line in pref:
        for e in exp:
            if str(line + e) not in mq:
                fill_the_table(str(line + e), automaton, mq)


def is_consistent(mq, pref, exp, alphabet):
    """
        Allows to know if the table is consistent or not, thanks to find_consistency_problem

        :return: False (if find_consistency_problem return [False, (a,e)] the table is not consistent)
        True  (if find_consistency_problem return only [True] the table is consistent)
        """
    res = find_consistency_problem(pref, exp, mq, alphabet)
    if res[0]:
        return True
    return False


def find_consistency_problem(pref, exp, mq, alphabet):
    """
        Finds the example making the table not consistent if it is not.

        :return: [False, (a,e)] if the word (a+e) make the table not consistent,
                  [True] if the table is consistent

        -- uses function compareOT
            """
    for word1 in red(pref):
        for word2 in red(pref):
            if compareOT(word1, word2, mq, exp):
                for e in exp:
                    for letter in alphabet:
                        if mq[str(word1 + letter + e)] != mq[str(word2 + letter + e)]:
                            return [False, (letter, e)]
    return [True]


def lstar_build_automaton(alphabet, mq, pref, exp):
    """
    Build the automaton thanks mq, pref and exp.

    :return: the automaton built

    -- uses functions red, compareOT
    """
    states = set()
    red_words = red(pref)
    for u in red_words:
        state = True
        for v in states:
            if compareOT(u, v, mq, exp):
                state = False
                break
        if state:
            states.add(u)
    final_states = set()
    transitions = {}
    for state in states:
        if mq[state] == 1:
            final_states.add(state)
        transitions[state] = {}
        for letter in alphabet:
            x = state + letter
            for other_state in states:
                if compareOT(x, other_state, mq, exp):
                    transitions[state][letter] = other_state
                    break
    return DFA(states=states, input_symbols=alphabet, transitions=transitions,
               initial_state="", final_states=final_states)


def LSTAR_USEEQ(answer, alphabet, mq, pref, exp, automaton):
    """
        Modifies the observation table in order to correct the false assumption, by using the counter-example returned.
        :param answer: the counter-example returned after the equivalence query
        """
    print("avant:")
    print("mq", mq)
    print("pref", pref)
    print("exp", exp)
    prefixes = get_prefixes(answer)
    for p in prefixes:
        pref[p] = "red"
        for a in alphabet:
            if str(p + a) not in prefixes and str(p + a) not in pref:
                pref[str(p + a)] = "blue"
    for line in pref:
        for e in exp:
            if str(line + e) not in mq:
                fill_the_table(str(line + e), automaton, mq)
    print("après:")
    print("mq", mq)
    print("pref", pref)
    print("exp", exp)


def red(pref):
    """
    Returns all the words from RED, representing the current DFA set of states.

    :return: a list containing prefixes from the RED category
    """
    red = []
    for i in pref:
        if pref[i] == "red":
            red.append(i)
    return red


def blue(pref):
    """
    Returns all the words from BLUE, representing the current states' successors which are not in RED.

    :return: a list containing prefixes from the BLUE category
    """
    blue = []
    for i in pref:
        if pref[i] == "blue":
            blue.append(i)
    return blue


def line(s, exp, mq):
    """
    Retrieve the values of a line from the table

    :param s:  The word for which we want to retrieve the line

    :return: Return the values in a list
    """
    values = []
    for e in exp:
        values.append(mq[s + e])
    return values


def different(s, mq, pref, exp):
    """
        Check if the line s is different from all lines of red

        :param s: Line of the table we want to compare
        :return: True if there's different False else

        -- uses function red
        -- uses function line
        """
    for u in red(pref):
        if line(s, exp, mq) == line(u, exp, mq):
            return False
    return True


def compareOT(word1, word2, mq, exp):
    """
    Compares the lines in the Observation Table given two words belonging to RED or BLUE

    param word1: first word to compare
    :param word2: second word to compare
    :return: True if the lines are equals, False if not
    """
    for e in exp:
        if mq[str(word1 + e)] != mq[str(word2 + e)]:
            return False
    return True


def get_prefixes(word):
    """
        Returns the word's prefixes in a list.
        :param word: the word to get prefixes from
        :return: a list containing the word's prefixes
        """
    prefixes = []
    for i in range(len(word) + 1):
        prefixes.append(word[0:i])
    return prefixes
