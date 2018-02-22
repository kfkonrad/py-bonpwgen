# /usr/bin/env python3.6
# coding=utf-8
import genpw
import sys
genpw.TEXFRIENDLY = True
genpw.RECURSIVE = True

# Interface
if len(sys.argv) < 2:
    print("Name des/der Server übergeben!", file=sys.stderr)
    exit(1)
for name in sys.argv[1:]:
    pw = genpw.main(12, 'y', 'y', 'y', 'n')
    print(name, end=" & ")
    print(pw, end=" & ")
    print(genpw.wordify(pw), end=" ")
    print(r"\\\hline")
