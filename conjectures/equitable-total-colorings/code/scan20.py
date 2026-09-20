"""scan20.py -- partial scan of order 20 using geng's res/mod splitting.
usage: python3 scan20.py <mod> <max_wall_seconds>
Runs residue classes 0,1,2,... of `mod` sequentially until the wall-time cap; writes
results_n20_r<res>m<mod>.tsv and summary_n20_r<res>m<mod>.json for each completed class.
The union of completed classes is an exact result for those classes (geng partitions the
generation tree; classes are NOT uniform random samples of the 510,489 graphs).
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scan

mod = int(sys.argv[1]); cap = float(sys.argv[2])
t0 = time.time()
done = []
for res in range(mod):
    if time.time() - t0 > cap:
        break
    tag = f"n20_r{res}m{mod}"
    s = scan.scan_order(20, extra_geng_args=(f"{res}/{mod}",), tag=tag)
    with open(os.path.join(scan.HERE, f"summary_{tag}.json"), "w") as f:
        json.dump(s, f, indent=1)
    done.append(s)
tot = sum(s["counts"]["total"] for s in done)
E = sum(s["counts"]["E"] for s in done); X = sum(s["counts"]["X"] for s in done); T2 = sum(s["counts"]["T2"] for s in done)
print(f"n=20 partial: {len(done)} of {mod} residue classes, graphs={tot} E={E} X={X} T2={T2}, wall={time.time()-t0:.0f}s")
for s in done:
    for g, sz in s["counterexamples"]:
        print("  n20 counterexample:", g, sz)
print("DONE20")
