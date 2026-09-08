"""scan.py -- for every connected cubic graph of the given orders (from geng):
   1. solve 'equitable 4-total coloring exists' (symmetry-broken CNF);
      SAT -> decode + verify the witness independently (verify_tc)  -> class E
   2. else solve 'plain 4-total coloring exists';
      SAT -> verify witness; graph is Type 1 with chi''_e >= 5 -> class X (COUNTEREXAMPLE)
      UNSAT -> Type 2                                             -> class T2
Per-graph records go to results_n<n>.tsv ; summary to summary.json ; one core only.
"""
import sys, os, time, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tc
from verify_tc import decode_model, check_total_coloring, is_cubic_simple, is_connected

HERE = os.path.dirname(os.path.abspath(__file__))
GENG = os.path.join(HERE, "dl/pynauty-2.8.8.1/src/nauty2_8_8/geng")


def scan_order(n, out_dir=HERE, extra_geng_args=(), tag=None):
    tag = tag or f"n{n}"
    t0 = time.time()
    p = subprocess.Popen([GENG, "-c", "-d3", "-D3", "-q", str(n), *extra_geng_args],
                         stdout=subprocess.PIPE, text=True, bufsize=1 << 16)
    cnt = dict(total=0, E=0, X=0, T2=0)
    counterexamples, type2 = [], []
    sizes_hist = {}
    tsv = open(os.path.join(out_dir, f"results_{tag}.tsv"), "w")
    tsv.write("graph6\tclass\tclass_sizes\n")
    t_eq = t_pl = 0.0
    for line in p.stdout:
        g6 = line.strip()
        if not g6:
            continue
        nn, edges = tc.parse_graph6(g6)
        assert nn == n and is_cubic_simple(nn, edges) and is_connected(nn, edges), g6
        cnt["total"] += 1
        ta = time.time()
        cl, nv = tc.encode(nn, edges, equitable=True, symbreak=True)
        sat, model = tc.solve(cl)
        t_eq += time.time() - ta
        if sat:
            vc, ec = decode_model(nn, edges, model)
            ok, msg, sizes = check_total_coloring(nn, edges, vc, ec, equitable=True)
            if not ok:
                raise RuntimeError(f"witness rejected for {g6}: {msg}")
            cnt["E"] += 1
            key = tuple(sorted(sizes, reverse=True))
            sizes_hist[key] = sizes_hist.get(key, 0) + 1
            tsv.write(f"{g6}\tE\t{list(key)}\n")
        else:
            ta = time.time()
            cl2, nv2 = tc.encode(nn, edges, equitable=False, symbreak=True)
            sat2, model2 = tc.solve(cl2)
            t_pl += time.time() - ta
            if sat2:
                vc, ec = decode_model(nn, edges, model2)
                ok, msg, sizes = check_total_coloring(nn, edges, vc, ec, equitable=False)
                if not ok:
                    raise RuntimeError(f"plain witness rejected for {g6}: {msg}")
                cnt["X"] += 1
                counterexamples.append((g6, sorted(sizes, reverse=True)))
                tsv.write(f"{g6}\tX\t{sorted(sizes, reverse=True)}\n")
                print(f"!!! COUNTEREXAMPLE n={n}: {g6} plain sizes {sorted(sizes, reverse=True)}", flush=True)
            else:
                cnt["T2"] += 1
                type2.append(g6)
                tsv.write(f"{g6}\tT2\t-\n")
        if cnt["total"] % 5000 == 0:
            print(f"  n={n}: {cnt} {time.time()-t0:.1f}s", flush=True)
    p.wait()
    tsv.close()
    wall = time.time() - t0
    summ = dict(n=n, tag=tag, counts=cnt, wall_s=round(wall, 2), t_equitable_solve_s=round(t_eq, 2),
                t_plain_solve_s=round(t_pl, 2), counterexamples=counterexamples, type2=type2,
                equitable_class_size_configs={str(k): v for k, v in sorted(sizes_hist.items())})
    print(f"n={n}: total={cnt['total']} E(equitable)={cnt['E']} X(counterex)={cnt['X']} T2={cnt['T2']} "
          f"wall={wall:.1f}s (solve eq {t_eq:.1f}s, plain {t_pl:.1f}s)", flush=True)
    return summ


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or [4, 6, 8, 10, 12, 14, 16, 18]
    allsum = []
    for n in ns:
        s = scan_order(n)
        allsum.append(s)
        with open(os.path.join(HERE, f"summary_n{n}.json"), "w") as f:
            json.dump(s, f, indent=1)
    print("DONE", flush=True)
