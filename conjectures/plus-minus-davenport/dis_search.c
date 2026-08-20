/* dis2.c — maximum dissociated set size in a finite abelian group
 * (equivalently: plus-minus weighted Davenport constant D_pm(G) = dis(G)+1).
 *
 * Generalised engine: up to 6 cyclic factors, N = prod(moduli) <= 4096.
 * Exact integer/bitmask arithmetic; no floating point anywhere.
 *
 * A set S is dissociated iff all 2^|S| subset sums are distinct iff no
 * nonempty {+1,-1}-weighted subsequence sums to zero. DFS over element
 * indices in increasing order, one representative per {g,-g} pair (sound:
 * g -> min(g,-g) maps dissociated sets to dissociated sets bijectively on
 * the class of dissociated sets, since no dissociated set contains both g
 * and -g), state = bitmask of achievable nonzero signed sums, prune when 0
 * becomes achievable.
 *
 * Modes:
 *   ./dis2 max    n1 [n2 ...]            find dis(G) + witness
 *   ./dis2 all    n1 [n2 ...] T          count all representative-form
 *                                        dissociated T-sets (exhaustive)
 *   ./dis2 decide n1 [n2 ...] T          find one dissociated T-set or
 *                                        prove none (early exit on hit)
 * Optional suffix for any mode:  -r LO HI   restrict the ROOT branch to
 * representative indices [LO,HI) — shard for parallel runs; results from
 * shards over a partition of [0,nreps) compose exactly (searches are
 * disjoint: root element differs).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>

#define MAXN 4096
#define MAXW (MAXN/64)
#define MAXR 6
#define MAXD 64

static int N, W, R;
static int nm[MAXR];
static uint16_t *addtab;
static uint16_t negtab[MAXN];
static int reps[MAXN], nreps;
static uint64_t nodes, count_T;
static int bestlen, bestset[MAXD], cur[MAXD];
static int target_T, decide_mode, found_flag;
static int root_lo = 0, root_hi = -1;

static void decode(int g, int *d) {
    for (int i = R - 1; i >= 0; i--) { d[i] = g % nm[i]; g /= nm[i]; }
}
static int encode(const int *d) {
    int g = 0;
    for (int i = 0; i < R; i++) g = g * nm[i] + d[i];
    return g;
}

static void build(void) {
    N = 1;
    for (int i = 0; i < R; i++) N *= nm[i];
    W = (N + 63) / 64;
    addtab = malloc((size_t)N * N * sizeof(uint16_t));
    if (!addtab) { fprintf(stderr, "alloc fail\n"); exit(1); }
    int da[MAXR], db[MAXR], dc[MAXR];
    for (int a = 0; a < N; a++) {
        decode(a, da);
        for (int i = 0; i < R; i++) dc[i] = (nm[i] - da[i]) % nm[i];
        negtab[a] = (uint16_t)encode(dc);
        for (int b = 0; b < N; b++) {
            decode(b, db);
            for (int i = 0; i < R; i++) dc[i] = (da[i] + db[i]) % nm[i];
            addtab[(size_t)a * N + b] = (uint16_t)encode(dc);
        }
    }
    nreps = 0;
    for (int g = 1; g < N; g++)
        if (g <= negtab[g]) reps[nreps++] = g;
}

static inline void mset(uint64_t *m, int b) { m[b >> 6] |= 1ULL << (b & 63); }

static int apply_elem(const uint64_t *mask, int g, uint64_t *out) {
    const uint16_t *rowp = addtab + (size_t)g * N;
    const uint16_t *rowm = addtab + (size_t)negtab[g] * N;
    memcpy(out, mask, W * sizeof(uint64_t));
    for (int w = 0; w < W; w++) {
        uint64_t x = mask[w];
        while (x) {
            int s = (w << 6) + __builtin_ctzll(x);
            x &= x - 1;
            mset(out, rowp[s]);
            mset(out, rowm[s]);
        }
    }
    mset(out, g);
    mset(out, negtab[g]);
    return (out[0] & 1ULL) != 0;   /* zero element has index 0 */
}

