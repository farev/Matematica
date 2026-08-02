/* afsfv.c — additive-square-free word search over an alphabet of INTEGER VECTORS.
 *
 * Generalises afsf.c from Z to Z^d.  A word w over an alphabet A subset of Z^d
 * contains an ADDITIVE SQUARE if it has a factor u v with |u| = |v| and
 * sum(u) = sum(v) as vectors.  Exact integer arithmetic; no floats.
 *
 * WHY VECTORS.  A one-parameter family of real alphabets such as
 *     A_t = {0, 1, t, 1+t}   (the "degenerate" 4-letter family, a+d = b+c)
 * has block-sum differences of the form P + Q t with P, Q integers bounded by
 * the block length.  For a word of length <= n we have |P|, |Q| <= n, so
 * whether a given word is additive-square-free depends on t ONLY through which
 * of the finitely many rationals -P/Q it equals.  The parameter line therefore
 * splits into finitely many cells:
 *
 *   - GENERIC cell (t not equal to any -P/Q in range, e.g. t irrational):
 *     an additive square requires P = Q = 0.  That is exactly the d = 2
 *     vector alphabet {(0,0), (1,0), (0,1), (1,1)}, which this program handles.
 *   - SPECIAL cells (t = -P/Q): scale to an integer alphabet and use d = 1.
 *
 * Checking one representative of every cell PROVES a statement about the whole
 * infinite family.  That is the point of this program.
 *
 * Incremental test: if w[0..n-2] is additive-square-free, appending a letter can
 * only create a square ending at the last position, so with vector prefix sums
 * S[i] we need, for all k with 2k <= n:  S[n] - S[n-k] != S[n-k] - S[n-2k],
 * i.e.  S[n] + S[n-2k] != 2 S[n-k]  componentwise-simultaneously.
 *
 * Build:  gcc -O2 -o afsfv afsfv.c
 * Usage:  ./afsfv exhaust d "v1|v2|..." [maxdepth] [nodebudget]
 *         ./afsfv rand    d "v1|v2|..." [maxdepth] [nodebudget] [seed] [restarts]
 *   where each vi is a comma-separated d-vector, e.g.
 *         ./afsfv exhaust 2 "0,0|1,0|0,1|1,1" 200 100000000
 *         ./afsfv exhaust 1 "0|1|3|4"        200 100000000
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXLEN 400000
#define MAXALPHA 32
#define MAXDIM 4

static int m, dim;
static long long alpha[MAXALPHA][MAXDIM];
static int maxdepth;
static long long node_budget;

static long long nodes;
static int best, truncated;
static int word[MAXLEN], bestword[MAXLEN];
static long long S[MAXLEN + 1][MAXDIM];

static inline int sq_at_end(int n)
{
    for (int k = 1; 2 * k <= n; k++) {
        int eq = 1;
        for (int c = 0; c < dim; c++) {
            if (S[n][c] + S[n - 2 * k][c] != 2 * S[n - k][c]) { eq = 0; break; }
        }
        if (eq) return 1;
    }
    return 0;
}

static void dfs(int n)
{
    if (n > best) { best = n; memcpy(bestword, word, (size_t)n * sizeof(int)); }
    if (n >= maxdepth)        { truncated = 1; return; }
    if (nodes >= node_budget) { truncated = 1; return; }

    for (int i = 0; i < m; i++) {
        word[n] = i;
        for (int c = 0; c < dim; c++) S[n + 1][c] = S[n][c] + alpha[i][c];
        nodes++;
        if (!sq_at_end(n + 1)) dfs(n + 1);
    }
}

static uint64_t rng_state;
static inline uint64_t xs64(void)
{
    uint64_t x = rng_state;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    return rng_state = x;
}

static void dfs_rand(int n)
{
    if (n > best) { best = n; memcpy(bestword, word, (size_t)n * sizeof(int)); }
    if (n >= maxdepth)        { truncated = 1; return; }
    if (nodes >= node_budget) { truncated = 1; return; }

    int order[MAXALPHA];
    for (int i = 0; i < m; i++) order[i] = i;
    for (int i = m - 1; i > 0; i--) {
        int j = (int)(xs64() % (uint64_t)(i + 1));
        int t = order[i]; order[i] = order[j]; order[j] = t;
    }
    for (int i = 0; i < m; i++) {
        int a = order[i];
        word[n] = a;
        for (int c = 0; c < dim; c++) S[n + 1][c] = S[n][c] + alpha[a][c];
        nodes++;
        if (!sq_at_end(n + 1)) dfs_rand(n + 1);
        if (nodes >= node_budget) { truncated = 1; return; }
    }
}

static void print_word(const int *w, int n)
{
    printf("word=");
    for (int i = 0; i < n; i++) {
        if (i) printf(" ");
        for (int c = 0; c < dim; c++) printf("%s%lld", c ? "," : "", alpha[w[i]][c]);
    }
    printf("\n");
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "usage: %s exhaust|rand d \"v1|v2|...\" [maxdepth] "
                        "[nodebudget] [seed] [restarts]\n", argv[0]);
        return 2;
    }
    const char *mode = argv[1];
    dim = atoi(argv[2]);
    if (dim < 1 || dim > MAXDIM) { fprintf(stderr, "bad dim\n"); return 2; }

    {
        char buf[4096];
        snprintf(buf, sizeof buf, "%s", argv[3]);
        m = 0;
        /* strtok_r, not strtok: the inner tokenizer would clobber the outer
         * one's static state and we would parse only the first vector. */
        char *outer = NULL, *inner = NULL;
        for (char *tk = strtok_r(buf, "|", &outer); tk;
             tk = strtok_r(NULL, "|", &outer)) {
            char vb[512]; snprintf(vb, sizeof vb, "%s", tk);
            int c = 0;
            for (char *u = strtok_r(vb, ",", &inner); u;
                 u = strtok_r(NULL, ",", &inner))
                alpha[m][c++] = strtoll(u, NULL, 10);
            if (c != dim) { fprintf(stderr, "vector of wrong dim\n"); return 2; }
            m++;
        }
    }
    /* reject duplicate letters */
    for (int i = 0; i < m; i++)
        for (int j = i + 1; j < m; j++) {
            int same = 1;
            for (int c = 0; c < dim; c++) if (alpha[i][c] != alpha[j][c]) { same = 0; break; }
            if (same) { fprintf(stderr, "duplicate letter\n"); return 2; }
        }

    maxdepth    = (argc > 4) ? atoi(argv[4]) : 2000;
    node_budget = (argc > 5) ? strtoll(argv[5], NULL, 10) : 200000000LL;
    if (maxdepth > MAXLEN) maxdepth = MAXLEN;

    printf("dim=%d alphabet=", dim);
    for (int i = 0; i < m; i++) {
        if (i) printf("|");
        for (int c = 0; c < dim; c++) printf("%s%lld", c ? "," : "", alpha[i][c]);
    }
    printf("\nmode=%s maxdepth=%d nodebudget=%lld\n", mode, maxdepth, node_budget);

    clock_t t0 = clock();
    memset(S[0], 0, sizeof S[0]);
    nodes = 0; best = 0; truncated = 0;

    if (strcmp(mode, "exhaust") == 0) {
        dfs(0);
        printf("nodes=%lld secs=%.3f\n", nodes, (double)(clock() - t0) / CLOCKS_PER_SEC);
        if (truncated) printf("RESULT truncated L>=%d\n", best);
        else           printf("RESULT exact L=%d\n", best);
        print_word(bestword, best);
    } else if (strcmp(mode, "rand") == 0) {
        uint64_t seed = (argc > 6) ? strtoull(argv[6], NULL, 10) : 12345ULL;
        long long restarts = (argc > 7) ? strtoll(argv[7], NULL, 10) : 1;
        rng_state = seed ? seed : 88172645463325252ULL;
        long long per = node_budget / (restarts > 0 ? restarts : 1), total = 0;
        int gbest = 0; static int gword[MAXLEN];
        for (long long r = 0; r < restarts; r++) {
            nodes = 0; best = 0; truncated = 0; memset(S[0], 0, sizeof S[0]);
            long long save = node_budget; node_budget = per;
            dfs_rand(0);
            node_budget = save; total += nodes;
            if (best > gbest) { gbest = best; memcpy(gword, bestword, (size_t)best * sizeof(int)); }
        }
        printf("nodes=%lld secs=%.3f seed=%llu restarts=%lld\n",
               total, (double)(clock() - t0) / CLOCKS_PER_SEC,
               (unsigned long long)seed, restarts);
        printf("RESULT lower_bound L>=%d\n", gbest);
        print_word(gword, gbest);
    } else { fprintf(stderr, "unknown mode\n"); return 2; }
    return 0;
}
