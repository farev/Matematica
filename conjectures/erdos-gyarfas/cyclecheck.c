/* cyclecheck.c — exact power-of-2 cycle detection for graphs in graph6 format.
 *
 * For each input graph (stdin, one graph6 per line, n <= 128) decides, by
 * exhaustive DFS, for each L in {4, 8, 16, 32, 64, 128} with L <= n whether
 * the graph contains a cycle of length exactly L.  Integer/bitset arithmetic
 * only; no floating point anywhere.
 *
 * Cycle enumeration: a cycle is counted at its minimum vertex v; DFS explores
 * paths from v through vertices > v only, closing back to v at depth L-1.
 * Pruning: BFS distances to v (within the induced subgraph on {v} u {u > v})
 * prune any path that cannot return to v in the remaining steps.
 *
 * Usage:
 *   cyclecheck            print graphs containing NO cycle of any length
 *                         2^k (4 <= 2^k <= n)  [counterexample filter]
 *   cyclecheck -a 4,8     print graphs with no C4 and no C8 (ignore others)
 *   cyclecheck -p         print "graph6 TAB lengths-present" for every graph
 *   cyclecheck -q         no per-graph output, just the stderr summary
 *
 * stderr summary: graphs read, graphs printed, and for each L how many
 * graphs lacked a C_L.
 *
 * Build: gcc -O3 -march=native -o cyclecheck cyclecheck.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 128
#define NLENS 6
static const int LENS[NLENS] = {4, 8, 16, 32, 64, 128};

typedef struct { uint64_t w[2]; } bset;

static inline void bset_zero(bset *b) { b->w[0] = 0; b->w[1] = 0; }
static inline void bset_set(bset *b, int i) { b->w[i >> 6] |= 1ULL << (i & 63); }
static inline void bset_clear(bset *b, int i) { b->w[i >> 6] &= ~(1ULL << (i & 63)); }
static inline int bset_test(const bset *b, int i) { return (b->w[i >> 6] >> (i & 63)) & 1; }

static int n;                       /* current graph order */
static bset adj[MAXN];              /* adjacency bitsets */
static int deg[MAXN], nbr[MAXN][MAXN];

/* ---------- graph6 ---------- */
static int parse_graph6(const char *s, char *err) {
    int idx = 0;
    if (s[0] == '~') {
        if (s[1] == '~') { sprintf(err, "order too large"); return -1; }
        n = ((s[1] - 63) << 12) | ((s[2] - 63) << 6) | (s[3] - 63);
        idx = 4;
    } else {
        n = s[0] - 63;
        idx = 1;
    }
    if (n < 1 || n > MAXN) { sprintf(err, "order %d out of range", n); return -1; }
    for (int i = 0; i < n; i++) bset_zero(&adj[i]);
    int bit = 0, val = 0, have = 0;
    for (int j = 1; j < n; j++)
        for (int i = 0; i < j; i++) {
            if (!have) {
                int c = s[idx++];
                if (c < 63 || c > 126) { sprintf(err, "bad char"); return -1; }
                val = c - 63; have = 6; bit = 5;
            }
            if ((val >> bit) & 1) { bset_set(&adj[i], j); bset_set(&adj[j], i); }
            bit--; have--;
        }
    for (int i = 0; i < n; i++) {
        deg[i] = 0;
        for (int j = 0; j < n; j++)
            if (bset_test(&adj[i], j)) nbr[i][deg[i]++] = j;
    }
    return 0;
}

/* ---------- cycle of length exactly L through minimum vertex v ---------- */
static int L_target, v_min;
static int dist_v[MAXN];
static bset used;

/* BFS distances to v within {v} u {u > v} */
static void bfs_from_v(void) {
    static int queue[MAXN];
    for (int i = 0; i < n; i++) dist_v[i] = MAXN + 1;
    int head = 0, tail = 0;
    dist_v[v_min] = 0; queue[tail++] = v_min;
    while (head < tail) {
        int u = queue[head++];
        for (int k = 0; k < deg[u]; k++) {
            int w = nbr[u][k];
            if (w >= v_min && dist_v[w] > dist_v[u] + 1) {
                dist_v[w] = dist_v[u] + 1;
                queue[tail++] = w;
            }
        }
    }
}

