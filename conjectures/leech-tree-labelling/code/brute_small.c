/* brute.c -- exhaustive brute force over all tree shapes and all weight vectors for small n.
   Independent of cover_search.c: no lemmas except the edge-weight bound w <= k+1+B-(n-1)
   (every edge lies on >= n-1 paths of weight >= w; at most k-w+1+B pairs have distance >= w).
   Mode 0: values 1..k covered (repeats allowed).  Mode 1: additionally all C(n,2) sums distinct.
   Prints max k for each n and mode. */
#include <stdio.h>
#include <string.h>
#include "shapes.h"
static int n, k, B, mode, wmax;
static int E[6][2], w[6];
static int best;
static int adjv[8][8];
static int covers(void) {
    int seen[512]; memset(seen, 0, sizeof(seen));
    int dist[8][8];
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) dist[i][j] = -1;
    for (int i = 0; i < n; i++) { dist[i][i] = 0; int st[8], sp = 0; st[sp++] = i;
        while (sp) { int v = st[--sp]; for (int u = 0; u < n; u++) if (adjv[v][u] && dist[i][u] < 0) { dist[i][u] = dist[i][v] + adjv[v][u]; st[sp++] = u; } } }
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
        int d = dist[i][j]; if (d >= 512) d = 511;
        if (mode == 1 && seen[d]) return 0;
        seen[d] = 1;
    }
    for (int v = 1; v <= k; v++) if (!seen[v]) return 0;
    return 1;
}
static int rec(int e) {
    if (e == n - 1) return covers();
    for (int x = 1; x <= wmax; x++) { w[e] = x; adjv[E[e][0]][E[e][1]] = adjv[E[e][1]][E[e][0]] = x; if (rec(e + 1)) return 1; }
    adjv[E[e][0]][E[e][1]] = adjv[E[e][1]][E[e][0]] = 0;
    return 0;
}
int main(void) {
    for (mode = 0; mode <= 1; mode++) {
        printf("mode %d (%s):", mode, mode ? "distinct" : "repeats allowed");
        for (n = 2; n <= 7; n++) {
            int N = n * (n - 1) / 2; int found = 0;
            for (k = N; k >= 1 && !found; k--) {
                B = N - k; wmax = k + 1 + B - (n - 1); if (wmax < 1) wmax = 1;
                for (int s = 0; s < NSHAPES[n] && !found; s++) {
                    memset(adjv, 0, sizeof(adjv));
                    for (int e = 0; e < n - 1; e++) { E[e][0] = SHAPES[n][s][e][0]; E[e][1] = SHAPES[n][s][e][1]; }
                    if (rec(0)) found = 1;
                }
                if (found) printf(" a(%d)=%d", n, k);
            }
            fflush(stdout);
        }
        printf("\n");
    }
    return 0;
}
