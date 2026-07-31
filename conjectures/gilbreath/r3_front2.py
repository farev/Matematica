"""X5b — stress-test of front pinning at LARGE entry scales.

r3_front.py established (mu ~ 8.2): a period-32 de Bruijn {0,2}-ocean on
columns [W, N) cannot invade an i.i.d.-parity strip on [0, W); the leftmost
value->=2 cell stays within ~2 columns of W, and no bad leads occur beyond
the shallow transient.  This script asks whether that pinning survives when
the entry scale mu = theta/(1-theta) is pushed to 64, 512, 4096.

Setup per (mu, W), theta = mu/(1+mu), N = 16*W:
  main run   : top parities i.i.d. on [0, W), de Bruijn period 32 on [W, N);
               values conditioned geometric at theta throughout.
  control run: i.i.d. parities EVERYWHERE (no ocean), same seeds; T0 =
               max over seeds of the last depth with lead >= 2.

CAVEAT discovered while calibrating (pilot runs, this file's design note):
the control's last bad-lead depth scales roughly like mu with a heavy tail,
because an i.i.d. column m ~ depth s can hold a plant of geometric size
~ mu log N that survives erosion all the way to the lead.  Those deep
columns are OCEAN in the main run, so the control T0 wildly overestimates
the strip-attributable transient at large mu, and the prescribed range
[3*T0, N-W] can be empty.  When that happens the log says so and the same
statistics are reported on the fallback deep-half range [N/2, N-W), plus
attribution diagnostics (see below).

Tracked per depth s in the main run:
  lead(s)  = cell (s, 0)
  ell(s)   = leftmost column with value >= 2          (global front)
  h(s)     = leftmost column >= W-2 with value >= 2   (ocean-side front;
             h - W grows  <=>  the sea eats into the ocean)
  r(s)     = leftmost column >= W-2 s.t. ALL of [r, r+16] valued <= 1
             (prescribed erosion proxy; note it also fires on cool
             "interior lakes" deep inside the ocean, so h(s) is the
             sharper interface measure)
Interface scale: max value over columns [W-32, W+32] at s = N/4, N/2, 3N/4.

Attribution: a bad lead caused by an ocean plant must transit the strip,
so ell(s) shows a leftward-moving dip from ~W to 0 during the ~W depths
before the bad lead; a strip-residue bad lead does not connect to W.  For
the first bad lead beyond N/2 (if any) the log prints the preceding ell
trajectory.

Run from inside conjectures/gilbreath:
    python3 r3_front2.py            # full run (~ a few minutes)
    python3 r3_front2.py --quick    # smoke test only
"""

import sys
import time

import numpy as np

from r3_common import de_bruijn, conditioned_geometric

DB_ORDER = 5          # ocean parity period 2^5 = 32
EROSION_RUN = 17      # r(s): require columns [r, r+16] all <= 1 (17 cells)
NO_HOT = -1           # sentinel for h(s)/r(s): no qualifying column


def build_top(W, N, theta, seed, two_zone):
    """Top row values. two_zone: i.i.d. strip [0,W) + de Bruijn ocean [W,N).
    Otherwise i.i.d. parities everywhere (control)."""
    rng = np.random.default_rng(seed)
    y = np.empty(N, dtype=np.uint8)
    if two_zone:
        y[:W] = rng.integers(0, 2, W)
        y[W:] = de_bruijn(DB_ORDER)[np.arange(W, N) % (2 ** DB_ORDER)]
    else:
        y[:] = rng.integers(0, 2, N)
    return conditioned_geometric(y, rng, theta)


def evolve_control(a):
    """Lead trace only; returns last depth with lead >= 2 (0 if never)."""
    x = np.asarray(a, dtype=np.int64)
    last_bad = 0
    for s in range(1, len(a)):
        x = np.abs(x[1:] - x[:-1])
        if x[0] >= 2:
            last_bad = s
    return last_bad


