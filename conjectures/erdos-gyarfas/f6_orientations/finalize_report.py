"""Insert the solver-run table into REPORT.md (replaces SAT_RESULTS_PLACEHOLDER)."""
import json, glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
order = ["sat_p29g8_cadical", "sat_p29g8_strong_cadical", "sat_p31g22_strong_cadical", "sat_p31g7_strong_cadical",
         "sat_p31g7_strong_kissat", "sat_p29g3_strong_cadical", "sat_p29g3_kissat", "sat_p31g11_strong_cadical"]
label = {"sat_p29g8_cadical": "p29 (8,1) original", "sat_p29g8_strong_cadical": "p29 (8,1) strengthened (n_t=0, a(C)=9)",
         "sat_p31g22_strong_cadical": "p31 (22,1) strengthened (n_t=0, a(C)=9)", "sat_p31g7_strong_cadical": "p31 (7,1) strengthened (186<=n_t<=232)",
         "sat_p31g7_strong_kissat": "p31 (7,1) strengthened", "sat_p29g3_strong_cadical": "p29 (3,1) strengthened (n_t<=101)",
         "sat_p29g3_kissat": "p29 (3,1) original", "sat_p31g11_strong_cadical": "p31 (11,1) strengthened (n_t<=116)"}
lines = ["| instance | solver | wall limit | outcome | solve time | conflicts / decisions / propagations |", "|---|---|---|---|---|---|"]
for k in order:
    fn = os.path.join(HERE, k + ".json")
    if not os.path.exists(fn):
        log = os.path.join(HERE, k + ".log")
        note = "killed at the hard cap (no statistics: pysat's Kissat exposes none, and a killed process writes nothing)" if "kissat" in k else "no result file (killed at the hard cap)"
        lines.append(f"| {label[k]} | {'kissat404' if 'kissat' in k else 'cadical195'} | - | TIMEOUT | - | {note} |")
        continue
    d = json.load(open(fn))
    st = d["stats"]
    stats = f"{st['conflicts']:,} / {st['decisions']:,} / {st['propagations']:,}" if isinstance(st, dict) else "not exposed"
    lines.append(f"| {label[k]} | {d['solver']} | {int(d['limit_seconds'])} s | **{d['status']}** | {d['solve_seconds']} s | {stats} |")
table = "\n".join(lines)
extra = open(os.path.join(HERE, "sat_results_text.md")).read() if os.path.exists(os.path.join(HERE, "sat_results_text.md")) else ""
rep = open(os.path.join(HERE, "REPORT.md")).read()
assert "SAT_RESULTS_PLACEHOLDER" in rep
rep = rep.replace("SAT_RESULTS_PLACEHOLDER", table + "\n\n" + extra)
open(os.path.join(HERE, "REPORT.md"), "w").write(rep)
print(table)
