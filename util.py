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

def initialise(alphabet, automaton, exp=None, pref=None):
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
            fill_the_table(str(word + e), automaton)

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
