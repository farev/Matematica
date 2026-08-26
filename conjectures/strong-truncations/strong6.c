/* strong6.c — decide strong 6-edge-colorability of truncations T(H).
 *
 * Input (stdin), one graph per line, two modes:
 *   default: multig -T lines "nv ne  u v mult  u v mult ..." (0-based),
 *            each H a connected cubic loopless multigraph; the program
 *            builds the truncation T(H): each vertex u of H becomes a
 *            triangle {u.0,u.1,u.2}, slot s of u corresponds to the s-th
 *            incident edge instance of u (instances expanded in input
 *            order, u-slots assigned in input order), each edge instance
 *            e = (u,v) becomes the link edge (u.slot_u(e), v.slot_v(e)).
 *   -g6:     graph6 lines; the graph itself is used (no truncation).
 *
 * A strong edge coloring: proper + every color class an induced matching
 * (no two same-colored edges joined by an edge or sharing a vertex).
 * Conflict graph C: vertices = edges of G; X~Y iff X,Y share a vertex or
 * some endpoint of X is adjacent to some endpoint of Y.  Strong
 * k-colorability of G == proper k-colorability of C.
 *
 * Solver: exhaustive DSATUR-style backtracking over C with forward
 * checking.  Symmetry: a maximum-first greedy clique is located and its
 * first min(k, |clique|) vertices are pre-colored 0,1,2,... (valid since
 * clique colors are pairwise distinct and colors are interchangeable).
 * The search is complete: "NOT k-colorable" verdicts are exhaustive.
 *
 * Output per line:
 *   R <lineno> <nvT> <M> <verdict> <nodes> [c_0 .. c_{M-1}] | <input line>
 * verdict: "6" (witness follows, colors in canonical edge order:
 * triangle edges (u.0-u.1),(u.0-u.2),(u.1-u.2) for u = 0..n-1, then link
 * edges in instance order; -g6 mode: edges (i,j), i<j, lex order) or
 * "NOT6 chi=<k>" (exact strong chromatic index, no witness printed) or
 * "CAP" (node cap hit; undecided here).
 *
 * Usage: strong6 [-g6] [-k K] [-cap NODES] < input
 *   -k K     decide K-colorability instead of 6 (witness/verdict as above)
 *   -chi     for NOT-K instances, escalate K until colorable (exact chi)
 * Build: gcc -O2 -o strong6 strong6.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 128            /* max vertices of the colored graph G */
#define MAXM 192            /* max edges of G = vertices of C */
#define NW 3                /* bitset words for MAXM */

typedef unsigned long long u64;

static int g_n;                     /* vertices of G */
static u64 adj[MAXN][2];            /* adjacency bitsets of G (MAXN<=128) */
static int eu[MAXM], ev[MAXM];      /* edge endpoints */
static int g_m;                     /* edges of G */
static u64 conf[MAXM][NW];          /* conflict bitsets over edges */
static int color[MAXM];
static long long nodes;
static long long node_cap = 200000000LL;

static void add_edge_g(int a, int b) {
    eu[g_m] = a; ev[g_m] = b; g_m++;
    adj[a][b >> 6] |= 1ULL << (b & 63);
    adj[b][a >> 6] |= 1ULL << (a & 63);
}

static int adj_q(int a, int b) {
    return (adj[a][b >> 6] >> (b & 63)) & 1ULL;
}

static void build_conflicts(void) {
    for (int i = 0; i < g_m; i++)
        for (int w = 0; w < NW; w++) conf[i][w] = 0;
    for (int i = 0; i < g_m; i++)
        for (int j = i + 1; j < g_m; j++) {
            int a = eu[i], b = ev[i], c = eu[j], d = ev[j];
            int hit = (a == c || a == d || b == c || b == d) ||
                      adj_q(a, c) || adj_q(a, d) || adj_q(b, c) || adj_q(b, d);
            if (hit) {
                conf[i][j >> 6] |= 1ULL << (j & 63);
                conf[j][i >> 6] |= 1ULL << (i & 63);
            }
        }
}

