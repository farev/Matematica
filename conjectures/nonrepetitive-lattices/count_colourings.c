/* count_colourings.c — replicate the vertex-by-vertex counting algorithm of
 * Tao–Zhang–Zhang–Toole (arXiv:2510.11263, Section 2): n(i) = number of
 * nonrepetitive c-colourings of the induced subgraph on the first i vertices
 * of a given vertex order, counted up to colour permutation (colours are
 * introduced in order of first use).
 *
 * stdin: n c
 *        n lines: deg nb1 nb2 ... (0-based indices into the vertex order,
 *                 adjacency of the whole n-vertex graph)
 * stdout: i n(i) for i = 1..n (n(i)=0 lines stop the enumeration early).
 *
 * The repetition test when vertex i receives a colour: any repetitive path
 * must contain vertex i (the earlier subgraph is nonrepetitive), so for each
 * earlier vertex u of the same colour grow two disjoint equally coloured
 * paths P1 (from u) and P2 (from i) inside {v_0..v_i}, first prepending pairs
 * then appending pairs, and report a repetition when last(P1)~first(P2) or
 * last(P2)~first(P1).  Every repetitive path w_1..w_2k through v_i arises
 * this way from the pair (w_j, w_{j+k}) containing v_i.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 128
static int n, C, deg[MAXN], nb[MAXN][MAXN], col[MAXN];
static unsigned char adj[MAXN][MAXN], used[MAXN];
static long long cnt[MAXN + 1];
static int limit;            /* vertices allowed: indices < limit */
static int d1[2 * MAXN], d2[2 * MAXN];   /* deques */
static int f1, b1, f2, b2;   /* front/back indices: elements d[f..b-1] */

static int found;

static void search(int phase) {
    if (found) return;
    /* repetition tests */
    if (adj[d1[b1 - 1]][d2[f2]] || adj[d2[b2 - 1]][d1[f1]]) { found = 1; return; }
    if (phase == 0) {
        /* prepend a pair (x before d1[f1], y before d2[f2]) */
        int a = d1[f1], b = d2[f2];
        for (int i = 0; i < deg[a]; i++) {
            int x = nb[a][i]; if (x >= limit || used[x]) continue;
            for (int j = 0; j < deg[b]; j++) {
                int y = nb[b][j]; if (y >= limit || y == x || used[y] || col[y] != col[x]) continue;
                used[x] = used[y] = 1; d1[--f1] = x; d2[--f2] = y;
                search(0);
                f1++; f2++; used[x] = used[y] = 0;
                if (found) return;
            }
        }
    }
    /* append a pair (phase 1; also allowed from phase 0 = switch to phase 1) */
    {
        int a = d1[b1 - 1], b = d2[b2 - 1];
        for (int i = 0; i < deg[a]; i++) {
            int x = nb[a][i]; if (x >= limit || used[x]) continue;
            for (int j = 0; j < deg[b]; j++) {
                int y = nb[b][j]; if (y >= limit || y == x || used[y] || col[y] != col[x]) continue;
                used[x] = used[y] = 1; d1[b1++] = x; d2[b2++] = y;
                search(1);
                b1--; b2--; used[x] = used[y] = 0;
                if (found) return;
            }
        }
    }
}

static int ok(int v) {
    limit = v + 1;
    for (int u = 0; u < v; u++) {
        if (col[u] != col[v]) continue;
        memset(used, 0, sizeof used);
        f1 = MAXN; b1 = MAXN + 1; d1[MAXN] = u;
        f2 = MAXN; b2 = MAXN + 1; d2[MAXN] = v;
        used[u] = used[v] = 1;
        found = 0;
        search(0);
        if (found) return 0;
    }
    return 1;
}

static void dfs(int i, int maxc) {
    if (i == n) return;
    int top = maxc + 1 < C - 1 ? maxc + 1 : C - 1;
    for (int c = 0; c <= top; c++) {
        col[i] = c;
        if (ok(i)) {
            cnt[i + 1]++;
            dfs(i + 1, c > maxc ? c : maxc);
        }
    }
    col[i] = -1;
}

int main(void) {
    if (scanf("%d %d", &n, &C) != 2) return 1;
    for (int v = 0; v < n; v++) {
        if (scanf("%d", &deg[v]) != 1) return 1;
        for (int i = 0; i < deg[v]; i++) { if (scanf("%d", &nb[v][i]) != 1) return 1; adj[v][nb[v][i]] = 1; }
    }
    for (int v = 0; v < n; v++) col[v] = -1;
    dfs(0, -1);
    for (int i = 1; i <= n; i++) { printf("%d %lld\n", i, cnt[i]); if (cnt[i] == 0) break; }
    return 0;
}
