/* brute699.c — exhaustive validator for Erdos #699 semantics.
 *
 * For every n in [nlo, nhi], every pair 1 <= i < j <= n/2:
 *   witnesses W(n,i,j) = { p prime : p | C(n,i), p | C(n,j) }   (all p <= n)
 *   base conjecture:      exists p in W with p >= i
 *   strengthening:        exists p in W with p >  i
 * Divisibility p | C(n,k) via Lucas: some base-p digit of k > digit of n.
 * Exact integer arithmetic only.
 *
 * Output: every base violation (CEX), every exceptional triple (EXC:
 * witnesses >= i exist but none > i), and per-n margin = min over pairs of
 * #witnesses >= i, streamed as CSV lines "n,minwit,argi,argj".
 *
 * Usage: ./brute699 nlo nhi [margin_out.csv] >> exceptions.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int *primes, nprimes;

static void sieve(int N) {
    char *c = calloc(N + 1, 1);
    int cap = N / 8 + 256; /* > pi(N) for all N */
    primes = malloc(sizeof(int) * cap);
    nprimes = 0;
    for (int p = 2; p <= N; p++) {
        if (!c[p]) {
            if (nprimes >= cap) { fprintf(stderr, "prime cap exceeded\n"); exit(9); } primes[nprimes++] = p;
            for (long long q = (long long)p * p; q <= N; q += p) c[q] = 1;
        }
    }
    free(c);
}

/* p | C(n,k) iff some base-p digit of k exceeds n's */
static inline int divides_binom(long long p, long long n, long long k) {
    while (k) {
        if (k % p > n % p) return 1;
        k /= p; n /= p;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s nlo nhi [margin.csv]\n", argv[0]); return 1; }
    int nlo = atoi(argv[1]), nhi = atoi(argv[2]);
    FILE *mf = argc > 3 ? fopen(argv[3], "w") : NULL;
    sieve(nhi);
    int W = (nprimes + 63) / 64;
    uint64_t *mask = malloc((size_t)(nhi / 2 + 1) * W * 8);
    uint64_t *geq = malloc((size_t)W * 8), *gt = malloc((size_t)W * 8);
    long long n_exc = 0, n_cex = 0;
    if (mf) fprintf(mf, "n,minwit,argi,argj\n");
    for (int n = nlo; n <= nhi; n++) {
        int half = n / 2, np = 0;
        while (np < nprimes && primes[np] <= n) np++;
        int w = (np + 63) / 64;
        memset(mask, 0, (size_t)(half + 1) * W * 8);
        for (int t = 0; t < np; t++) {
            long long p = primes[t];
            for (int k = 1; k <= half; k++)
                if (divides_binom(p, n, k)) mask[(size_t)k * W + t / 64] |= 1ULL << (t % 64);
        }
        /* geq = primes >= i, gt = primes > i; start i=1: all primes */
        memset(geq, 0, W * 8); memset(gt, 0, W * 8);
        for (int t = 0; t < np; t++) { geq[t/64] |= 1ULL << (t%64); gt[t/64] |= 1ULL << (t%64); }
        int minwit = -1, argi = 0, argj = 0;
        int pt = 0; /* index of smallest prime not yet cleared */
        for (int i = 1; i < half; i++) {
            /* update masks: geq = primes >= i, gt = primes > i */
            /* clear from geq all primes < i, from gt all primes <= i */
            while (pt < np && primes[pt] < i) { geq[pt/64] &= ~(1ULL << (pt%64)); gt[pt/64] &= ~(1ULL << (pt%64)); pt++; }
            if (pt < np && primes[pt] == i) gt[pt/64] &= ~(1ULL << (pt%64)); /* p=i out of gt only */
            uint64_t *mi = mask + (size_t)i * W;
            for (int j = i + 1; j <= half; j++) {
                uint64_t *mj = mask + (size_t)j * W;
                int cnt = 0, any_gt = 0;
                for (int t = 0; t < w; t++) {
                    uint64_t c = mi[t] & mj[t];
                    cnt += __builtin_popcountll(c & geq[t]);
                    any_gt |= (c & gt[t]) != 0;
                }
                if (minwit < 0 || cnt < minwit) { minwit = cnt; argi = i; argj = j; }
                if (cnt == 0) { printf("CEX %d %d %d\n", n, i, j); fflush(stdout); n_cex++; }
                else if (!any_gt) {
                    printf("EXC %d %d %d :", n, i, j);
                    for (int t = 0; t < np; t++)
                        if ((mi[t/64] & mask[(size_t)j*W + t/64] & geq[t/64]) >> (t%64) & 1
                            && divides_binom(primes[t], n, i) && divides_binom(primes[t], n, j))
                            printf(" %d", primes[t]);
                    printf("\n"); fflush(stdout);
                    n_exc++;
                }
            }
            if (pt < np && primes[pt] == i) { geq[pt/64] &= ~(1ULL << (pt%64)); pt++; } /* for next i, p=i < i+1 leaves geq */
        }
        if (mf && minwit >= 0) fprintf(mf, "%d,%d,%d,%d\n", n, minwit, argi, argj);
    }
    fprintf(stderr, "done [%d,%d]: %lld exceptional, %lld violations\n", nlo, nhi, n_exc, n_cex);
    if (mf) fclose(mf);
    return n_cex ? 2 : 0;
}
