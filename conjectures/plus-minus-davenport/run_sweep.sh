#!/bin/bash
# Sweep driver: one line of cells.txt per group (moduli list), 3 workers,
# per-cell timeout 3600 s. Results land in data/sweep/<moduli>.txt and are
# consolidated by make_table.py. Rerunnable: finished cells are skipped.
cd "$(dirname "$0")"
mkdir -p data/sweep
run_cell() {
  set -- $1
  key=$(echo "$@" | tr ' ' '_')
  out="data/sweep/${key}.txt"
  [ -s "$out" ] && return
  timeout 3600 ./dpm_search $@ > "$out".tmp 2>&1 && mv "$out".tmp "$out" \
    || { echo "TIMEOUT $@" > "$out"; rm -f "$out".tmp; }
}
export -f run_cell
xargs -a cells.txt -d '\n' -I{} -P ${WORKERS:-3} bash -c 'run_cell "{}"'
echo SWEEP-COMPLETE
