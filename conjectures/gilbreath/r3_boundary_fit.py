"""X8 — boundary fit: P*(mu) refinement, direct cooling-time test, persistence.

NUMERICAL throughout (floating-point densities, Monte Carlo seeds).

Three experiments on the fully periodic de Bruijn parity construction
(period P repeated over the whole top row, entries conditioned geometric
at scale mu = theta/(1-theta)):

1. Boundary refinement.  Bad-lead density (lead >= 2 at depths [4P, 16P])
   over mu in {8,...,512} x P in {8,...,1024}, 4 base seeds, with 4 extra
   seeds on the two P values straddling the 0.05 crossing.  P*(mu) by
   linear interpolation in log2(P).  Least-squares fit of
   log P* = a + b log mu, plus residuals of the two candidate laws
   P* ~ mu^(2/3) and P* ~ mu/ln(mu).
   NOTE: span=16 here (depths [4P, 16P]); the earlier coarse table in
   r3_boundary.py used span=32 (depths [4P, 32P]).

2. Direct cooling-time measurement.  Same construction with a huge period
   (P = 8192, de Bruijn order 13) and top length N = 6000 < P, so the
   measured depths see only the pre-period band.  T_hot(mu) = first depth
   where the fraction of cells >= 2 in the current row drops below 1e-3.
   Race hypothesis: T_hot tracks P*.

3. Persistence check at (P, mu) = (8, 8) and (32, 8).  Lead trace to depth
   49150 (top length 49152), bad-lead density per consecutive window of
   4096 depths.  Claim under test: density is stationary in depth.

Run from inside conjectures/gilbreath:  python3 r3_boundary_fit.py
All output is duplicated to r3_boundary_fit.log.
"""

import time

import numpy as np

from r3_boundary import bad_density
from r3_common import conditioned_geometric, de_bruijn, lead_trace

LOG_PATH = "r3_boundary_fit.log"
_log = open(LOG_PATH, "w")


def say(msg=""):
    print(msg)
    _log.write(msg + "\n")
    _log.flush()


# ----------------------------------------------------------------------
# Task 1: boundary refinement and the P*(mu) fit
# ----------------------------------------------------------------------

MUS = [8, 16, 32, 64, 128, 256, 512]
PS = [8, 16, 32, 64, 128, 256, 512, 1024]
SPAN = 16
BASE_SEEDS = [700, 701, 702, 703]
EXTRA_SEEDS = [704, 705, 706, 707]
THRESH = 0.05


def find_pstar(means):
    """Crossing of the density curve (aligned with PS) through THRESH.

    Uses the LAST index still >= THRESH, then interpolates linearly in
    log2(P) to the next point.  Returns (pstar_float_or_None, tag).
    """
    above = [i for i, d in enumerate(means) if d >= THRESH]
    if not above:
        return None, "< %d (already dead at smallest P)" % PS[0]
    i = max(above)
    if i == len(PS) - 1:
        return None, "> %d (censored)" % PS[-1]
    d0, d1 = means[i], means[i + 1]
    l0, l1 = np.log2(PS[i]), np.log2(PS[i + 1])
    frac = (d0 - THRESH) / (d0 - d1)
    lstar = l0 + frac * (l1 - l0)
    return 2.0 ** lstar, "interp between P=%d (%.3f) and P=%d (%.3f)" % (
        PS[i], d0, PS[i + 1], d1)


