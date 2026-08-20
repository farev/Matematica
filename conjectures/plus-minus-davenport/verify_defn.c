/* verify_defn.c — definitional exhaustion, algorithmically independent of
 * dis_search.c.
 *
 * Enumerates T-subsets of ALL N group elements (0 included — it always
 * fails) in increasing index order and tests dissociatedness by the
 * definition itself: the 2^k subset sums, tracked as a bitmask over G,
 * must be pairwise distinct. Incremental step: shifted = mask + g; the new
 * sums are distinct among themselves automatically (s -> s+g is a
 * bijection), so distinctness of the union needs exactly
 * mask & shifted == 0. A subset with a colliding prefix is skipped,
 * justified by definitional monotonicity: two equal sub-subset sums of the
 * prefix are equal sub-subset sums of every superset.
 *
 * No {+1,-1} weights, no signed sums, no representative reduction
 * anywhere: this is a different predicate and a different search space
 * from dis_search.c; the two agree only through the (proved) equivalence
 * lemma L1 and the normalization lemma L5 of NOTE.md.
 *
 * Usage: ./verify_defn n1 [n2 ...] T        (up to 6 moduli, N <= 1024)
 * Prints: number of dissociated T-subsets, nodes, extensions tried.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>

#define MAXN 1024
#define MAXW (MAXN/64)
#define MAXR 6

static int N, W, R, T;
static int nm[MAXR];
static uint16_t *addtab;
static uint64_t nodes, found, leaves;
static int cur[64];
static int first_printed;

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
        for (int b = 0; b < N; b++) {
            decode(b, db);
            for (int i = 0; i < R; i++) dc[i] = (da[i] + db[i]) % nm[i];
            addtab[(size_t)a * N + b] = (uint16_t)encode(dc);
        }
    }
}

static int step(const uint64_t *mask, int g, uint64_t *out) {
    uint64_t shifted[MAXW];
    memset(shifted, 0, W * sizeof(uint64_t));
    const uint16_t *row = addtab + (size_t)g * N;
    for (int w = 0; w < W; w++) {
        uint64_t x = mask[w];
        while (x) {
            int s = (w << 6) + __builtin_ctzll(x);
            x &= x - 1;
            int t = row[s];
            shifted[t >> 6] |= 1ULL << (t & 63);
        }
    }
    for (int w = 0; w < W; w++)
        if (mask[w] & shifted[w]) return 1;
    for (int w = 0; w < W; w++) out[w] = mask[w] | shifted[w];
    return 0;
}

static void print_elem(int g) {
    int d[MAXR];
    decode(g, d);
    if (R == 1) { printf("%d", d[0]); return; }
    printf("(");
    for (int i = 0; i < R; i++) printf("%s%d", i ? "," : "", d[i]);
    printf(")");
}

static void dfs(int start, const uint64_t *mask, int depth) {
    nodes++;
    if (depth == T) {
        found++;
        if (!first_printed) {
            first_printed = 1;
            printf("first_witness=");
            for (int i = 0; i < T; i++) { if (i) printf(","); print_elem(cur[i]); }
            printf("\n");
        }
        return;
    }
    if (N - start < T - depth) return;
    uint64_t next[MAXW];
    for (int g = start; g < N; g++) {
        leaves++;
        if (!step(mask, g, next)) {
            cur[depth] = g;
            dfs(g + 1, next, depth + 1);
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s n1 [n2 ...] T\n", argv[0]); return 2; }
    int nums[16], nn = 0;
    for (int i = 1; i < argc && nn < 16; i++) nums[nn++] = atoi(argv[i]);
    T = nums[nn - 1];
    R = nn - 1;
    if (R < 1 || R > MAXR) { fprintf(stderr, "1..%d moduli\n", MAXR); return 2; }
    for (int i = 0; i < R; i++) nm[i] = nums[i];
    build();
    if (N > MAXN) { fprintf(stderr, "N too big\n"); return 2; }
    uint64_t mask0[MAXW];
    memset(mask0, 0, W * sizeof(uint64_t));
    mask0[0] = 1;  /* empty subset: the single sum 0 (zero has index 0) */
    dfs(0, mask0, 0);
    printf("group=");
    for (int i = 0; i < R; i++) printf("%s%d", i ? "x" : "", nm[i]);
    printf(" N=%d T=%d dissociated_T_subsets=%" PRIu64
           " nodes=%" PRIu64 " extensions_tried=%" PRIu64 "\n",
           N, T, found, nodes, leaves);
    free(addtab);
    return 0;
}
