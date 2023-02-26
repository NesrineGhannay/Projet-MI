"""
Allows to make our automaton's table close ?
input = the table corresponding to the actual automaton
output = the updating table corresponding to the new actual automaton
-- uses function membership_test
"""

def blue(pref):
    blue = []
    for i in pref:
        if pref[i] == "blue":
            blue.append(i)
    return blue

def red(pref):
    red = []
    for i in pref:
        if pref[i] == "red":
            red.append(i)
    return red
def different(mq, pref, exp, s):
    dernier = exp[len(exp) - 1]
    for u in red(pref):
        if mq[s + dernier] == mq[u + dernier]:
            return False
    return True

def test_appartenance(u):
    return 0

def lstar_close(mq, pref, exp, alphabet):
    dernier = exp[len(exp) - 1]
    for s in blue(pref):
        if different(mq, pref, exp, s):
            pref[s] = "red"
            for a in alphabet :
                mq[s + a + dernier] = test_appartenance(s + a + dernier)
                pref[s + a] = "blue"
    return mq, pref, exp



# TEST

mq = {"": 1, "a": 0, "b": 0}
pref = {"":"red", "a":"blue", "b":"blue"}
exp = [""]
alphabet = {"a","b"}

print(lstar_close(mq, pref, exp, alphabet)[0], lstar_close(mq, pref, exp, alphabet)[1],lstar_close(mq, pref, exp, alphabet)[2])