def task1():
    say("=" * 72)
    say("TASK 1 — boundary refinement (bad-lead density, depths [4P, %dP])"
        % SPAN)
    say("span=%d here; the earlier coarse table (r3_boundary.py, "
        "r3_boundary2.log) used span=32, so absolute densities are not "
        "directly comparable to that table." % SPAN)
    say("base seeds %s, extra seeds %s on the two straddling P values"
        % (BASE_SEEDS, EXTRA_SEEDS))
    say("")

    t0 = time.time()
    dens = {}  # (mu, P) -> list of per-seed densities
    for mu in MUS:
        for P in PS:
            dens[(mu, P)] = [bad_density(P, mu, sd, span=SPAN)
                             for sd in BASE_SEEDS]

    # refinement pass: extra seeds on the straddling pair per mu
    refined = {}
    for mu in MUS:
        means = [float(np.mean(dens[(mu, P)])) for P in PS]
        above = [i for i, d in enumerate(means) if d >= THRESH]
        if above and max(above) < len(PS) - 1:
            i = max(above)
            for P in (PS[i], PS[i + 1]):
                dens[(mu, P)].extend(
                    bad_density(P, mu, sd, span=SPAN) for sd in EXTRA_SEEDS)
                refined[(mu, P)] = True

    say("density table, mean +- std over seeds "
        "(* = 8 seeds on that cell, else 4):")
    hdr = "         " + "".join("P=%-5d      " % P for P in PS)
    say(hdr)
    for mu in MUS:
        cells = []
        for P in PS:
            d = dens[(mu, P)]
            star = "*" if (mu, P) in refined else " "
            cells.append("%.3f+-%.3f%s" % (np.mean(d), np.std(d), star))
        say("mu=%-4d  " % mu + " ".join(cells))
    say("")

    # crossings
    pstars = {}
    say("P*(mu): density crossing of %.2f, linear interpolation in log2(P)"
        % THRESH)
    for mu in MUS:
        means = [float(np.mean(dens[(mu, P)])) for P in PS]
        pstar, tag = find_pstar(means)
        pstars[mu] = pstar
        if pstar is None:
            say("  mu=%-4d  P* %s" % (mu, tag))
        else:
            say("  mu=%-4d  P* = %8.1f   (%s)" % (mu, pstar, tag))
    say("")

    # least-squares fit over uncensored points
    unc = [(mu, p) for mu, p in pstars.items() if p is not None]
    say("uncensored points used in the fit: %s" % [m for m, _ in unc])
    x = np.log([m for m, _ in unc])
    y = np.log([p for _, p in unc])
    n = len(x)
    b, a = np.polyfit(x, y, 1)
    fit = a + b * x
    resid = y - fit
    sse = float(resid @ resid)
    sxx = float(((x - x.mean()) ** 2).sum())
    se_b = np.sqrt(sse / (n - 2) / sxx) if n > 2 else float("nan")
    say("least squares  log P* = a + b log mu :")
    say("  b = %.4f +- %.4f (standard error), a = %.4f "
        "(prefactor e^a = %.2f), RSS = %.5f, n = %d"
        % (b, se_b, a, np.exp(a), sse, n))
    say("")

    # competing one-parameter laws (slope fixed, intercept fitted)
    say("competing laws (intercept fitted by least squares, slope fixed):")
    for name, pred in [
            ("P* ~ mu^(2/3)", (2.0 / 3.0) * x),
            ("P* ~ mu/ln(mu)", x - np.log(x)),
    ]:
        c = float(np.mean(y - pred))
        r = y - (c + pred)
        say("  %-16s prefactor = %.2f, RSS = %.5f" % (name, np.exp(c), float(r @ r)))
        for (mu, _), ri in zip(unc, r):
            say("      mu=%-4d residual (log units) = %+.4f" % (mu, ri))
    say("")
    say("task 1 runtime: %.1f s" % (time.time() - t0))
    say("")
    return pstars


# ----------------------------------------------------------------------
# Task 2: direct cooling time in the pre-period band
# ----------------------------------------------------------------------

COOL_MUS = [8, 64, 512]
COOL_SEEDS = [800, 801, 802]
COOL_N = 6000
COOL_ORDER = 13          # P = 8192 > N: only the pre-period band is seen
COOL_MAX_DEPTH = 5000
COOL_THRESH = 1e-3


def hot_time(mu, seed):
    P = 2 ** COOL_ORDER
    y = de_bruijn(COOL_ORDER)[np.arange(COOL_N) % P]
    theta = mu / (1 + mu)
    rng = np.random.default_rng(seed)
    x = conditioned_geometric(y, rng, theta)
    checkpoints = {}
    marks = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}
    for s in range(1, COOL_MAX_DEPTH + 1):
        x = np.abs(x[1:] - x[:-1])
        f = np.count_nonzero(x >= 2) / len(x)
        if s in marks:
            checkpoints[s] = f
        if f < COOL_THRESH:
            return s, f, checkpoints
    return None, f, checkpoints


