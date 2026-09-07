/*
 * goodperm_subset.c — relaxation probe: enforce the Mersenne residue structure
 * (NOTE.md Lemma 2) and the block constraints ONLY for block lengths in a given
 * list.  Counts the permutations satisfying this relaxation (capped).
 *
 * Usage: goodperm_subset n L1,L2,... [cap]
 *   n must be 2^m - 1.  Block constraint for length L: no block of L
 *   consecutive terms (proper) has sum divisible by L.
 *   cap: stop after this many solutions (default 1000000).
 * Output: "n=.. lengths=.. count=.. (capped?) nodes=.. time=..s"
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXN 1023
static int n, m_bits, nL, Ls[MAXN];
static long long cap; static int maxprint=0;
static int a[MAXN + 2];
static long long pre[MAXN + 2];
static unsigned char used[MAXN + 2];
static long long cnt = 0, nodes = 0;
static int res[12][1024];
static unsigned char resused[12][1024];
static int capped = 0;

static void rec(int t) {
    if (capped) return;
    if (t > n) { cnt++; if (cnt <= maxprint) { for (int i=1;i<=n;i++) printf("%d%c", a[i], i==n?'\n':' '); } if (cnt >= cap) capped = 1; return; }
    for (int v = 1; v <= n && !capped; v++) {
        if (used[v]) continue;
        int ok = 1;
        for (int k = 1; k < m_bits; k++) {
            int mask = (1 << k) - 1;
            int r = t & mask, vr = v & mask;
            if (res[k][r] >= 0) { if (res[k][r] != vr) { ok = 0; break; } }
            else if (resused[k][vr]) { ok = 0; break; }
        }
        if (!ok) continue;
        nodes++;
        pre[t] = pre[t - 1] + v;
        for (int i = 0; i < nL; i++) {
            int L = Ls[i];
            if (L <= t && L < n && (pre[t] - pre[t - L]) % L == 0) { ok = 0; break; }
        }
        if (!ok) continue;
        used[v] = 1; a[t] = v;
        int setk[12]; int nset = 0;
        for (int k = 1; k < m_bits; k++) {
            int mask = (1 << k) - 1;
            int r = t & mask, vr = v & mask;
            if (res[k][r] < 0) { res[k][r] = vr; resused[k][vr] = 1; setk[nset++] = k; }
        }
        rec(t + 1);
        for (int i = 0; i < nset; i++) {
            int k = setk[i]; int mask = (1 << k) - 1;
            res[k][t & mask] = -1; resused[k][v & mask] = 0;
        }
        used[v] = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: goodperm_subset n L1,L2,... [cap]\n"); return 2; }
    n = atoi(argv[1]);
    cap = argc > 3 ? atoll(argv[3]) : 1000000; maxprint = argc > 4 ? atoi(argv[4]) : 0;
    int q = n + 1; m_bits = 0;
    while ((q & 1) == 0) { q >>= 1; m_bits++; }
    if (q != 1 || n > MAXN) { fprintf(stderr, "n must be 2^m-1 <= %d\n", MAXN); return 2; }
    char *s = argv[2]; nL = 0;
    while (*s) { Ls[nL++] = (int)strtol(s, &s, 10); if (*s == ',') s++; }
    for (int k = 0; k < 12; k++) for (int r = 0; r < 1024; r++) { res[k][r] = -1; resused[k][r] = 0; }
    for (int k = 1; k < m_bits; k++) { res[k][0] = 0; resused[k][0] = 1; }
    clock_t c0 = clock();
    pre[0] = 0; rec(1);
    printf("n=%d lengths=%s count=%lld%s nodes=%lld time=%.2fs\n", n, argv[2], cnt,
           capped ? " (capped)" : "", nodes, (double)(clock() - c0) / CLOCKS_PER_SEC);
    return 0;
}
