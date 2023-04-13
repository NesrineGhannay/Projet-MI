

def restriction(mot, alphabet):
    motRestreint = ""
    for caractere in mot:
        if caractere in alphabet:
            motRestreint += caractere
    return motRestreint


"""
On complète l'automate de base par un état puits qui est un état d'erreur (P_err = nouvel automate)
input = Automate à compléter
output = Automate dans lequel on a ajouté l'état d'erreur.
"""
def completedAutomata(automate):

    return automate