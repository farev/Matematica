#!/bin/bash
# Regenerates results/ladder_bnb.csv: small boundaries (n<=12) run fresh
# serially; n>=13 rows parsed from the committed run outputs in results/.
set -e
out=results/ladder_bnb.csv
echo "n,m,verdict,nodes,seconds,workers,source" > $out
for spec in "3 1 SAT" "3 2 UNSAT" "4 2 SAT" "4 3 UNSAT" "5 4 SAT" "5 5 UNSAT" \
            "6 5 SAT" "6 6 UNSAT" "7 7 SAT" "7 8 UNSAT" "8 9 SAT" "8 10 UNSAT" \
            "9 12 SAT" "9 13 UNSAT" "10 14 SAT" "10 15 UNSAT" \
            "11 17 SAT" "11 18 UNSAT" "12 21 SAT" "12 22 UNSAT"; do
  set -- $spec
  line=$(./bnb $1 $2 | head -1)
  nodes=$(sed -n 's/.*nodes=\([0-9]*\).*/\1/p' <<<"$line")
  secs=$(sed -n 's/.*time=\([0-9.]*\)s.*/\1/p' <<<"$line")
  verdict=$(awk '{print $1}' <<<"$line")
  [ "$verdict" = "$3" ] || { echo "VERDICT MISMATCH at n=$1 m=$2: $verdict != $3"; exit 1; }
  echo "$1,$2,$verdict,$nodes,$secs,1,fresh" >> $out
done
# big rows from committed outputs
awk -F'[= ]' '/UNSAT/{print "13,25,UNSAT," $3 "," $5+0 ",1,results/n13_m25.txt"}' results/n13_m25.txt | sed 's/,99.35s/,99.35/' >> $out
grep -o 'total_nodes=[0-9]* wall=[0-9.]*' results/n14_m29.txt | sed 's/total_nodes=\([0-9]*\) wall=\([0-9.]*\)/14,29,UNSAT,\1,\2,4,results\/n14_m29.txt/' >> $out
for f in results/n15_m33.txt results/n16_m42.txt results/n16_m38.txt; do
  if [ -s "$f" ]; then
    nm=$(sed -n 's/.*n=\([0-9]*\) m=\([0-9]*\):.*/\1,\2/p' "$f" | head -1)
    v=$(grep -oE 'UNSAT|SAT' "$f" | head -1)
    tn=$(grep -o 'total_nodes=[0-9]*' "$f" | cut -d= -f2)
    wl=$(grep -o 'wall=[0-9.]*' "$f" | cut -d= -f2)
    [ -n "$nm" ] && echo "$nm,$v,$tn,$wl,4,$f" >> $out
  fi
done
cat $out
