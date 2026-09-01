/* graham475c.c — v3 engine. Exhaustive per-prime verification of Graham's
 * rearrangement conjecture (Erdős #475): every A ⊆ Z_p\{0} has an ordering
 * with all partial sums distinct mod p.
 *
 * Orbit enumeration (unchanged from v2, Burnside-validated): canonical reps
 * of the F_p^*-scaling orbits = subsets containing 1 whose bitmask is minimal
 * among the |A| dilations (1/a)·A, a ∈ A.
 *
 * Per-set decision (deterministic from (p,t,rank,SEED)), tiered:
 *   T1: 64 random shuffles.
 *   T2: local-search repair — swap hill-climbing on the collision count,
 *       8 restarts × 30k moves.
 *   T3: 16 randomized-order bounded DFS restarts (budgets 1e5 · 2^i capped).
 *   T4: big local search — 192 restarts × 250k moves.
 *   T5: COMPLETE deterministic DFS, unbounded (adjudication; only a genuine
 *       counterexample or a pathological survivor reaches it).
 * A set reaching T3+ is "hard" (witness logged). A T5 entry is logged with
 * ADJUDICATE. DFS exhaustion => NO valid ordering => counterexample (loud).
 *
 * Flags: -z  forbid 0 as a partial sum (negative-control mode: then
 *            {x,-x} and other zero-sum sets must come back NO).
 *        -s a1,a2,...  decide the single given set (t from list), verbose.
 *
 * usage: graham475c p tmin tmax nthreads seed [hardfile]
 *        graham475c p -s 1,2,5,... [-z]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

static int P, TMIN, TMAX, NTHREADS, FORBID0 = 0;
static uint64_t SEED, WSAMPLE = 0; /* if >0, log witness for reps with
                                      rep_index % WSAMPLE == 0 */
static FILE *hardf = NULL;
static pthread_mutex_t hardmu = PTHREAD_MUTEX_INITIALIZER;
static int INV[64];

typedef struct {
    int t, tid;
    uint64_t reps, hard, adjud, fail, maxnodes, t3wit, t4wit;
} job_t;

static inline uint64_t xs64(uint64_t *s) {
    uint64_t x = *s; x ^= x << 13; x ^= x >> 7; x ^= x << 17; return *s = x;
}

/* validity scan; returns 1 if perm has distinct partial sums (and nonzero if
 * FORBID0). */
static inline int valid(const int *perm, int t, int p) {
    uint64_t seen = FORBID0 ? 1ULL : 0ULL;
    int sum = 0;
    for (int i = 0; i < t; i++) {
        sum += perm[i]; if (sum >= p) sum -= p;
        if (seen & (1ULL << sum)) return 0;
        seen |= 1ULL << sum;
    }
    return 1;
}

/* collision count of a permutation: number of duplicated prefix-sum slots.
 * cnt[] must be zeroed size p; it is used and re-zeroed here. */
static inline int cost_of(const int *perm, int t, int p, int *cnt, int *sums) {
    int sum = 0, cost = 0;
    for (int i = 0; i < t; i++) {
        sum += perm[i]; if (sum >= p) sum -= p;
        sums[i] = sum;
        if (cnt[sum]++) cost++;
    }
    if (FORBID0) cost += cnt[0];
    for (int i = 0; i < t; i++) cnt[sums[i]] = 0;
    return cost;
}

/* local search: swap two positions, hill-climb with sideways moves.
 * returns 1 + witness in perm if cost 0 reached. */
