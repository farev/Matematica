"""Checks on Masselot's v1.1 revision (paper dated 2026-08-21).

1. Section 6.1 reports, for the C18 refinement stage over all 9*2
   marginal pairs: 19,152 marginal-compatible refinements, 7,560 with
   squared norm 33, and 0 solutions of the full C18 system. Recompute
   all three from scratch.

2. Appendix A prints the six order-32 constructions as [P, N]
   coordinate lists. Extract them from the PDF text layer and compare,
   as sets, with the pinned witness JSONs of v1.0 (which passed
   check_sds on 2026-08-12).

Run from conjectures/signed-difference-sets/:
    python3 masselot-review/check_v11_revision.py <path-to-v1.1-pdf>
"""

import glob
import json
import os
import re
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qrlib  # noqa: E402
from validate_pipeline import profile_ok  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def check_c18_counts():
    k, lam, s = 29, 4, 13
    _, C9s = qrlib.enum_system([9], 4, k, lam, s)
    _, C2s = qrlib.enum_system([2], 18, k, lam, s)
    assert len(C9s) == 9 and len(C2s) == 2
    pair_split = {t: [p for p in product(range(-2, 3), repeat=2)
                      if sum(p) == t] for t in range(-4, 5)}
    peak18, off18 = k + lam, 2 * lam
    add18, _, _ = qrlib.add_table([18])
    neg18 = qrlib.neg_table([18])
    n_marginal = n_norm = n_sol = 0
    for T in C9s:
        for R in C2s:
            for combo in product(*[pair_split[t] for t in T]):
                vec = [0] * 18
                even = odd = 0
                for i, (b0, b1) in enumerate(combo):
                    vec[i] = b0
                    vec[i + 9] = b1
                    if i % 2 == 0:
                        even += b0
                        odd += b1
                    else:
                        odd += b0
                        even += b1
                if (even, odd) != tuple(R):
                    continue
                n_marginal += 1
                if sum(c * c for c in vec) != peak18:
                    continue
                n_norm += 1
                if profile_ok(vec, add18, neg18, peak18, off18):
                    n_sol += 1
    # independent recount of the marginal-compatible total: DP over
    # fibers on (even-sum, odd-sum), no vectors materialized
    n_marginal_dp = 0
    for T in C9s:
        states = {(0, 0): 1}
        for i, t in enumerate(T):
            nxt = {}
            for (e, o), cnt in states.items():
                for (b0, b1) in pair_split[t]:
                    de, do = (b0, b1) if i % 2 == 0 else (b1, b0)
                    key = (e + de, o + do)
                    nxt[key] = nxt.get(key, 0) + cnt
            states = nxt
        for R in C2s:
            n_marginal_dp += states.get(tuple(R), 0)
    print(f"[1] C18 refinement stage over all {len(C9s)}x{len(C2s)} "
          f"marginal pairs:")
    print(f"    marginal-compatible refinements: {n_marginal} "
          f"(DP recount: {n_marginal_dp}; paper: 19,152)")
    print(f"    with squared norm 33:            {n_norm} (paper: 7,560)")
    print(f"    full C18 system solutions:       {n_sol} (paper: 0)")
    return (n_marginal == n_marginal_dp and n_norm == 7560
            and n_sol == 0)


GROUPS = [
    ("C2 x C16", [2, 16], "sds_32_20_4_2_16.json"),
    ("C4 x C8", [4, 8], "sds_32_20_4_4_8.json"),
    ("C2^2 x C8", [2, 2, 8], "sds_32_20_4_2_2_8.json"),
    ("C2 x C4^2", [2, 4, 4], "sds_32_20_4_2_4_4.json"),
    ("C2^3 x C4", [2, 2, 2, 4], "sds_32_20_4_2_2_2_4.json"),
    ("C2^5", [2, 2, 2, 2, 2], "sds_32_20_4_2_2_2_2_2.json"),
]


def json_sets(fname, G):
    with open(os.path.join(HERE, "witnesses", fname)) as f:
        w = json.load(f)
    vec = w["coefficient_vector"]
    P, N = set(), set()
    for i, a in enumerate(vec):
        if not a:
            continue
        x, c = i, []
        for n in reversed(G):
            c.append(x % n)
            x //= n
        g = tuple(reversed(c))
        (P if a == 1 else N).add(g)
    return P, N


def check_appendix(pdf_path):
    from pypdf import PdfReader
    text = ""
    for page in PdfReader(pdf_path).pages:
        text += page.extract_text() + "\n"
    apx = text[text.index("Explicit order-32 constructions"):]
    # tuples appear in order: P-set then N-set for each of the six
    # groups; a tuple is (d,d) up to (d,d,d,d,d), coordinates may have
    # two digits (e.g. (0,10))
    tuples = [tuple(int(x) for x in re.findall(r"\d+", t))
              for t in re.findall(r"\((?:\s*\d+\s*,)+\s*\d+\s*\)", apx)]
    ok_all = True
    pos = 0
    for name, G, fname in GROUPS:
        P, N = json_sets(fname, G)
        r = len(G)
        mine = [t for t in tuples[pos:] if True]
        seg = []
        while len(seg) < len(P) + len(N):
            t = tuples[pos]
            if len(t) != r:
                print(f"    parse error at {name}: tuple {t}")
                return False
            seg.append(t)
            pos += 1
        pP, pN = set(seg[: len(P)]), set(seg[len(P):])
        ok = (pP == P) and (pN == N)
        ok_all &= ok
        print(f"    {name}: printed P ({len(pP)}) == file P: {pP == P}; "
              f"printed N ({len(pN)}) == file N: {pN == N}")
    return ok_all


def main():
    ok1 = check_c18_counts()
    print("[2] Appendix A constructions vs pinned v1.0 witness files:")
    ok2 = check_appendix(sys.argv[1])
    print(f"\nrevision checks: {'ALL PASS' if ok1 and ok2 else 'FAIL'}")
    sys.exit(0 if ok1 and ok2 else 1)


if __name__ == "__main__":
    main()