/* depth d = number of edges walked so far; u = current vertex */
static int dfs(int u, int d) {
    if (d == L_target - 1)
        return bset_test(&adj[u], v_min);
    int rem = L_target - d - 1;   /* steps remaining after moving to w */
    for (int k = 0; k < deg[u]; k++) {
        int w = nbr[u][k];
        if (w <= v_min || bset_test(&used, w)) continue;
        if (dist_v[w] > rem) continue;
        bset_set(&used, w);
        if (dfs(w, d + 1)) { bset_clear(&used, w); return 1; }
        bset_clear(&used, w);
    }
    return 0;
}

static int has_cycle_len(int L) {
    L_target = L;
    for (v_min = 0; v_min + L <= n + 0 && v_min < n; v_min++) {
        /* need at least L vertices >= v_min, i.e. n - v_min >= L */
        if (n - v_min < L) break;
        bfs_from_v();
        bset_zero(&used);
        bset_set(&used, v_min);
        /* start: walk to first neighbour w > v_min; enforce w's identity as
         * path[1]; direction symmetry is not broken (factor 2 cost, fine). */
        if (dfs(v_min, 0)) return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    int mode_print_all = 0, mode_quiet = 0;
    int avoid_explicit = 0;
    int avoid[NLENS] = {0};
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-p")) mode_print_all = 1;
        else if (!strcmp(argv[i], "-q")) mode_quiet = 1;
        else if (!strcmp(argv[i], "-a") && i + 1 < argc) {
            avoid_explicit = 1;
            char *tok = strtok(argv[++i], ",");
            while (tok) {
                int L = atoi(tok), ok = 0;
                for (int k = 0; k < NLENS; k++) if (LENS[k] == L) { avoid[k] = 1; ok = 1; }
                if (!ok) { fprintf(stderr, "bad length %s\n", tok); return 2; }
                tok = strtok(NULL, ",");
            }
        } else { fprintf(stderr, "unknown arg %s\n", argv[i]); return 2; }
    }

    char line[8192], err[64];
    long long nread = 0, nprint = 0;
    long long lack[NLENS] = {0};
    while (fgets(line, sizeof line, stdin)) {
        size_t len = strlen(line);
        while (len && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = 0;
        if (!len) continue;
        if (parse_graph6(line, err)) { fprintf(stderr, "parse error (%s): %s\n", err, line); return 3; }
        nread++;
        int present[NLENS];
        for (int k = 0; k < NLENS; k++)
            present[k] = (LENS[k] <= n) ? has_cycle_len(LENS[k]) : 0;
        for (int k = 0; k < NLENS; k++)
            if (LENS[k] <= n && !present[k]) lack[k]++;
        if (mode_print_all) {
            printf("%s\t", line);
            int first = 1;
            for (int k = 0; k < NLENS; k++)
                if (present[k]) { printf(first ? "%d" : ",%d", LENS[k]); first = 0; }
            if (first) printf("-");
            printf("\n");
        } else if (!mode_quiet) {
            int print = 1;
            if (avoid_explicit) {
                for (int k = 0; k < NLENS; k++)
                    if (avoid[k] && LENS[k] <= n && present[k]) { print = 0; break; }
            } else {
                for (int k = 0; k < NLENS; k++)
                    if (LENS[k] <= n && present[k]) { print = 0; break; }
            }
            if (print) { printf("%s\n", line); nprint++; }
        }
        if ((nread & 0xFFFFF) == 0)
            fprintf(stderr, "[progress] %lld graphs\n", nread);
    }
    fprintf(stderr, "read %lld printed %lld", nread, nprint);
    for (int k = 0; k < NLENS; k++)
        fprintf(stderr, " lackC%d %lld", LENS[k], lack[k]);
    fprintf(stderr, "\n");
    return 0;
}
