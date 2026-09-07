/*
 * goodperm.c — exhaustive search for "good" permutations (MO 514690, Weiss 2026).
 *
 * A permutation a_1..a_n of {1..n} is GOOD if every proper consecutive block
 * of length L >= 2 (L < n) has non-integer average, i.e. its sum is not
 * divisible by L.
 *
 * Usage: goodperm n [mode] [maxreport]
 *   mode 0 (default): plain backtracking, no structural pruning; valid for every n.
 *   mode 1: additionally enforces the residue structure that every good
 *           permutation must satisfy when n = 2^m - 1 (NOTE.md, Lemma 2):
 *           for each k < m the map (t mod 2^k) -> (a_t mod 2^k) is a bijection
 *           with 0 -> 0.  Only meaningful for n = 2^m - 1; refused otherwise.
 *   maxreport: how many good permutations to print (default 10).
 *
 * Output: every good permutation found (up to maxreport) as one line, then a
 * summary line "n=.. mode=.. count=.. nodes=.. time=..s".
 *
 * The block test is incremental: when a_t is placed, all blocks ending at t
 * are tested with prefix sums, O(t) per node.  Values are exact integers
 * (64-bit); no floating point anywhere.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXN 1023

static int n, mode, maxreport;
static int a[MAXN + 2];
static long long pre[MAXN + 2];
static unsigned char used[MAXN + 2];
static long long count_good = 0, nodes = 0;
static int m_bits;                 /* n = 2^m - 1 => m_bits = m */
/* residue structure: res[k][r] = assigned residue (mod 2^k) for positions t ≡ r (mod 2^k), or -1 */
static int res[12][1024];
static unsigned char resused[12][1024];

static void report(void) {
    if (count_good <= maxreport) {
        for (int i = 1; i <= n; i++) printf("%d%c", a[i], i == n ? '\n' : ' ');
        fflush(stdout);
    }
}

static void rec(int t) {
    if (t > n) { count_good++; report(); return; }
    for (int v = 1; v <= n; v++) {
        if (used[v]) continue;
        if (mode == 1) {
            int ok = 1;
            for (int k = 1; k < m_bits; k++) {
                int mask = (1 << k) - 1;
                int r = t & mask, vr = v & mask;
                if (res[k][r] >= 0) { if (res[k][r] != vr) { ok = 0; break; } }
                else if (resused[k][vr]) { ok = 0; break; }
            }
            if (!ok) continue;
        }
        nodes++;
        pre[t] = pre[t - 1] + v;
        int ok = 1;
        /* blocks ending at t of length L = 2..t, excluding the whole permutation */
        int Lmax = (t == n) ? n - 1 : t;
        for (int L = 2; L <= Lmax; L++) {
            if ((pre[t] - pre[t - L]) % L == 0) { ok = 0; break; }
        }
        if (!ok) continue;
        used[v] = 1; a[t] = v;
        int setk[12]; int nset = 0;
        if (mode == 1) {
            for (int k = 1; k < m_bits; k++) {
                int mask = (1 << k) - 1;
                int r = t & mask, vr = v & mask;
                if (res[k][r] < 0) { res[k][r] = vr; resused[k][vr] = 1; setk[nset++] = k; }
            }
        }
        rec(t + 1);
        for (int i = 0; i < nset; i++) {
            int k = setk[i]; int mask = (1 << k) - 1;
            int r = t & mask, vr = v & mask;
            res[k][r] = -1; resused[k][vr] = 0;
        }
        used[v] = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: goodperm n [mode] [maxreport]\n"); return 2; }
    n = atoi(argv[1]);
    mode = argc > 2 ? atoi(argv[2]) : 0;
    maxreport = argc > 3 ? atoi(argv[3]) : 10;
    if (n < 1 || n > MAXN) { fprintf(stderr, "n out of range\n"); return 2; }
    m_bits = 0;
    if (mode == 1) {
        int q = n + 1;
        while ((q & 1) == 0) { q >>= 1; m_bits++; }
        if (q != 1) { fprintf(stderr, "mode 1 requires n = 2^m - 1\n"); return 2; }
        for (int k = 0; k < 12; k++) for (int r = 0; r < 1024; r++) { res[k][r] = -1; resused[k][r] = 0; }
        /* 0 -> 0 for every level k (positions divisible by 2^k carry multiples of 2^k) */
        for (int k = 1; k < m_bits; k++) { res[k][0] = 0; resused[k][0] = 1; }
    }
    clock_t c0 = clock();
    pre[0] = 0;
    rec(1);
    double secs = (double)(clock() - c0) / CLOCKS_PER_SEC;
    printf("n=%d mode=%d count=%lld nodes=%lld time=%.2fs\n", n, mode, count_good, nodes, secs);
    return 0;
}
