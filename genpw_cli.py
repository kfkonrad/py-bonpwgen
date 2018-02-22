# Interface
# Skriptspezifisch
import genpw
import sys

WORDIFY = True

genpw.TEXFRIENDLY = False
genpw.RECURSIVE = True

if len(sys.argv) != 6:
    if len(sys.argv) > 1:
        print(
            "Falsche Argumentzahl übergeben. Argumente werden verworfen, " +
            "interaktiver Modus wird aktiv.",
            file=sys.stderr)
    while True:
        try:
            length = int(input("Länge des Passworts angeben: "))
            if length <= 0:
                raise ValueError
            break
        except ValueError:
            print("Bitte gültige Zahl größer Null eingeben.", file=sys.stderr)
    while True:
        print(
            "Welche der folgenden Zeichenvorräte sollen im Passwort vorkommen?"
        )
        b = []
        b.append(input("Kleinbuchstaben (y/n) "))
        b.append(input("Großbuchstaben (y/n) "))
        b.append(input("Zahlen (y/n) "))
        b.append(input("Sonderzeichen (y/n) "))
        if "y" not in b:
            print(
                "Wenigstens ein Zeichenvorrät muss ausgewählt sein.",
                file=sys.stderr)
        else:
            break
else:
    length = int(sys.argv[1])
    b = sys.argv[2:]
    try:
        if int(length) <= 0:
            raise ValueError
    except ValueError:
        print("Bitte gültige Zahl größer Null eingeben.", file=sys.stderr)
        exit(1)
    if "y" not in b:
        print(
            "Wenigstens ein Zeichenvorrät muss ausgewählt sein.",
            file=sys.stderr)
        exit(1)

for i in range(len(b)):
    if "y" == b[i]:
        b[i] = True
    else:
        b[i] = False
pw = genpw.main(length, *b)
print(pw)
if WORDIFY:
    print(genpw.wordify(pw))
