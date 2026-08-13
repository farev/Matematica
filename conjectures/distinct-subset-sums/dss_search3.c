/* dss_search3.c — difference-set engine for the DSS search.
 *
 * Same problem and same tree as dss_search.c (see that header for the
 * mathematical setup and prunes P1-P4), but the state carried per node is the
 * DIFFERENCE SET of the achievable subset sums, not the sums themselves:
 *
 *   D(T) = { x - y : x > y achievable sums of the chosen suffix T }.
 *
 * A candidate a collides iff a is a difference of two achievable sums,
 * i.e. iff bit a of D is set — an O(1) test replacing the per-candidate
 * bitset convolution of dss_search.c. When an element a is accepted, the new
 * sums are S ∪ (S + a), so the new differences are exactly
 *
 *   D' = D ∪ (D + a) ∪ (D - a)|>0 ∪ (a - D)|>0 ∪ {a}.
 *
 * The (a - D) term is a bit-reversal around a, so the engine also maintains
 * R = reverse of D within the fixed LB = 64*W - 1 frame:
 *   R bit k = D bit (LB - k).
 * Then (a - D)|>0 = (R >> (LB - a)) restricted to bits 1..a-1, and bit 0 of
 * that word is automatically clear because the candidate was accepted
 * (a not in D). R is updated by the mirrored formula. Bits shifted above
 * LB fall off the top word, which is exactly the right semantics because
 * LB bounds the largest achievable sum (LB >= n*m).
 *
 * Modes:
 *   default: node-for-node identical tree to dss_search.c — node counts on
 *            full traversals must match it and dss_reference.py exactly.
 *   --tight: replaces the consecutive-integer window caps by exact caps over
 *            the true candidate pool. Every future element lies in
 *            V = [1, c-1] \ D, because D only grows down the tree, so an
 *            element equal to a current difference can never be added later.
 *            The node builds V as a descending array with prefix sums and
 *            prefix squares; the candidate loop then iterates only over V,
 *            enforcing per candidate a = V[i]:
 *              - a >= fmin[r]                                   (P1)
 *              - at least r-1 further members of V below a      (pool size)
 *              - total + a + (sum of the r-1 largest members of V below a)
 *                    >= 2^n - 1                                 (tight P2)
 *              - sqsum + a^2 + (their squares) >= (4^n - 1)/3   (tight P3)
 *            All four conditions are monotone along the descending iteration,
 *            so each failure is a break, not a skip. This is strictly
 *            stronger than the default prunes (V-caps <= consecutive caps),
 *            hence shrinks the tree; statuses and solution sets must be
 *            unchanged vs the default mode.
 *            (V is NOT truncated at fmin[r]: only the largest remaining
 *            element must clear fmin[r]; smaller ones may lie below it.)
 *
 * Build: gcc -O3 -march=native -fopenmp -o dss_search3 dss_search3.c
 * Usage: ./dss_search3 n m [--enum] [--tight] [--threads T] [--split D]
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
#define MAXW 128
#define VCAP 1100

static const int fmin[10] = {0, 1, 2, 4, 7, 13, 24, 44, 84, 161};

static int N, M, W, LB, ENUM = 0, TIGHT = 0, SPLIT = 3;
static u64 TARGET_SUM, TARGET_SQ;
static volatile int g_found = 0;

typedef struct {
    int depth;
    int chosen[MAXN];
    u64 total, sqsum;
    u64 D[MAXW], R[MAXW];
} State;

typedef struct { u64 nodes[MAXN + 1]; u64 solutions; } Stats;

static inline int getbit(const u64 *B, int i)
{
    return (int)((B[i >> 6] >> (i & 63)) & 1u);
}
static inline void setbit(u64 *B, int i) { B[i >> 6] |= (u64)1 << (i & 63); }

/* dst |= src << s (bits above LB fall off the top; s >= 0) */
static inline void or_shl(u64 *dst, const u64 *src, int s)
{
    int q = s >> 6, b = s & 63;
    if (b) {
        for (int i = W - 1; i > q; i--)
            dst[i] |= (src[i - q] << b) | (src[i - q - 1] >> (64 - b));
        if (q < W) dst[q] |= src[0] << b;
    } else {
        for (int i = W - 1; i >= q; i--) dst[i] |= src[i - q];
    }
}
/* dst |= src >> s */
static inline void or_shr(u64 *dst, const u64 *src, int s)
{
    int q = s >> 6, b = s & 63;
    if (b) {
        for (int i = 0; i < W - q - 1; i++)
            dst[i] |= (src[i + q] >> b) | (src[i + q + 1] << (64 - b));
        if (q < W) dst[W - q - 1] |= src[W - 1] >> b;
    } else {
        for (int i = 0; i + q < W; i++) dst[i] |= src[i + q];
    }
}

