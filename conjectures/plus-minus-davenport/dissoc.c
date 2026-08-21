/* dissoc.c — maximal dissociated set in a finite abelian group (C engine).
 *
 * Mirrors dissoc.py's DFS exactly (same rep order, same pruning) so node
 * counts must MATCH the Python engine on any group where both run.
 *
 * Usage:  ./dissoc f1 f2 ... [need=K] [order=asc|desc]
 *   Group = C_f1 + C_f2 + ...   Elements are mixed-radix indices.
 *   need=K: stop early at a dissociated K-set (witness mode).
 *   order=desc: DFS over class reps in DESCENDING index order — a
 *   different traversal for independent-verdict cross-checking.
 *
 * Exit: prints lmax, witness, node count. Exact integer arithmetic only.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int nfac, fac[16];
static long n;                 /* group order */
static uint16_t *add;          /* add[x*n+y] */
static int *negt;
static int reps[4096], R;      /* class representatives, order used by DFS */
static int cap, target;
static int best;
static int best_set[64], cur_set[64];
static long long nodes;

/* sums stack: sums[0..(1<<depth)-1]; membership bitmap over G */
static uint16_t sums[1 << 12];
static uint64_t inset[(4096 + 63) / 64];

static void coords_of(long x, int *c) {
    for (int i = nfac - 1; i >= 0; i--) { c[i] = x % fac[i]; x /= fac[i]; }
}
static long index_of(const int *c) {
    long x = 0;
    for (int i = 0; i < nfac; i++) x = x * fac[i] + ((c[i] % fac[i]) + fac[i]) % fac[i];
    return x;
}

static void build_tables(void) {
    add = malloc(sizeof(uint16_t) * n * n);
    negt = malloc(sizeof(int) * n);
    int cx[16], cy[16], cz[16];
    for (long x = 0; x < n; x++) {
        coords_of(x, cx);
        for (int i = 0; i < nfac; i++) cz[i] = -cx[i];
        negt[x] = (int)index_of(cz);
        for (long y = 0; y < n; y++) {
            coords_of(y, cy);
            for (int i = 0; i < nfac; i++) cz[i] = cx[i] + cy[i];
            add[x * n + y] = (uint16_t)index_of(cz);
        }
    }
}

static inline int bit_test(long i) { return (inset[i >> 6] >> (i & 63)) & 1; }
static inline void bit_set(long i) { inset[i >> 6] |= 1ULL << (i & 63); }
static inline void bit_clr(long i) { inset[i >> 6] &= ~(1ULL << (i & 63)); }

static int extend(int start, int depth) {
    if (best >= target) return 1;
    if (depth + (R - start) <= best) return 0;
    int nsum = 1 << depth;
    for (int idx = start; idx < R; idx++) {
        if (best >= target) return 1;
        int g = reps[idx];
        const uint16_t *row = add + (long)g * n;
        /* legality: sums and sums+g disjoint */
        int ok = 1;
        for (int s = 0; s < nsum; s++) {
            if (bit_test(row[sums[s]])) { ok = 0; break; }
        }
        if (!ok) continue;
        nodes++;
        cur_set[depth] = g;
        for (int s = 0; s < nsum; s++) {
            uint16_t t = row[sums[s]];
            sums[nsum + s] = t;
            bit_set(t);
        }
        if (depth + 1 > best) {
            best = depth + 1;
            memcpy(best_set, cur_set, sizeof(int) * (depth + 1));
            if (best >= target) return 1;
        }
        extend(idx + 1, depth + 1);
        for (int s = 0; s < nsum; s++) bit_clr(sums[nsum + s]);
        if (best >= target) return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    int need = -1, desc = 0;
    for (int i = 1; i < argc; i++) {
        if (!strncmp(argv[i], "need=", 5)) need = atoi(argv[i] + 5);
        else if (!strcmp(argv[i], "order=desc")) desc = 1;
        else if (!strncmp(argv[i], "order=", 6)) ;
        else fac[nfac++] = atoi(argv[i]);
    }
    n = 1;
    for (int i = 0; i < nfac; i++) n *= fac[i];
    if (n > 4096) { fprintf(stderr, "group too large (max 4096)\n"); return 2; }
    build_tables();
    R = 0;
    for (long g = 1; g < n; g++) if (g <= negt[g]) reps[R++] = (int)g;
    if (desc) { /* reverse rep order */
        for (int i = 0; i < R / 2; i++) {
            int t = reps[i]; reps[i] = reps[R - 1 - i]; reps[R - 1 - i] = t;
        }
    }
    cap = 0; while ((2L << cap) <= n) cap++;   /* cap = floor(log2 n) */
    target = (need > 0) ? need : cap;
    long lower = 0;
    for (int i = 0; i < nfac; i++) {
        int b = 0; while ((2 << b) <= fac[i]) b++; lower += b;
    }
    printf("group order %ld, classes %d, product lower %ld, cap %d, target %d%s\n",
           n, R, lower, cap, target, desc ? ", order=desc" : "");
    sums[0] = 0; bit_set(0);
    best = 0; nodes = 0;
    extend(0, 0);
    printf("lmax = %d  nodes = %lld\nwitness =", best, nodes);
    for (int i = 0; i < best; i++) printf(" %d", best_set[i]);
    printf("\nwitness coords =");
    int c[16];
    for (int i = 0; i < best; i++) {
        coords_of(best_set[i], c);
        printf(" (");
        for (int j = 0; j < nfac; j++) printf("%d%s", c[j], j + 1 < nfac ? "," : "");
        printf(")");
    }
    printf("\nD_pm = %d\n", best + 1);
    return 0;
}
