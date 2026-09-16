/* repcheck.c — find repetitively coloured paths in a coloured graph.
 *
 * stdin:  V C kmax cap
 *         then V lines: deg nb1 nb2 ... (0-based vertex ids)
 *         then V ints: colour of each vertex
 * stdout: one line per repetitive path v1 ... v2k (k <= kmax), canonical
 *         orientation (v1 < v2k), at most `cap` lines.
 *
 * Method (Toole 2013, as described in Tao–Zhang–Zhang–Toole 2025): for each
 * ordered pair (u,v) of distinct equally coloured vertices grow two disjoint
 * paths P1 = u..., P2 = v... in parallel with identical colour sequences,
 * extending both at their ends; whenever end(P1) is adjacent to start(P2),
 * P1 followed by P2 is a repetitively coloured path.  Every repetitive path
 * v1..v2k is found from the pair (v1, v_{k+1}), so the enumeration is
 * complete for k <= kmax.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int V, C, kmax, cap, emitted = 0;
static int *deg, **nb, *col;
static unsigned char *adj;   /* V*V adjacency matrix */
static int *P1, *P2;
static unsigned char *used;

static void emit(int k) {
    if (P1[0] > P2[k-1]) return;          /* canonical orientation */
    if (emitted >= cap) return;
    for (int i = 0; i < k; i++) printf("%d ", P1[i]);
    for (int i = 0; i < k; i++) printf("%d%c", P2[i], i == k-1 ? '\n' : ' ');
    emitted++;
}

static void rec(int k) {
    /* P1[0..k-1], P2[0..k-1] filled, all distinct, same colour sequence */
    if (adj[P1[k-1] * V + P2[0]]) emit(k);
    if (k == kmax || emitted >= cap) return;
    int a = P1[k-1], b = P2[k-1];
    for (int i = 0; i < deg[a]; i++) {
        int x = nb[a][i];
        if (used[x]) continue;
        for (int j = 0; j < deg[b]; j++) {
            int y = nb[b][j];
            if (y == x || used[y] || col[y] != col[x]) continue;
            used[x] = used[y] = 1;
            P1[k] = x; P2[k] = y;
            rec(k + 1);
            used[x] = used[y] = 0;
            if (emitted >= cap) return;
        }
    }
}

int main(void) {
    if (scanf("%d %d %d %d", &V, &C, &kmax, &cap) != 4) return 1;
    deg = malloc(V * sizeof(int)); nb = malloc(V * sizeof(int*));
    col = malloc(V * sizeof(int)); adj = calloc((size_t)V * V, 1);
    for (int v = 0; v < V; v++) {
        if (scanf("%d", &deg[v]) != 1) return 1;
        nb[v] = malloc(deg[v] * sizeof(int));
        for (int i = 0; i < deg[v]; i++) { if (scanf("%d", &nb[v][i]) != 1) return 1; adj[v * V + nb[v][i]] = 1; }
    }
    for (int v = 0; v < V; v++) if (scanf("%d", &col[v]) != 1) return 1;
    P1 = malloc(kmax * sizeof(int)); P2 = malloc(kmax * sizeof(int));
    used = calloc(V, 1);
    for (int u = 0; u < V && emitted < cap; u++)
        for (int v = 0; v < V && emitted < cap; v++) {
            if (u == v || col[u] != col[v]) continue;
            P1[0] = u; P2[0] = v; used[u] = used[v] = 1;
            rec(1);
            used[u] = used[v] = 0;
        }
    return 0;
}
