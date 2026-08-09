/* sds_search.c — exhaustive search for signed difference sets in a
 * finite abelian group.
 *
 * SDS(v,k,lam) in G: A in Z[G], coefficients in {-1,0,+1}, exactly k
 * nonzero, and for every d != 0:  C(d) = sum_g A(g)A(g-d) = lam.
 * Writing s = sqrt(k + lam(v-1)) (must be a nonnegative integer),
 * |P| = (k+s)/2 elements carry +1 and |M| = (k-s)/2 carry -1.
 *
 * Search: depth-first over group elements in index order, assigning
 * +1 / -1 / 0, with
 *   - exact incremental correlation sums c[d],
 *   - interval pruning: c[d] can still move by at most openp[d] (the
 *     number of ordered pairs with difference d not yet fully decided
 *     and not killed by a 0), so prune when lam is outside
 *     [c[d]-openp[d], c[d]+openp[d]],
 *   - slot-count pruning (remaining +/- budgets vs remaining elements),
 *   - translation reduction (default): fix A[0] = +1 — every SDS with
 *     |P| >= 1 has a translate with 0 in P, so existence and
 *     nonexistence transfer; disabled by --all for complete raw
 *     enumeration.
 *
 * Output: one WITNESS line per found set (up to a cap in find-first
 * mode; unlimited in --all), then a RESULT line with node counts.
 * Exhaustive completion with 0 witnesses is a nonexistence proof for
 * the cell (relative to the correctness of this program; witnesses are
 * verified independently, and the engine is validated against known
 * cells and an independent Python implementation — see check_engine.py).
 *
 * gcc -O2 -o sds_search sds_search.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXV 64
#define MAXFAC 8

static int v, k, lam, s, nP, nM;
static int nfac, fac[MAXFAC];
static int addt[MAXV][MAXV];   /* index of g+h */
static int negt[MAXV];         /* index of -g */
static int difft[MAXV][MAXV];  /* index of g-h */

static int8_t A[MAXV];         /* -1,0,+1 assigned so far */
static int16_t c[MAXV];        /* correlation sums, index by d=1..v-1 */
static int16_t openp[MAXV];    /* open ordered pairs per difference */
static int nz[MAXV], nnz;      /* decided nonzero element indices */

static uint64_t nodes = 0, witnesses = 0;
static int allmode = 0, quiet = 0;
static uint64_t witness_cap = 25;
static uint64_t node_limit = 0;      /* 0 = unlimited */
static int aborted = 0;

static void decode(int idx, int *co) {
    for (int i = nfac - 1; i >= 0; i--) { co[i] = idx % fac[i]; idx /= fac[i]; }
}
static int encode(const int *co) {
    int idx = 0;
    for (int i = 0; i < nfac; i++) idx = idx * fac[i] + co[i];
    return idx;
}

static void build_tables(void) {
    int ca[MAXFAC], cb[MAXFAC], cc[MAXFAC];
    for (int i = 0; i < v; i++) {
        decode(i, ca);
        for (int j = 0; j < nfac; j++) cc[j] = (fac[j] - ca[j]) % fac[j];
        negt[i] = encode(cc);
        for (int j = 0; j < v; j++) {
            decode(j, cb);
            int cs[MAXFAC];
            for (int t = 0; t < nfac; t++) cs[t] = (ca[t] + cb[t]) % fac[t];
            addt[i][j] = encode(cs);
        }
    }
    for (int i = 0; i < v; i++)
        for (int j = 0; j < v; j++)
            difft[i][j] = addt[i][negt[j]];
}

static void print_witness(void) {
    printf("WITNESS P=");
    int first = 1;
    for (int g = 0; g < v; g++) if (A[g] == 1) { printf(first?"%d":",%d", g); first = 0; }
    printf(" M=");
    first = 1;
    for (int g = 0; g < v; g++) if (A[g] == -1) { printf(first?"%d":",%d", g); first = 0; }
    printf("\n");
}

/* decide element i with value val (-1,0,+1); push correlation and
 * open-pair updates.  Returns 0 and undoes nothing if a prune fires
 * (caller undoes via undo()). */
static void apply(int i, int val) {
    /* pairs with max index = i whose past endpoint is nonzero are
     * resolved now (pairs to decided-zero elements were already removed
     * when that zero was assigned); pairs with min = i, max > i die if
     * val == 0 */
    for (int h = 0; h < i; h++) {
        if (A[h] == 0) continue;
        /* ordered pairs (i,h) diff difft[i][h] and (h,i) diff difft[h][i] */
        openp[difft[i][h]]--;
        openp[difft[h][i]]--;
    }
    if (val == 0) {
        for (int h = i + 1; h < v; h++) {
            openp[difft[i][h]]--;
            openp[difft[h][i]]--;
        }
    } else {
        for (int t = 0; t < nnz; t++) {
            int h = nz[t];
            int b = A[h] * val;
            c[difft[i][h]] += b;
            c[difft[h][i]] += b;
        }
        nz[nnz++] = i;
    }
    A[i] = (int8_t)val;
}

