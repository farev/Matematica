#!/bin/bash
# production sweep in decade chunks; each writes census/gaphist/summary
set -e
cd "$(dirname "$0")"
for RANGE in "1000000000 10000000000 c2" "10000000000 100000000000 c3" "100000000000 1000000000000 c4"; do
  set -- $RANGE
  echo "=== chunk $3: [$1, $2) start $(date -u +%H:%M:%S) ==="
  ./grimm_sweep $1 $2 4 data/$3
  echo "=== chunk $3 done $(date -u +%H:%M:%S) ==="
done
echo ALL CHUNKS DONE
