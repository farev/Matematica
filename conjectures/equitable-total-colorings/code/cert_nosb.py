"""cert_nosb.py -- DRUP-certified plain-4-total-coloring UNSAT for every Type-2 graph of
orders 4..18, WITHOUT the symmetry-breaking clauses (so nothing rests on the color
permutation argument).  Proofs go to proofs_nosb/.  One core."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cert, tc
cert.PROOFDIR = os.path.join(HERE, "proofs_nosb")
out = []
t0 = time.time()
for n in [4, 6, 8, 10, 12, 14, 16, 18]:
    gs = open(os.path.join(HERE, f"t2_n{n}.g6")).read().split()
    for i, g6 in enumerate(gs):
        nn, E = tc.parse_graph6(g6)
        r = cert.certify(nn, E, False, False, f"n{n}_T2_{i:04d}_plain_nosymbreak")
        r["graph6"] = g6
        out.append(r)
    print(f"n={n}: {len(gs)} plain-UNSAT proofs without symmetry breaking verified ({time.time()-t0:.0f}s)", flush=True)
with open(os.path.join(HERE, "cert_type2_nosymbreak_all.json"), "w") as f:
    json.dump(out, f, indent=1)
print("ALL PROOFS VERIFIED (no symmetry breaking):", len(out), "max proof lines", max(x["proof_lines"] for x in out),
      f"total {time.time()-t0:.0f}s", flush=True)
