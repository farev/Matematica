/* Engine B: independent exact computation of d_pm(G) = max size of a
 * plus-minus zero-sum-free set (= maximum dissociated subset) of a finite
 * abelian group G = Z_{n1} + ... + Z_{nr}, r <= 8.
 *
 * Independent of the Python engine (dpm.py): different language, different
 * data structures (explicit signed-sum list + membership flags with an
 * append-log undo, instead of Python set copies), different candidate loop.
 *
 * Algorithm: DFS over index-increasing sets of class representatives
 * {g, -g}.  State: mem[] = indicator of the signed-subset-sum set A of the
 * chosen elements; list[0..nlist) = elements of A.  Extension by g is
 * allowed iff mem[g] == 0 and mem[-g] == 0 (NOTE.md, Lemma 2).  On
 * extension, A grows to A | (A+g) | (A-g): walk the old list, append
 * unseen sums; on backtrack, clear exactly the appended entries.
 *
 * Output: d_pm, D_pm = d_pm + 1, number of pm-zsf sets of maximum size,
 * total DFS nodes, the lexicographically first maximum witness.
 *
 * Usage: ./dpm_fast n1 [n2 [n3 [n4]]]
 * Exact integer arithmetic throughout; no floating point anywhere.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int R;                 /* rank */
static long ord[8];           /* cyclic orders */
static long rad[8];           /* mixed radix */
static long N;                /* |G| */

static long g_add(long a, long b) {
    long s = 0;
    for (int i = 0; i < R; i++) {
        long x = (a / rad[i]) % ord[i], y = (b / rad[i]) % ord[i];
        s += ((x + y) % ord[i]) * rad[i];
    }
    return s;
}
static long g_neg(long a) {
    long s = 0;
    for (int i = 0; i < R; i++) {
        long x = (a / rad[i]) % ord[i];
        s += ((ord[i] - x) % ord[i]) * rad[i];
    }
    return s;
}

static long *reps;  static int M;      /* class representatives */
static long *negr;                     /* neg of each rep */
static char *mem;                      /* indicator of A */
static long *list;  static long nlist; /* elements of A */
static long *chosen; static int nch;
static long best = 0;
static unsigned long long nbest = 0, nodes = 0;
static long witness[64];

static void dfs(int start) {
    if (nch > best) {
        best = nch; nbest = 1;
        memcpy(witness, chosen, (size_t)nch * sizeof(long));
    } else if (nch == best && nch > 0) {
        nbest++;
    }
    for (int j = start; j < M; j++) {
        long g = reps[j], h = negr[j];
        if (mem[g] || mem[h]) continue;
        nodes++;
        long old_nlist = nlist;
        for (long i = 0; i < old_nlist; i++) {
            long s = list[i];
            long t1 = g_add(s, g), t2 = g_add(s, h);
            if (!mem[t1]) { mem[t1] = 1; list[nlist++] = t1; }
            if (!mem[t2]) { mem[t2] = 1; list[nlist++] = t2; }
        }
        chosen[nch++] = g;
        dfs(j + 1);
        nch--;
        for (long i = old_nlist; i < nlist; i++) mem[list[i]] = 0;
        nlist = old_nlist;
    }
}

int main(int argc, char **argv) {
    R = argc - 1;
    if (R < 1 || R > 8) { fprintf(stderr, "usage: %s n1 ... n8\n", argv[0]); return 1; }
    N = 1;
    for (int i = 0; i < R; i++) { ord[i] = atol(argv[1 + i]); N *= ord[i]; }
    { long m = N; for (int i = 0; i < R; i++) { m /= ord[i]; rad[i] = m; } }

    reps = malloc((size_t)N * sizeof(long)); negr = malloc((size_t)N * sizeof(long));
    char *seen = calloc((size_t)N, 1);
    M = 0;
    for (long g = 1; g < N; g++) {
        if (seen[g]) continue;
        long h = g_neg(g);
        seen[g] = 1; seen[h] = 1;
        reps[M] = g < h ? g : h; negr[M] = g < h ? h : g; M++;
    }
    mem = calloc((size_t)N, 1);
    list = malloc((size_t)N * sizeof(long));
    chosen = malloc(64 * sizeof(long));
    nlist = 0; list[nlist++] = 0; mem[0] = 1;

    dfs(0);

    printf("G =");
    for (int i = 0; i < R; i++) printf(" Z_%ld", ord[i]);
    printf("  |G| = %ld  classes = %d\n", N, M);
    printf("d_pm = %ld  D_pm = %ld  n_extremal = %llu  nodes = %llu\n",
           best, best + 1, nbest, nodes);
    printf("witness:");
    for (int i = 0; i < best; i++) {
        printf(" (");
        for (int j = 0; j < R; j++) printf("%ld%s", (witness[i]/rad[j])%ord[j], j+1<R?",":"");
        printf(")");
    }
    printf("\n");
    return 0;
}
