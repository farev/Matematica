#!/usr/bin/env python3
"""Drive the production campaign: NW stride workers over ascending tasks.
Every completed task row is a permanent certified range; resume-safe."""
import subprocess, os, sys

K, W, NW = 45, 30, 4
TOT = 1 << (K - W)

def done_ids(fn):
    ids = set()
    if os.path.exists(fn):
        for line in open(fn):
            try:
                ids.add(int(line.split(",")[0]))
            except (ValueError, IndexError):
                pass
    return ids

def main():
    procs = []
    for w in range(NW):
        fn = f"data/grid45_w{w}.csv"
        ids = done_ids(fn)
        k = w
        while k in ids:
            k += NW
        count = (TOT - k + NW - 1) // NW if k < TOT else 0
        if count <= 0:
            print(f"worker {w}: class complete")
            continue
        p = subprocess.Popen(["nice", "-n", "10", "./engine", "grid", str(K), str(W),
                              str(k), str(NW), str(count), fn])
        print(f"worker {w}: resume at task {k}, {count} tasks")
        procs.append(p)
    for p in procs:
        p.wait()

if __name__ == "__main__":
    main()
