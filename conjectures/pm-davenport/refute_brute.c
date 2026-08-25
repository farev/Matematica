/* Engine C: fully independent brute-force refutation check.
 *
 * Claim being checked: the group G = Z_{n1} + ... + Z_{nr} has NO
 * dissociated (= plus-minus zero-sum-free) subset of size t.
 *
 * Method, deliberately dumb: enumerate ALL t-element subsets of the class
 * representatives {g,-g} (g != 0) and, for each, enumerate ALL 3^t - 1
 * nonzero coefficient vectors in {-1,0,+1}^t directly, testing whether any
 * signed sum is 0.  No incremental signed-sum sets, no pruning shared with
 * engines A/B; the only shared mathematics is the reduction to one
 * representative per class (Lemma 1 in NOTE.md: dissociated sets have
 * distinct elements, no inverse pairs, and dissociativity is invariant
 * under replacing an element by its inverse).
 *
 * Output: number of subsets tested, number found dissociated (must be 0
 * for the refutation to hold), and any dissociated subsets found.
 *
 * Usage: ./refute_brute t n1 [n2 ...]
 */
#include <stdio.h>
#include <stdlib.h>

static int R; static long ord[8], rad[8], N;

static long g_neg(long a) {
    long s = 0;
    for (int i = 0; i < R; i++) {
        long x = (a / rad[i]) % ord[i];
        s += ((ord[i] - x) % ord[i]) * rad[i];
    }
    return s;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s t n1 [n2 ...]\n", argv[0]); return 2; }
    int t = atoi(argv[1]);
    R = argc - 2; N = 1;
    for (int i = 0; i < R; i++) { ord[i] = atol(argv[2 + i]); N *= ord[i]; }
    { long m = N; for (int i = 0; i < R; i++) { m /= ord[i]; rad[i] = m; } }

    /* class representatives, own construction */
    long *reps = malloc((size_t)N * sizeof(long));
    char *seen = calloc((size_t)N, 1);
    int M = 0;
    for (long g = 1; g < N; g++) {
        if (!seen[g]) { seen[g] = 1; seen[g_neg(g)] = 1; reps[M++] = g; }
    }

    /* decode reps into coordinate arrays for the direct modular check */
    long (*co)[8] = malloc((size_t)M * sizeof(*co));
    for (int i = 0; i < M; i++)
        for (int j = 0; j < R; j++) co[i][j] = (reps[i] / rad[j]) % ord[j];

    int idx[64];
    for (int i = 0; i < t; i++) idx[i] = i;
    unsigned long long tested = 0, found = 0;

    while (1) {
        tested++;
        /* direct check: all 3^t - 1 nonzero eps vectors */
        long npow = 1; for (int i = 0; i < t; i++) npow *= 3;
        int ok = 1;
        for (long code = 1; code < npow && ok; code++) {
            long c = code; long s[8] = {0};
            int nonzero_seen = 0;
            for (int i = 0; i < t; i++) {
                int e = (int)(c % 3); c /= 3;         /* 0, 1, 2 -> eps 0, +1, -1 */
                if (e == 0) continue;
                nonzero_seen = 1;
                long sign = (e == 1) ? 1 : -1;
                for (int j = 0; j < R; j++) {
                    s[j] = (s[j] + sign * co[idx[i]][j]) % ord[j];
                    if (s[j] < 0) s[j] += ord[j];
                }
            }
            if (!nonzero_seen) continue;
            int allz = 1;
            for (int j = 0; j < R; j++) if (s[j]) { allz = 0; break; }
            if (allz) ok = 0;                          /* relation found */
        }
        if (ok) {
            found++;
            printf("DISSOCIATED SUBSET FOUND:");
            for (int i = 0; i < t; i++) {
                printf(" (");
                for (int j = 0; j < R; j++) printf("%ld%s", co[idx[i]][j], j+1<R?",":"");
                printf(")");
            }
            printf("\n");
        }
        /* next combination */
        int i = t - 1;
        while (i >= 0 && idx[i] == M - t + i) i--;
        if (i < 0) break;
        idx[i]++;
        for (int j = i + 1; j < t; j++) idx[j] = idx[j - 1] + 1;
    }

    printf("G =");
    for (int i = 0; i < R; i++) printf(" Z_%ld", ord[i]);
    printf("  |G| = %ld  M = %d  t = %d\n", N, M, t);
    printf("subsets tested = %llu  dissociated found = %llu  => %s\n",
           tested, found,
           found ? "REFUTATION FAILS" : "REFUTATION CONFIRMED: no dissociated subset of this size");
    return found ? 1 : 0;
}