static void undo(int i, int val) {
    if (val != 0) {
        nnz--;
        for (int t = 0; t < nnz; t++) {
            int h = nz[t];
            int b = A[h] * val;
            c[difft[i][h]] -= b;
            c[difft[h][i]] -= b;
        }
    } else {
        for (int h = i + 1; h < v; h++) {
            openp[difft[i][h]]++;
            openp[difft[h][i]]++;
        }
    }
    for (int h = 0; h < i; h++) {
        if (A[h] == 0) continue;
        openp[difft[i][h]]++;
        openp[difft[h][i]]++;
    }
    A[i] = 0;
}

static int feasible(void) {
    for (int d = 1; d < v; d++) {
        int lo = c[d] - openp[d], hi = c[d] + openp[d];
        if (lam < lo || lam > hi) return 0;
    }
    return 1;
}

static void dfs(int i, int pleft, int mleft) {
    if (node_limit && nodes >= node_limit) { aborted = 1; return; }
    nodes++;
    if (i == v) {
        for (int d = 1; d < v; d++) if (c[d] != lam) return;
        witnesses++;
        if (!quiet && (allmode || witnesses <= witness_cap)) print_witness();
        return;
    }
    int left = v - i;
    if (pleft + mleft > left) return;
    /* value order: +1, -1, 0 */
    if (pleft > 0) {
        apply(i, 1);
        if (feasible()) dfs(i + 1, pleft - 1, mleft);
        undo(i, 1);
        if (aborted) return;
    }
    if (mleft > 0) {
        apply(i, -1);
        if (feasible()) dfs(i + 1, pleft, mleft - 1);
        undo(i, -1);
        if (aborted) return;
    }
    if (pleft + mleft < left) {
        apply(i, 0);
        if (feasible()) dfs(i + 1, pleft, mleft);
        undo(i, 0);
    }
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "usage: %s v k lam f1,f2,... [--all] [--quiet] "
                        "[--cap=N] [--nodelimit=N]\n", argv[0]);
        return 2;
    }
    v = atoi(argv[1]); k = atoi(argv[2]); lam = atoi(argv[3]);
    nfac = 0;
    char *tok = strtok(argv[4], ",");
    while (tok) { fac[nfac++] = atoi(tok); tok = strtok(NULL, ","); }
    for (int i = 5; i < argc; i++) {
        if (!strcmp(argv[i], "--all")) allmode = 1;
        else if (!strcmp(argv[i], "--quiet")) quiet = 1;
        else if (!strncmp(argv[i], "--cap=", 6)) witness_cap = strtoull(argv[i]+6, 0, 10);
        else if (!strncmp(argv[i], "--nodelimit=", 12)) node_limit = strtoull(argv[i]+12, 0, 10);
    }
    int order = 1;
    for (int i = 0; i < nfac; i++) order *= fac[i];
    if (order != v || v > MAXV) { fprintf(stderr, "bad group\n"); return 2; }

    long t = k + (long)lam * (v - 1);
    if (t < 0) { printf("RESULT SDS(%d,%d,%d) NONEXIST trivially (s^2<0) nodes=0 witnesses=0\n", v, k, lam); return 0; }
    s = 0; while ((long)(s + 1) * (s + 1) <= t) s++;
    if ((long)s * s != t || (k + s) % 2 != 0 || k - s < 0) {
        printf("RESULT SDS(%d,%d,%d) NONEXIST trivially (s not admissible) nodes=0 witnesses=0\n", v, k, lam);
        return 0;
    }
    nP = (k + s) / 2; nM = (k - s) / 2;

    build_tables();
    for (int d = 1; d < v; d++) { c[d] = 0; openp[d] = (int16_t)v; }
    nnz = 0; memset(A, 0, sizeof A);

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    if (!allmode && nP >= 1) {
        /* translation reduction: fix A[0] = +1 */
        apply(0, 1);
        if (feasible()) dfs(1, nP - 1, nM);
        undo(0, 1);
    } else {
        dfs(0, nP, nM);
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;

    printf("RESULT SDS(%d,%d,%d,[", v, k, lam);
    for (int i = 0; i < nfac; i++) printf(i ? ",%d" : "%d", fac[i]);
    printf("]) %s nP=%d nM=%d nodes=%llu witnesses=%llu mode=%s secs=%.3f\n",
           aborted ? "ABORTED" : (witnesses ? "EXIST" : "NONEXIST"),
           nP, nM,
           (unsigned long long)nodes, (unsigned long long)witnesses,
           allmode ? "all" : "reduced0P", secs);
    return aborted ? 3 : 0;
}
