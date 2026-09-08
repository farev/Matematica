/* sa.c -- simulated annealing over m-subsets of {1..W}, minimising the number of
 * dissociated k-subsets (exact count).  Objective 0  <=>  d(A) <= k-1.
 *
 * Build:  gcc -O2 -o sa sa.c -lm
 * Usage:  ./sa m k W seed time_limit_s [iters_per_restart] [T0] [T1] [w_km1] [init_mode]
 *   init_mode 0: uniform random m-subset of [1,W]
 *             1: {1..m} with 2 random replacements
 *             2: random m-subset of [1, min(W, 2m+8)]
 *             3: elements from environment variable INIT (space-separated), remaining slots random
 *   w_km1: optional weight on the number of dissociated (k-1)-subsets (secondary term).
 *
 * Dissociation test: incremental sorted-merge of subset sums (2^k sums); a
 * collision during the merge means a nontrivial relation.
 * Incremental re-evaluation: a move replaces one slot, so only the k-subsets
 * containing that slot are re-counted (C(m-1,k-1) of them).
 * A full recount is done at the end of each restart and checked against the
 * incrementally-maintained objective (abort on mismatch).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAXM 40
#define MAXK 8
#define MAXW 65536

static int m, k, W;
static int a[MAXM];
static unsigned char inA[MAXW + 1];
static double w_km1 = 0.0;

static unsigned long long rs = 88172645463325252ULL;
static inline unsigned long long rng(void) {
    rs ^= rs << 7; rs ^= rs >> 9; return rs;
}
static inline double urand(void) { return (rng() >> 11) * (1.0 / 9007199254740992.0); }
static inline int rint_(int n) { return (int)(rng() % (unsigned long long)n); }

/* returns 1 iff the kk values in b have all 2^kk subset sums distinct */
static inline int dissoc(const int *b, int kk) {
    int sums[1 << MAXK], tmp[1 << MAXK];
    int n = 1; sums[0] = 0;
    for (int j = 0; j < kk; j++) {
        int x = b[j];
        int p = 0, q = 0, t = 0;
        while (p < n && q < n) {
            int s1 = sums[p], s2 = sums[q] + x;
            if (s1 == s2) return 0;
            if (s1 < s2) tmp[t++] = sums[p++]; else tmp[t++] = sums[q++] + x;
        }
        while (p < n) tmp[t++] = sums[p++];
        while (q < n) tmp[t++] = sums[q++] + x;
        n *= 2;
        memcpy(sums, tmp, n * sizeof(int));
    }
    return 1;
}

/* number of dissociated kk-subsets of the current set that contain slot i, with
 * the value v placed in slot i (a[i] itself is ignored). */
static long long count_with(int i, int v, int kk) {
    int others[MAXM]; int n = 0;
    for (int j = 0; j < m; j++) if (j != i) others[n++] = a[j];
    int r = kk - 1;
    int idx[MAXK], b[MAXK];
    for (int j = 0; j < r; j++) idx[j] = j;
    long long c = 0;
    b[0] = v;
    for (;;) {
        for (int j = 0; j < r; j++) b[j + 1] = others[idx[j]];
        c += dissoc(b, kk);
        int j = r - 1;
        while (j >= 0 && idx[j] == n - r + j) j--;
        if (j < 0) break;
        idx[j]++;
        for (int l = j + 1; l < r; l++) idx[l] = idx[l - 1] + 1;
    }
    return c;
}

/* full count of dissociated kk-subsets of the current set */
static long long full_count(int kk) {
    int idx[MAXK], b[MAXK];
    for (int j = 0; j < kk; j++) idx[j] = j;
    long long c = 0;
    for (;;) {
        for (int j = 0; j < kk; j++) b[j] = a[idx[j]];
        c += dissoc(b, kk);
        int j = kk - 1;
        while (j >= 0 && idx[j] == m - kk + j) j--;
        if (j < 0) break;
        idx[j]++;
        for (int l = j + 1; l < kk; l++) idx[l] = idx[l - 1] + 1;
    }
    return c;
}

static int cmpint(const void *x, const void *y) { return *(const int *)x - *(const int *)y; }

