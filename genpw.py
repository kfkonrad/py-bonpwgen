# /usr/bin/env python3.6
# coding=utf-8
import secrets as random  # war: import random
import sys

# Allgemein für Library
TEXFRIENDLY = False
RECURSIVE = True

setNum = "1234567890"  # 10
setalph = "abcdefghijklmnopqrstuvwxyz"  # 26
setAlph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 26
setSon = """§!@#$%^&*()-=[];'\,./_+{}:"|<>?"""  # 31
# Summe:93
"""Iterative Funktionen"""

# ergänzt den namespace um randint Funktion wie sie auch im Modul random
# verfügbar ist
random.randint = lambda x, y: x + random.randbelow(y - x + 1)
random.prevset = None


def getSet(sets, prevset):
    # Wählt ein anderes Set als das vorherige mit entsprechend passender
    # Wahrscheinlichkeit
    setlen = 0
    for s in sets:
        setlen += len(s)
    while True:
        thisset = random.randint(1, setlen)
        slen = 0
        erg = -1
        for j in range(len(sets)):
            slen += len(sets[j])
            if thisset > slen:
                erg = j
        if erg != prevset:
            prevset = erg
            break
    return erg, prevset


def random_getSet(sets):
    ret, random.prevset = getSet(sets, random.prevset)
    return sets[ret]


random.getSet = random_getSet
del (random_getSet)

random.choiceOfSets = lambda sets: random.choice(random.getSet(sets))


def random_getSet_reset():
    random.prevset = None


random.getSet_reset = random_getSet_reset
del (random_getSet_reset)


def genPW(length, sets):
    if len(sets) > 1:
        hasAllSets = False
        while not hasAllSets:
            # Stellt sicher, dass jeder Zeichenraum vertreten ist
            ret = ''.join(random.choiceOfSets(sets) for i in range(length))
            random.getSet_reset(
            )  # sollte nach jeder Anwendung von random.choiceOfSets oder
            # random.getSet gemacht werden!
            hasSet = []
            for s in sets:  # Vorhandene Sets feststellen
                charinset = False
                for char in ret:
                    if char in s:
                        charinset = True
                        break
                hasSet.append(charinset)
            setcounter = 0
            for booln in hasSet:  # Vorhandene Sets aufsummieren
                if booln:
                    setcounter += 1
            if setcounter == len(
                    sets) or setcounter == length:  # Summe der Sets prüfen
                hasAllSets = True
    else:  # Ausnahme für ein einzelnes Set, hier wird der Algorithmus
        # einfacher
        ret = ''.join(random.choice(sets[0]) for i in range(length))
    return ret


"""Rekursive Funktionen"""


def random_functional_getPW(length, sets):  # Initialisierung der Rekursion
    return random.getPW_rek(sets, None, "", length, length)


def random_functional_getPW_rek(sets, prevset, pw, length, origlength):
    # Fortsetzung der Rekursion mit 2 Abbrüchen, ruft idR random.getPW_rek2
    # auf.
    if length == 0:
        return random.checkPW(pw, sets, origlength)
    if len(sets) == 1:
        return ''.join(random.choice(sets[0]) for i in range(0, length))
    return random.getPW_rek(*random.getPW_rek2(sets, prevset, pw), length - 1,
                            origlength)


def random_functional_getPW_rek2(sets, prevset, pw):
    # Erzeugt Zufallszahl zwischen 1 und Länge aller sets zusammen, ruft damit
    # random.getPW_rek2_helper auf.
    return random.getPW_rek2_helper(sets, prevset, pw,
                                    random.randint(
                                        1, sum(len(elem) for elem in sets)))


def random_functional_getPW_rek2_helper(sets, prevset, pw, rand):
    # Wählt gewichtet nach Anzahl der Zeichen das durch rand bestimmte set aus,
    # ruft random.getPW_rek2_check auf.
    for i in range(0, len(sets)):
        if rand - sum(len(elem) for elem in sets[:i + 1]) <= 0:
            return random.getPW_rek2_check(sets, sets[i], prevset, pw)


def random_functional_getPW_rek2_check(sets, chosen, prevset, pw):
    # Prüft ob chosen gleich prevset, wenn ja zurück zu random.getPW_rek2,
    # sonst gibt es das um 1 längere PW an random.getPW_rek zurück.
    if chosen == prevset:
        return random.getPW_rek2(sets, prevset, pw)
    return sets, chosen, pw + random.choice(chosen)


def random_functional_checkPW(pw, sets, origlength):
    # Finale Überprüfung, ob das pw meine constraints erfüllt, wenn ja wird pw
    # zurückgegeben, wenn nicht alles von vorne, Aufruf random.genPW
    if all(any(char in thisset for char in pw) for thisset in sets) or (
            len(pw) == sum(
                any(char in thisset for char in pw) for thisset in sets)):
        return pw
    return random.genPW(origlength, sets)


random.genPW = random_functional_getPW
del (random_functional_getPW)

random.getPW_rek = random_functional_getPW_rek
del (random_functional_getPW_rek)

