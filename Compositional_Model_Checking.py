import util
from automata.fa.dfa import DFA

def restriction(word, alphabet):
    """
    Restricts a word to a given alphabet.
    :return: The word restricted to the letters belonging to the alphabet
    """
    restricted_word = ""
    for letter in word:
        if letter in alphabet:
            restricted_word += letter
    return restricted_word


def completedAutomata(states, alphabet, transitions, initial_state, final_states):
    """
    The automaton P (of property) is completed by a well state which is an error state (P_err = new automaton)

    :param states : the states of the automaton P
    :param alphabet: the alphabet of the automaton P
    :param transitions: the transitions of the automaton P
    :param initial_state
    : the initial states of the automaton P
    :param final_states: the finals states of the automaton P

    :return: DFA P in which the error status was added = P_err.

    """
    add_pi = False
    new_states = copy_set(states)
    new_transitions = copy_transitions(transitions)
    for state in new_states:
        if state not in new_transitions:
            new_transitions[state] = {}
        for char in alphabet:
            if char not in new_transitions[state]:
                new_transitions[state][char] = "pi"
                add_pi = True
    if add_pi:
        new_states.add("pi")
        new_transitions["pi"] = {}
        for char in alphabet:
            new_transitions["pi"][char] = "pi"
    return DFA(states=new_states, input_symbols=alphabet, transitions=new_transitions, initial_state=initial_state,
               final_states=final_states)


def completedAutomataByDFA(automaton):
    """
    The automaton P (of property) is completed by a well state which is an error state (P_err = new automaton)

    :param automaton: the dfa to be completed
    :return: DFA P in which the error status was added = P_err.

    """
    return completedAutomata(automaton.states, automaton.input_symbols, automaton.transitions, automaton.initial_state,
                             automaton.final_states)


def print_transitions(T):
    """
    Print transitions as complete sentence
    :param T : transitions

    """
    print("T ", T)
    for source in T:
        for label in T[source]:
            target = T[source][label]
            print("Transition from", source, "to", target, "labelled by", label)


def synchronization(M1, M2):
    """
    Function to make transition if the letter is on both system
    :param M1 : First system component
    :param M2 : Second system component

    :return: All transitions create if a letter is on both system
    """
    T = {}
    T1 = M1.transitions
    T2 = M2.transitions
    for q1 in T1:
        for q2 in T2:
            for a in T1[q1]:
                for b in T2[q2]:
                    if a == b:
                        if not ((q1, q2) in T):
                            T[(q1, q2)] = {}
                        if T1[q1][a] != "pi" and T2[q2][b] != "pi" :
                            target = (T1[q1][a], T2[q2][b])
                        else:
                            target = "pi"
                        T[(q1, q2)][a] = target
    return T


def interleaving(T, M1, M2):
    """
        Function to make transition if the letter isn't on both system
        :param T : Transitions already created
        :param M1 : First system component
        :param M2 : Second system component

        :return: All transitions create
        """
    T1 = M1.transitions
    T2 = M2.transitions
    for q1 in T1:
        for q2 in T2:
            for a in T1[q1]:
                if a not in M2.input_symbols:
                    if not ((q1, q2) in T):
                        T[(q1, q2)] = {}
                    if T1[q1][a] != "pi" and q2 != "pi":
                        target = (T1[q1][a], q2)
                    else:
                        target = "pi"
                    T[(q1, q2)][a] = target
            for b in T2[q2]:
                if b not in M1.input_symbols:
                    if not ((q1, q2) in T):
                        T[(q1, q2)] = {}
                    if q1 != "pi" and T2[q2][b] != "pi":
                        target = (q1, T2[q2][b])
                    else:
                        target = "pi"
                    T[(q1, q2)][b] = target
    return T


def get_final_states(states1, states2):
    """
    Returns the final states set for the parallel composition of two DFAs.
    :param states1: final states set for the first DFA
    :param states2: final states set for the second DFA
    :return: A set of final states composed of
    """
    states = set()
    for state1 in states1:
        for state2 in states2:
            states.add((state1, state2))
    return states


def parallel_composition(M1, M2):
    """
    Parallel Composition of two systems
    :param M1 : First system component
    :param M2 : Second system component

    :return : DFA who is the composition of M1 and M2
    """
    # Q : les etats (states)
    Q = set()
    Q1 = M1.states
    Q2 = M2.states
    for q1 in Q1:
        for q2 in Q2:
            Q.add((q1, q2))
    # q_0 : etat initial
    q1_0 = M1.initial_state
    q2_0 = M2.initial_state
    q_0 = (q1_0, q2_0)
    # aM : alphabet
    aM1 = M1.input_symbols
    aM2 = M2.input_symbols
    aM = aM1 | aM2
    # les transitons
    # si lettre dans intersection des alphabets de M1 et M2
    T = synchronization(M1, M2)
    # si lettre existante dans un seul des alphabet
    T_ = interleaving(T, M1, M2)
    # F : final and accepted states
    F = get_final_states(M1.final_states, M2.final_states)
    # suppression des états inutiles (sans transitions)
    reachable_states = {q_0}
    for start_state in T_:
        for char in T_[start_state]:
            reachable_states.add(T_[start_state][char])
    clean_transitions = copy_transitions(T_)
    for start_state in T_:
        if start_state not in reachable_states:
            clean_transitions.pop(start_state)
    reachable_final_states = copy_set(F)
    for state in F:
        if state not in reachable_states:
            reachable_final_states.remove(state)
    # redirection vers un état d'erreur unique
    if "pi" in reachable_states:
        if "pi" not in clean_transitions:
            clean_transitions["pi"] = {}
        for letter in aM:
            clean_transitions["pi"][letter] = "pi"
    return DFA(states=reachable_states, input_symbols=aM, transitions=clean_transitions, initial_state=q_0,
               final_states=reachable_final_states, allow_partial=True)