/* greedy clique in C seeded at the max-degree conflict vertex */
static int find_clique(int *cl) {
    int deg[MAXM], best = 0;
    for (int i = 0; i < g_m; i++) {
        deg[i] = 0;
        for (int w = 0; w < NW; w++) deg[i] += __builtin_popcountll(conf[i][w]);
        if (deg[i] > deg[best]) best = i;
    }
    int sz = 0;
    u64 cand[NW];
    for (int w = 0; w < NW; w++) cand[w] = conf[best][w];
    cl[sz++] = best;
    for (;;) {
        int pick = -1, pdeg = -1;
        for (int w = 0; w < NW; w++) {
            u64 x = cand[w];
            while (x) {
                int j = (w << 6) + __builtin_ctzll(x);
                x &= x - 1;
                if (deg[j] > pdeg) { pdeg = deg[j]; pick = j; }
            }
        }
        if (pick < 0) break;
        cl[sz++] = pick;
        for (int w = 0; w < NW; w++) cand[w] &= conf[pick][w];
    }
    return sz;
}

static int K;                      /* number of colors */

/* exhaustive backtracking; returns 1 if K-colorable, 0 if not, -1 cap */
static int solve_rec(int colored_cnt) {
    if (colored_cnt == g_m) return 1;
    if (++nodes > node_cap) return -1;
    /* pick uncolored edge with fewest available colors (fail-first) */
    int best = -1, bestavail = K + 1, bestmask = 0;
    for (int i = 0; i < g_m; i++) {
        if (color[i] >= 0) continue;
        int used = 0;
        for (int w = 0; w < NW; w++) {
            u64 x = conf[i][w];
            while (x) {
                int j = (w << 6) + __builtin_ctzll(x);
                x &= x - 1;
                if (color[j] >= 0) used |= 1 << color[j];
            }
        }
        int avail = K - __builtin_popcount(used & ((1 << K) - 1));
        if (avail == 0) return 0;
        if (avail < bestavail) { bestavail = avail; best = i; bestmask = used; }
        if (avail == 1) break;
    }
    for (int c = 0; c < K; c++) {
        if (bestmask & (1 << c)) continue;
        color[best] = c;
        int r = solve_rec(colored_cnt + 1);
        if (r) { if (r < 0) { color[best] = -1; return -1; } return 1; }
        color[best] = -1;
    }
    return 0;
}

static int solve(int k) {
    K = k;
    for (int i = 0; i < g_m; i++) color[i] = -1;
    int cl[MAXM];
    int cs = find_clique(cl);
    if (cs > k) return 0;          /* clique exceeds palette: immediate no */
    int fixed = cs < k ? cs : k;
    for (int i = 0; i < fixed; i++) color[cl[i]] = i;
    nodes = 0;
    return solve_rec(fixed);
}

/* ---- input parsing ---- */

/* multig -T line -> build T(H); returns 0 on parse failure */
static int build_truncation(const char *line) {
    int nv, ne;
    const char *p = line;
    char *q;
    nv = (int)strtol(p, &q, 10); if (q == p) return 0; p = q;
    ne = (int)strtol(p, &q, 10); if (q == p) return 0; p = q;
    if (nv <= 0 || 3 * nv > MAXN) return 0;
    int slots[MAXN]; /* next free slot per H-vertex */
    memset(slots, 0, sizeof(int) * nv);
    g_n = 3 * nv; g_m = 0;
    memset(adj, 0, sizeof(u64) * 2 * g_n);
    /* triangle edges first, canonical order */
    for (int u = 0; u < nv; u++) {
        add_edge_g(3 * u, 3 * u + 1);
        add_edge_g(3 * u, 3 * u + 2);
        add_edge_g(3 * u + 1, 3 * u + 2);
    }
    /* link edges in instance order */
    for (int t = 0; t < ne; t++) {
        int a = (int)strtol(p, &q, 10); if (q == p) return 0; p = q;
        int b = (int)strtol(p, &q, 10); if (q == p) return 0; p = q;
        int mult = (int)strtol(p, &q, 10); if (q == p) return 0; p = q;
        if (a < 0 || b < 0 || a >= nv || b >= nv || a == b || mult < 1) return 0;
        for (int r = 0; r < mult; r++) {
            if (slots[a] > 2 || slots[b] > 2) return 0;
            int sa = slots[a]++, sb = slots[b]++;
            add_edge_g(3 * a + sa, 3 * b + sb);
        }
    }
    for (int u = 0; u < nv; u++) if (slots[u] != 3) return 0; /* must be cubic */
    return 1;
}

