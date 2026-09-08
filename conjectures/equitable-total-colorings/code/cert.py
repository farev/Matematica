"""cert.py -- DRUP-certified UNSAT verdicts through satpipe.solve_certified
(CaDiCaL verdict, Glucose 4 DRUP proof, checked by the repository's rup_check).

  python3 cert.py R            # graph R: equitable-4TC UNSAT with proof (sym-broken and plain CNF)
  python3 cert.py type2 <tag>  # every T2 line of results_<tag>.tsv: plain-4TC UNSAT with proof
  python3 cert.py cx <tag>     # every X line of results_<tag>.tsv: equitable UNSAT with proof
"""
import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/tmp/claude-0/-home-user-Matematica/bc2c3ee2-f3c1-5718-9876-930480583604/scratchpad/work")
import tc
from satpipe import solve_certified

PROOFDIR = os.path.join(HERE, "proofs")


def certify(n, edges, equitable, symbreak, tag):
    cl, nv = tc.encode(n, edges, equitable=equitable, symbreak=symbreak)
    t = time.time()
    verdict, model, proof = solve_certified(cl, nv, tag, PROOFDIR, want_proof=True, verbose=False)
    dt = time.time() - t
    assert verdict == "UNSAT", (tag, verdict)
    plen = sum(1 for _ in open(proof))
    return dict(tag=tag, n=n, equitable=equitable, symbreak=symbreak, nclauses=len(cl), nvars=nv,
                proof=os.path.relpath(proof, HERE), proof_lines=plen, seconds=round(dt, 3))


if __name__ == "__main__":
    mode = sys.argv[1]
    out = []
    if mode == "R":
        n, E = tc.graph_R()
        out.append(certify(n, E, True, True, "R_equitable_symbreak"))
        out.append(certify(n, E, True, False, "R_equitable_nosymbreak"))
    else:
        tag = sys.argv[2]
        want = {"type2": "T2", "cx": "X"}[mode]
        rows = [l.split("\t") for l in open(os.path.join(HERE, f"results_{tag}.tsv")).read().splitlines()[1:]]
        gs = [r[0] for r in rows if r[1] == want]
        print(f"{len(gs)} graphs of class {want} in results_{tag}.tsv", flush=True)
        for i, g6 in enumerate(gs):
            n, E = tc.parse_graph6(g6)
            safe = g6.replace("?", "Q").replace("/", "S").replace("\\", "B").replace("`", "G").replace("|", "P").replace("~", "T").replace("@", "A").replace("[", "L").replace("]", "M").replace("^", "H").replace("_", "U").replace("{", "l").replace("}", "m").replace("'", "q").replace('"', "d").replace("<", "s").replace(">", "b").replace(":", "c").replace(";", "e").replace("=", "f").replace("&", "j").replace("$", "k").replace("#", "n").replace("!", "o").replace("%", "p").replace("(", "r").replace(")", "t").replace("*", "u").replace("+", "v").replace(",", "w").replace("-", "x").replace(".", "y")
            if want == "T2":
                out.append(certify(n, E, False, True, f"{tag}_T2_{i:04d}_{safe}"))
            else:
                out.append(certify(n, E, True, True, f"{tag}_X_{i:04d}_{safe}_eq_symbreak"))
                out.append(certify(n, E, True, False, f"{tag}_X_{i:04d}_{safe}_eq_nosymbreak"))
            out[-1]["graph6"] = g6
            if (i + 1) % 50 == 0:
                print(f"  certified {i+1}/{len(gs)}", flush=True)
    for o in out:
        print(o, flush=True)
    with open(os.path.join(HERE, f"cert_{mode}{'_' + sys.argv[2] if len(sys.argv) > 2 else ''}.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("ALL PROOFS VERIFIED:", len(out), flush=True)