def assumption_garantee(alphabet, m1, m2, property):
    """
    Main program: Uses Compositional Model Checking approach to learn regular language
    :param alphabet: System alphabet
    :param m1:  First system component
    :param m2: Second system component
    :param property: Property to be verified
    :return: Return the automaton if the property is satisfied
    """
    mq, pref, exp = {}, {}, []
    M1_P = parallel_composition(m1, property)
    print("M1_P", M1_P)

    util.initialise(alphabet, M1_P, mq, exp, pref)

    util.make_close_and_consistent(mq, pref, exp, alphabet, M1_P)

    assumption = util.lstar_build_lts(alphabet, mq, pref, exp)
    answer = learning(m1, m2, assumption, property, alphabet, (mq, pref, exp))
    if answer == False:
        print("ERROR")
    else:
        print("Automate trouvé : ")
        return answer

def learning(m1, m2, assumption, property, alphabet, tables):
    """
    Model Checking Program
    :param m1: First system component
    :param m2: Second system component
    :param assumption: The determined automaton
    :param property: Property to be verified
    :param angluin: Input that allows to retrieve the methods of Angluin
    :param alphabet: System alphabet
    :return: the correct assumption or False if it's not possible to generate it
    """
    mq, pref, exp = tables

    M1_P = parallel_composition(m1, property)

    answer = False
    while not answer:
        print("\nM1_P", M1_P)
        print("mq", mq)
        print("pref", pref)
        print("exp", exp)
        print("A_i", assumption)

        compo = parallel_composition(assumption, m1)
        print("A_i || M1", compo)

        first_result = satisfies(compo, property) # first oracle
        print("first result", first_result)

        if first_result == True:
            print("m2", m2)
            print("assumption", assumption)

            completed_assumption = completedAutomataByDFA(assumption)

            cex = satisfies(m2, completed_assumption)
            print("cex", cex)

            if cex == True:
                answer = True

            elif real_error(m1, cex, property, alphabet):
                print("real_error")
                return False

            else:
                util.LSTAR_USEEQ(restriction(cex, alphabet), alphabet, mq, pref, exp, M1_P)
                util.make_close_and_consistent(mq, pref, exp, alphabet, M1_P)

                assumption = util.lstar_build_lts(alphabet, mq, pref, exp)
        else:
            util.LSTAR_USEEQ(restriction(first_result, alphabet), alphabet, mq, pref, exp, M1_P)
            util.make_close_and_consistent(mq, pref, exp, alphabet, M1_P)

            assumption = util.lstar_build_lts(alphabet, mq, pref, exp)

    return assumption


def real_error(m1, cex, property, alphabet):
    """
    Determine if the property is satisfable

    :param m1: First system component
    :param cex: Counter-example
    :param property: Property that we want to satisfy
    :param alphabet: Counter-example alphabet
    :return: True if the counter_example not satisfies the property

    -- uses function trace
    -- uses function satisfies
    -- uses function parallel_composition
    """
    composition = parallel_composition(m1, property)
    return not util.membership_query(restriction(cex, alphabet), composition)


def trace(cex, alphabet):  # TODO enlever alphabet des paramètres
    """
    Determine the trace of a word
    :param cex: The word tha we want to determine the trace
    :param alphabet: Counter-example alphabet
    :return: Return the trace
    """
    states = {""}
    transition = {}
    state = ""
    alphabet = set()
    for i in cex:
        alphabet.add(i)
        state_avant = state
        state += str(i)
        transition[state_avant] = {}
        transition[state_avant][i] = state
        states.add(state)
    return DFA(states=states, input_symbols=alphabet, transitions=transition, initial_state="", final_states={state},
               allow_partial=True)

def satisfies(M, P):
    """
    Returns True if the system M satisfies property P.
    :param M: DFA representing the system
    :param P: error LTS representing the property
    :return: True if M satisfies P, False if not
    """
    restricted_symbols = set()
    for symbol in M.input_symbols:
        if symbol not in P.input_symbols:
            restricted_symbols.add(symbol)
    print("restricted symbols", restricted_symbols)
    if len(restricted_symbols) > 0:
        P_complete = extend_alphabet(P, restricted_symbols)
        P = P_complete
    # P is now able to read words from the M alphabet
    return M.__le__(P, witness=True, lts=True)


def copy_set(s):
    result = set()
    for element in s:
        result.add(element)
    return result


def copy_transitions(transitions):
    result = {}
    for state in transitions:
        result[state] = {}
        for symbol in transitions[state]:
            result[state][symbol] = transitions[state][symbol]
    return result


def extend_alphabet(A, symbols_to_add):
    """
    Extends the alphabet and adds a simple transition loop on each state for each symbol to add. It produces a DFA
    with the same behaviour, but which will be able to read words from its alphabet extended with the symbols given
    in parameter.
    :param A: DFA to which the symbols will be added
    :param symbols_to_add: list of symbols to be added to the DFA
    :return: the completed DFA
    """
    # we are not using copy() to get the original alphabet because it is represented by a frozenset (immutable)
    completed_alphabet = copy_set(A.input_symbols)

    # we are not using copy() to get the original transition set because it is represented by a frozendict (immutable)
    completed_transitions = copy_transitions(A.transitions)

    for symbol in symbols_to_add:
        completed_alphabet.add(symbol)
        for state in A.states:
            completed_transitions[state][symbol] = state
    automate_complete = DFA(states=A.states.copy(), input_symbols=completed_alphabet, transitions=completed_transitions,
                            initial_state=A.initial_state, final_states=A.final_states.copy())
    return automate_complete
