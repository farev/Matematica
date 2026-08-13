/* dss_search_basic.c — UNOPTIMIZED reference engine (kept verbatim as a
 * second implementation of the identical tree; node counts must match
 * dss_search.c and dss_reference.py exactly on full traversals).
 *
 * Original header: exhaustive search for n-element sets of positive integers
 * with all 2^n subset sums distinct (DSS sets) and largest element exactly m.
 *
 * Question answered per run: does a DSS n-set with max element = m exist?
 * Sweeping m upward from f(n-1) and taking the first FOUND gives
 * f(n) = A276661(n), the least possible largest element.
 *
 * Method: descending construction a_n = m > a_{n-1} > ... > a_1 >= 1.
 * State: bitset of achievable subset sums of the chosen suffix.
 * A candidate a collides iff sums & (sums << a) != 0 (two subsets of the
 * new set would share a sum); this incremental test is exact by induction
 * on the largest element in which two colliding subsets differ.
 *
 * Exact prunes (all integer arithmetic, no floats anywhere):
 *   P1 window:   with r elements left to choose below current min c, the
 *                next element a (the largest remaining, i.e. the r-th
 *                smallest of the final set) satisfies fmin[r] <= a <= c-1,
 *                where fmin[r] = f(r) is the known minimal max of an
 *                r-element DSS set (bootstrap: the ladder re-derives f(r)
 *                for r = 1..9 in increasing order before any level uses it).
 *   P2 sum:      total + a + sum_{j=1..r-1}(a-j) >= 2^n - 1, since the 2^n
 *                distinct subset sums are nonnegative integers <= total sum.
 *                Monotone in a -> break the descending loop on failure.
 *   P3 moment:   sqsum + a^2 + sum_{j=1..r-1}(a-j)^2 >= (4^n - 1)/3.
 *                (Erdos-Moser second moment: the 2^n subset sums have
 *                variance sum(a_i^2)/4 and 2^n distinct integers have
 *                variance >= (4^n-1)/12.) Monotone in a -> break.
 *   P4 collide:  bitset test above (not monotone -> skip, don't break).
 *
 * Output: RESULT line with status FOUND/NONE, exact node counts per depth
 * (deterministic for full traversals), wall time, thread count.
 * In --enum mode all solutions at (n, m) are printed, not just the first.
 *
 * Build: gcc -O3 -march=native -fopenmp -o dss_search dss_search.c
 * Usage: ./dss_search n m [--enum] [--threads T] [--split D]
 */
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif

typedef uint64_t u64;

#define MAXN 12
#define MAXW 128            /* 8192 bits of sum space: enough for n*m <= 8191 */

/* f(r) = A276661(r) for r = 0..9; ladder order keeps the bootstrap honest:
 * a level-n run consults only r <= n-1, which earlier levels re-derived. */
static const int fmin[10] = {0, 1, 2, 4, 7, 13, 24, 44, 84, 161};

static int N, M, ENUM = 0, SPLIT = 3;
static u64 TARGET_SUM;      /* 2^N - 1 */
static u64 TARGET_SQ;       /* (4^N - 1)/3 */

static volatile int g_found = 0;

typedef struct {
    int depth;              /* elements chosen so far */
    int chosen[MAXN];
    u64 total, sqsum;
    int nw;                 /* active words in sums */
    u64 sums[MAXW];
} State;

typedef struct { u64 nodes[MAXN + 1]; u64 solutions; } Stats;

/* shift-test-merge: out = S | (S << a); returns 0 on collision */
static inline int add_elem(const u64 *S, int nw, int a, u64 total,
                           u64 *out, int *out_nw)
{
    int q = a >> 6, s = a & 63;
    int nw2 = (int)((total + (u64)a) >> 6) + 1;
    for (int i = 0; i < nw2; i++) {
        u64 lo = (i >= q && i - q < nw) ? S[i - q] : 0;
        u64 hi = (s && i > q && i - q - 1 < nw) ? S[i - q - 1] : 0;
        u64 sh = s ? ((lo << s) | (hi >> (64 - s))) : lo;
        u64 orig = (i < nw) ? S[i] : 0;
        if (sh & orig) return 0;
        out[i] = sh | orig;
    }
    *out_nw = nw2;
    return 1;
}

static void report_solution(const int *chosen, int n)
{
    #pragma omp critical(solout)
    {
        printf("SOLUTION n=%d m=%d set=", N, M);
        for (int i = n - 1; i >= 0; i--)
            printf("%d%c", chosen[i], i ? ',' : '\n');
        fflush(stdout);
    }
}

/* recursive full search below a state */
static void search(State *st, Stats *stats)
{
    if (!ENUM && g_found) return;
    int r = N - st->depth;
    if (r == 0) {
        stats->solutions++;
        report_solution(st->chosen, N);
        if (!ENUM) g_found = 1;
        return;
    }
    int c = st->chosen[st->depth - 1];
    int lo = fmin[r], hi = c - 1;
    for (int a = hi; a >= lo; a--) {
        /* P2 + P3, both monotone increasing in a */
        u64 msum = st->total + (u64)a, msq = st->sqsum + (u64)a * a;
        for (int j = 1; j <= r - 1; j++) {
            u64 v = (u64)(a - j);
            msum += v; msq += v * v;
        }
        if (msum < TARGET_SUM || msq < TARGET_SQ) break;
        State child;
        if (!add_elem(st->sums, st->nw, a, st->total, child.sums, &child.nw))
            continue;                                   /* P4 */
        child.depth = st->depth + 1;
        memcpy(child.chosen, st->chosen, sizeof(int) * st->depth);
        child.chosen[st->depth] = a;
        child.total = st->total + (u64)a;
        child.sqsum = st->sqsum + (u64)a * a;
        stats->nodes[child.depth]++;
        search(&child, stats);
        if (!ENUM && g_found) return;
    }
}