/* child D/R from parent after accepting element a */
static void make_child(const State *p, State *ch, int a)
{
    memcpy(ch->D, p->D, sizeof(u64) * (size_t)W);
    memcpy(ch->R, p->R, sizeof(u64) * (size_t)W);
    or_shl(ch->D, p->D, a);
    or_shr(ch->D, p->D, a);
    or_shr(ch->D, p->R, LB - a);
    setbit(ch->D, a);
    or_shr(ch->R, p->R, a);
    or_shl(ch->R, p->R, a);
    or_shl(ch->R, p->D, LB - a);
    setbit(ch->R, LB - a);
}

/* --tight helper: extract V = [1, hi] \ D as a descending array with prefix
 * sums / prefix squares: ps[i] = sum of vals[0..i-1] (the i largest members
 * of V), psq[i] likewise for squares. Returns the number of members. */
static inline int build_valid(const u64 *D, int hi, int *vals,
                              u64 *ps, u64 *psq)
{
    int nv = 0;
    ps[0] = 0; psq[0] = 0;
    for (int a = hi; a >= 1; a--)
        if (!getbit(D, a)) {
            vals[nv] = a;
            ps[nv + 1] = ps[nv] + (u64)a;
            psq[nv + 1] = psq[nv] + (u64)a * (u64)a;
            nv++;
        }
    return nv;
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
    if (hi < lo) return;
    if (TIGHT) {
        int vals[VCAP]; u64 ps[VCAP + 1], psq[VCAP + 1];
        int nv = build_valid(st->D, hi, vals, ps, psq);
        if (nv < r) return;
        for (int i = 0; i < nv; i++) {
            int a = vals[i];
            if (a < lo) break;                       /* P1 */
            if (i + r > nv) break;                   /* pool exhausted */
            u64 caps = (u64)a + (ps[i + r] - ps[i + 1]);
            u64 capq = (u64)a * (u64)a + (psq[i + r] - psq[i + 1]);
            if (st->total + caps < TARGET_SUM ||
                st->sqsum + capq < TARGET_SQ) break; /* tight P2/P3 */
            State child;
            child.depth = st->depth + 1;
            memcpy(child.chosen, st->chosen, sizeof(int) * st->depth);
            child.chosen[st->depth] = a;
            child.total = st->total + (u64)a;
            child.sqsum = st->sqsum + (u64)a * a;
            make_child(st, &child, a);
            stats->nodes[child.depth]++;
            search(&child, stats);
            if (!ENUM && g_found) return;
        }
        return;
    }
    u64 g = 0, h = 0;
    for (int j = 0; j <= r - 1; j++) {
        u64 v = (u64)(hi - j);
        g += v; h += v * v;
    }
    for (int a = hi; a >= lo; a--) {
        if (st->total + g < TARGET_SUM || st->sqsum + h < TARGET_SQ) break;
        if (!getbit(st->D, a)) {
            State child;
            child.depth = st->depth + 1;
            memcpy(child.chosen, st->chosen, sizeof(int) * st->depth);
            child.chosen[st->depth] = a;
            child.total = st->total + (u64)a;
            child.sqsum = st->sqsum + (u64)a * a;
            make_child(st, &child, a);
            stats->nodes[child.depth]++;
            search(&child, stats);
            if (!ENUM && g_found) return;
        }
        h -= 2 * g - (u64)r;
        g -= (u64)r;
    }
}

