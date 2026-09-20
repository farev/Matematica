#!/bin/bash
# post-scan pipeline, strictly sequential (one core)
cd /tmp/claude-0/-home-user-Matematica/bc2c3ee2-f3c1-5718-9876-930480583604/scratchpad/hedge-etc
until grep -q '^DONE' scan.log; do sleep 5; done
echo "post.sh start $(date)"
python3 - <<'EOF'
import json
for n in [16,18]:
    s=json.load(open(f'summary_n{n}.json'))
    open(f'cx_n{n}.g6','w').write(''.join(g+'\n' for g,_ in s['counterexamples']))
for n in [4,6,8,10,12,14,16,18]:
    s=json.load(open(f'summary_n{n}.json'))
    open(f't2_n{n}.g6','w').write(''.join(g+'\n' for g in s['type2']))
EOF
echo "== cert R =="; python3 cert.py R 2>&1 | tail -3
echo "== cert counterexamples n16 =="; python3 cert.py cx n16 2>&1 | tail -2
echo "== cert counterexamples n18 =="; python3 cert.py cx n18 2>&1 | tail -2
echo "== brute --equitable on all counterexamples (SAT-free) == $(date)"
python3 brute.py --equitable $(cat cx_n16.g6 cx_n18.g6) > brute_cx_equitable.txt 2>&1; tail -3 brute_cx_equitable.txt
echo "== brute all colorings on Type-2 graphs n<=14 (SAT-free) == $(date)"
python3 brute.py $(cat t2_n4.g6 t2_n6.g6 t2_n8.g6 t2_n10.g6 t2_n12.g6 t2_n14.g6) > brute_t2_le14.txt 2>&1; awk -F'\t' '{print $4}' brute_t2_le14.txt | sort | uniq -c
echo "== brute --first on a sample of class-E graphs (SAT-free positive control) == $(date)"
(grep -P '\tE\t' results_n16.tsv | head -30 | cut -f1) > e_sample.g6
python3 brute.py --equitable --first $(cat e_sample.g6) > brute_e_sample.txt 2>&1; awk -F'\t' '{print $4}' brute_e_sample.txt | sort | uniq -c
echo "== cert type2 n<=16 == $(date)"
for n in 4 6 8 10 12 14 16; do python3 cert.py type2 n$n 2>&1 | tail -1; done
echo "== cert type2 n18 == $(date)"
python3 cert.py type2 n18 2>&1 | tail -1
echo "== brute all colorings on n16 counterexamples (SAT-free, capped 600s) == $(date)"
timeout 600 python3 brute.py $(cat cx_n16.g6) > brute_cx16_all.txt 2>&1; cat brute_cx16_all.txt
echo "post.sh end $(date)"
