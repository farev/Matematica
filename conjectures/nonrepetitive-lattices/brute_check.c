/* brute_check.c — independent, from-the-definition nonrepetitiveness check.
 * Enumerates EVERY simple path of the graph by DFS and, whenever the path has
 * even length 2k, tests directly whether colour(v_i) == colour(v_{i+k}) for
 * all i.  No shared code or ideas with repcheck.c (which grows two paths in
 * parallel).  Exponential, intended for patches of <= ~30 vertices.
 * stdin: V
 *        V lines: deg nb1 ... (0-based)
 *        V ints: colours
 * stdout: number of simple paths enumerated, number of repetitions found,
 *         and the first repetition if any.  Exit 0 if nonrepetitive, 1 if not.
 */
#include <stdio.h>
#include <stdlib.h>
static int V, *deg, **nb, *col, path[64], len = 0;
static unsigned char *used;
static long long npaths = 0, nrep = 0;
static int first[64], firstlen = 0;

static void dfs(int v) {
    path[len++] = v; used[v] = 1; npaths++;
    if (len % 2 == 0) {
        int k = len / 2, rep = 1;
        for (int i = 0; i < k; i++) if (col[path[i]] != col[path[i + k]]) { rep = 0; break; }
        if (rep) { nrep++; if (!firstlen) { firstlen = len; for (int i = 0; i < len; i++) first[i] = path[i]; } }
    }
    for (int i = 0; i < deg[v]; i++) if (!used[nb[v][i]]) dfs(nb[v][i]);
    used[v] = 0; len--;
}

int main(void) {
    if (scanf("%d", &V) != 1) return 2;
    deg = malloc(V * sizeof(int)); nb = malloc(V * sizeof(int*)); col = malloc(V * sizeof(int));
    used = calloc(V, 1);
    for (int v = 0; v < V; v++) {
        if (scanf("%d", &deg[v]) != 1) return 2;
        nb[v] = malloc(deg[v] * sizeof(int));
        for (int i = 0; i < deg[v]; i++) if (scanf("%d", &nb[v][i]) != 1) return 2;
    }
    for (int v = 0; v < V; v++) if (scanf("%d", &col[v]) != 1) return 2;
    for (int s = 0; s < V; s++) dfs(s);
    printf("simple paths (directed, all lengths): %lld; repetitively coloured: %lld\n", npaths, nrep);
    if (nrep) { printf("first repetition:"); for (int i = 0; i < firstlen; i++) printf(" %d", first[i]); printf("\n"); return 1; }
    printf("NONREPETITIVE\n");
    return 0;
}
