/* hunt.c — simulated-annealing search for connected cubic graphs with no
 * cycles of length 4, 8, or 16 (optionally 32).
 *
 * On n <= 31 vertices, a cubic graph with no C4/C8/C16 contains no cycle of
 * any power-of-2 length at all, i.e. it would be a counterexample to the
 * Erdos-Gyarfas conjecture.  For 33 <= n <= 63 a hit must still be screened
 * for 32-cycles (cyclecheck does that exactly).
 *
 * State space: connected simple cubic graphs on n vertices.
 * Move: random 2-edge swap {a,b},{c,d} -> {a,c},{b,d} or {a,d},{b,c},
 *       rejected if it breaks simplicity or connectivity.
 * Energy: sum over target lengths L of w_L * (#cycles of length exactly L),
 *       counted exactly by min-vertex DFS with distance pruning.
 * Schedule: geometric cooling with reheats on stagnation; random restarts.
 *
 * All arithmetic on the graph side is exact; the only floating point is the
 * Metropolis acceptance test, which affects only the search trajectory,
 * never the validity of a reported hit (hits are re-verified externally).
 *
 * Usage: hunt <n> <seed> <max_moves> [Lmax]
 *   Lmax: largest power-of-2 length counted in the energy (default 16).
 * Output: progress + best-found graph in graph6 on stdout; a zero-energy hit
 * is flagged with "HIT".
 *
 * Build: gcc -O3 -march=native -o hunt hunt.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#define MAXN 64

static int n;
static uint64_t adj[MAXN];
static int deg[MAXN], nbr[MAXN][3];

/* ---------- rng: splitmix64 ---------- */
static uint64_t rng_state;
static inline uint64_t rng_next(void) {
    uint64_t z = (rng_state += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
static inline int rng_below(int m) { return (int)(rng_next() % (uint64_t)m); }
static inline double rng_unit(void) { return (rng_next() >> 11) * 0x1.0p-53; }

/* ---------- adjacency helpers ---------- */
static void rebuild_lists(void) {
    for (int i = 0; i < n; i++) {
        deg[i] = 0;
        uint64_t m = adj[i];
        while (m) { int j = __builtin_ctzll(m); m &= m - 1; nbr[i][deg[i]++] = j; }
    }
}
static inline void add_edge(int a, int b) { adj[a] |= 1ULL << b; adj[b] |= 1ULL << a; }
static inline void del_edge(int a, int b) { adj[a] &= ~(1ULL << b); adj[b] &= ~(1ULL << a); }
static inline int has_edge(int a, int b) { return (adj[a] >> b) & 1; }

static int connected(void) {
    uint64_t seen = 1ULL, frontier = 1ULL;
    while (frontier) {
        uint64_t next = 0;
        uint64_t f = frontier;
        while (f) { int u = __builtin_ctzll(f); f &= f - 1; next |= adj[u]; }
        frontier = next & ~seen;
        seen |= next;
    }
    return seen == ((n == 64) ? ~0ULL : ((1ULL << n) - 1));
}

/* ---------- exact cycle counting, lengths 3..Lmax ---------- */
static int Lmax;                 /* count cycles up to this length */
static long long ccount[MAXN + 1];
static int dist_v[MAXN];
static int path1;                /* second vertex of current path (direction breaking) */
static int v_min;

static void bfs_from(int v) {
    static int queue[MAXN];
    for (int i = 0; i < n; i++) dist_v[i] = MAXN + 1;
    int head = 0, tail = 0;
    dist_v[v] = 0; queue[tail++] = v;
    while (head < tail) {
        int u = queue[head++];
        for (int k = 0; k < deg[u]; k++) {
            int w = nbr[u][k];
            if (w > v && dist_v[w] > dist_v[u] + 1) { dist_v[w] = dist_v[u] + 1; queue[tail++] = w; }
        }
    }
}

static uint64_t used;
static void dfs_count(int u, int d) {
    /* d edges walked, currently at u; cycles counted once via path1 < u */
    if (d >= 2 && has_edge(u, v_min) && path1 < u)
        ccount[d + 1]++;
    if (d + 1 >= Lmax) return;
    for (int k = 0; k < deg[u]; k++) {
        int w = nbr[u][k];
        if (w <= v_min || ((used >> w) & 1)) continue;
        if (dist_v[w] > Lmax - d - 1) continue;
        used |= 1ULL << w;
        dfs_count(w, d + 1);
        used &= ~(1ULL << w);
    }
}

static void count_cycles(void) {
    memset(ccount, 0, sizeof ccount);
    for (v_min = 0; v_min < n - 2; v_min++) {
        bfs_from(v_min);
        for (int k = 0; k < deg[v_min]; k++) {
            int w = nbr[v_min][k];
            if (w <= v_min) continue;
            path1 = w;
            used = (1ULL << v_min) | (1ULL << w);
            dfs_count(w, 1);
        }
    }
}

static long long W4 = 4, W8 = 2, W16 = 1;
static int girth_min = 0;        /* if > 0: energy = # cycles shorter than this */
static long long energy(void) {
    count_cycles();
    long long e = 0;
    if (girth_min > 0) {
        for (int L = 3; L < girth_min; L++) e += ccount[L];
        return e;
    }
    for (int L = 4; L <= Lmax; L *= 2)
        e += (L == 4 ? W4 : L == 8 ? W8 : W16) * ccount[L];
    return e;
}

/* ---------- random connected cubic start ---------- */
static void random_cubic(void) {
    /* configuration model with retries until simple; then retry until connected */
    for (;;) {
        int stubs[3 * MAXN], ns = 0;
        for (int i = 0; i < n; i++) for (int k = 0; k < 3; k++) stubs[ns++] = i;
        for (int i = ns - 1; i > 0; i--) {
            int j = rng_below(i + 1);
            int t = stubs[i]; stubs[i] = stubs[j]; stubs[j] = t;
        }
        memset(adj, 0, sizeof adj);
        int ok = 1;
        for (int i = 0; i < ns; i += 2) {
            int a = stubs[i], b = stubs[i + 1];
            if (a == b || has_edge(a, b)) { ok = 0; break; }
            add_edge(a, b);
        }
        if (!ok) continue;
        rebuild_lists();
        if (connected()) return;
    }
}

static void print_g6(FILE *f) {
    /* graph6 for n < 63 */
    fputc(n + 63, f);
    int bit = 5, val = 0;
    for (int j = 1; j < n; j++)
        for (int i = 0; i < j; i++) {
            if (has_edge(i, j)) val |= 1 << bit;
            if (--bit < 0) { fputc(val + 63, f); bit = 5; val = 0; }
        }
    if (bit < 5) fputc(val + 63, f);
    fputc('\n', f);
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: hunt n seed max_moves [Lmax [w4 w8 w16 [girthmin]]]\n"); return 2; }
    n = atoi(argv[1]);
    uint64_t seed = strtoull(argv[2], NULL, 10);
    long long max_moves = atoll(argv[3]);
    Lmax = (argc > 4) ? atoi(argv[4]) : 16;
    if (argc > 7) { W4 = atoll(argv[5]); W8 = atoll(argv[6]); W16 = atoll(argv[7]); }
    if (argc > 8) { girth_min = atoi(argv[8]); Lmax = girth_min - 1; }
    if (n < 6 || n > 62 || (n & 1)) { fprintf(stderr, "bad n\n"); return 2; }
    rng_state = seed * 0x9E3779B97F4A7C15ULL + 12345;

    random_cubic();

    /* Phase 1: with a cheap energy (cycles up to length 8 only), drive the
     * graph to C4 = C8 = 0 — the {4,8}-free manifold — then switch to the
     * full energy.  For n < 24 no {4,8}-free cubic graph exists (exhaustive
     * runs in this directory), so phase 1 just does its best. */
    int full_Lmax = Lmax;
    Lmax = girth_min > 0 ? (girth_min > 9 ? 8 : girth_min - 1) : 8;
    {
        long long E1 = energy();
        double T1 = 6.0;
        for (long long mv = 0; mv < max_moves / 4 && E1 > 0; mv++) {
            int a = rng_below(n), b = nbr[a][rng_below(3)];
            int c = rng_below(n), d = nbr[c][rng_below(3)];
            if (a == c || a == d || b == c || b == d) continue;
            int x, y, w, z;
            if (rng_next() & 1) { x = a; y = c; w = b; z = d; }
            else               { x = a; y = d; w = b; z = c; }
            if (has_edge(x, y) || has_edge(w, z)) continue;
            del_edge(a, b); del_edge(c, d);
            add_edge(x, y); add_edge(w, z);
            rebuild_lists();
            if (!connected()) {
                del_edge(x, y); del_edge(w, z);
                add_edge(a, b); add_edge(c, d);
                rebuild_lists();
                continue;
            }
            long long E2 = energy();
            if (E2 <= E1 || rng_unit() < exp(-(double)(E2 - E1) / T1)) E1 = E2;
            else {
                del_edge(x, y); del_edge(w, z);
                add_edge(a, b); add_edge(c, d);
                rebuild_lists();
            }
            T1 *= 0.99993;
            if (T1 < 0.05) T1 = 0.05;
        }
        fprintf(stderr, "[n=%d seed=%llu] phase1 done E8=%lld\n",
                n, (unsigned long long)seed, E1);
    }
    Lmax = full_Lmax;

    long long E = energy();
    long long bestE = E;
    uint64_t best_adj[MAXN];
    memcpy(best_adj, adj, sizeof adj);

    double T = 3.0;
    const double COOL = 0.999985;
    long long since_improve = 0;

    for (long long mv = 0; mv < max_moves && bestE > 0; mv++) {
        /* pick two random edges via random vertices+slots */
        int a = rng_below(n), b = nbr[a][rng_below(3)];
        int c = rng_below(n), d = nbr[c][rng_below(3)];
        if (a == c || a == d || b == c || b == d) continue;
        int x, y, w, z;
        if (rng_next() & 1) { x = a; y = c; w = b; z = d; }   /* {a,c},{b,d} */
        else               { x = a; y = d; w = b; z = c; }    /* {a,d},{b,c} */
        if (has_edge(x, y) || has_edge(w, z)) continue;
        del_edge(a, b); del_edge(c, d);
        add_edge(x, y); add_edge(w, z);
        rebuild_lists();
        if (!connected()) {
            del_edge(x, y); del_edge(w, z);
            add_edge(a, b); add_edge(c, d);
            rebuild_lists();
            continue;
        }
        long long E2 = energy();
        int accept = (E2 <= E) || (rng_unit() < exp(-(double)(E2 - E) / T));
        if (accept) {
            E = E2;
            if (E < bestE) {
                bestE = E;
                memcpy(best_adj, adj, sizeof adj);
                since_improve = 0;
                fprintf(stderr, "[n=%d seed=%llu] move %lld E=%lld (C4=%lld C8=%lld C16=%lld%s) T=%.3f\n",
                        n, (unsigned long long)seed, mv, E,
                        ccount[4], ccount[8], Lmax >= 16 ? ccount[16] : 0,
                        Lmax >= 32 ? " +C32" : "", T);
            }
        } else {
            del_edge(x, y); del_edge(w, z);
            add_edge(a, b); add_edge(c, d);
            rebuild_lists();
        }
        T *= COOL;
        if (++since_improve > 200000) {     /* reheat + restart from best */
            memcpy(adj, best_adj, sizeof adj);
            rebuild_lists();
            E = energy();
            T = 2.0;
            since_improve = 0;
        }
        if (T < 0.12) T = 0.12;
    }

    memcpy(adj, best_adj, sizeof adj);
    rebuild_lists();
    long long finalE = energy();
    printf("RESULT n=%d seed=%llu bestE=%lld C4=%lld C8=%lld C16=%lld\n",
           n, (unsigned long long)seed, finalE, ccount[4], ccount[8],
           Lmax >= 16 ? ccount[16] : 0);
    if (finalE == 0) printf("HIT\n");
    print_g6(stdout);
    return 0;
}