static void gen_prefix(State *st, Stats *stats, State **tasks,
                       int *ntasks, int *cap)
{
    int r = N - st->depth;
    if (r == 0) {
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
    if (hi < lo) return;
    if (TIGHT) {
        int vals[VCAP]; u64 ps[VCAP + 1], psq[VCAP + 1];
        int nv = build_valid(st->D, hi, vals, ps, psq);
        if (nv < r) return;
        for (int i = 0; i < nv; i++) {
            int a = vals[i];
            if (a < lo) break;
            if (i + r > nv) break;
            u64 caps = (u64)a + (ps[i + r] - ps[i + 1]);
            u64 capq = (u64)a * (u64)a + (psq[i + r] - psq[i + 1]);
            if (st->total + caps < TARGET_SUM ||
                st->sqsum + capq < TARGET_SQ) break;
            State child;
            child.depth = st->depth + 1;
            memcpy(child.chosen, st->chosen, sizeof(int) * st->depth);
            child.chosen[st->depth] = a;
            child.total = st->total + (u64)a;
            child.sqsum = st->sqsum + (u64)a * a;
            make_child(st, &child, a);
            stats->nodes[child.depth]++;
            gen_prefix(&child, stats, tasks, ntasks, cap);
        }
        return;
    }
    u64 g = 0, h = 0;
    for (int j = 0; j <= r - 1; j++) {
        u64 v = (u64)(hi - j);
        g += v; h += v * v;
    }
    for (int a = hi; a >= lo; a--) {
        if (st->total + g < TARGET_SUM || st->sqsum + h < TARGET_SQ) break;
        if (!getbit(st->D, a)) {
            State child;
            child.depth = st->depth + 1;
            memcpy(child.chosen, st->chosen, sizeof(int) * st->depth);
            child.chosen[st->depth] = a;
            child.total = st->total + (u64)a;
            child.sqsum = st->sqsum + (u64)a * a;
            make_child(st, &child, a);
            stats->nodes[child.depth]++;
            gen_prefix(&child, stats, tasks, ntasks, cap);
        }
        h -= 2 * g - (u64)r;
        g -= (u64)r;
    }
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: %s n m [--enum] [--tight] [--threads T] [--split D]\n", argv[0]); return 2; }
    N = atoi(argv[1]); M = atoi(argv[2]);
    int nthreads = 0;
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "--enum")) ENUM = 1;
        else if (!strcmp(argv[i], "--tight")) TIGHT = 1;
        else if (!strcmp(argv[i], "--threads")) nthreads = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--split")) SPLIT = atoi(argv[++i]);
    }
    if (N < 2 || N > 10 || M < 1 || M >= VCAP || (u64)N * (u64)M >= 64u * MAXW - 64) {
        fprintf(stderr, "bad n/m\n"); return 2;
    }
    if (SPLIT >= N) SPLIT = N - 1;
    W = (int)(((u64)N * (u64)M) / 64 + 2);
    LB = 64 * W - 1;
    TARGET_SUM = ((u64)1 << N) - 1;
    TARGET_SQ  = (((u64)1 << (2 * N)) - 1) / 3;
#ifdef _OPENMP
    if (nthreads > 0) omp_set_num_threads(nthreads);
#endif
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    State root;
    memset(&root, 0, sizeof root);
    root.depth = 1; root.chosen[0] = M;
    root.total = (u64)M; root.sqsum = (u64)M * M;
    setbit(root.D, M);            /* sums {0, m}: the only difference is m */
    setbit(root.R, LB - M);

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
    printf("tasks=%d time=%.3f threads=%d mode=%s\n", ntasks, secs, usedthreads,
           TIGHT ? "tight" : "exact");
    return 0;
}