/* enumerate prefix states down to depth SPLIT (counting those nodes),
 * collecting the depth-SPLIT states as parallel tasks */
static void gen_prefix(State *st, Stats *stats, State **tasks,
                       int *ntasks, int *cap)
{
    int r = N - st->depth;
    if (r == 0) {           /* only reachable when N <= SPLIT (tiny runs) */
        stats->solutions++;
        report_solution(st->chosen, N);
        if (!ENUM) g_found = 1;
        return;
    }
    if (st->depth == SPLIT) {
        if (*ntasks == *cap) {
            *cap *= 2;
            *tasks = realloc(*tasks, sizeof(State) * (size_t)*cap);
        }
        (*tasks)[(*ntasks)++] = *st;
        return;
    }
    int c = st->chosen[st->depth - 1];
    int lo = fmin[r], hi = c - 1;
    for (int a = hi; a >= lo; a--) {
        u64 msum = st->total + (u64)a, msq = st->sqsum + (u64)a * a;
        for (int j = 1; j <= r - 1; j++) {
            u64 v = (u64)(a - j);
            msum += v; msq += v * v;
        }
        if (msum < TARGET_SUM || msq < TARGET_SQ) break;
        State child;
        if (!add_elem(st->sums, st->nw, a, st->total, child.sums, &child.nw))
            continue;
        child.depth = st->depth + 1;
        memcpy(child.chosen, st->chosen, sizeof(int) * st->depth);
        child.chosen[st->depth] = a;
        child.total = st->total + (u64)a;
        child.sqsum = st->sqsum + (u64)a * a;
        stats->nodes[child.depth]++;
        gen_prefix(&child, stats, tasks, ntasks, cap);
    }
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: %s n m [--enum] [--threads T] [--split D]\n", argv[0]); return 2; }
    N = atoi(argv[1]); M = atoi(argv[2]);
    int nthreads = 0;
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "--enum")) ENUM = 1;
        else if (!strcmp(argv[i], "--threads")) nthreads = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--split")) SPLIT = atoi(argv[++i]);
    }
    if (N < 2 || N > 10 || M < 1 || (u64)N * (u64)M >= 64u * MAXW) {
        fprintf(stderr, "bad n/m\n"); return 2;
    }
    if (SPLIT >= N) SPLIT = N - 1;
    TARGET_SUM = ((u64)1 << N) - 1;
    TARGET_SQ  = (((u64)1 << (2 * N)) - 1) / 3;
#ifdef _OPENMP
    if (nthreads > 0) omp_set_num_threads(nthreads);
#endif

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    State root;
    root.depth = 1; root.chosen[0] = M;
    root.total = (u64)M; root.sqsum = (u64)M * M;
    root.nw = (int)(root.total >> 6) + 1;
    memset(root.sums, 0, sizeof(u64) * (size_t)(root.nw));
    root.sums[0] = 1;                       /* empty subset: sum 0 */
    root.sums[M >> 6] |= (u64)1 << (M & 63);/* subset {m}: sum m   */
    if ((M >> 6) >= root.nw) root.nw = (M >> 6) + 1;

    Stats total_stats; memset(&total_stats, 0, sizeof total_stats);
    total_stats.nodes[1] = 1;

    int cap = 1 << 12, ntasks = 0;
    State *tasks = malloc(sizeof(State) * (size_t)cap);
    gen_prefix(&root, &total_stats, &tasks, &ntasks, &cap);

    #pragma omp parallel
    {
        Stats local; memset(&local, 0, sizeof local);
        #pragma omp for schedule(dynamic, 1)
        for (int i = 0; i < ntasks; i++) {
            if (!ENUM && g_found) continue;
            search(&tasks[i], &local);
        }
        #pragma omp critical(statmerge)
        {
            for (int d = 0; d <= MAXN; d++) total_stats.nodes[d] += local.nodes[d];
            total_stats.solutions += local.solutions;
        }
    }
    free(tasks);

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double secs = (double)(t1.tv_sec - t0.tv_sec) + 1e-9 * (double)(t1.tv_nsec - t0.tv_nsec);

    u64 tot = 0;
    for (int d = 0; d <= MAXN; d++) tot += total_stats.nodes[d];
    int usedthreads = 1;
#ifdef _OPENMP
    usedthreads = omp_get_max_threads();
#endif
    printf("RESULT n=%d m=%d status=%s solutions=%llu nodes=%llu depth_nodes=",
           N, M, total_stats.solutions ? "FOUND" : "NONE",
           (unsigned long long)total_stats.solutions, (unsigned long long)tot);
    for (int d = 1; d <= N; d++)
        printf("%llu%c", (unsigned long long)total_stats.nodes[d], d < N ? ',' : ' ');
    printf("tasks=%d time=%.3f threads=%d\n", ntasks, secs, usedthreads);
    return 0;
}
