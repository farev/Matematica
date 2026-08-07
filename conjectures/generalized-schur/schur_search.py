#!/usr/bin/env python3
"""Find S(k; t_1..t_k) exactly: explore with Cadical (no proof), certify the
boundary with Glucose42 + DRUP (checked by rup_check) and an independently
verified witness at S-1.

Usage: schur_search.py 3,4,4 --lb 28 [--ub-guess 40] [--step-timeout 900]
Exploration: SAT at n proves S > n (witness kept); first UNSAT at n proves
S <= n. Values are exact only after the certified boundary pair passes.
Prints one line per step:  ts n verdict seconds
"""
import argparse, os, subprocess, sys, time
from schur3 import decide, encode, write_witness, rup_check


def probe(ts, n, timeout_s, workdir):
    """Cadical, no proof. Returns ('SAT', coloring)/('UNSAT', None)/('TIMEOUT', None)."""
    import multiprocessing as mp

    def run(q):
        r = decide(ts, n, workdir, "probe", proof=False, solver="cadical")
        q.put(r)

    q = mp.Queue()
    p = mp.Process(target=run, args=(q,))
    t0 = time.time()
    p.start()
    p.join(timeout_s)
    if p.is_alive():
        p.terminate()
        p.join()
        return "TIMEOUT", None, time.time() - t0
    res, aux = q.get()
    return res, aux, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ts")
    ap.add_argument("--lb", type=int, required=True,
                    help="known/proved lower bound: S > lb-1, i.e. a good coloring of [1,lb-1] is believed to exist; climb starts at lb-1 to confirm")
    ap.add_argument("--step-timeout", type=int, default=900)
    ap.add_argument("--workdir", default="search")
    ap.add_argument("--certify", action="store_true",
                    help="after locating S, rerun boundary pair with Glucose+DRUP and verify both certificates")
    a = ap.parse_args()
    ts = tuple(int(x) for x in a.ts.split(","))
    tag = "s" + "_".join(map(str, ts))
    os.makedirs(a.workdir, exist_ok=True)

    n = a.lb - 1
    last_sat = None
    val = None
    while True:
        res, aux, el = probe(ts, n, a.step_timeout, a.workdir)
        print(f"{ts} n={n} {res} {el:.1f}s", flush=True)
        if res == "SAT":
            last_sat = (n, aux)
            n += 1
        elif res == "UNSAT":
            val = n
            break
        else:
            print(f"{ts} STOPPED: timeout at n={n} (S > {last_sat[0] if last_sat else '?'} established)", flush=True)
            return 3
    if last_sat is None or last_sat[0] != val - 1:
        # climb started above a SAT point or jumped; re-probe val-1 to anchor
        res, aux, el = probe(ts, val - 1, a.step_timeout, a.workdir)
        print(f"{ts} n={val-1} {res} {el:.1f}s (anchor)", flush=True)
        if res != "SAT":
            print(f"{ts} INCONSISTENT: UNSAT at {val} but not SAT at {val-1}; lb wrong?", flush=True)
            return 4
        last_sat = (val - 1, aux)
    print(f"{ts} S = {val} (uncertified: Cadical verdicts)", flush=True)

    if a.certify:
        t0 = time.time()
        res, aux = decide(ts, val, a.workdir, tag, proof=True, solver="glucose")
        assert res == "UNSAT", f"certify: Glucose disagrees at {val}"
        ok, msg = rup_check(*aux)
        print(f"{ts} UNSAT n={val} glucose+drup {time.time()-t0:.1f}s rup={'VERIFIED' if ok else 'FAIL'}", flush=True)
        if not ok:
            return 5
        wf = os.path.join(a.workdir, f"{tag}_n{val-1}.witness")
        write_witness(wf, ts, val - 1, last_sat[1])
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_witness.py"), wf],
                           capture_output=True, text=True)
        print(r.stdout.strip(), flush=True)
        if r.returncode != 0:
            return 6
        print(f"{ts} S = {val} CERTIFIED (drup VERIFIED at {val}, witness OK at {val-1})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