/* small hash set of printed solutions (to avoid printing duplicates) */
#define HSIZE (1 << 16)
static unsigned long long hset[HSIZE];
static int hcount = 0;
static unsigned long long hash_set(const int *s) {
    unsigned long long h = 1469598103934665603ULL;
    for (int j = 0; j < m; j++) { h ^= (unsigned long long)s[j]; h *= 1099511628211ULL; h ^= h >> 29; }
    return h | 1ULL;
}
static int seen_insert(unsigned long long h) {
    unsigned long long p = h & (HSIZE - 1);
    while (hset[p]) { if (hset[p] == h) return 1; p = (p + 1) & (HSIZE - 1); }
    if (hcount < HSIZE / 2) { hset[p] = h; hcount++; }
    return 0;
}

static void print_set(FILE *fp, const char *tag) {
    int s[MAXM]; memcpy(s, a, m * sizeof(int)); qsort(s, m, sizeof(int), cmpint);
    fprintf(fp, "%s", tag);
    for (int j = 0; j < m; j++) fprintf(fp, " %d", s[j]);
    fprintf(fp, "\n");
    fflush(fp);
}

static double now(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

static int nfound = 0;
static double t_start;
static unsigned long long seed_g;
static void report_if_zero(void) {
    int s[MAXM]; memcpy(s, a, m * sizeof(int)); qsort(s, m, sizeof(int), cmpint);
    unsigned long long h = hash_set(s);
    if (seen_insert(h)) return;
    long long chk = full_count(k);
    if (chk != 0) { fprintf(stderr, "INCONSISTENCY: incremental f=0 but full=%lld\n", chk); print_set(stderr, "BAD"); exit(2); }
    char tag[128]; snprintf(tag, sizeof tag, "FOUND m=%d k=%d W=%d seed=%llu t=%.1f :", m, k, W, seed_g, now() - t_start);
    print_set(stdout, tag);
    nfound++;
}

static void init_set(int mode) {
    memset(inA, 0, sizeof(inA));
    int hi = W;
    if (mode == 2) { hi = 2 * m + 8; if (hi > W) hi = W; if (hi < m) hi = m; }
    if (mode == 3) {
        const char *e = getenv("INIT"); int j = 0;
        if (e) { char *q = (char *)e; while (*q && j < m) { char *r; long v = strtol(q, &r, 10); if (r == q) { q++; continue; } q = r; if (v >= 1 && v <= W && !inA[v]) { a[j++] = (int)v; inA[v] = 1; } } }
        for (; j < m; j++) { int v; do { v = 1 + rint_(W); } while (inA[v]); a[j] = v; inA[v] = 1; }
        return;
    }
    if (mode == 1) {
        for (int j = 0; j < m; j++) { a[j] = j + 1; inA[a[j]] = 1; }
        for (int t = 0; t < 2; t++) {
            int i = rint_(m), v;
            do { v = 1 + rint_(W); } while (inA[v]);
            inA[a[i]] = 0; a[i] = v; inA[v] = 1;
        }
        return;
    }
    for (int j = 0; j < m; j++) {
        int v; do { v = 1 + rint_(hi); } while (inA[v]);
        a[j] = v; inA[v] = 1;
    }
}

/* propose a new value for slot i: mixture of structured moves */
static int propose(int i) {
    int v = 0;
    if (W <= m) return -1;                    /* no free value: no move possible */
    for (int tries = 0; tries < 50; tries++) {
        double u = urand();
        if (u < 0.30) {                       /* v = a_j + a_l */
            int j = rint_(m), l = rint_(m); if (j == l) continue;
            v = a[j] + a[l];
        } else if (u < 0.50) {                /* v = |a_j - a_l| */
            int j = rint_(m), l = rint_(m); if (j == l) continue;
            v = abs(a[j] - a[l]);
        } else if (u < 0.65) {                /* v = a_j + a_l - a_p */
            int j = rint_(m), l = rint_(m), p = rint_(m);
            if (j == l || j == p || l == p) continue;
            v = a[j] + a[l] - a[p];
        } else if (u < 0.85) {                /* local */
            int r = 1 + rint_(4); v = a[i] + (rint_(2) ? r : -r);
        } else {                              /* uniform */
            v = 1 + rint_(W);
        }
        if (v >= 1 && v <= W && !inA[v]) return v;
    }
    for (;;) { v = 1 + rint_(W); if (!inA[v]) return v; }
}

int main(int argc, char **argv) {
    if (argc < 6) {
        fprintf(stderr, "usage: %s m k W seed time_limit_s [iters_per_restart] [T0] [T1] [w_km1] [init_mode]\n", argv[0]);
        return 1;
    }
    m = atoi(argv[1]); k = atoi(argv[2]); W = atoi(argv[3]);
    unsigned long long seed = strtoull(argv[4], 0, 10);
    double tlimit = atof(argv[5]);
    long long iters = argc > 6 ? atoll(argv[6]) : 200000;
    double T0 = argc > 7 ? atof(argv[7]) : 5.0;
    double T1 = argc > 8 ? atof(argv[8]) : 0.05;
    w_km1 = argc > 9 ? atof(argv[9]) : 0.0;
    int init_mode = argc > 10 ? atoi(argv[10]) : 0;
    if (m > MAXM || k > MAXK || k < 2 || W > MAXW || W < m) { fprintf(stderr, "bad params\n"); return 1; }
    rs = seed * 0x9E3779B97F4A7C15ULL + 12345; for (int t = 0; t < 20; t++) rng();

    t_start = now(); seed_g = seed;
    long long best_ever = -1; int best_set[MAXM];
    long long total_iters = 0; int restarts = 0;

    while (now() - t_start < tlimit) {
        init_set(init_mode);
        long long f = full_count(k);
        double g = f + (w_km1 > 0 ? w_km1 * full_count(k - 1) : 0.0);
        long long fbest = f; int rbest[MAXM]; memcpy(rbest, a, m * sizeof(int));
        if (f == 0) report_if_zero();
        long long cache_cnt[MAXM]; double cache_g[MAXM]; unsigned char cache_ok[MAXM];
        memset(cache_ok, 0, sizeof(cache_ok));
        long long it;
        for (it = 0; it < iters; it++) {
            if ((it & 1023) == 0 && now() - t_start > tlimit) break;
            double T = T0 * pow(T1 / T0, (double)it / (double)iters);
            int i = rint_(m);
            int v = propose(i);
            if (v < 0) break;                 /* W == m: nothing to do */
            long long c_old, c_new; double g_old, g_new;
            if (cache_ok[i]) { c_old = cache_cnt[i]; g_old = cache_g[i]; }
            else {
                c_old = count_with(i, a[i], k);
                g_old = c_old + (w_km1 > 0 ? w_km1 * count_with(i, a[i], k - 1) : 0.0);
                cache_cnt[i] = c_old; cache_g[i] = g_old; cache_ok[i] = 1;
            }
            c_new = count_with(i, v, k);
            g_new = c_new + (w_km1 > 0 ? w_km1 * count_with(i, v, k - 1) : 0.0);
            double delta = g_new - g_old;
            if (delta <= 0 || urand() < exp(-delta / T)) {
                inA[a[i]] = 0; a[i] = v; inA[v] = 1;
                f += c_new - c_old; g += delta;
                memset(cache_ok, 0, sizeof(cache_ok));
                if (f < fbest) { fbest = f; memcpy(rbest, a, m * sizeof(int)); }
                if (f == 0) report_if_zero();
            }
        }
        total_iters += it; restarts++;
        long long chk = full_count(k);
        if (chk != f) { fprintf(stderr, "INCONSISTENCY at end of restart: f=%lld full=%lld\n", f, chk); return 2; }
        if (best_ever < 0 || fbest < best_ever) { best_ever = fbest; memcpy(best_set, rbest, m * sizeof(int)); }
    }
    double el = now() - t_start;
    printf("SUMMARY m=%d k=%d W=%d seed=%llu restarts=%d iters=%lld time=%.1fs best_obj=%lld found=%d rate=%.0f it/s\n",
           m, k, W, seed, restarts, total_iters, el, best_ever, nfound, total_iters / (el > 0 ? el : 1));
    memcpy(a, best_set, m * sizeof(int));
    print_set(stdout, "BEST :");
    return 0;
}
