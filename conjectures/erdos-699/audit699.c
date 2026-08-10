/* audit699.c — independent third-path auditor for the scan699 sweep.
 *
 * For sampled (n, i): recompute the level-i strict-failure set from scratch
 * by (a) trial-division factoring of n, n-1, ..., n-i+1 (no shared code with
 * the segmented sieve), (b) building T_i = {p > i : n mod p < i} from those
 * factorizations plus a direct residue check, and (c) scanning EVERY
 * j in (i, n/2] with the Lucas digit test against all of T_i, recording any
 * j dominated by all (strict failure), classified by the p = i test.
 *
 * The sample is drawn by a recorded LCG seed; the known exceptional (n,i)
 * are appended as positive controls (the auditor must rediscover them).
 *
 * Usage: ./audit699 seed count nmax   > audit_report.txt
 * Every line: AUDIT,n,i,g,failcount[,j:kind...]   — to be diffed against the
 * sweep census restricted to the sampled (n,i).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>

typedef uint64_t u64;

static inline int div_binom(u64 p, u64 n, u64 k) {
    while (k) { if (k % p > n % p) return 1; k /= p; n /= p; }
    return 0;
}
static int is_prime_td(u64 x) {
    if (x < 2) return 0;
    for (u64 d = 2; d * d <= x; d++) if (x % d == 0) return 0;
    return 1;
}
static int factor_td(u64 x, u64 *pr) {   /* distinct primes by trial division */
    int c = 0;
    for (u64 d = 2; d * d <= x; d++) if (x % d == 0) {
        pr[c++] = d;
        while (x % d == 0) x /= d;
    }
    if (x > 1) pr[c++] = x;
    return c;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s seed count nmax\n", argv[0]); return 1; }
    u64 seed = strtoull(argv[1], 0, 10);
    int count = atoi(argv[2]);
    u64 nmax = strtoull(argv[3], 0, 10);
    u64 s = seed;
    printf("# audit699 seed=%" PRIu64 " count=%d nmax=%" PRIu64 "\n", seed, count, nmax);
    /* positive controls: the known exceptional (n,i) */
    u64 ctrl[][2] = {{10,3},{16,2},{28,3},{28,5},{244,3},{512,2},{2048,2},{2188,3},{1594324,3}};
    int nctrl = sizeof(ctrl) / sizeof(ctrl[0]);
    for (int it = 0; it < count + nctrl; it++) {
        u64 n, i, g;
        if (it < nctrl) { n = ctrl[it][0]; i = ctrl[it][1]; }
        else {
            do {
                s = s * 6364136223846793005ULL + 1442695040888963407ULL;
                n = 100000 + (s >> 12) % (nmax - 100000);
            } while (is_prime_td(n));
        }
        /* g = n - prevprime(n) by direct search */
        u64 pp = n; while (!is_prime_td(pp)) pp--;
        g = n - pp;
        if (it >= nctrl) {
            if (g < 2) { printf("AUDIT,%" PRIu64 ",-,%" PRIu64 ",prime-gap<2\n", n, g); continue; }
            s = s * 6364136223846793005ULL + 1442695040888963407ULL;
            i = 2 + (s >> 12) % (g - 1);
        }
        /* T_i from trial-division factorizations of n-r, r < i */
        u64 T[200]; int nt = 0;
        for (u64 r = 0; r < i; r++) {
            u64 pr[64]; int c = factor_td(n - r, pr);
            for (int t = 0; t < c; t++)
                if (pr[t] > i && n % pr[t] == r)   /* independent residue check */
                    T[nt++] = pr[t];
        }
        /* full scan over j */
        u64 half = n / 2;
        int fails = 0;
        char buf[4096]; int bl = 0; buf[0] = 0;
        for (u64 j = i + 1; j <= half; j++) {
            int witness = 0;
            for (int t = 0; t < nt; t++)
                if (div_binom(T[t], n, j)) { witness = 1; break; }
            if (witness) continue;
            int saved = is_prime_td(i) && div_binom(i, n, i) && div_binom(i, n, j);
            fails++;
            bl += snprintf(buf + bl, sizeof buf - bl, ",%" PRIu64 ":%s", j, saved ? "EXC" : "CEX");
        }
        printf("AUDIT,%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%d%s\n", n, i, g, fails, buf);
        fflush(stdout);
    }
    return 0;
}