static int localsearch(const int *el, int t, int p, int *perm,
                       int restarts, int moves, uint64_t *rng) {
    int cnt[64] = {0}, sums[64], cand[64];
    for (int rs = 0; rs < restarts; rs++) {
        for (int i = 0; i < t; i++) perm[i] = el[i];
        for (int i = t - 1; i > 0; i--) {
            int j = (int)(xs64(rng) % (uint64_t)(i + 1));
            int tmp = perm[i]; perm[i] = perm[j]; perm[j] = tmp;
        }
        int cost = cost_of(perm, t, p, cnt, sums);
        if (cost == 0) return 1;
        int stale = 0;
        for (int mv = 0; mv < moves && stale < 4000; mv++) {
            int i = (int)(xs64(rng) % (uint64_t)t);
            int j = (int)(xs64(rng) % (uint64_t)t);
            if (i == j) continue;
            int tmp = perm[i]; perm[i] = perm[j]; perm[j] = tmp;
            int nc = cost_of(perm, t, p, cnt, sums);
            if (nc == 0) return 1;
            /* accept improvements and (rarely) sideways/worse moves */
            if (nc < cost) { cost = nc; stale = 0; }
            else if (nc == cost && (xs64(rng) & 3)) { stale++; }
            else if ((xs64(rng) & 63) == 0) { cost = nc; stale++; }
            else { tmp = perm[i]; perm[i] = perm[j]; perm[j] = tmp; stale++; }
        }
        (void)cand;
    }
    return 0;
}

/* randomized/deterministic DFS. budget 0 = unbounded. random iff rng != NULL.
 * returns 1 witness (wit = element values), 0 budget out, -1 exhausted. */
static int dfs2(const int *el, int t, int p, int *wit, uint64_t budget,
                uint64_t *rng, uint64_t *nodes_out) {
    int pos[64], sum[64], off[64], idx[64];
    uint64_t used = 0, seen0 = FORBID0 ? 1ULL : 0ULL, seen = seen0, nodes = 0;
    int d = 0;
    pos[0] = -1; sum[0] = 0;
    off[0] = rng ? (int)(xs64(rng) % (uint64_t)t) : 0;
    while (d >= 0) {
        int i = ++pos[d];
        if (i >= t) {
            d--;
            if (d >= 0) {
                used &= ~(1ULL << idx[d]);
                seen &= ~(1ULL << sum[d + 1]);
            }
            continue;
        }
        int ii = i + off[d]; if (ii >= t) ii -= t;
        if (used & (1ULL << ii)) continue;
        int ns = sum[d] + el[ii];
        if (ns >= p) ns -= p;
        if (seen & (1ULL << ns)) continue;
        nodes++;
        if (budget && nodes > budget) { *nodes_out += nodes; return 0; }
        used |= 1ULL << ii; seen |= 1ULL << ns;
        sum[d + 1] = ns; idx[d] = ii;
        if (d + 1 == t) {
            *nodes_out += nodes;
            for (int q = 0; q < t; q++) wit[q] = el[idx[q]];
            return 1;
        }
        d++; pos[d] = -1;
        off[d] = rng ? (int)(xs64(rng) % (uint64_t)t) : 0;
    }
    *nodes_out += nodes;
    return -1;
}

/* decide: 1 = witness (wit filled), 0 = NO valid ordering (complete).
 * tier_out: highest tier used (1..5). */
static int decide(const int *el, int t, int p, int *wit, uint64_t seed0,
                  uint64_t *maxnodes, int *tier_out) {
    uint64_t rng = seed0 ? seed0 : 1;
    int perm[64];
    *tier_out = 1;
    for (int tr = 0; tr < 64; tr++) {                     /* T1 */
        for (int i = 0; i < t; i++) perm[i] = el[i];
        for (int i = t - 1; i > 0; i--) {
            int j = (int)(xs64(&rng) % (uint64_t)(i + 1));
            int tmp = perm[i]; perm[i] = perm[j]; perm[j] = tmp;
        }
        if (valid(perm, t, p)) { memcpy(wit, perm, t * sizeof(int)); return 1; }
    }
    *tier_out = 2;                                        /* T2 */
    if (localsearch(el, t, p, perm, 8, 30000, &rng)) {
        memcpy(wit, perm, t * sizeof(int)); return 1;
    }
    *tier_out = 3;                                        /* T3 */
    {
        uint64_t nodes = 0;
        for (int i = 0; i < 16; i++) {
            uint64_t b = 100000ULL << (i < 8 ? i : 8);
            int r = dfs2(el, t, p, wit, b, &rng, &nodes);
            if (nodes > *maxnodes) *maxnodes = nodes;
            if (r == 1) return 1;
            if (r == -1) return 0;
        }
    }
    *tier_out = 4;                                        /* T4 */
    if (localsearch(el, t, p, perm, 192, 250000, &rng)) {
        memcpy(wit, perm, t * sizeof(int)); return 1;
    }
    *tier_out = 5;                                        /* T5: complete */
    {
        uint64_t nodes = 0;
        int r = dfs2(el, t, p, wit, 0, NULL, &nodes);
        if (nodes > *maxnodes) *maxnodes = nodes;
        return r == 1 ? 1 : 0;
    }
}

