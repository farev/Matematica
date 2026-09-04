#!/usr/bin/env python3
"""Refresh the drat-trim verification counts in the Kobon documents after more proofs
have been verified.  Replaces the previously written numbers (given on the command line)
in their specific phrases only.  usage: refresh_counts.py <cubedir> <repo> <old_ver> <old_unver> <old_hours>
"""
import os
import re
import shutil
import subprocess
import sys

cubedir, repo, old_ver, old_unver, old_hours = sys.argv[1:6]
conj = os.path.join(repo, 'conjectures', 'kobon-triangles')
here = os.path.dirname(os.path.abspath(__file__))
ver, hours, failed = 0, 0.0, 0
for line in open(os.path.join(cubedir, 'verified.log')):
    m = re.match(r'cube (\d+) (VERIFIED|FAILED) ([\d.]+)s', line)
    if m:
        if m.group(2) == 'VERIFIED':
            ver += 1
            hours += float(m.group(3)) / 3600
        else:
            failed += 1
assert failed == 0, 'a proof FAILED verification: stop and investigate'
new_ver, new_unver, new_hours = str(ver), str(561 - ver), f'{hours:.1f}'
print('verified', new_ver, 'unverified', new_unver, 'hours', new_hours)
subprocess.run([sys.executable, os.path.join(here, 'summarize_cubes.py'), cubedir,
                os.path.join(conj, 'data', 'cubes_T2_summary.md'), os.path.join(conj, 'data', 'cubes_T2.csv')],
               check=True, capture_output=True)
shutil.copy(os.path.join(cubedir, 'verified.log'), os.path.join(conj, 'data', 'cubes_verified.log'))
pats = [
    (rf'\b{old_ver} DRAT proofs `drat-trim`-checked', f'{new_ver} DRAT proofs `drat-trim`-checked'),
    (rf'\b{old_ver} of the 561 DRAT proofs were `drat-trim`-verified', f'{new_ver} of the 561 DRAT proofs were `drat-trim`-verified'),
    (rf'\b{old_ver} of the DRAT proofs were checked by `drat-trim`', f'{new_ver} of the DRAT proofs were checked by `drat-trim`'),
    (rf'\({old_hours} core-hours; the remaining {old_unver} proofs', f'({new_hours} core-hours; the remaining {new_unver} proofs'),
    (rf'\b{old_ver} of 561 DRAT proofs verified by `drat-trim`', f'{new_ver} of 561 DRAT proofs verified by `drat-trim`'),
    (rf'core-hours solving, {old_hours} verifying', f'core-hours solving, {new_hours} verifying'),
    (rf'\b{old_ver} proofs `drat-trim`-verified by session end', f'{new_ver} proofs `drat-trim`-verified by session end'),
    (rf'\({old_hours} core-hours; the remaining {old_unver} kept', f'({new_hours} core-hours; the remaining {new_unver} kept'),
    (rf'\b{old_ver} DRAT proofs `drat-trim`-verified', f'{new_ver} DRAT proofs `drat-trim`-verified'),
    (rf'\b{old_ver} proofs drat-trim-verified so far', f'{new_ver} proofs drat-trim-verified so far'),
]
for path in [os.path.join(conj, f) for f in ('README.md', 'NOTE.md', 'PAGE.md', 'WRITEUP.md')] + \
            [os.path.join(repo, 'log', '2026-09-02-kobon-triangles.md'), os.path.join(repo, 'README.md')]:
    s = open(path).read()
    n = 0
    for pat, rep in pats:
        s, k = re.subn(pat, rep, s)
        n += k
    open(path, 'w').write(s)
    print(os.path.basename(path), 'replacements:', n)