def task2(pstars):
    say("=" * 72)
    say("TASK 2 — direct cooling time, pre-period band only")
    say("P = 2^%d = %d (> N), N = %d, hot fraction = frac(cells >= 2) in the"
        % (COOL_ORDER, 2 ** COOL_ORDER, COOL_N))
    say("current row; T_hot = first depth with hot fraction < %g "
        "(censored at depth %d); seeds %s"
        % (COOL_THRESH, COOL_MAX_DEPTH, COOL_SEEDS))
    say("")
    t0 = time.time()
    thots = {}
    for mu in COOL_MUS:
        per_seed = []
        for sd in COOL_SEEDS:
            T, f, cp = hot_time(mu, sd)
            per_seed.append(T)
            prof = "  ".join("s=%d:%.4f" % (s, cp[s]) for s in sorted(cp))
            tlab = str(T) if T is not None else ("censored (f=%.2e at %d)"
                                                 % (f, COOL_MAX_DEPTH))
            say("  mu=%-4d seed=%d  T_hot = %s" % (mu, sd, tlab))
            say("           hot-fraction profile: %s" % prof)
        if all(T is not None for T in per_seed):
            thots[mu] = float(np.mean(per_seed))
            say("  mu=%-4d  mean T_hot = %.1f  (per-seed %s)"
                % (mu, thots[mu], per_seed))
        else:
            thots[mu] = None
            say("  mu=%-4d  T_hot censored in at least one seed" % mu)
        say("")

    say("T_hot vs P* comparison (race hypothesis: they track each other):")
    say("  mu     T_hot      P*        P*/T_hot")
    for mu in COOL_MUS:
        T = thots.get(mu)
        P = pstars.get(mu)
        tl = "%.1f" % T if T is not None else "censored"
        pl = "%.1f" % P if P is not None else "censored"
        rl = "%.3f" % (P / T) if (T and P) else "n/a"
        say("  %-6d %-10s %-9s %s" % (mu, tl, pl, rl))
    say("")
    say("task 2 runtime: %.1f s" % (time.time() - t0))
    say("")
    return thots


# ----------------------------------------------------------------------
# Task 3: persistence of the bad-lead density in depth
# ----------------------------------------------------------------------

PERSIST_CASES = [(8, 8), (32, 8)]
PERSIST_SEEDS = [900, 901]
PERSIST_N = 49152
PERSIST_WIN = 4096


def task3():
    say("=" * 72)
    say("TASK 3 — persistence: bad-lead density per window of %d depths"
        % PERSIST_WIN)
    say("top length N = %d, lead trace to depth %d, seeds %s"
        % (PERSIST_N, PERSIST_N - 2, PERSIST_SEEDS))
    say("")
    t0 = time.time()
    for P, mu in PERSIST_CASES:
        B = int(np.log2(P))
        theta = mu / (1 + mu)
        for sd in PERSIST_SEEDS:
            y = de_bruijn(B)[np.arange(PERSIST_N) % P]
            rng = np.random.default_rng(sd)
            a = conditioned_geometric(y, rng, theta)
            leads = lead_trace(a, PERSIST_N - 2)
            bad = (leads >= 2)
            wdens = []
            say("  (P=%d, mu=%d) seed=%d, overall density %.4f"
                % (P, mu, sd, float(bad.mean())))
            for w0 in range(0, len(bad), PERSIST_WIN):
                w = bad[w0:w0 + PERSIST_WIN]
                wdens.append(float(w.mean()))
                say("    depths %5d-%5d  (%4d leads)  density %.4f"
                    % (w0 + 1, w0 + len(w), len(w), wdens[-1]))
            wd = np.array(wdens)
            half = len(wd) // 2
            slope = np.polyfit(np.arange(len(wd)), wd, 1)[0]
            say("    first-half mean %.4f, second-half mean %.4f, "
                "trend slope %+.5f per window"
                % (wd[:half].mean(), wd[half:].mean(), slope))
            say("")
    say("task 3 runtime: %.1f s" % (time.time() - t0))
    say("")


if __name__ == "__main__":
    t_all = time.time()
    say("r3_boundary_fit.py — NUMERICAL — %s"
        % time.strftime("%Y-%m-%d %H:%M:%S"))
    say("")
    pstars = task1()
    task2(pstars)
    task3()
    say("total runtime: %.1f s" % (time.time() - t_all))
    _log.close()
