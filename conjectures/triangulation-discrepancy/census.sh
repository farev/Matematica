#!/bin/bash
# census of disc(T) for n = 14..17; n = 17 in 4 res/mod parts (sequential; one core)
cd "$(dirname "$0")"  # expects ./plantri55/plantri and ./disc built here
for n in 14 15 16; do
  s=$(date +%s)
  ./plantri55/plantri $n 2>plantri_$n.log | ./disc -q -d 3 > n${n}_disc3.txt 2> n${n}.log
  echo "n=$n wall=$(( $(date +%s) - s )) s" >> timings.log
done
for k in 0 1 2 3; do
  s=$(date +%s)
  ./plantri55/plantri 17 $k/4 2>plantri_17_$k.log | ./disc -q -d 3 > n17_${k}_disc3.txt 2> n17_$k.log
  echo "n=17 part $k/4 wall=$(( $(date +%s) - s )) s" >> timings.log
done
echo CENSUS_DONE
