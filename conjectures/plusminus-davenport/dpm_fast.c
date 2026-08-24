/* Implementation C: fast exhaustive DFS for d_pm of a finite abelian group.
 *
 * Same tree as dpm_core.py::search_dpm (same class ordering, same pruning),
 * so node counts must match the Python engine exactly on shared cells --
 * that agreement is part of the certificate. Independently written; bitset
 * reachability instead of numpy boolean vectors.
 *
 * Usage: ./dpm_fast m1 m2 ... [-c NODECAP] [-s SHARD/NSHARDS] [-x SIZE]
 *   -s i/k : only explore root branches (first chosen class index) j with
 *            j % k == i. Sharded runs partition the tree; node counts add.
 *   -x L   : existence mode: stop as soon as a pm-zsf set of size L is found.
 * Output: one line "moduli=... dpm=D nodes=N capped=0/1 stopped=0/1 witness=..."
 * Exact integer arithmetic only.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 1024
#define MAXW (MAXN/64)
#define MAXMOD 16

static int moduli[MAXMOD], nmod = 0;
static int N = 1;
static int neg[MAXN];
static int *addg[MAXN];        /* addg[g][x] = x + g */
static int classes[MAXN], nclasses = 0;
static int W;                  /* words in bitset */

static long long nodes = 0, node_cap = -1;
static int capped = 0, stopped = 0, exist_target = -1;
static int best = 0;
static int bestwit[64], curwit[64];
static int shard = -1, nshards = 1;

static inline void bs_or(uint64_t *dst, const uint64_t *src) {
    for (int i = 0; i < W; i++) dst[i] |= src[i];
}

/* dst |= (R + g) : for each x in R set bit addg[g][x] */
static inline void bs_or_shift(uint64_t *dst, const uint64_t *R, const int *ag) {
    for (int w = 0; w < W; w++) {
        uint64_t m = R[w];
        while (m) {
            int b = __builtin_ctzll(m);
            m &= m - 1;
            int y = ag[(w << 6) | b];
            dst[y >> 6] |= 1ULL << (y & 63);
        }
    }
}

static void rec(int start, int depth, const uint64_t *R) {
    nodes++;
    if (node_cap >= 0 && nodes > node_cap) { capped = 1; return; }
    if (depth > best) {
        best = depth;
        memcpy(bestwit, curwit, sizeof(int) * depth);
    }
    if (exist_target >= 0 && depth >= exist_target) { stopped = 1; return; }
    uint64_t newR[MAXW];
    for (int i = start; i < nclasses; i++) {
        if (depth == 0 && shard >= 0 && (i % nshards) != shard) continue;
        int g = classes[i], ng = neg[g];
        memcpy(newR, R, sizeof(uint64_t) * W);
        bs_or_shift(newR, R, addg[g]);
        bs_or_shift(newR, R, addg[ng]);
        newR[g >> 6] |= 1ULL << (g & 63);
        newR[ng >> 6] |= 1ULL << (ng & 63);
        if (newR[0] & 1ULL) continue;      /* 0 in R: prune */
        curwit[depth] = g;
        rec(i + 1, depth + 1, newR);
        if (capped || stopped) return;
    }
}

int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-c")) { node_cap = atoll(argv[++i]); }
        else if (!strcmp(argv[i], "-s")) { sscanf(argv[++i], "%d/%d", &shard, &nshards); }
        else if (!strcmp(argv[i], "-x")) { exist_target = atoi(argv[++i]); }
        else { moduli[nmod++] = atoi(argv[i]); }
    }
    for (int i = 0; i < nmod; i++) N *= moduli[i];
    if (N > MAXN) { fprintf(stderr, "N too large\n"); return 2; }
    W = (N + 63) / 64;
    /* index: mixed radix, last modulus fastest (same as dpm_core) */
    int radix[MAXMOD];
    { int acc = 1; for (int i = nmod - 1; i >= 0; i--) { radix[i] = acc; acc *= moduli[i]; } }
    int tup[MAXMOD];
    for (int e = 0; e < N; e++) {
        for (int i = 0; i < nmod; i++) tup[i] = (e / radix[i]) % moduli[i];
        int ne = 0;
        for (int i = 0; i < nmod; i++) ne += ((moduli[i] - tup[i]) % moduli[i]) * radix[i];
        neg[e] = ne;
    }
    for (int g = 0; g < N; g++) {
        addg[g] = malloc(sizeof(int) * N);
        int gt[MAXMOD];
        for (int i = 0; i < nmod; i++) gt[i] = (g / radix[i]) % moduli[i];
        for (int x = 0; x < N; x++) {
            int s = 0;
            for (int i = 0; i < nmod; i++)
                s += (((x / radix[i]) % moduli[i]) + gt[i]) % moduli[i] * radix[i];
            addg[g][x] = s;
        }
    }
    for (int g = 1; g < N; g++) if (g <= neg[g]) classes[nclasses++] = g;
    uint64_t R0[MAXW];
    memset(R0, 0, sizeof(uint64_t) * W);
    rec(0, 0, R0);
    if (shard >= 0) printf("shard=%d/%d ", shard, nshards);
    printf("moduli=");
    for (int i = 0; i < nmod; i++) printf("%d%s", moduli[i], i + 1 < nmod ? "," : "");
    printf(" N=%d nclasses=%d dpm=%d nodes=%lld capped=%d stopped=%d witness=", N, nclasses, best, nodes, capped, stopped);
    for (int i = 0; i < best; i++) {
        int e = bestwit[i];
        printf("(");
        for (int j = 0; j < nmod; j++)
            printf("%d%s", (e / radix[j]) % moduli[j], j + 1 < nmod ? "," : "");
        printf(")%s", i + 1 < best ? ";" : "");
    }
    printf("\n");
    return 0;
}
