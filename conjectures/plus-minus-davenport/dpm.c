/* dpm.c — exact plus-minus weighted Davenport constant D±(G) by exhaustive DFS.
 *
 * G = Z_{d1} ⊕ ... ⊕ Z_{dr}, given as factor list on the command line.
 * D±(G) = 1 + L(G), where L(G) is the maximum length of a ±zero-sum-free
 * sequence: a sequence g_1..g_k over G with no nonempty I ⊆ {1..k} and signs
 * ε_i ∈ {+1,−1} such that Σ_{i∈I} ε_i g_i = 0.
 *
 * Model (proved in NOTE.md, Lemma 1): a ±free sequence has distinct elements
 * and at most one element of each sign class {g, −g}; freeness is invariant
 * under g ↦ −g; hence ±free sequences of length k correspond exactly to
 * ±free k-subsets of the sign classes, and it suffices to search subsets of
 * class representatives.  Mode --raw searches raw element multisets instead
 * (no class reduction, repetitions allowed) and must satisfy
 * rawcount[k] = 2^k * count[k] for odd-order G (Lemma 1 check).
 *
 * State: reach set R = { all signed subset sums of the chosen elements }.
 * A class c extends a free set iff 0 ∉ R' = R ∪ (R+c) ∪ (R−c) ∪ {c, −c};
 * then R' is the new reach set.
 *
 * Usage: ./dpm d1 [d2 ...] [--raw] [--target S] [--enum S] [--maxdepth D]
 *   default        full census DFS: count[k] = number of ±free k-subsets of
 *                  classes (exact), max L, lex-first witness of size L.
 *   --raw          census over raw element multisets (nondecreasing element
 *                  index; repetitions allowed and immediately pruned by
 *                  g − g = 0).
 *   --target S     stop at first free set of size S (existence run only;
 *                  counts below S still exact, above S not explored).
 *   --enum S       print every free set of size exactly S (census intact).
 *   --maxdepth D   do not explore sets larger than D.
 *
 * Element encoding: e = x_1 + d_1*(x_2 + d_2*(x_3 + ...)), x_i ∈ Z_{d_i}.
 * Output prints elements as tuples (x_1,...,x_r).
 *
 * Exact integer arithmetic only. Single-threaded, deterministic.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXR 8
#define MAXDEPTH_HARD 64

static int r, d[MAXR];
static int N;                 /* |G| */
static int16_t *addtab;       /* addtab[a*N+b] = a+b in G */
static int *neg;              /* neg[g] = -g */
static int *cls;  static int m;   /* class representatives (g <= neg[g]), g != 0 */

static uint8_t *inR;          /* reach membership */
static int *list;  static int cnt;   /* reach as list for undo */
static uint64_t count[MAXDEPTH_HARD + 1];
static uint64_t nodes;
static int best = 0;
static int stackCls[MAXDEPTH_HARD];      /* chosen elements (raw values) */
static int bestWit[MAXDEPTH_HARD];
static int enumSize = -1, targetSize = -1, maxDepth = MAXDEPTH_HARD;
static int rawMode = 0;
static int foundTarget = 0;

static void decode(int e, int *x) {
    for (int i = 0; i < r; i++) { x[i] = e % d[i]; e /= d[i]; }
}
static void print_elem(FILE *f, int e) {
    int x[MAXR]; decode(e, x);
    fputc('(', f);
    for (int i = 0; i < r; i++) fprintf(f, "%d%s", x[i], i + 1 < r ? "," : "");
    fputc(')', f);
}

/* add element value g (not 0) to reach; return previous cnt on success,
 * -1 (state restored) if 0 would enter the reach set. */
static int try_add(int g) {
    int ng = neg[g];
    int base = cnt;
    int v = g;
    if (!inR[v]) { inR[v] = 1; list[cnt++] = v; }
    v = ng;
    if (!inR[v]) { inR[v] = 1; list[cnt++] = v; }
    const int16_t *rowg = addtab + (size_t)g * N;
    const int16_t *rown = addtab + (size_t)ng * N;
    for (int i = 0; i < base; i++) {
        int a = list[i];
        int v1 = rowg[a];
        if (v1 == 0) goto fail;
        if (!inR[v1]) { inR[v1] = 1; list[cnt++] = v1; }
        int v2 = rown[a];
        if (v2 == 0) goto fail;
        if (!inR[v2]) { inR[v2] = 1; list[cnt++] = v2; }
    }
    return base;
fail:
    for (int j = base; j < cnt; j++) inR[list[j]] = 0;
    cnt = base;
    return -1;
}
static void rollback(int base) {
    for (int j = base; j < cnt; j++) inR[list[j]] = 0;
    cnt = base;
}

