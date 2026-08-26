#!/usr/bin/env python3
"""Second-pass resolution and cross-checking for census outputs.

Reads strong6 output files; every CAP line is decided by Engine B (SAT),
every NOT6 line is INDEPENDENTLY re-decided by Engine B; disagreements
are fatal.  Emits a patched census file where CAP lines are replaced by
the SAT verdict (marked engine=B) and NOT6 lines carry engine=A+B.

Usage: resolve_undecided.py in.txt > out.txt
"""
import sys

from engine_b import parse_T, decide


def main():
    fn = sys.argv[1]
    n_cap = n_not = 0
    for line in open(fn):
        if not line.startswith("R "):
            continue
        head, _, raw = line.partition(" | ")
        toks = head.split()
        verdict = toks[4]
        raw = raw.strip()
        if verdict == "CAP":
            n, edges = parse_T(raw)
            sat, witness, _ = decide(n, edges, 6)
            n_cap += 1
            if sat:
                print("R %s %s %s 6 B %s | %s" %
                      (toks[1], toks[2], toks[3], " ".join(map(str, witness)), raw))
            else:
                sat7, _, _ = decide(n, edges, 7)
                assert sat7, "chi > 7?!"
                print("R %s %s %s NOT6 B chi=7 | %s" %
                      (toks[1], toks[2], toks[3], raw))
        elif verdict.startswith("NOT"):
            n, edges = parse_T(raw)
            sat, _, _ = decide(n, edges, 6)
            assert not sat, "ENGINE DISAGREEMENT on line: " + line
            n_not += 1
            toks[5] = "A+B"          # nodes slot -> engine tag; raw unchanged
            print(" ".join(toks) + " | " + raw)
        else:
            print(line.rstrip())
    print("resolve: %d CAP decided by B, %d NOT6 B-confirmed" %
          (n_cap, n_not), file=sys.stderr)


if __name__ == "__main__":
    main()