random.getPW_rek2 = random_functional_getPW_rek2
del (random_functional_getPW_rek2)

random.getPW_rek2_helper = random_functional_getPW_rek2_helper
del (random_functional_getPW_rek2_helper)

random.getPW_rek2_check = random_functional_getPW_rek2_check
del (random_functional_getPW_rek2_check)

random.checkPW = random_functional_checkPW
del (random_functional_checkPW)


def main(anzahl_in, set1, set2, set3, set4):
    truevals = ("y", True)
    set1 = True if set1 in truevals else False
    set2 = True if set2 in truevals else False
    set3 = True if set3 in truevals else False
    set4 = True if set4 in truevals else False

    global setSon, setNum, setalph, setAlph, RECURSIVE
    sets = []
    if set4:
        sets.append(setSon)
    if set3:
        sets.append(setNum)
    if set2:
        sets.append(setAlph)
    if set1:
        sets.append(setalph)
    if RECURSIVE:
        if anzahl_in > 200:
            print(
                "Passwörter von mehr als 200 Zeichen können nicht rekursiv " +
                "bestimmt werden, schalte um auf iterativ",
                file=sys.stderr)
            RECURSIVE = False
    return random.genPW(anzahl_in, sets) if RECURSIVE else genPW(
        anzahl_in, sets)


def wordify(text):
    ret = ""
    for zeichen in text:
        if zeichen == "A":
            ret += "Anton"
        elif zeichen == "B":
            ret += "Berta"
        elif zeichen == "C":
            ret += 'C"asar' if TEXFRIENDLY else "Cäsar"
        elif zeichen == "D":
            ret += "Dora"
        elif zeichen == "E":
            ret += "Emil"
        elif zeichen == "F":
            ret += "Friedrich"
        elif zeichen == "G":
            ret += "Gustav"
        elif zeichen == "H":
            ret += "Heinrich"
        elif zeichen == "I":
            ret += "Ida"
        elif zeichen == "J":
            ret += "Julius"
        elif zeichen == "K":
            ret += "Kaufmann"
        elif zeichen == "L":
            ret += "Ludwig"
        elif zeichen == "M":
            ret += "Martha"
        elif zeichen == "N":
            ret += "Nordpol"
        elif zeichen == "O":
            ret += "Otto"
        elif zeichen == "P":
            ret += "Paula"
        elif zeichen == "Q":
            ret += "Quelle"
        elif zeichen == "R":
            ret += "Richard"
        elif zeichen == "S":
            ret += "Siegfried"
        elif zeichen == "T":
            ret += "Theodor"
        elif zeichen == "U":
            ret += "Ulrich"
        elif zeichen == "V":
            ret += "Viktor"
        elif zeichen == "W":
            ret += "Wilhelm"
        elif zeichen == "X":
            ret += "Xanthippe"
        elif zeichen == "Y":
            ret += "Ypsilon"
        elif zeichen == "Z":
            ret += "Zeppelin"
        elif zeichen == "a":
            ret += "anton"
        elif zeichen == "b":
            ret += "berta"
        elif zeichen == "c":
            ret += 'c"asar' if TEXFRIENDLY else "cäsar"
        elif zeichen == "d":
            ret += "dora"
        elif zeichen == "e":
            ret += "emil"
        elif zeichen == "f":
            ret += "friedrich"
        elif zeichen == "g":
            ret += "gustav"
        elif zeichen == "h":
            ret += "heinrich"
        elif zeichen == "i":
            ret += "ida"
        elif zeichen == "j":
            ret += "julius"
        elif zeichen == "k":
            ret += "kaufmann"
        elif zeichen == "l":
            ret += "ludwig"
        elif zeichen == "m":
            ret += "martha"
        elif zeichen == "n":
            ret += "nordpol"
        elif zeichen == "o":
            ret += "otto"
        elif zeichen == "p":
            ret += "paula"
        elif zeichen == "q":
            ret += "quelle"
        elif zeichen == "r":
            ret += "richard"
        elif zeichen == "s":
            ret += "siegfried"
        elif zeichen == "t":
            ret += "theodor"
        elif zeichen == "u":
            ret += "ulrich"
        elif zeichen == "v":
            ret += "viktor"
        elif zeichen == "w":
            ret += "wilhelm"
        elif zeichen == "x":
            ret += "xanthippe"
        elif zeichen == "y":
            ret += "ypsilon"
        elif zeichen == "z":
            ret += "zeppelin"
        elif zeichen == "0":
            ret += "Null"
        elif zeichen == "1":
            ret += "Eins"
        elif zeichen == "2":
            ret += "Zwei"
        elif zeichen == "3":
            ret += "Drei"
        elif zeichen == "4":
            ret += "Vier"
        elif zeichen == "5":
            ret += 'F"unf' if TEXFRIENDLY else "Fünf"
        elif zeichen == "6":
            ret += "Sechs"
        elif zeichen == "7":
            ret += "Sieben"
        elif zeichen == "8":
            ret += "Acht"
        elif zeichen == "9":
            ret += "Neun"
        else:
            ret += zeichen
        ret += " "
    return ret[:-1]
