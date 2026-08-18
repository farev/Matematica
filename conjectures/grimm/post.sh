#!/bin/bash
cd "$(dirname "$0")"
# wait for production to finish
while ! grep -q "ALL CHUNKS DONE" data/production.log; do sleep 20; done
{
echo "=== seam checks ==="
python3 - <<'PY'
import re
vals = {}
for c in ("c1","c2","c3","c4"):
    txt = open(f"data/{c}.summary.txt").read()
    fp = int(re.search(r"first_prime=(\d+)", txt).group(1))
    lr = int(re.search(r"last_right_prime=(\d+)", txt).group(1))
    np_ = int(re.search(r"primes_in_range=(\d+)", txt).group(1))
    vals[c] = (fp, lr, np_)
    print(c, vals[c])
ok = True
for a, b in (("c1","c2"),("c2","c3"),("c3","c4")):
    if vals[a][1] != vals[b][0]:
        print(f"SEAM BREAK {a}->{b}: {vals[a][1]} != {vals[b][0]}"); ok = False
tot = {"c1c2": vals["c1"][2]+vals["c2"][2],
       "c3": vals["c3"][2], "c4": vals["c4"][2],
       "all": sum(v[2] for v in vals.values())}
print("pi(1e10) check:", tot["c1c2"], "expected 455052511", tot["c1c2"]==455052511)
print("pi(1e11)-pi(1e10) check:", tot["c3"], "expected 3663002302", tot["c3"]==3663002302)
print("pi(1e12)-pi(1e11) check:", tot["c4"], "expected 33489857205", tot["c4"]==33489857205)
print("pi(1e12) check:", tot["all"], "expected 37607912018", tot["all"]==37607912018)
print("SEAMS OK" if ok else "SEAMS BROKEN")
PY
echo "=== verify c3 (sampled) ==="
python3 verify_census.py --check data/c3.census.csv --sample 250
echo "=== verify c4 (sampled) ==="
python3 verify_census.py --check data/c4.census.csv --sample 250
echo "=== mine stats ==="
python3 mine_stats.py c1 c2 c3 c4
echo "=== analyze tight ==="
python3 analyze_tight.py
echo "=== POSTPROCESSING COMPLETE ==="
} > data/post.log 2>&1
