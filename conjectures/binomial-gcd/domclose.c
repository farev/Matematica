/* domclose.c — close UNKNOWN family levels for Erdos #699.
 *
 * Reads jobs from stdin, one per line:
 *   n i  p1 t1  p2 t2  ...  (all decimal; n may exceed 2^64 — parsed as u128)
 * where (p, t) runs over ALL admissible primes at level i (p > i prime,
 * t = n mod p < i; the list must be complete = full factorization of the
 * window n..n-i+1 restricted to primes > i).
 *
 * For the admissible prime with the smallest Lucas-dominated set, the tool
 * DFS-enumerates every j in (i, n/2] dominated by n in base p (these are the
 * only j any admissible prime fails to cover), tests each against all other
 * admissible primes by exact Kummer, and classifies survivors via p = i.
 * Output: per job, either "CLEAN n i <nodes>" or explicit EXC/CEX lines.
 *
 * Exact integer arithmetic (u128).
 * Build: gcc -O2 -march=native -o domclose domclose.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;

#define MAXP 64
#define MAXD 130

static u128 parse_u128(const char *s, const char **end) {
    u128 v = 0;
    while (*s == ' ') s++;
    while (*s >= '0' && *s <= '9') { v = v * 10 + (*s - '0'); s++; }
    if (end) *end = s;
    return v;
}

static void print_u128(u128 v, char *buf) {
    char tmp[50]; int k = 0;
    if (!v) { strcpy(buf, "0"); return; }
    while (v) { tmp[k++] = '0' + (int)(v % 10); v /= 10; }
    for (int a = 0; a < k; a++) buf[a] = tmp[k - 1 - a];
    buf[k] = 0;
}

/* p | C(n,j)? exact Kummer via digit domination (all u128) */
static inline int pdivides(u128 p, u128 n, u128 j) {
    while (j) {
        if (j % p > n % p) return 1;
        j /= p; n /= p;
    }
    return 0;
}

static long double u128_ld(u128 v) {
    return (long double)(u64)(v >> 64) * 18446744073709551616.0L
         + (long double)(u64)v;
}

static u128 NH;                 /* n/2 */
static u128 NN;                 /* n */
static u64 II;                  /* level i */
static u128 P[MAXP]; static u64 T[MAXP];   /* admissible primes and t's */
static int NP;
static int BEST;                /* index of enumeration prime */
static u128 ND[MAXD];           /* digits of n base P[BEST], LSB first */
static int NDIG;
static u128 PW[MAXD];           /* powers of P[BEST] */
static u64 nodes_hits;
static u128 emitted;

static void classify(u128 j) {
    for (int a = 0; a < NP; a++) {
        if (a == BEST) continue;
        if (pdivides(P[a], NN, j)) return;      /* covered by p > i */
    }
    /* survivor: no admissible p > i divides C(n,j); p = i? */
    char bn[50], bj[50];
    print_u128(NN, bn); print_u128(j, bj);
    int iprime = II >= 2;
    for (u64 d = 2; d * d <= II; d++) if (II % d == 0) { iprime = 0; break; }
    int rescue = 0;
    if (iprime && (u64)(NN % ((u128)II * II)) < II && pdivides(II, NN, j)) rescue = 1;
    printf("%s n=%s i=%llu j=%s\n", rescue ? "EXC" : "CEX",
           bn, (unsigned long long)II, bj);
    fflush(stdout);
    nodes_hits++;
    if (nodes_hits > 10000) {
        printf("JOBFAIL n=%s i=%llu: hit cap exceeded, aborting job (bug canary)\n",
               bn, (unsigned long long)II);
        exit(3);
    }
}

/* DFS over digits from most significant; acc = partial value */
static void dfs(int pos, u128 acc) {
    if (pos < 0) {
        if (acc > II && acc <= NH) { emitted++; classify(acc); }
        return;
    }
    for (u128 d = 0; d <= ND[pos]; d++) {
        u128 v = acc + PW[pos] * d;
        if (v > NH) break;                      /* larger digits only grow v */
        dfs(pos - 1, v);
    }
}

int main(void) {
    char *line = NULL; size_t cap = 0;
    while (getline(&line, &cap, stdin) > 0) {
        const char *s = line;
        NN = parse_u128(s, &s);
        if (!NN) continue;
        II = (u64)parse_u128(s, &s);
        NP = 0;
        while (1) {
            u128 p = parse_u128(s, &s);
            if (!p) break;
            u128 t = parse_u128(s, &s);
            P[NP] = p; T[NP] = (u64)t; NP++;
        }
        NH = NN / 2;
        /* choose enumeration prime: smallest dominated-set size prod(d+1) */
        long double best_sz = 1e33L; BEST = -1;
        for (int a = 0; a < NP; a++) {
            long double sz = 1;
            u128 m = NN;
            while (m) { sz *= u128_ld(m % P[a]) + 1; m /= P[a]; }
            if (sz < best_sz) { best_sz = sz; BEST = a; }
        }
        if (BEST < 0) { fprintf(stderr, "no admissible primes?\n"); continue; }
        { char bb[50]; print_u128(P[BEST], bb);
          fprintf(stderr, "job n~2^%.1Lf i=%llu base=%s domsize~%.3Lg\n",
                  u128_ld(NN) > 0 ? (long double)(__builtin_log2l(u128_ld(NN))) : 0.0L,
                  (unsigned long long)II, bb, best_sz); }
        NDIG = 0;
        { u128 m = NN; while (m) { ND[NDIG] = m % P[BEST]; m /= P[BEST]; NDIG++; } }
        PW[0] = 1;
        for (int d = 1; d < NDIG; d++) PW[d] = PW[d - 1] * P[BEST];
        nodes_hits = 0; emitted = 0;
        dfs(NDIG - 1, 0);
        char bn[50], be[50], bb[50];
        print_u128(NN, bn); print_u128(emitted, be); print_u128(P[BEST], bb);
        if (!nodes_hits)
            printf("CLEAN n=%s i=%llu enumerated=%s base=%s\n",
                   bn, (unsigned long long)II, be, bb);
        fflush(stdout);
    }
    return 0;
}
