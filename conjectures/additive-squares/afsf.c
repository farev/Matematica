/* afsf.c — additive-square-free word search over a finite integer alphabet.
 *
 * A word w over an alphabet A (subset of Z) contains an ADDITIVE SQUARE if it
 * has a factor u v with |u| = |v| and sum(u) = sum(v).  w is additive-square-
 * free (afsf) if it has no such factor.  L(A) denotes the length of the longest
 * additive-square-free word over A, or infinity if arbitrarily long ones exist.
 *
 * Everything here is exact integer arithmetic (int64 prefix sums).  No floats.
 *
 * Incremental test: if w[0..n-2] is afsf, then appending a letter can only
 * create a square that ENDS at the last position, so with prefix sums
 * S[0]=0, S[i]=w[0]+...+w[i-1], the word of length n is afsf iff for all
 * k with 2k <= n:   S[n] - S[n-k] != S[n-k] - S[n-2k],
 * i.e.               S[n] + S[n-2k] != 2*S[n-k].
 *
 * Modes:
 *   exhaust  — full DFS over the tree of afsf words.  If it completes without
 *              hitting the node budget or the depth cap, L(A) is EXACT.
 *   rand     — randomized-restart DFS (letters visited in a random order per
 *              node); reports the longest word found.  Lower bound only.
 *
 * Build:  gcc -O2 -o afsf afsf.c
 * Usage:  ./afsf exhaust "0,1,3,4" [maxdepth] [nodebudget]
 *         ./afsf rand    "0,1,2,5" [maxdepth] [nodebudget] [seed] [restarts]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXLEN 200000
#define MAXALPHA 32

static int m;                       /* alphabet size */
static long long alpha[MAXALPHA];   /* the alphabet, ascending */
static int maxdepth;
static long long node_budget;

static long long nodes;
static int best;
static int truncated;               /* 1 if depth cap or budget stopped us */
static int word[MAXLEN];
static int bestword[MAXLEN];
static long long S[MAXLEN + 1];

/* --- exact incremental additive-square test ------------------------------ */
/* Does the length-n word have an additive square ending at its last letter? */
static inline int sq_at_end(int n)
{
    const long long sn = S[n];
    for (int k = 1; 2 * k <= n; k++) {
        if (sn + S[n - 2 * k] == 2 * S[n - k]) return 1;
    }
    return 0;
}

/* --- exhaustive DFS ------------------------------------------------------ */
static void dfs(int n)
{
    if (n > best) { best = n; memcpy(bestword, word, (size_t)n * sizeof(int)); }
    if (n >= maxdepth)      { truncated = 1; return; }
    if (nodes >= node_budget) { truncated = 1; return; }

    for (int i = 0; i < m; i++) {
        word[n] = i;
        S[n + 1] = S[n] + alpha[i];
        nodes++;
        if (!sq_at_end(n + 1)) dfs(n + 1);
    }
}

/* --- randomized-restart DFS --------------------------------------------- */
static uint64_t rng_state;
static inline uint64_t xorshift64(void)
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
    for (int i = m - 1; i > 0; i--) {          /* Fisher-Yates */
        int j = (int)(xorshift64() % (uint64_t)(i + 1));
        int t = order[i]; order[i] = order[j]; order[j] = t;
    }
    for (int i = 0; i < m; i++) {
        int a = order[i];
        word[n] = a;
        S[n + 1] = S[n] + alpha[a];
        nodes++;
        if (!sq_at_end(n + 1)) dfs_rand(n + 1);
        if (nodes >= node_budget) { truncated = 1; return; }
    }
}

/* ------------------------------------------------------------------------ */
static void print_word(const int *w, int n)
{
    printf("word=");
    for (int i = 0; i < n; i++) printf("%s%lld", i ? "," : "", alpha[w[i]]);
    printf("\n");
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "usage: %s exhaust|rand \"a,b,c\" [maxdepth] "
                        "[nodebudget] [seed] [restarts]\n", argv[0]);
        return 2;
    }
    const char *mode = argv[1];

    /* parse alphabet */
    {
        char buf[1024];
        snprintf(buf, sizeof buf, "%s", argv[2]);
        m = 0;
        for (char *t = strtok(buf, ","); t; t = strtok(NULL, ","))
            alpha[m++] = strtoll(t, NULL, 10);
    }
    /* sort ascending, reject duplicates */
    for (int i = 0; i < m; i++)
        for (int j = i + 1; j < m; j++)
            if (alpha[j] < alpha[i]) { long long t = alpha[i]; alpha[i] = alpha[j]; alpha[j] = t; }
    for (int i = 1; i < m; i++)
        if (alpha[i] == alpha[i - 1]) { fprintf(stderr, "duplicate letter\n"); return 2; }

    maxdepth    = (argc > 3) ? atoi(argv[3]) : 2000;
    node_budget = (argc > 4) ? strtoll(argv[4], NULL, 10) : 200000000LL;
    if (maxdepth > MAXLEN) maxdepth = MAXLEN;

    printf("alphabet=");
    for (int i = 0; i < m; i++) printf("%s%lld", i ? "," : "", alpha[i]);
    printf("\nmode=%s maxdepth=%d nodebudget=%lld\n", mode, maxdepth, node_budget);

    clock_t t0 = clock();
    S[0] = 0; nodes = 0; best = 0; truncated = 0;

    if (strcmp(mode, "exhaust") == 0) {
        dfs(0);
        double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
        printf("nodes=%lld secs=%.3f\n", nodes, secs);
        if (truncated) printf("RESULT truncated L>=%d\n", best);
        else           printf("RESULT exact L=%d\n", best);
        print_word(bestword, best);
    } else if (strcmp(mode, "rand") == 0) {
        uint64_t seed  = (argc > 5) ? strtoull(argv[5], NULL, 10) : 12345ULL;
        long long restarts = (argc > 6) ? strtoll(argv[6], NULL, 10) : 1;
        rng_state = seed ? seed : 88172645463325252ULL;
        long long per = node_budget / (restarts > 0 ? restarts : 1);
        long long total = 0;
        int gbest = 0; static int gword[MAXLEN];
        for (long long r = 0; r < restarts; r++) {
            nodes = 0; best = 0; truncated = 0; S[0] = 0;
            long long save = node_budget; node_budget = per;
            dfs_rand(0);
            node_budget = save;
            total += nodes;
            if (best > gbest) { gbest = best; memcpy(gword, bestword, (size_t)best * sizeof(int)); }
        }
        double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
        printf("nodes=%lld secs=%.3f seed=%llu restarts=%lld\n",
               total, secs, (unsigned long long)seed, restarts);
        printf("RESULT lower_bound L>=%d\n", gbest);
        print_word(gword, gbest);
    } else {
        fprintf(stderr, "unknown mode %s\n", mode);
        return 2;
    }
    return 0;
}