static void report_set(int depth) {
    count[depth]++;
    if (depth > best) {
        best = depth;
        memcpy(bestWit, stackCls, sizeof(int) * depth);
    }
    if (depth == enumSize) {
        printf("ENUM");
        for (int i = 0; i < depth; i++) { fputc(' ', stdout); print_elem(stdout, stackCls[i]); }
        fputc('\n', stdout);
    }
    if (depth == targetSize) foundTarget = 1;
}

/* class-subset DFS: extend with classes cls[k], k >= startIdx */
static void dfs(int startIdx, int depth) {
    if (depth > 0) report_set(depth);
    if (foundTarget || depth >= maxDepth) return;
    for (int k = startIdx; k < m; k++) {
        nodes++;
        int base = try_add(cls[k]);
        if (base < 0) continue;
        stackCls[depth] = cls[k];
        dfs(k + 1, depth + 1);
        rollback(base);
        if (foundTarget) return;
    }
}

/* raw-multiset DFS: extend with elements g >= startVal (any nonzero element,
 * repetitions allowed — a repeat is pruned inside try_add since g-g=0
 * enters via (R+neg g) once g ∈ R... more directly: adding g twice puts
 * 0 = g + neg g in R' because after the first add, neg g ∈ R, and the second
 * add computes neg g + g = 0). */
static void dfs_raw(int startVal, int depth) {
    if (depth > 0) report_set(depth);
    if (foundTarget || depth >= maxDepth) return;
    for (int g = startVal; g < N; g++) {
        nodes++;
        int base = try_add(g);
        if (base < 0) continue;
        stackCls[depth] = g;
        dfs_raw(g, depth + 1);   /* nondecreasing: multisets counted once */
        rollback(base);
        if (foundTarget) return;
    }
}

int main(int argc, char **argv) {
    r = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--raw")) { rawMode = 1; }
        else if (!strcmp(argv[i], "--target")) { targetSize = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--enum")) { enumSize = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--maxdepth")) { maxDepth = atoi(argv[++i]); }
        else {
            if (r >= MAXR) { fprintf(stderr, "too many factors\n"); return 1; }
            d[r] = atoi(argv[i]);
            if (d[r] < 2) { fprintf(stderr, "bad factor %s\n", argv[i]); return 1; }
            r++;
        }
    }
    if (r == 0) { fprintf(stderr, "usage: %s d1 [d2 ...] [--raw] [--target S] [--enum S] [--maxdepth D]\n", argv[0]); return 1; }
    long long NN = 1;
    for (int i = 0; i < r; i++) { NN *= d[i]; }
    if (NN > 4096) { fprintf(stderr, "N too large (%lld > 4096)\n", NN); return 1; }
    N = (int)NN;

    addtab = malloc((size_t)N * N * sizeof(int16_t));
    neg = malloc(N * sizeof(int));
    inR = calloc(N, 1);
    list = malloc(N * sizeof(int));
    cls = malloc(N * sizeof(int));
    if (!addtab || !neg || !inR || !list || !cls) { fprintf(stderr, "oom\n"); return 1; }

    int xa[MAXR], xb[MAXR];
    for (int a = 0; a < N; a++) {
        decode(a, xa);
        for (int b = 0; b < N; b++) {
            decode(b, xb);
            int e = 0, mul = 1;
            for (int i = 0; i < r; i++) { e += ((xa[i] + xb[i]) % d[i]) * mul; mul *= d[i]; }
            addtab[(size_t)a * N + b] = (int16_t)e;
        }
    }
    for (int a = 0; a < N; a++) {
        decode(a, xa);
        int e = 0, mul = 1;
        for (int i = 0; i < r; i++) { e += ((d[i] - xa[i]) % d[i]) * mul; mul *= d[i]; }
        neg[a] = e;
    }
    m = 0;
    for (int g = 1; g < N; g++) if (g <= neg[g]) cls[m++] = g;

    printf("GROUP");
    for (int i = 0; i < r; i++) printf(" %d", d[i]);
    printf("\nN %d NONZERO %d CLASSES %d\n", N, N - 1, m);
    printf("MODE %s%s%s\n", rawMode ? "raw" : "census",
           targetSize >= 0 ? " target" : "", enumSize >= 0 ? " enum" : "");

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    cnt = 0;
    if (rawMode) dfs_raw(1, 0); else dfs(0, 0);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double secs = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);

    for (int k = 1; k <= best; k++) printf("FREE %d %llu\n", k, (unsigned long long)count[k]);
    printf("L %d\nDPM %d\n", best, best + 1);
    printf("WITNESS");
    for (int i = 0; i < best; i++) { fputc(' ', stdout); print_elem(stdout, bestWit[i]); }
    printf("\nNODES %llu TIME %.3fs%s\n", (unsigned long long)nodes, secs,
           foundTarget ? " (stopped at target)" : (maxDepth < MAXDEPTH_HARD ? " (depth-capped)" : ""));
    return 0;
}
