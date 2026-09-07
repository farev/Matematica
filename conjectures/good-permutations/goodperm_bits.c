/*
 * goodperm_bits.c — second, independently organised engine for good
 * permutations of n = 2^m - 1 (cross-check of goodperm.c mode 1).
 *
 * By NOTE.md Lemma 2 every good permutation of [2^m - 1] has the form
 *     bit_k(a_t) = b_k(t mod 2^k) XOR bit_k(t),   k = 0..m-1,
 * with b_0 = 0 and b_k(0) = 0; conversely every such family of bit
 * functions defines a permutation of [n] with a_0 = 0 (bijectivity is
 * automatic, no "used" bookkeeping).  By Lemma 3 only odd block lengths
 * need testing.  This engine searches the bits b_k(r) in position order:
 * at position t the bits b_k(t mod 2^k) with 2^k > t are still free (the
 * others were fixed by an earlier position), so the candidates for a_t are
 * exactly the 2^{#free} values obtained by enumerating those bits.  Block
 * sums are tracked with one sliding accumulator per odd length L
 * (S_L = sum of the last L terms, updated by +a_t - a_{t-L}), not with
 * prefix sums.
 *
 * Usage: goodperm_bits n [maxreport]   (n = 2^m - 1, m <= 10)
 * Output: good permutations (up to maxreport) and
 *   "n=.. count=.. nodes=.. time=..s"
 * where nodes counts every candidate value tested against the block
 * constraints (the same quantity goodperm.c reports).
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAXM 10
#define MAXN ((1 << MAXM) - 1)

static int n, m, maxreport;
static int b[MAXM][1 << MAXM];      /* b[k][r], r < 2^k */
static int a[MAXN + 2];
static long long S[MAXN + 2];       /* S[L] = sum of the last L placed terms, for odd L */
static long long cnt = 0, nodes = 0;

static void report(void) {
    if (cnt <= maxreport) {
        for (int i = 1; i <= n; i++) printf("%d%c", a[i], i == n ? '\n' : ' ');
        fflush(stdout);
    }
}

/* place value v at position t (bits already set), test odd blocks ending at t */
static int test_and_place(int t, int v) {
    nodes++;
    /* update sliding sums for all odd L >= 3 with L <= t; block proper needs L <= n-1 */
    int Lmax = t < n ? t : n - 1;
    /* we must update S[L] for every odd L <= n-1 (even those > t, which are still
       accumulating); do it for all odd L up to n-1 and test only L <= Lmax */
    for (int L = 3; L <= n - 1; L += 2) {
        S[L] += v;
        if (t > L) S[L] -= a[t - L];
        if (L <= Lmax && S[L] % L == 0) {
            /* undo the updates done so far (L' <= L) */
            for (int L2 = 3; L2 <= L; L2 += 2) { S[L2] -= v; if (t > L2) S[L2] += a[t - L2]; }
            return 0;
        }
    }
    a[t] = v;
    return 1;
}
static void unplace(int t, int v) {
    for (int L = 3; L <= n - 1; L += 2) { S[L] -= v; if (t > L) S[L] += a[t - L]; }
}

static void rec(int t) {
    if (t > n) { cnt++; report(); return; }
    /* free bits at position t: k with 2^k > t, k <= m-1; r = t mod 2^k = t */
    int kfree_lo = 0;
    while (kfree_lo < m && (1 << kfree_lo) <= t) kfree_lo++;
    int nfree = m - kfree_lo;           /* bits kfree_lo..m-1 are free */
    /* fixed part of g(t) from bits k < kfree_lo */
    int gfixed = 0;
    for (int k = 1; k < kfree_lo; k++) gfixed |= b[k][t & ((1 << k) - 1)] << k;
    for (int pat = 0; pat < (1 << nfree); pat++) {
        int g = gfixed | (pat << kfree_lo);
        int v = t ^ g;
        if (v < 1 || v > n) continue;   /* cannot happen for b(0)=0, kept as a guard */
        for (int k = kfree_lo; k < m; k++) b[k][t] = (pat >> (k - kfree_lo)) & 1;
        if (test_and_place(t, v)) { rec(t + 1); unplace(t, v); }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: goodperm_bits n [maxreport]\n"); return 2; }
    n = atoi(argv[1]); maxreport = argc > 2 ? atoi(argv[2]) : 10;
    int q = n + 1; m = 0;
    while ((q & 1) == 0) { q >>= 1; m++; }
    if (q != 1 || m > MAXM || m < 2) { fprintf(stderr, "n must be 2^m-1, 2<=m<=%d\n", MAXM); return 2; }
    for (int k = 0; k < MAXM; k++) for (int r = 0; r < (1 << MAXM); r++) b[k][r] = 0; /* b_k(0)=0, b_0=0 */
    for (int L = 0; L <= n; L++) S[L] = 0;
    clock_t c0 = clock();
    rec(1);
    printf("n=%d count=%lld nodes=%lld time=%.2fs\n", n, cnt, nodes, (double)(clock() - c0) / CLOCKS_PER_SEC);
    return 0;
}