/* graph6 line -> graph; returns 0 on failure */
static int build_graph6(const char *line) {
    const unsigned char *s = (const unsigned char *)line;
    if (*s == ':' || *s == '&') return 0;      /* sparse6/digraph6 unsupported */
    int n;
    if (s[0] == 126) return 0;                  /* n > 62 unsupported */
    n = s[0] - 63; s++;
    if (n < 1 || n > MAXN) return 0;
    g_n = n; g_m = 0;
    memset(adj, 0, sizeof(u64) * 2 * (unsigned)n);
    int nbits = n * (n - 1) / 2, bit = 0;
    int i = 0, j = 1; /* column-major upper triangle: (0,1),(0,2),(1,2),(0,3).. */
    while (bit < nbits) {
        if (!*s || *s == '\n') return 0;
        int val = *s - 63; s++;
        for (int b = 5; b >= 0 && bit < nbits; b--, bit++) {
            if ((val >> b) & 1) add_edge_g(i, j);
            i++;
            if (i == j) { j++; i = 0; }
        }
    }
    return 1;
}

int main(int argc, char **argv) {
    int g6 = 0, kk = 6, do_chi = 1;
    for (int a = 1; a < argc; a++) {
        if (!strcmp(argv[a], "-g6")) g6 = 1;
        else if (!strcmp(argv[a], "-k") && a + 1 < argc) kk = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-cap") && a + 1 < argc) node_cap = atoll(argv[++a]);
        else if (!strcmp(argv[a], "-nochi")) do_chi = 0;
    }
    char line[65536];
    long lineno = 0, n_yes = 0, n_no = 0, n_cap = 0;
    while (fgets(line, sizeof line, stdin)) {
        lineno++;
        size_t L = strlen(line);
        while (L && (line[L - 1] == '\n' || line[L - 1] == '\r')) line[--L] = 0;
        if (!L) continue;
        int ok = g6 ? build_graph6(line) : build_truncation(line);
        if (!ok) { fprintf(stderr, "parse error line %ld: %s\n", lineno, line); return 2; }
        build_conflicts();
        int r = solve(kk);
        long long used_nodes = nodes;
        if (r == 1) {
            n_yes++;
            printf("R %ld %d %d %d %lld", lineno, g_n, g_m, kk, used_nodes);
            for (int i = 0; i < g_m; i++) printf(" %d", color[i]);
            printf(" | %s\n", line);
        } else if (r == 0) {
            n_no++;
            int chi = kk;
            if (do_chi) {
                for (chi = kk + 1; chi <= g_m; chi++) if (solve(chi) == 1) break;
            }
            printf("R %ld %d %d NOT%d %lld chi=%d | %s\n",
                   lineno, g_n, g_m, kk, used_nodes, do_chi ? chi : -1, line);
        } else {
            n_cap++;
            printf("R %ld %d %d CAP %lld | %s\n", lineno, g_n, g_m, used_nodes, line);
        }
    }
    fprintf(stderr, "strong6: %ld graphs, %ld colorable(%d), %ld not, %ld capped\n",
            lineno, n_yes, kk, n_no, n_cap);
    return 0;
}
