#!/bin/bash
# Official frozen-engine ladder, in value order. Every run is resumable
# per-unit (--resume) and appends its final record to an official JSONL.
# Safe to re-execute after any interruption: completed m-runs re-verify
# from the resume ledgers in seconds.
cd "$(dirname "$0")" || exit 1
mkdir -p results
{
  echo "=== run_official start $(date -u +%FT%TZ)"
  # 1. odd Giuga ladder through 13 (the record-matching range)
  python3 search.py --eps -1 --parity odd --m 1 --mmax 13 --jobs 4 \
    --split-depth 7 --resume results/resume_odd_giuga.jsonl \
    --out results/odd_giuga_official.jsonl
  echo "=== odd giuga <=13 done rc=$? $(date -u +%FT%TZ)"
  # 2. odd PPN ladder through 13 (locks the first new PPN bound)
  python3 search.py --eps 1 --parity odd --m 1 --mmax 13 --jobs 4 \
    --split-depth 7 --resume results/resume_odd_ppn.jsonl \
    --out results/odd_ppn_official.jsonl
  echo "=== odd ppn <=13 done rc=$? $(date -u +%FT%TZ)"
  # 3. the prize: odd Giuga m=14
  python3 search.py --eps -1 --parity odd --m 14 --jobs 4 \
    --split-depth 8 --resume results/resume_odd_giuga.jsonl \
    --out results/odd_giuga_official.jsonl
  echo "=== odd giuga m=14 done rc=$? $(date -u +%FT%TZ)"
  # 4. second frontier: odd PPN m=14
  python3 search.py --eps 1 --parity odd --m 14 --jobs 4 \
    --split-depth 8 --resume results/resume_odd_ppn.jsonl \
    --out results/odd_ppn_official.jsonl
  echo "=== odd ppn m=14 done rc=$? $(date -u +%FT%TZ)"
  # 5. official control records (validated informally already)
  python3 search.py --eps -1 --parity all --m 1 --mmax 7 --jobs 4 \
    --split-depth 5 --resume results/resume_control_giuga.jsonl \
    --out results/control_giuga_official.jsonl
  python3 search.py --eps 1 --parity all --m 1 --mmax 7 --jobs 4 \
    --split-depth 5 --resume results/resume_control_ppn.jsonl \
    --out results/control_ppn_official.jsonl
  echo "=== controls <=7 done rc=$? $(date -u +%FT%TZ)"
  # 6. m=8 controls (wide windows; may be long — last on purpose)
  python3 search.py --eps 1 --parity all --m 8 --jobs 4 \
    --split-depth 5 --resume results/resume_control_ppn.jsonl \
    --out results/control_ppn_official.jsonl
  python3 search.py --eps -1 --parity all --m 8 --jobs 4 \
    --split-depth 5 --resume results/resume_control_giuga.jsonl \
    --out results/control_giuga_official.jsonl
  echo "=== all official runs done $(date -u +%FT%TZ)"
} >> results/official_driver.log 2>&1
