/* plain.c -- minimal second engine for Leech's covering tree problem, written independently of
   cover_search.c: only the weight-window recursion (next weight in [q_prev, mex]), the excess budget,
   singleton interchangeability, and (mode -d) immediate pruning of any repeated path sum.
   No block bounds, no parity, no canonical forms.  Usage: ./plain n k [-d] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 14
static int n, k, N, B, distinct;
static int comp[MAXN];              /* component label of each vertex */
static int dist[MAXN][MAXN];
static int cnt[600];                 /* multiplicity of each realized distance (all values) */
static int covered;                  /* number of distinct values in 1..k realized */
static long long nodes;
static int eu[MAXN], ev[MAXN], ew[MAXN], ne;
static int found;
static void rec(int x, int qprev) {
    nodes++;
    if (covered == k) { found = 1; printf("WITNESS n=%d k=%d edges:", n, k); for (int i = 0; i < ne; i++) printf(" (%d,%d,%d)", eu[i], ev[i], ew[i]); printf(" (rest free)\n"); return; }
    int m = 1; while (m <= k && cnt[m]) m++;      /* mex */
    if (m < qprev) return;
    /* components */
    int first_single = -1, second_single = -1;
    for (int v = 0; v < n; v++) { int single = 1; for (int u = 0; u < n; u++) if (u != v && comp[u] == comp[v]) single = 0; if (single) { if (first_single < 0) first_single = v; else if (second_single < 0) second_single = v; } }
    for (int q = qprev; q <= m && !found; q++)
    for (int u = 0; u < n && !found; u++) for (int v = 0; v < n && !found; v++) {
        if (comp[u] == comp[v]) continue;
        if (u > v && comp[u] != comp[v]) { /* unordered component pair: require comp[u] < comp[v] */ }
        if (comp[u] > comp[v]) continue;
        /* singleton canonicalization */
        int us = 1, vs = 1;
        for (int t = 0; t < n; t++) { if (t != u && comp[t] == comp[u]) us = 0; if (t != v && comp[t] == comp[v]) vs = 0; }
        if (us && vs) { if (!(u == first_single && v == second_single)) continue; }
        else if (us) { if (u != first_single) continue; }
        else if (vs) { if (v != first_single) continue; }
        /* cross distances */
        int ex = 0, bad = 0, added[MAXN*MAXN], na = 0;
        for (int a = 0; a < n && !bad; a++) if (comp[a] == comp[u]) for (int b = 0; b < n; b++) if (comp[b] == comp[v]) {
            int d = dist[a][u] + q + dist[v][b];
            if (d >= 600) { bad = 1; break; }
            if (cnt[d]) { if (distinct) { bad = 1; break; } ex++; }
            else if (d > k) ex++;
            cnt[d]++; added[na++] = d;
            if (d <= k && cnt[d] == 1) covered++;
        }
        if (!bad && x + ex <= B) {
            int cu = comp[u], cv = comp[v];
            int savecomp[MAXN]; memcpy(savecomp, comp, sizeof(comp));
            for (int a = 0; a < n; a++) if (savecomp[a] == cu) for (int b = 0; b < n; b++) if (savecomp[b] == cv) { int d = dist[a][u] + q + dist[v][b]; dist[a][b] = dist[b][a] = d; }
            for (int t = 0; t < n; t++) if (comp[t] == cv) comp[t] = cu;
            eu[ne] = u; ev[ne] = v; ew[ne] = q; ne++;
            rec(x + ex, q);
            ne--;
            memcpy(comp, savecomp, sizeof(comp));
            for (int a = 0; a < n; a++) if (comp[a] == cu) for (int b = 0; b < n; b++) if (comp[b] == cv) dist[a][b] = dist[b][a] = -1;
        }
        for (int i = 0; i < na; i++) { int d = added[i]; if (d <= k && cnt[d] == 1) covered--; cnt[d]--; }
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); k = atoi(argv[2]); distinct = (argc > 3 && !strcmp(argv[3], "-d"));
    N = n * (n - 1) / 2; B = N - k;
    for (int i = 0; i < n; i++) { comp[i] = i; for (int j = 0; j < n; j++) dist[i][j] = (i == j) ? 0 : -1; }
    rec(0, 1);
    printf("PLAIN %sn=%d k=%d found=%d nodes=%lld\n", distinct ? "distinct " : "", n, k, found, nodes);
    return 0;
}
