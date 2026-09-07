/* Exact enumeration of all simple cycles of length <= L in a graph.
 * Rooted DFS: for each root r, walk simple paths through vertices > r,
 * pruned by BFS distance to r inside the subgraph induced on {v >= r}.
 * Each cycle is reported exactly once (root = its minimum vertex, and
 * direction fixed by path[1] < last vertex).
 *
 * usage: cycles graphfile L Lout outfile
 *   graphfile: first line n; then n lines "deg v1 v2 ..."
 *   prints counts by length 3..L to stdout; writes cycles of length >= Lout
 *   to outfile as lines "len v0 v1 ... v_{len-1}".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXDEG 8
static int n, L, Lout;
static int *deg, (*adj)[MAXDEG];
static int *dist, *onpath, *path, *queue;
static long long counts[64];
static FILE *out;
static int root;

static void dfs(int x, int depth) {
    for (int k = 0; k < deg[x]; k++) {
        int y = adj[x][k];
        if (y == root) {
            if (depth + 1 >= 3 && path[1] < x) {
                int len = depth + 1;
                counts[len]++;
                if (len >= Lout) {
                    fprintf(out, "%d", len);
                    for (int i = 0; i < len; i++) fprintf(out, " %d", path[i]);
                    fputc('\n', out);
                }
            }
        } else if (y > root && !onpath[y] && depth + 1 + dist[y] <= L) {
            onpath[y] = 1;
            path[depth + 1] = y;
            dfs(y, depth + 1);
            onpath[y] = 0;
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: cycles graphfile L Lout outfile\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("graphfile"); return 1; }
    L = atoi(argv[2]); Lout = atoi(argv[3]);
    out = fopen(argv[4], "w");
    if (!out) { perror("outfile"); return 1; }
    if (fscanf(f, "%d", &n) != 1) return 1;
    deg = calloc(n, sizeof(int));
    adj = calloc(n, sizeof(*adj));
    for (int i = 0; i < n; i++) {
        if (fscanf(f, "%d", &deg[i]) != 1) return 1;
        if (deg[i] > MAXDEG) { fprintf(stderr, "degree too large\n"); return 1; }
        for (int k = 0; k < deg[i]; k++) if (fscanf(f, "%d", &adj[i][k]) != 1) return 1;
    }
    fclose(f);
    dist = malloc(n * sizeof(int)); onpath = calloc(n, sizeof(int));
    path = malloc((L + 2) * sizeof(int)); queue = malloc(n * sizeof(int));
    memset(counts, 0, sizeof(counts));
    for (root = 0; root < n; root++) {
        /* BFS from root inside vertices >= root */
        for (int i = 0; i < n; i++) dist[i] = 1 << 28;
        int qh = 0, qt = 0;
        dist[root] = 0; queue[qt++] = root;
        while (qh < qt) {
            int x = queue[qh++];
            if (dist[x] >= L) break;
            for (int k = 0; k < deg[x]; k++) {
                int y = adj[x][k];
                if (y >= root && dist[y] > dist[x] + 1) { dist[y] = dist[x] + 1; queue[qt++] = y; }
            }
        }
        path[0] = root; onpath[root] = 1;
        dfs(root, 0);
        onpath[root] = 0;
    }
    fclose(out);
    for (int l = 3; l <= L; l++) printf("len %d: %lld\n", l, counts[l]);
    return 0;
}
