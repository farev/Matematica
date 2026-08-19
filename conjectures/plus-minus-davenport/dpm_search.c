/* dpm_search.c — exact computation of the plus-minus weighted Davenport
 * constant D±(G) for G = Z_a x Z_b x Z_c x Z_d (trailing moduli 1 for lower
 * rank). Engine E1 of this conjecture directory.
 *
 * D±(G) = 1 + maxlen±(G), where maxlen±(G) is the maximum length of a
 * plus-minus zero-sum-free sequence over G; equivalently (NOTE.md Lemma 0)
 * the maximum size of a dissociated subset of G.
 *
 * Method: depth-first enumeration of ALL ±zsf multisets, encoded as
 * nondecreasing sequences over a fixed element order. State: the set
 * T = { all signed subset sums } as a bitset. Extension by g is legal iff
 * g != 0 and g ∉ T; then T' = T ∪ (T+g) ∪ (T−g) ∪ {g, −g}. There is no
 * other pruning, so (#nodes − 1) = #±zsf multisets enumerated — an exact
 * invariant compared across independent engines (E2, E4).
 *
 * Default: elements restricted to sign-representatives (one of {g, −g};
 * sound by NOTE.md Lemma 1); with --no-signred all nonzero elements are
 * used, which enumerates every dissociated SUBSET of G and must satisfy
 * N_full(l) = 2^l N_rep(l) for groups of odd order (NOTE.md §5 check).
 *
 * Exact integer arithmetic throughout; no floating point.
 *
 * Usage: ./dpm_search a [b] [c] [d] [--no-signred] [--count-by-size]
 *                     [--maxdepth D] [--prefix k1 k2 ...]
 * --prefix takes indices into the rep array (for parallel subtree splits;
 *   the printed node count then covers that subtree only, prefix node
 *   included; the root is counted by no subtree).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 4096
#define MAXW (MAXN/64)
#define MAXDEPTH 64

static int M[4] = {1, 1, 1, 1};
static int N = 1, W;
static int *addtab;
static int neg[MAXN];
static int reps[MAXN], nreps;
static uint64_t Tstack[MAXDEPTH + 2][MAXW];
static int seq[MAXDEPTH + 2];
static long long nodes = 0;
static long long bysize[MAXDEPTH + 2];
static int best = 0;
static int track_bysize = 0, no_signred = 0;
static int maxdepth = MAXDEPTH;
static int bestseq[MAXDEPTH + 2];

static inline int getbit(const uint64_t *T, int i) {
    return (int)((T[i >> 6] >> (i & 63)) & 1ULL);
}
static inline void setbit(uint64_t *T, int i) {
    T[i >> 6] |= 1ULL << (i & 63);
}

static void build_child(const uint64_t *T, uint64_t *Tp, int g) {
    int ng = neg[g];
    memcpy(Tp, T, sizeof(uint64_t) * (size_t)W);
    setbit(Tp, g);
    setbit(Tp, ng);
    const int *rowg = addtab + (size_t)g * N;
    const int *rowng = addtab + (size_t)ng * N;
    for (int w = 0; w < W; w++) {
        uint64_t t = T[w];
        while (t) {
            int i = (w << 6) + __builtin_ctzll(t);
            t &= t - 1;
            setbit(Tp, rowg[i]);
            setbit(Tp, rowng[i]);
        }
    }
    if (Tp[0] & 1ULL) {           /* 0 ∈ T' is impossible if g was legal */
        fprintf(stderr, "INVARIANT VIOLATION at g=%d\n", g);
        exit(2);
    }
}

static void dfs(int depth, int start) {
    nodes++;
    bysize[depth]++;
    if (depth > best) {
        best = depth;
        memcpy(bestseq, seq, sizeof(int) * depth);
        bestseq[depth] = -1;
    }
    if (depth >= maxdepth) return;
    const uint64_t *T = Tstack[depth];
    uint64_t *Tp = Tstack[depth + 1];
    for (int k = start; k < nreps; k++) {
        int g = reps[k];
        if (getbit(T, g)) continue;
        build_child(T, Tp, g);
        seq[depth] = g;
        dfs(depth + 1, k);
        seq[depth] = -1;
    }
}

