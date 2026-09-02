#!/usr/bin/env python3
"""Finalise the Kobon cube campaign: summary + CSV into the repo, patch placeholders.
usage: finalize_kobon.py <cubedir> <repo_conj_dir> <log_file> <top_readme>
"""
import glob
import os
import re
import shutil
import subprocess
import sys

cubedir, conj, logf, topreadme = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__))
data = os.path.join(conj, 'data')
os.makedirs(data, exist_ok=True)
summ = os.path.join(data, 'cubes_T2_summary.md')
csv = os.path.join(data, 'cubes_T2.csv')
subprocess.run([sys.executable, os.path.join(here, 'summarize_cubes.py'), cubedir, summ, csv], check=True)
for f in glob.glob(os.path.join(cubedir, 'run_*.out')) + [os.path.join(cubedir, 'verified.log'), os.path.join(cubedir, 'index.txt')]:
    if os.path.exists(f):
        shutil.copy(f, os.path.join(data, 'cubes_' + os.path.basename(f)))
# numbers
solved, ver = {}, {}
for f in glob.glob(os.path.join(cubedir, 'run_*.out')) + glob.glob(os.path.join(cubedir, '*.done')):
    for line in open(f):
        m = re.match(r'cube (\d+) (UNSAT|SAT|UNKNOWN) ([\d.]+)s', line)
        if m:
            solved[int(m.group(1))] = (m.group(2), float(m.group(3)))
for line in open(os.path.join(cubedir, 'verified.log')):
    m = re.match(r'cube (\d+) (VERIFIED|FAILED) ([\d.]+)s', line)
    if m:
        ver[int(m.group(1))] = (m.group(2), float(m.group(3)))
n = 561
cubes = len(solved)
unsat = sum(1 for v in solved.values() if v[0] == 'UNSAT')
times = sorted(v[1] for v in solved.values())
hardest = max(solved.items(), key=lambda kv: kv[1][1])
verified = sum(1 for v in ver.values() if v[0] == 'VERIFIED')
failed = sum(1 for v in ver.values() if v[0] == 'FAILED')
vals = {
    'cubes': f'{cubes}' if cubes == n else f'{cubes} of {n}',
    'solve_hours': f'{sum(times)/3600:.1f}',
    'median': f'{times[len(times)//2]:.0f}',
    'hardest': f'{hardest[0]}',
    'hardest_s': f'{hardest[1][1]:.0f}',
    'verified': f'{verified}',
    'verify_hours': f'{sum(v[1] for v in ver.values())/3600:.1f}',
    'unverified': f'{cubes - verified}',
}
print('numbers:', vals, 'unsat', unsat, 'failed', failed)
assert unsat == cubes and failed == 0, 'campaign not clean: check before publishing'
subs = {'{{%s}}' % k: v for k, v in vals.items()}
subs['[[561]]'] = vals['cubes']
subs['[[N_ver]]'] = vals['verified']
subs['[[N_verified]]'] = vals['verified']
subs['[[hours]] core-hours solving, [[hours]] verifying'] = f"{vals['solve_hours']} core-hours solving, {vals['verify_hours']} verifying"
for path in [os.path.join(conj, 'NOTE.md'), os.path.join(conj, 'README.md'), os.path.join(conj, 'PAGE.md'),
             os.path.join(conj, 'WRITEUP.md'), logf, topreadme]:
    s = open(path).read()
    for k, v in subs.items():
        s = s.replace(k, v)
    open(path, 'w').write(s)
    left = re.findall(r'\{\{\w+\}\}|\[\[[^\]]+\]\]', s)
    print(os.path.basename(path), 'remaining placeholders:', left)