static void log_hard(int p, int t, uint64_t rank, const int *el, int tt,
                     int ok, const int *wit, int tier) {
    pthread_mutex_lock(&hardmu);
    if (hardf) {
        fprintf(hardf, "p=%d t=%d rank=%llu tier=%d A=", p, t,
                (unsigned long long)rank, tier);
        for (int i = 0; i < tt; i++)
            fprintf(hardf, "%d%c", el[i], i + 1 < tt ? ',' : ' ');
        if (ok) {
            fprintf(hardf, "wit=");
            for (int i = 0; i < tt; i++)
                fprintf(hardf, "%d%c", wit[i], i + 1 < tt ? ',' : '\n');
        } else fprintf(hardf, "NO-VALID-ORDERING\n");
        fflush(hardf);
    }
    pthread_mutex_unlock(&hardmu);
}

static void *worker(void *arg) {
    job_t *jb = (job_t *)arg;
    int t = jb->t, p = P;
    int k = t - 1, n = p - 2;
    int c[64], el[64], wit[64];
    for (int i = 0; i < k; i++) c[i] = i;
    uint64_t rank = 0;
    while (1) {
        if ((int)(rank % (uint64_t)NTHREADS) == jb->tid) {
            el[0] = 1;
            for (int i = 0; i < k; i++) el[i + 1] = c[i] + 2;
            uint64_t mask = 0;
            for (int i = 0; i < t; i++) mask |= 1ULL << el[i];
            int canon = 1;
            for (int i = 1; i < t && canon; i++) {
                int c0 = INV[el[i]];
                uint64_t m2 = 0;
                for (int q = 0; q < t; q++) m2 |= 1ULL << (el[q] * c0 % p);
                if (m2 < mask) canon = 0;
            }
            if (canon) {
                jb->reps++;
                uint64_t seed0 = SEED ^ (0xA24BAED4963EE407ULL * (rank + 1))
                                      ^ ((uint64_t)p << 32) ^ ((uint64_t)t << 20);
                int tier = 0;
                int ok = decide(el, t, p, wit, seed0, &jb->maxnodes, &tier);
                if (ok && WSAMPLE && rank % WSAMPLE == 0)
                    log_hard(p, t, rank, el, t, ok, wit, tier);
                if (tier >= 3 || !ok) {
                    jb->hard++;
                    if (tier == 3) jb->t3wit++;
                    if (tier == 4) jb->t4wit++;
                    if (tier == 5) jb->adjud++;
                    log_hard(p, t, rank, el, t, ok, wit, tier);
                }
                if (!ok) {
                    jb->fail++;
                    fprintf(stderr,
                            "*** COUNTEREXAMPLE CANDIDATE p=%d t=%d A=", p, t);
                    for (int i = 0; i < t; i++) fprintf(stderr, "%d ", el[i]);
                    fprintf(stderr, "***\n");
                }
            }
        }
        rank++;
        int i = k - 1;
        while (i >= 0 && c[i] == n - k + i) i--;
        if (i < 0) break;
        c[i]++;
        for (int j = i + 1; j < k; j++) c[j] = c[j - 1] + 1;
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc >= 3 && strcmp(argv[2], "-s") == 0) {
        /* single-set mode; optional trailing flags: -z (forbid 0 sums),
         * -l (deterministic complete DFS only => lexicographically minimal
         *     witness, value-ascending) */
        P = atoi(argv[1]);
        for (int x = 1; x < P; x++)
            for (int y = 1; y < P; y++) if (x * y % P == 1) INV[x] = y;
        int lexmin = 0;
        for (int a = 4; a < argc; a++) {
            if (strcmp(argv[a], "-z") == 0) FORBID0 = 1;
            if (strcmp(argv[a], "-l") == 0) lexmin = 1;
        }
        int el[64], t = 0, wit[64], tier = 0;
        char *tok = strtok(argv[3], ",");
        while (tok) { el[t++] = atoi(tok) % P; tok = strtok(NULL, ","); }
        /* sort ascending so -l yields the true lex-min ordering */
        for (int i = 1; i < t; i++)
            for (int j = i; j > 0 && el[j] < el[j - 1]; j--) {
                int tmp = el[j]; el[j] = el[j - 1]; el[j - 1] = tmp;
            }
        uint64_t mx = 0;
        int ok;
        if (lexmin) {
            uint64_t nodes = 0;
            ok = dfs2(el, t, P, wit, 0, NULL, &nodes) == 1;
            mx = nodes; tier = 5;
        } else
            ok = decide(el, t, P, wit, 12345, &mx, &tier);
        printf("p=%d t=%d forbid0=%d -> %s (tier %d, maxnodes %llu)\n",
               P, t, FORBID0, ok ? "WITNESS" : "NO-VALID-ORDERING", tier,
               (unsigned long long)mx);
        if (ok) {
            for (int i = 0; i < t; i++) printf("%d ", wit[i]);
            printf("\n");
        }
        return ok ? 0 : 1;
    }
    if (argc < 6) {
        fprintf(stderr, "usage: %s p tmin tmax nthreads seed [hardfile] [wsample]\n"
                        "       %s p -s a1,a2,... [-z] [-l]\n", argv[0], argv[0]);
        return 2;
    }
    P = atoi(argv[1]); TMIN = atoi(argv[2]); TMAX = atoi(argv[3]);
    NTHREADS = atoi(argv[4]); SEED = strtoull(argv[5], NULL, 0);
    if (argc > 6) hardf = fopen(argv[6], "a");
    if (argc > 7) WSAMPLE = strtoull(argv[7], NULL, 0);
    if (P < 3 || P > 62) { fprintf(stderr, "need 3<=p<=62\n"); return 2; }
    for (int x = 1; x < P; x++)
        for (int y = 1; y < P; y++) if (x * y % P == 1) INV[x] = y;
    for (int t = TMIN; t <= TMAX; t++) {
        struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
        pthread_t th[64]; job_t jb[64];
        for (int i = 0; i < NTHREADS; i++) {
            jb[i] = (job_t){ .t = t, .tid = i };
            pthread_create(&th[i], NULL, worker, &jb[i]);
        }
        uint64_t nr = 0, nh = 0, na = 0, nf = 0, mx = 0, w3 = 0, w4 = 0;
        for (int i = 0; i < NTHREADS; i++) {
            pthread_join(th[i], NULL);
            nr += jb[i].reps; nh += jb[i].hard; na += jb[i].adjud;
            nf += jb[i].fail; w3 += jb[i].t3wit; w4 += jb[i].t4wit;
            if (jb[i].maxnodes > mx) mx = jb[i].maxnodes;
        }
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double el = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
        printf("RESULT p=%d t=%d reps=%llu hard=%llu t3=%llu t4=%llu "
               "adjud=%llu fail=%llu maxnodes=%llu time=%.2fs\n",
               P, t, (unsigned long long)nr, (unsigned long long)nh,
               (unsigned long long)w3, (unsigned long long)w4,
               (unsigned long long)na, (unsigned long long)nf,
               (unsigned long long)mx, el);
        fflush(stdout);
    }
    if (hardf) fclose(hardf);
    return 0;
}
