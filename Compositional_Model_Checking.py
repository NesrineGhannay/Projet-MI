from automata.fa.dfa import DFA


def restriction(mot, alphabet):
    motRestreint = ""
    for caractere in mot:
        if caractere in alphabet:
            motRestreint += caractere
    return motRestreint


"""
On complète l'automate de base par un état puits qui est un état d'erreur (P_err = nouvel automate)
input = Automate de la propriété à compléter P
output = Automate P dans lequel on a ajouté l'état d'erreur = P_err.
"""
def completedAutomata(states, alphabet, transitions, initial_state, final_states):

    ajouter_pi = False
    for dico in transitions:
        for char in alphabet:
            if char not in transitions[dico]:
                transitions[dico][char] = "pi"
                ajouter_pi = True
                if "pi" not in states:
                    states.add("pi")
    if ajouter_pi :
        transitions["pi"] = {}
        for char in alphabet :
            transitions["pi"][char] = "pi"
    return DFA(states=states, input_symbols=alphabet, transitions=transitions, initial_state=initial_state, final_states=final_states)


# TEST
# etats ={"0", "1"}
# input_symbols={"b", "a"}
# transition={"0" : {"b" : "1"}, "1" : {"a" : "0", "b" : "1"}}
# ini_state="0"
# fin_states={"1"}
#
# print(completedAutomata(etats, input_symbols, transition, ini_state, fin_states))
