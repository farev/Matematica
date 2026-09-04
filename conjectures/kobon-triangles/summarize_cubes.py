#!/usr/bin/env python3
"""Summarise a cube campaign: solver outcomes/times from run_*.out and .done markers,
drat-trim results from verified.log; emit a markdown summary and a CSV certificate index.
usage: summarize_cubes.py <cubedir> <out.md> <out.csv>
"""
import glob
import os
import re
import sys


def main():
    cubedir, out_md, out_csv = sys.argv[1:4]
    idx = {}
    for line in open(os.path.join(cubedir, 'index.txt')):
        if line.startswith('#'):
            continue
        k, S, osz = line.split()
        idx[int(k)] = (S, int(osz))
    solved = {}
    for f in glob.glob(os.path.join(cubedir, 'run_*.out')) + glob.glob(os.path.join(cubedir, '*.done')):
        for line in open(f):
            m = re.match(r'cube (\d+) (UNSAT|SAT|UNKNOWN) ([\d.]+)s', line)
            if m:
                k = int(m.group(1))
                solved[k] = (m.group(2), float(m.group(3)))   # last record wins
    ver = {}
    p = os.path.join(cubedir, 'verified.log')
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r'cube (\d+) (VERIFIED|FAILED) ([\d.]+)s solve=([\d.]+)s proof_bytes=(\d+) sha256=(\w+)', line)
            if m:
                ver[int(m.group(1))] = (m.group(2), float(m.group(3)), int(m.group(5)), m.group(6))
    n = len(idx)
    st = {}
    for k in idx:
        st[solved.get(k, ('MISSING', 0))[0]] = st.get(solved.get(k, ('MISSING', 0))[0], 0) + 1
    times = sorted(((v[1], k) for k, v in solved.items()), reverse=True)
    tot = sum(v[1] for v in solved.values())
    vst = {}
    for k in idx:
        s = ver.get(k, ('UNVERIFIED',))[0]
        vst[s] = vst.get(s, 0) + 1
    vtot = sum(v[1] for v in ver.values())
    pbytes = sum(v[2] for v in ver.values())
    with open(out_md, 'w') as f:
        f.write(f'# Cube campaign summary: {os.path.basename(cubedir)}\n\n')
        f.write(f'- cubes: {n}; orbits cover {sum(v[1] for v in idx.values())} subsets\n')
        f.write(f'- solver outcomes: {st}\n')
        f.write(f'- total solve time: {tot/3600:.2f} core-hours; hardest cubes: ' +
                ', '.join(f'#{k} ({idx[k][0]}) {t:.0f}s' for t, k in times[:8]) + '\n')
        if solved:
            f.write(f'- median solve time: {sorted(v[1] for v in solved.values())[len(solved)//2]:.1f}s\n')
        f.write(f'- drat-trim: {vst}; total verification time {vtot/3600:.2f} core-hours; '
                f'total proof size {pbytes/1e9:.2f} GB\n')
    with open(out_csv, 'w') as f:
        f.write('cube,imperfect_lines,orbit_size,solver_result,solve_seconds,drat_trim,verify_seconds,proof_bytes,proof_sha256\n')
        for k in sorted(idx):
            S, osz = idx[k]
            sres, stime = solved.get(k, ('MISSING', 0))
            v = ver.get(k, ('UNVERIFIED', 0, 0, ''))
            f.write(f'{k},{S},{osz},{sres},{stime:.1f},{v[0]},{v[1]:.1f},{v[2]},{v[3]}\n')
    print(open(out_md).read())


if __name__ == '__main__':
    main()
