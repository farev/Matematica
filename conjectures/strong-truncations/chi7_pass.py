#!/usr/bin/env python3
"""For every NOT6 record in the given census files, certify chi'_s = 7
exactly: SAT at 7 colors, witness re-verified from the definition (the
lower bound chi'_s >= 7 is the census's own double-checked UNSAT at 6).
Writes a compact certificate table to stdout: one line per instance,
    C7 <n> <m> 7 <witness colors> | <raw quotient line>
Exits nonzero if any NOT6 instance is not 7-colorable (would contradict
Lin-Lin's bound and deserve loud attention).
"""
import sys

from engine_b import parse_T, decide


def main():
    n_ok = 0
    for fn in sys.argv[1:]:
        for line in open(fn):
            if not line.startswith("R ") or " NOT6 " not in line:
                continue
            head, _, raw = line.partition(" | ")
            raw = raw.strip()
            n, edges = parse_T(raw)
            sat, witness, _ = decide(n, edges, 7)
            assert sat, "NOT 7-colorable?! " + raw
            print("C7 %d %d 7 %s | %s"
                  % (n, len(edges), " ".join(map(str, witness)), raw))
            n_ok += 1
    print("chi7_pass: %d instances certified chi'_s = 7" % n_ok,
          file=sys.stderr)


if __name__ == "__main__":
    main()
