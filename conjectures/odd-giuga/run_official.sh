#!/bin/bash
# Official frozen-engine (v5) run set. Every run resumable per-unit
# (--resume) and appended to an official JSONL. Safe to re-execute after
# any interruption. Order: the two odd frontier ladders (the bounds),
# the even control censuses m<=8 (published answers), then the
# 9-factor Giuga census (new territory).
cd "$(dirname "$0")" || exit 1
mkdir -p results
{
  echo "=== run_official v5 start $(date -u +%FT%TZ)"
  python3 search.py --eps -1 --parity odd --m 1 --mmax 12 --jobs 4 \
    --split-depth 7 --resume results/resume_odd_giuga.jsonl \
    --out results/odd_giuga_official.jsonl
  echo "=== odd giuga <=12 done rc=$? $(date -u +%FT%TZ)"
  python3 search.py --eps 1 --parity odd --m 1 --mmax 12 --jobs 4 \
    --split-depth 7 --resume results/resume_odd_ppn.jsonl \
    --out results/odd_ppn_official.jsonl
  echo "=== odd ppn <=12 done rc=$? $(date -u +%FT%TZ)"
  python3 search.py --eps -1 --parity all --m 1 --mmax 8 --jobs 4 \
    --split-depth 6 --resume results/resume_control_giuga.jsonl \
    --out results/control_giuga_official.jsonl
  echo "=== control giuga <=8 done rc=$? $(date -u +%FT%TZ)"
  python3 search.py --eps 1 --parity all --m 1 --mmax 8 --jobs 4 \
    --split-depth 6 --resume results/resume_control_ppn.jsonl \
    --out results/control_ppn_official.jsonl
  echo "=== control ppn <=8 done rc=$? $(date -u +%FT%TZ)"
  python3 search.py --eps -1 --parity all --m 9 --jobs 4 \
    --split-depth 6 --resume results/resume_giuga9.jsonl \
    --out results/giuga9_census.jsonl
  echo "=== giuga 9-factor census done rc=$? $(date -u +%FT%TZ)"
  echo "=== all official v5 runs done $(date -u +%FT%TZ)"
} >> results/official_driver.log 2>&1
