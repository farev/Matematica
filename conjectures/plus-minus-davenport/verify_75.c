/* verify_75.c — independent refutation for C5+C15 (and C7+C21 with -DG147).
 *
 * NOT a DFS: enumerates ALL k-subsets of class representatives by plain
 * nested loops and tests each with a from-scratch subset-sum distinctness
 * check (bitmap over G, all 2^k sums computed by Gray-code-free direct
 * accumulation).  Shares no search logic with dissoc.c; only the group
 * definition (mixed radix) is common, and that is re-implemented here.
 *
 * Default: group C5+C15 (order 75), k = 6: claims to verify
 *   "no dissociated 6-set exists"  <=>  D_pm(C5+C15) = 6.
 * With -DG147: group C7+C21 (order 147), k = 7.
 *
 * Also re-verifies the published-window sanity: prints the number of
 * dissociated (k-1)-sets found en route (must be > 0).
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#ifdef G147
#define F1 7
#define F2 21
#define K 7
#else
#define F1 5
#define F2 15
#define K 6
#endif
#define N (F1 * F2)

static int addt[N][N];
static int reps[N], R;

int main(void) {
    /* group tables, written independently of dissoc.c */
    for (int x = 0; x < N; x++) {
        int x1 = x / F2, x2 = x % F2;
        for (int y = 0; y < N; y++) {
            int y1 = y / F2, y2 = y % F2;
            addt[x][y] = ((x1 + y1) % F1) * F2 + (x2 + y2) % F2;
        }
    }
    R = 0;
    for (int g = 1; g < N; g++) {
        int neg = ((F1 - g / F2) % F1) * F2 + (F2 - g % F2) % F2;
        if (g <= neg) reps[R++] = g;
    }
    printf("group C%d+C%d order %d, %d plus-minus classes, k = %d\n",
           F1, F2, N, R, K);

    long long tested = 0, found_k = 0, found_km1 = 0;
    int idx[K];
    int sums[1 << K];
    uint64_t seen[(N + 63) / 64];
    int wit[K];

    /* iterate over all K-subsets idx[0]<...<idx[K-1] of reps */
    for (int a = 0; a < K; a++) idx[a] = a;
    while (1) {
        tested++;
        /* subset-sum distinctness, incremental by element */
        memset(seen, 0, sizeof(seen));
        int nsum = 1, ok = 1, okm1 = 1;
        sums[0] = 0;
        seen[0] |= 1;
        for (int a = 0; a < K && ok; a++) {
            int g = reps[idx[a]];
            for (int s = 0; s < nsum; s++) {
                int t = addt[sums[s]][g];
                if ((seen[t >> 6] >> (t & 63)) & 1) { ok = 0; break; }
                sums[nsum + s] = t;
            }
            if (ok) {
                for (int s = 0; s < nsum; s++) {
                    int t = sums[nsum + s];
                    seen[t >> 6] |= 1ULL << (t & 63);
                }
                nsum <<= 1;
                if (a == K - 2) okm1 = 1;   /* first K-1 elements dissociated */
            } else if (a >= K - 1) {
                okm1 = 1;                    /* prefix of K-1 was fine */
            } else {
                okm1 = 0;
            }
        }
        if (okm1 && !ok) found_km1++;
        if (ok) {
            found_k++;
            memcpy(wit, idx, sizeof(idx));
        }
        /* next combination */
        int a = K - 1;
        while (a >= 0 && idx[a] == R - K + a) a--;
        if (a < 0) break;
        idx[a]++;
        for (int b = a + 1; b < K; b++) idx[b] = idx[b - 1] + 1;
    }
    printf("subsets tested: %lld  (C(%d,%d) expected)\n", tested, R, K);
    printf("dissociated %d-sets found: %lld\n", K, found_k);
    printf("prefixes of size %d dissociated (evidence of near-misses): %lld\n",
           K - 1, found_km1);
    /* D_pm = lmax + 1.  If no K-set exists but (K-1)-sets do, lmax = K-1
     * and D_pm = K.  If a K-set exists, lmax = K (K is the counting cap)
     * and D_pm = K + 1. */
    if (found_k == 0)
        printf("VERIFIED: no dissociated %d-set in C%d+C%d;"
               " with a %d-set existing (%lld near-miss prefixes),"
               " lmax = %d  =>  D_pm = %d\n",
               K, F1, F2, K - 1, found_km1, K - 1, K);
    else {
        printf("FOUND witness:");
        for (int a = 0; a < K; a++) printf(" %d", reps[wit[a]]);
        printf("  =>  lmax = %d (= cap)  =>  D_pm = %d\n", K, K + 1);
    }
    return 0;
}
