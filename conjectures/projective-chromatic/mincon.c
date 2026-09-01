/* Min-conflicts + random-walk search for proper k-colorings of PG(n-1,2).
 * Generic in n (2..8) and k. Move: pick a random monochromatic line, pick a
 * random point on it, recolor it to the color minimizing its conflict count
 * (ties random); with probability WALK, recolor to a uniform random color.
 * Prints witnesses (one line per witness) and stats. Used both to hunt at
 * n=8 k=5 and to sample the witness space at n=7 k=5.
 *
 * Usage: ./mincon n k seed max_witnesses max_seconds [walk_pct]
 * Witness lines start with "W " then comma-separated colors of points 1..M.
 * Every printed witness is independently re-verified in Python downstream.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static int N, K, M, NLINES;
static int (*lines_)[3];
static int **plines; /* per point: list of line ids */
static int *npl;
static int *color;
static int (*lcc)[8]; /* line color counts, K<=8 */
static int *monolist; /* ids of currently monochromatic lines */
static int *monopos;  /* line id -> position in monolist or -1 */
static int nmono;
static int *weight;   /* breakout: per-line weight, bumped at local minima */

static uint64_t rng_s;
static inline uint64_t rnd(void) {
    rng_s ^= rng_s << 13; rng_s ^= rng_s >> 7; rng_s ^= rng_s << 17;
    return rng_s;
}

static void mono_add(int li) {
    if (monopos[li] < 0) { monopos[li] = nmono; monolist[nmono++] = li; }
}
static void mono_del(int li) {
    int p = monopos[li];
    if (p >= 0) {
        int last = monolist[--nmono];
        monolist[p] = last; monopos[last] = p; monopos[li] = -1;
    }
}

static void build(void) {
    M = (1 << N) - 1;
    NLINES = M * (M - 1) / 6;
    lines_ = malloc(sizeof(int[3]) * NLINES);
    int c = 0;
    for (int x = 1; x <= M; x++)
        for (int y = x + 1; y <= M; y++) {
            int z = x ^ y;
            if (z > y) { lines_[c][0] = x; lines_[c][1] = y; lines_[c][2] = z; c++; }
        }
    if (c != NLINES) { fprintf(stderr, "bad line count\n"); exit(1); }
    npl = calloc(M + 1, sizeof(int));
    for (int i = 0; i < NLINES; i++)
        for (int j = 0; j < 3; j++) npl[lines_[i][j]]++;
    plines = malloc((M + 1) * sizeof(int *));
    for (int p = 1; p <= M; p++) { plines[p] = malloc(npl[p] * sizeof(int)); npl[p] = 0; }
    for (int i = 0; i < NLINES; i++)
        for (int j = 0; j < 3; j++) {
            int p = lines_[i][j];
            plines[p][npl[p]++] = i;
        }
    color = malloc((M + 1) * sizeof(int));
    lcc = malloc(sizeof(int[8]) * NLINES);
    monolist = malloc(NLINES * sizeof(int));
    monopos = malloc(NLINES * sizeof(int));
    weight = malloc(NLINES * sizeof(int));
    for (int i = 0; i < NLINES; i++) weight[i] = 1;
}

static void init_random(void) {
    for (int p = 1; p <= M; p++) color[p] = rnd() % K;
    memset(lcc, 0, sizeof(int[8]) * NLINES);
    nmono = 0;
    for (int i = 0; i < NLINES; i++) monopos[i] = -1;
    for (int i = 0; i < NLINES; i++) {
        for (int j = 0; j < 3; j++) lcc[i][color[lines_[i][j]]]++;
        for (int cc = 0; cc < K; cc++) if (lcc[i][cc] == 3) mono_add(i);
    }
}

static void recolor(int p, int nc) {
    int oc = color[p];
    if (oc == nc) return;
    for (int t = 0; t < npl[p]; t++) {
        int li = plines[p][t];
        if (lcc[li][oc] == 3) mono_del(li);
        lcc[li][oc]--;
        lcc[li][nc]++;
        if (lcc[li][nc] == 3) mono_add(li);
    }
    color[p] = nc;
}

/* weighted conflicts point p would have with color c = sum of weights of
 * lines through p whose other two points both have color c */
static int conf(int p, int c) {
    int oc = color[p], cnt = 0;
    for (int t = 0; t < npl[p]; t++) {
        int li = plines[p][t];
        int cc = lcc[li][c] - (oc == c ? 1 : 0);
        if (cc == 2) cnt += weight[li];
    }
    return cnt;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: mincon n k seed max_wit max_sec [walk_pct]\n"); return 2; }
    N = atoi(argv[1]); K = atoi(argv[2]);
    rng_s = strtoull(argv[3], 0, 10); if (!rng_s) rng_s = 1;
    int maxwit = atoi(argv[4]);
    long maxsec = atol(argv[5]);
    int walk_pct = argc > 6 ? atoi(argv[6]) : 15;
    build();
    time_t t0 = time(0);
    long flips = 0, restarts = 0;
    int found = 0, best = 1 << 30;
    init_random();
    long since_best = 0;
    int local_best = NLINES;
    while (time(0) - t0 < maxsec && found < maxwit) {
        if (nmono == 0) {
            printf("W ");
            for (int p = 1; p <= M; p++) printf("%d%s", color[p], p == M ? "\n" : ",");
            fflush(stdout);
            found++;
            restarts++;
            init_random();
            local_best = NLINES; since_best = 0;
            continue;
        }
        int li = monolist[rnd() % nmono];
        /* breakout move: best (point,color) over the 3 points x (K-1) colors
         * by weighted delta; random walk with small prob */
        if (rnd() % 100 < (unsigned)walk_pct) {
            int p = lines_[li][rnd() % 3];
            recolor(p, rnd() % K);
        } else {
            int bp = -1, bc = -1, bestv = 1 << 30, nties = 0;
            for (int j = 0; j < 3; j++) {
                int p = lines_[li][j];
                int oc = color[p];
                int cur = conf(p, oc); /* weighted mono through p now (its own color) */
                for (int c = 0; c < K; c++) {
                    if (c == oc) continue;
                    int v = conf(p, c) - cur; /* weighted delta for lines through p */
                    if (v < bestv) { bestv = v; bp = p; bc = c; nties = 1; }
                    else if (v == bestv) { nties++; if (rnd() % nties == 0) { bp = p; bc = c; } }
                }
            }
            if (bestv > 0) {
                /* local minimum w.r.t. this line: bump weights of all current
                 * mono lines (breakout), then take the move anyway */
                for (int t = 0; t < nmono; t++) weight[monolist[t]]++;
            }
            recolor(bp, bc);
        }
        flips++;
        if (nmono < local_best) { local_best = nmono; since_best = 0; } else since_best++;
        if (nmono < best) best = nmono;
        if (since_best > 20000000) {
            restarts++; init_random(); local_best = NLINES; since_best = 0;
            for (int i = 0; i < NLINES; i++) weight[i] = 1;
        }
    }
    fprintf(stderr, "n=%d k=%d seed=%llu: %d witnesses, best=%d, flips=%ld, restarts=%ld, %lds\n",
            N, K, (unsigned long long)rng_s, found, best, flips, restarts, (long)(time(0) - t0));
    return found ? 0 : 1;
}
