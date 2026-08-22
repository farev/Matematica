#!/bin/bash
cd "$(dirname "$0")"
./dpm 7 21 --raw > run_7_21_raw.txt 2>&1 &
P1=$!
python3 dpm_indep.py 7 21 > run_7_21_indep.txt 2>&1 &
P2=$!
./dpm 7 21 --enum 7 | grep -v "^ENUM" > run_7_21_enum_header.txt 2>&1
./dpm 7 21 --enum 7 2>/dev/null | grep "^ENUM" > enum_7_21_size7.txt
python3 verify_maximality.py --group 7 21 --size 7 --expect 2016 --file enum_7_21_size7.txt > max_7_21.txt 2>&1
python3 verify_maximality.py --group 5 15 --size 5 --expect 85155 --file enum_5_15_size5.txt > max_5_15.txt 2>&1
wait $P1 $P2
echo ALLDONE
