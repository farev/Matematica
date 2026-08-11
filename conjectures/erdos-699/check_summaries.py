#!/usr/bin/env python3
"""check_summaries.py — aggregate the per-chunk SUMMARY lines into
data/summary.csv and run the record-prime-gap control.

SUMMARY format (sweep.c):
  SUMMARY lo hi composites hard_rows exc_cand exc weakfail maxg secs

Controls:
  * chunk ranges must tile [4, N] with no gap or overlap;
  * weakfail must be 0 everywhere (else the session's headline changes);
  * max over chunks of maxg must equal (G - 1) where G is the largest
    record prime gap whose starting prime p satisfies p + G <= N, from
    the pinned A005250 (gaps) / A002386 (starting primes) .seq files —
    since max_{composite n <= N} (n - prevprime(n)) is attained at the
    composite just below the end of the largest gap fully inside range.
Usage: python3 check_summaries.py N chunk1.txt chunk2.txt ...
"""
import sys, re


def seq_terms(path):
    terms = []
    for line in open(path):
        m = re.match(r"^%[STU] A\d+ (.*)$", line.strip())
        if m:
            terms += [int(x) for x in m.group(1).rstrip(",").split(",") if x]
    return terms


def main():
    N = int(sys.argv[1])
    chunks = []
    for fn in sys.argv[2:]:
        for line in open(fn):
            if line.startswith("SUMMARY"):
                v = line.split()
                chunks.append((fn,) + tuple(int(x) for x in v[1:8])
                              + (int(v[8]), float(v[9])))
    chunks.sort(key=lambda c: c[1])
    ok = True
    # tiling
    expect = 4
    for c in chunks:
        if c[1] != expect:
            print(f"TILING GAP: chunk {c[0]} starts at {c[1]}, expected {expect}")
            ok = False
        expect = c[2] + 1
    if expect != N + 1:
        print(f"TILING: last chunk ends at {expect-1}, expected {N}")
        ok = False
    # weakfails
    for c in chunks:
        if c[7] != 0:
            print(f"WEAKFAIL count {c[7]} in {c[0]} — HEADLINE EVENT")
            ok = False
    # gap control
    gaps = seq_terms("data/A005250.seq")
    starts = seq_terms("data/A002386.seq")
    G = max(g for g, p in zip(gaps, starts) if p + g <= N)
    maxg = max(c[8] for c in chunks)
    if maxg == G - 1:
        print(f"record-gap control PASS: max hard-row gap {maxg} = {G}-1 "
              f"(largest record gap {G} fully below {N}, A005250/A002386)")
    else:
        print(f"record-gap control FAIL: maxg {maxg} vs expected {G-1}")
        ok = False
    tot_comp = sum(c[3] for c in chunks)
    tot_rows = sum(c[4] for c in chunks)
    tot_exc = sum(c[6] for c in chunks)
    tot_secs = sum(c[9] for c in chunks)
    with open("data/summary.csv", "w") as f:
        f.write("chunk,lo,hi,composites,hard_rows,exc_candidates,exceptions,"
                "weakfails,max_gap,engine_secs\n")
        for c in chunks:
            f.write(",".join(str(x) for x in c) + "\n")
        f.write(f"TOTAL,4,{N},{tot_comp},{tot_rows},,{tot_exc},0,{maxg},"
                f"{tot_secs:.2f}\n")
    print(f"chunks: {len(chunks)}; composites {tot_comp:,}; hard rows "
          f"{tot_rows:,}; exceptions {tot_exc}; engine time {tot_secs:.0f}s")
    print("SUMMARY CONTROLS", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
