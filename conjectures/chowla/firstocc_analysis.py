"""Compare a lambda first-occurrence spectrum against a PRNG control ensemble.

Reads the CSV output of `firstocc_stats` (one file per stream) and reports:

  1. the overall Conway-normalised mean R for lambda, and where it falls in the
     control ensemble (in control-sigma and by rank);
  2. the control ensemble's own mean against the exact model value E[R] = 1,
     which is the check that the statistic is unbiased;
  3. the popcount-resolved means, with the control band per popcount class;
  4. a weighted-regression slope of mean_R on (popcount - k/2).  Under a
     density bias P(lambda = -1) = 1/2 + delta this slope is predicted to be
     about -4*delta (to first order), so it is the natural place for the known
     negative bias of lambda to show up.  Comparing lambda's slope against the
     control slopes is a calibrated test with no fitted nuisance parameters.

All error bars come from the control ensemble, never from an independence
assumption: the 2^k first-occurrence times are drawn from a single stream and
are not independent, so a naive sigma/sqrt(2^k) would be wrong.

Usage:
    python3 firstocc_analysis.py LAMBDA_STATS.csv CONTROL_STATS.csv ...
"""

import sys
import statistics as st


def load(path):
    scalars, pc, ov = {}, [], []
    sec = None
    label = None
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        if line.startswith("popcount,"):
            sec = "pc"; continue
        if line.startswith("nontrivial_overlaps,"):
            sec = "ov"; continue
        if line.startswith("stat,"):
            sec = "sc"; continue
        if line.startswith("#"):
            continue
        f = line.split(",")
        if sec == "sc" and len(f) == 4:
            scalars[f[0]] = float(f[3]); label = f[1]
        elif sec == "pc" and len(f) == 4:
            pc.append((int(f[0]), int(f[1]), float(f[2])))
        elif sec == "ov" and len(f) == 3:
            ov.append((int(f[0]), int(f[1]), float(f[2])))
    return label, scalars, pc, ov


def slope(pc, k):
    """Size-weighted least-squares slope of mean_R on (popcount - k/2)."""
    sw = sum(c for _, c, _ in pc)
    xb = sum(c * (p - k / 2) for p, c, _ in pc) / sw
    yb = sum(c * m for _, c, m in pc) / sw
    num = sum(c * (p - k / 2 - xb) * (m - yb) for p, c, m in pc)
    den = sum(c * (p - k / 2 - xb) ** 2 for p, c, _ in pc)
    return num / den if den else float("nan")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    lab_l, sc_l, pc_l, ov_l = load(sys.argv[1])
    ctrls = [load(p) for p in sys.argv[2:]]
    # popcount classes run 0..k and every one of them is populated once all
    # patterns have occurred, so k is recoverable from the table's length
    k = len(pc_l) - 1

    print(f"# first-occurrence spectrum, k = {k}")
    print(f"# lambda stream: {sys.argv[1]}")
    print(f"# {len(ctrls)} i.i.d. fair-coin control streams\n")

    cv = [c[1]["mean_R"] for c in ctrls]
    m, s = st.mean(cv), st.stdev(cv)
    lv = sc_l["mean_R"]
    rank = sorted(cv + [lv]).index(lv) + 1
    print("## overall")
    print(f"lambda   mean_R = {lv:.6f}")
    print(f"controls mean_R = {m:.6f} +- {s:.6f} (sd of {len(cv)} streams), "
          f"range [{min(cv):.6f}, {max(cv):.6f}]")
    print(f"lambda - controls = {lv-m:+.6f} = {(lv-m)/s:+.2f} control-sigma; "
          f"rank {rank}/{len(cv)+1}")
    print(f"controls vs exact model E[R]=1: {m-1:+.6f} +- "
          f"{s/len(cv)**0.5:.6f}  ({(m-1)/(s/len(cv)**0.5):+.1f} SE)")
    print(f"lambda N_k = {int(sc_l['N_k'])} (code {int(sc_l['N_k_code'])}); "
          f"control N_k range [{int(min(c[1]['N_k'] for c in ctrls))}, "
          f"{int(max(c[1]['N_k'] for c in ctrls))}]\n")

    print("## popcount-resolved mean R  (control band = mean +- sd over streams)")
    print("popcount  count      lambda     control_mean  control_sd   z")
    cpc = {}
    for _, _, pc, _ in ctrls:
        for p, c, mr in pc:
            cpc.setdefault(p, []).append(mr)
    for p, c, mr in pc_l:
        vals = cpc.get(p, [])
        if len(vals) < 2:
            continue
        cm, cs = st.mean(vals), st.stdev(vals)
        z = (mr - cm) / cs if cs else float("nan")
        print(f"{p:>6}  {c:>9}  {mr:>10.5f}  {cm:>12.5f}  {cs:>10.5f}  {z:>+6.2f}")

    sl = slope(pc_l, k)
    csl = [slope(c[2], k) for c in ctrls]
    cm, cs = st.mean(csl), st.stdev(csl)
    print("\n## popcount slope of mean_R  (model: 0 for a fair coin)")
    print(f"lambda   slope = {sl:+.3e} per unit popcount")
    print(f"controls slope = {cm:+.3e} +- {cs:.3e}")
    print(f"lambda - controls = {(sl-cm)/cs:+.2f} control-sigma")
    print(f"resolution (1 control-sigma) = {cs:.2e} per unit popcount")

    print("\n## overlap-class mean R  (Conway normalisation should flatten this)")
    cov = {}
    for _, _, _, ov in ctrls:
        for o, c, mr in ov:
            cov.setdefault(o, []).append(mr)
    print("nontriv_overlaps  count     lambda     control_mean  control_sd")
    for o, c, mr in ov_l:
        vals = cov.get(o, [])
        if len(vals) < 2:
            continue
        print(f"{o:>16}  {c:>8}  {mr:>10.5f}  {st.mean(vals):>12.5f}  "
              f"{st.stdev(vals):>10.5f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