static void dfs(int start, const uint64_t *mask, int depth) {
    nodes++;
    if (found_flag) return;
    if (target_T > 0) {
        if (depth == target_T) {
            count_T++;
            if (count_T == 1) memcpy(bestset, cur, depth * sizeof(int));
            if (decide_mode) found_flag = 1;
            return;
        }
        if (nreps - start < target_T - depth) return;
    } else if (depth > bestlen) {
        bestlen = depth;
        memcpy(bestset, cur, depth * sizeof(int));
    }
    int hi = (depth == 0 && root_hi >= 0) ? root_hi : nreps;
    int lo = (depth == 0) ? root_lo : start;
    uint64_t next[MAXW];
    for (int j = lo; j < hi; j++) {
        int g = reps[j];
        if (!apply_elem(mask, g, next)) {
            cur[depth] = g;
            dfs(j + 1, next, depth + 1);
            if (found_flag) return;
        }
    }
}

static void print_elem(int g) {
    int d[MAXR];
    decode(g, d);
    if (R == 1) { printf("%d", d[0]); return; }
    printf("(");
    for (int i = 0; i < R; i++) printf("%s%d", i ? "," : "", d[i]);
    printf(")");
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s max|all|decide n1 [n2 ...] [T] [-r LO HI]\n", argv[0]); return 2; }
    const char *mode = argv[1];
    int nums[16], nn = 0;
    int i = 2;
    for (; i < argc; i++) {
        if (!strcmp(argv[i], "-r")) {
            root_lo = atoi(argv[i + 1]);
            root_hi = atoi(argv[i + 2]);
            i += 2;
        } else nums[nn++] = atoi(argv[i]);
    }
    int T = 0, nmods = nn;
    if (!strcmp(mode, "all") || !strcmp(mode, "decide")) { T = nums[nn - 1]; nmods = nn - 1; }
    if (nmods < 1 || nmods > MAXR) { fprintf(stderr, "1..%d moduli\n", MAXR); return 2; }
    R = nmods;
    for (int k = 0; k < R; k++) nm[k] = nums[k];
    build();
    if (N > MAXN) { fprintf(stderr, "N too big\n"); return 2; }

    uint64_t mask0[MAXW];
    memset(mask0, 0, W * sizeof(uint64_t));
    nodes = 0; count_T = 0; found_flag = 0;

    char gname[128], *p = gname;
    for (int k = 0; k < R; k++) p += sprintf(p, "%s%d", k ? "x" : "", nm[k]);

    if (!strcmp(mode, "max")) {
        target_T = 0; decide_mode = 0; bestlen = 0;
        dfs(0, mask0, 0);
        printf("group=%s N=%d dis=%d Dpm=%d nodes=%" PRIu64 " root=[%d,%d) witness=",
               gname, N, bestlen, bestlen + 1, nodes, root_lo, root_hi < 0 ? nreps : root_hi);
        for (int k = 0; k < bestlen; k++) { if (k) printf(","); print_elem(bestset[k]); }
        printf("\n");
    } else if (!strcmp(mode, "all")) {
        target_T = T; decide_mode = 0;
        dfs(0, mask0, 0);
        printf("group=%s N=%d T=%d count=%" PRIu64 " nodes=%" PRIu64 " root=[%d,%d)\n",
               gname, N, T, count_T, nodes, root_lo, root_hi < 0 ? nreps : root_hi);
        if (count_T) {
            printf("first=");
            for (int k = 0; k < T; k++) { if (k) printf(","); print_elem(bestset[k]); }
            printf("\n");
        }
    } else if (!strcmp(mode, "decide")) {
        target_T = T; decide_mode = 1;
        dfs(0, mask0, 0);
        printf("group=%s N=%d T=%d exists=%s nodes=%" PRIu64 " root=[%d,%d)\n",
               gname, N, T, count_T ? "YES" : "NO", nodes, root_lo, root_hi < 0 ? nreps : root_hi);
        if (count_T) {
            printf("witness=");
            for (int k = 0; k < T; k++) { if (k) printf(","); print_elem(bestset[k]); }
            printf("\n");
        }
    } else { fprintf(stderr, "unknown mode\n"); return 2; }
    free(addtab);
    return 0;
}
