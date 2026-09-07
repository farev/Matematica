"""Run one SAT solver on a DIMACS file with a wall-clock limit (cooperative
interrupt via a timer thread; the caller additionally wraps this in
`timeout -s KILL` as a hard cap). Usage: python3 solve.py file.cnf solver seconds outprefix"""
import sys, time, threading, json
from pysat.formula import CNF
from pysat.solvers import Solver

fn, name, seconds, outprefix = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
t0 = time.time()
cnf = CNF(from_file=fn)
s = Solver(name=name, bootstrap_with=cnf.clauses)
tload = time.time() - t0
t1 = time.time()
r = None
if name.startswith("kissat"):
    # pysat's Kissat is non-incremental: a single solve() call; the wall cap is
    # enforced externally by `timeout -s KILL` (no statistics on timeout).
    r = s.solve()
else:
    chunk = 5000
    while time.time() - t1 < seconds:
        s.conf_budget(chunk)
        r = s.solve_limited()
        if r is not None:
            break
        chunk = min(chunk * 2, 100000)
dt = time.time() - t1
status = {True: "SAT", False: "UNSAT", None: "TIMEOUT"}[r]
try:
    st = s.accum_stats()
except Exception as e:
    st = str(e)
res = {"file": fn, "solver": name, "status": status, "solve_seconds": round(dt, 1), "load_seconds": round(tload, 1),
       "limit_seconds": seconds, "stats": st, "nv": cnf.nv, "nclauses": len(cnf.clauses)}
if r:
    with open(outprefix + ".model", "w") as f:
        f.write(" ".join(map(str, s.get_model())) + "\n")
with open(outprefix + ".json", "w") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res))