def evolve_main(a, W):
    """Full tracking.  Arrays indexed by depth s (index 0 unused):
    lead, ell (sentinel = row length if no cell >= 2), h, r (sentinel
    NO_HOT), and iface = {checkpoint depth: max value in cols [W-32,W+32]}.
    """
    N = len(a)
    x = np.asarray(a, dtype=np.int64)
    lead = np.zeros(N, dtype=np.int64)
    ell = np.full(N, N + 1, dtype=np.int64)
    hh = np.full(N, NO_HOT, dtype=np.int64)
    rr = np.full(N, NO_HOT, dtype=np.int64)
    K = EROSION_RUN
    lo = W - 2
    cps = (N // 4, N // 2, 3 * N // 4)
    iface = {}
    for s in range(1, N):
        x = np.abs(x[1:] - x[:-1])
        L = len(x)
        lead[s] = x[0]
        hot = x >= 2
        j = int(hot.argmax())
        ell[s] = j if hot[j] else L  # "no hot cell" sentinel (past end)
        if L > lo:
            oc = hot[lo:]
            j2 = int(oc.argmax())
            hh[s] = lo + j2 if oc[j2] else NO_HOT
        if L >= lo + K:
            b = (x[lo:] <= 1).astype(np.int64)
            cs = np.concatenate(([0], np.cumsum(b)))
            ok = (cs[K:] - cs[:-K]) == K
            jj = int(ok.argmax())
            rr[s] = lo + jj if ok[jj] else NO_HOT
        if s in cps:
            iface[s] = int(x[max(0, W - 32):min(L, W + 33)].max())
    return lead, ell, hh, rr, iface


def front_stats(ell, lo, hi, W):
    seg = ell[lo:hi]
    return dict(
        mn=int(seg.min()) - W,
        md=int(np.median(seg)) - W,
        c8=int(np.sum(seg < W - 8)),
        c2=int(np.sum(seg < W // 2)),
    )


def fmt(vals):
    return "[" + ", ".join(str(v) for v in vals) + "]"


def config_report(mu, W, seeds):
    theta = mu / (1.0 + mu)
    N = 16 * W
    t_start = time.time()
    seeds = list(seeds)

    # -- control: i.i.d. everywhere, prescribed T0 --------------------------
    t0_per_seed = []
    for sd in seeds:
        a = build_top(W, N, theta, sd, two_zone=False)
        t0_per_seed.append(evolve_control(a))
    T0 = max(max(t0_per_seed), 1)

    print(f"== mu = {mu}  (theta = {theta:.6f})  W = {W}  N = {N}  "
          f"seeds = {seeds} ==")
    print(f"  control (iid everywhere) last bad-lead depth per seed: "
          f"{fmt(t0_per_seed)}  ->  T0 = {T0} "
          f"(median {int(np.median(t0_per_seed))})")
    if 6 * T0 > N:
        print(f"  WARNING: 6*T0 = {6 * T0} exceeds N = {N}: the prescribed "
              f"steady range is not comfortably inside the array.")
    r1_lo, hi = 3 * T0, N - W
    r1_ok = r1_lo < hi
    r2_lo = N // 2
    if not r1_ok:
        print(f"  NOTE: prescribed range [3*T0, N-W) = [{r1_lo}, {hi}) is "
              f"EMPTY (control T0 is dominated by deep iid plants at "
              f"columns > W that are ocean in the main run); falling back "
              f"to the deep-half range [{r2_lo}, {hi}).")

    # -- main two-zone runs -------------------------------------------------
    per = dict(last8=[], last2=[], r1=[], r2=[], firstR1=[], firstR2=[],
               lastbad=[], nbad_r2=[], dens=[], hmax=[], hmed=[],
               lakes=[], lakemin=[])
    iface_all, r_cp_all = {}, {}
    trace_lines = []
    for sd in seeds:
        a = build_top(W, N, theta, sd, two_zone=True)
        lead, ell, hh, rr, iface = evolve_main(a, W)

        # front horizon: last depth (< N-W) where the strip interior is hot
        in8 = np.nonzero(ell[1:hi] < W - 8)[0]
        in2 = np.nonzero(ell[1:hi] < W // 2)[0]
        per["last8"].append(int(in8[-1]) + 1 if len(in8) else 0)
        per["last2"].append(int(in2[-1]) + 1 if len(in2) else 0)
        if r1_ok:
            per["r1"].append(front_stats(ell, r1_lo, hi, W))
        per["r2"].append(front_stats(ell, r2_lo, hi, W))

        # leads
        bad = np.nonzero(lead >= 2)[0]
        per["lastbad"].append(int(bad.max()) if len(bad) else 0)
        if r1_ok:
            b1 = bad[bad >= r1_lo]
            per["firstR1"].append(int(b1.min()) if len(b1) else -1)
        b2 = bad[bad >= r2_lo]
        per["firstR2"].append(int(b2.min()) if len(b2) else -1)
        per["nbad_r2"].append(int(np.sum((bad >= r2_lo) & (bad < hi))))
        per["dens"].append(float(np.mean(lead[r2_lo:hi] >= 2)))
        if len(b2):
            s0 = int(b2.min())
            offs = [2 * W, W, W // 2, W // 4, 32, 8, 1]
            tr = ", ".join(f"s-{o}: {int(ell[s0 - o]) - W:+d}"
                           for o in offs if s0 - o >= 1)
            trace_lines.append(
                f"    seed {sd}: first bad lead beyond N/2 at s = {s0} "
                f"(lead {int(lead[s0])}); ell-W before it: {tr}")

        # ocean-side front h(s) on the deep-half range
        hseg = hh[r2_lo:hi]
        hv = hseg[hseg >= 0]
        per["hmax"].append(int(hv.max()) - W if len(hv) else None)
        per["hmed"].append(int(np.median(hv)) - W if len(hv) else None)

        # prescribed r(s): checkpoints + lake census on the deep half
        for cp, v in iface.items():
            iface_all.setdefault(cp, []).append(v)
            r_cp_all.setdefault(cp, []).append(int(rr[cp]))
        rseg = rr[r2_lo:hi]
        rv = rseg[rseg >= 0]
        per["lakes"].append(int(len(rv)))
        per["lakemin"].append(int(rv.min()) - W if len(rv) else None)

    # -- report -------------------------------------------------------------
    print("  FRONT (ell = leftmost column with value >= 2):")
    print(f"    last depth with ell < W-8  (range [1, {hi})): "
          f"{fmt(per['last8'])}")
    print(f"    last depth with ell < W/2  (range [1, {hi})): "
          f"{fmt(per['last2'])}")
    for tag, key, lo in (("[3*T0, N-W)", "r1", r1_lo),
                         ("[N/2,  N-W)", "r2", r2_lo)):
        if key == "r1" and not r1_ok:
            continue
        st = per[key]
        print(f"    range {tag} = [{lo}, {hi}):")
        print(f"      (a) min ell-W per seed: {fmt([d['mn'] for d in st])}"
              f"   (overall {min(d['mn'] for d in st)});  "
              f"median ell-W per seed: {fmt([d['md'] for d in st])}")
        print(f"      (b) # depths ell < W-8: {fmt([d['c8'] for d in st])} "
              f"(total {sum(d['c8'] for d in st)});  "
              f"# depths ell < W/2: {fmt([d['c2'] for d in st])} "
              f"(total {sum(d['c2'] for d in st)})")
    print("  LEADS:")
    if r1_ok:
        print(f"    (c) first bad lead at depth >= 3*T0 = {r1_lo} per seed "
              f"(-1 = none): {fmt(per['firstR1'])}")
    print(f"        first bad lead at depth >= N/2 = {r2_lo} per seed "
          f"(-1 = none): {fmt(per['firstR2'])}")
    print(f"        last bad lead overall per seed: {fmt(per['lastbad'])}")
    print(f"    (d) bad-lead density on [{r2_lo}, {hi}): "
          f"{np.mean(per['dens']):.5f} +- {np.std(per['dens']):.5f}  "
          f"(counts per seed {fmt(per['nbad_r2'])})")
    for ln in trace_lines:
        print(ln)
    print("  INTERFACE / OCEAN SIDE:")
    for cp in sorted(iface_all):
        vals = iface_all[cp]
        rvals = r_cp_all[cp]
        rtxt = ("none" if all(r < 0 for r in rvals) else fmt(
            [("-" if r < 0 else r - W) for r in rvals]))
        print(f"    depth {cp}: interface max value in cols "
              f"[{max(0, W - 32)}, {W + 32}]: median "
              f"{int(np.median(vals))}, max {max(vals)};  r(s)-W: {rtxt}")
    print(f"    ocean-side front h-W on [{r2_lo}, {hi}): median per seed "
          f"{fmt(per['hmed'])}, max per seed {fmt(per['hmax'])}")
    print(f"    cool 17-runs ('lakes') beyond W-2 on [{r2_lo}, {hi}): "
          f"# depths per seed {fmt(per['lakes'])}; nearest lake "
          f"min r-W per seed: {fmt(per['lakemin'])}")
    print(f"  [elapsed {time.time() - t_start:.1f} s]")
    print()


def appendix_transit(mu, W, seed, lo, hi, step):
    """Trace one deep hot episode: print (depth, ell-W, value at ell, lead)
    every `step` rows in [lo, hi].  A ballistic plant transit shows ell
    marching left ~1 column/row carrying a mu-scale value; a {0,2}-front
    invasion would show interface-adjacent value-2 cells instead."""
    theta = mu / (1.0 + mu)
    N = 16 * W
    a = build_top(W, N, theta, seed, two_zone=True)
    x = np.asarray(a, dtype=np.int64)
    print(f"  -- transit trace: mu = {mu}, W = {W}, seed = {seed}, "
          f"depths [{lo}, {hi}] step {step} --")
    print("     depth   ell-W   value@ell   lead")
    for s in range(1, hi + 1):
        x = np.abs(x[1:] - x[:-1])
        if s < lo or (s - lo) % step:
            continue
        hot = x >= 2
        j = int(hot.argmax())
        if hot[j]:
            print(f"     {s:>5}  {j - W:>6}  {int(x[j]):>10}  {int(x[0]):>5}")
        else:
            print(f"     {s:>5}    none           -  {int(x[0]):>5}")
    print()


def main():
    quick = "--quick" in sys.argv
    total_start = time.time()
    print("r3_front2.py — front pinning at large entry scale mu")
    print(f"numpy {np.__version__}; ocean parity period {2 ** DB_ORDER}; "
          f"erosion run length {EROSION_RUN}")
    print()
    if quick:
        config_report(mu=64, W=128, seeds=range(500, 502))
    else:
        for mu in (64, 512, 4096):
            config_report(mu, W=256, seeds=range(500, 506))
        for mu in (64, 512, 4096):
            config_report(mu, W=1024, seeds=range(500, 504))
        print("APPENDIX: anatomy of the deep hot episodes at mu = 4096")
        print("  (are they {0,2}-front invasion or ballistic plant "
              "transit?)")
        appendix_transit(4096, 256, seed=504, lo=3560, hi=3880, step=16)
        appendix_transit(4096, 256, seed=505, lo=1600, hi=2160, step=32)
        appendix_transit(4096, 1024, seed=501, lo=8000, hi=9664, step=64)
    print(f"total elapsed: {time.time() - total_start:.1f} s")


if __name__ == "__main__":
    main()
