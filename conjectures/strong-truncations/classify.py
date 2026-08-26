#!/usr/bin/env python3
"""Classify census records: does the quotient H contain a balloon
(doubled edge whose two endpoints have a common neighbour)?  Tabulate
verdict x balloon and report any off-diagonal instance:

  * NOT6 without a balloon  -> the Balloon Lemma is not the only
    obstruction (breaks the characterization conjecture),
  * 6-colorable with a balloon -> contradicts the PROVED Balloon Lemma
    (engine bug somewhere: investigate immediately).

Usage: classify.py census*.txt
"""
import sys
from collections import Counter


def parse_H(raw):
    t = raw.split()
    nv, ne = int(t[0]), int(t[1])
    vals = [int(x) for x in t[2:]]
    mult = {}
    nb = [set() for _ in range(nv)]
    for i in range(ne):
        a, b, m = vals[3 * i], vals[3 * i + 1], vals[3 * i + 2]
        mult[(a, b)] = m
        nb[a].add(b)
        nb[b].add(a)
    return nv, mult, nb


def has_balloon(nv, mult, nb):
    for (a, b), m in mult.items():
        if m == 2 and (nb[a] & nb[b]) - {a, b}:
            return True
    return False


def has_double(mult):
    return any(m >= 2 for m in mult.values())


def main():
    tab = Counter()
    offenders = []
    for fn in sys.argv[1:]:
        for line in open(fn):
            if not line.startswith("R "):
                continue
            head, _, raw = line.partition(" | ")
            verdict = head.split()[4]
            raw = raw.strip()
            if not raw[0].isdigit():
                continue
            nv, mult, nb = parse_H(raw)
            bal = has_balloon(nv, mult, nb)
            dbl = has_double(mult)
            v = "7" if verdict.startswith("NOT") else ("6" if verdict == "6" else "?")
            tab[(v, bal, dbl)] += 1
            if v == "7" and not bal:
                offenders.append(("NOT6-no-balloon", fn, line.rstrip()))
            if v == "6" and bal:
                offenders.append(("SIX-with-balloon", fn, line.rstrip()))
    print("verdict  balloon  double   count")
    for (v, bal, dbl), n in sorted(tab.items()):
        print("  %s      %-5s    %-5s   %d" % (v, bal, dbl, n))
    if offenders:
        print("\nOFF-DIAGONAL INSTANCES:")
        for tag, fn, line in offenders[:50]:
            print(tag, fn, line)
        print("(%d total)" % len(offenders))
    else:
        print("\nclean: NOT6 <=> balloon, on every record read")


if __name__ == "__main__":
    main()
