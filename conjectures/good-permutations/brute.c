/* brute.c — plain backtracking search for "good" permutations (MO 514690).
 * No structural lemma is assumed: positions are filled left to right with any
 * unused value, and every proper block ending at the current position is
 * checked (sum not divisible by length).  Counts all good permutations.
 *
 * Build: gcc -O2 -o brute brute.c
 * Usage: ./brute n [maxprint]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

static int n, maxprint = 5;
static int a[64];
static long P[65];
static uint64_t used;
static unsigned long long nodes = 0, solutions = 0;

static void rec(int t) {                /* place a[t], t = 1..n */
    if (t > n) {
        solutions++;
        if (solutions <= (unsigned long long)maxprint) {
            printf("SOL:");
            for (int i = 1; i <= n; i++) printf(" %d", a[i]);
            printf("\n");
        }
        return;
    }
    for (int v = 1; v <= n; v++) {
        if (used & (1ULL << v)) continue;
        nodes++;
        P[t] = P[t - 1] + v;
        int ok = 1;
        /* blocks ending at t of length L = 2..t, excluding the whole permutation */
        int Lmax = (t == n) ? n - 1 : t;
        for (int L = 2; L <= Lmax; L++) {
            if ((P[t] - P[t - L]) % L == 0) { ok = 0; break; }
        }
        if (!ok) continue;
        a[t] = v;
        used |= (1ULL << v);
        rec(t + 1);
        used &= ~(1ULL << v);
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s n [maxprint]\n", argv[0]); return 1; }
    n = atoi(argv[1]);
    if (argc > 2) maxprint = atoi(argv[2]);
    if (n < 2 || n > 62) { fprintf(stderr, "n out of range\n"); return 1; }
    clock_t c0 = clock();
    P[0] = 0;
    rec(1);
    double secs = (double)(clock() - c0) / CLOCKS_PER_SEC;
    printf("n=%d good_permutations=%llu nodes=%llu time=%.3fs\n", n, solutions, nodes, secs);
    return 0;
}