int main(int argc, char **argv) {
    int prefix[MAXDEPTH], nprefix = 0, nmod = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--count-by-size")) track_bysize = 1;
        else if (!strcmp(argv[i], "--no-signred")) no_signred = 1;
        else if (!strcmp(argv[i], "--maxdepth")) maxdepth = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--prefix")) {
            while (i + 1 < argc && (argv[i+1][0] != '-' || argv[i+1][1] == 0))
                prefix[nprefix++] = atoi(argv[++i]);
        }
        else if (nmod < 4) M[nmod++] = atoi(argv[i]);
    }
    if (nmod < 1 || M[0] < 1) { fprintf(stderr, "usage: dpm_search a [b] [c] [d] [flags]\n"); return 1; }
    N = M[0] * M[1] * M[2] * M[3];
    if (N > MAXN) { fprintf(stderr, "group too large (max %d)\n", MAXN); return 1; }
    W = (N + 63) / 64;
    addtab = malloc(sizeof(int) * (size_t)N * N);
    if (!addtab) { fprintf(stderr, "OOM\n"); return 1; }
    for (int i = 0; i < N; i++) {
        int c1[4], t = i;
        for (int q = 3; q >= 0; q--) { c1[q] = t % M[q]; t /= M[q]; }
        neg[i] = ((((M[0]-c1[0])%M[0])*M[1] + (M[1]-c1[1])%M[1])*M[2]
                  + (M[2]-c1[2])%M[2])*M[3] + (M[3]-c1[3])%M[3];
        for (int j = 0; j < N; j++) {
            int c2[4], u = j;
            for (int q = 3; q >= 0; q--) { c2[q] = u % M[q]; u /= M[q]; }
            addtab[(size_t)i * N + j] =
                ((((c1[0]+c2[0])%M[0])*M[1] + (c1[1]+c2[1])%M[1])*M[2]
                 + (c1[2]+c2[2])%M[2])*M[3] + (c1[3]+c2[3])%M[3];
        }
    }
    nreps = 0;
    for (int i = 1; i < N; i++)
        if (no_signred || i <= neg[i]) reps[nreps++] = i;

    memset(Tstack[0], 0, sizeof(uint64_t) * (size_t)W);
    memset(seq, -1, sizeof(seq));
    int depth0 = 0, startk = 0;
    for (int p = 0; p < nprefix; p++) {
        int k = prefix[p];
        if (k < 0 || k >= nreps) { fprintf(stderr, "bad prefix index\n"); return 1; }
        int g = reps[k];
        if (getbit(Tstack[depth0], g)) {
            printf("%d %d %d %d %d PREFIX-ILLEGAL\n", M[0], M[1], M[2], M[3], N);
            return 0;
        }
        build_child(Tstack[depth0], Tstack[depth0 + 1], g);
        seq[depth0] = g;
        depth0++;
        startk = k;
    }
    best = depth0;
    memcpy(bestseq, seq, sizeof(int) * depth0);
    bestseq[depth0] = -1;
    dfs(depth0, startk);

    printf("%d %d %d %d %d maxlen=%d dpm=%d nodes=%lld", M[0], M[1], M[2], M[3],
           N, best, best + 1, nodes);
    printf(" witness=");
    for (int i = 0; i < best && bestseq[i] >= 0; i++) {
        int g = bestseq[i];
        int w4 = g % M[3], z = (g / M[3]) % M[2],
            y = (g / (M[2] * M[3])) % M[1], x = g / (M[1] * M[2] * M[3]);
        printf("(%d,%d,%d,%d)", x, y, z, w4);
    }
    if (track_bysize) {
        printf(" bysize=");
        for (int l = 0; l <= best; l++)
            printf("%s%lld", l ? "," : "", bysize[l]);
    }
    printf("\n");
    free(addtab);
    return 0;
}
