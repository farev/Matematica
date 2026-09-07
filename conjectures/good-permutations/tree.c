/* tree.c — structured exhaustive search for good permutations of {1..n},
 * n = 2^m - 1 (MO 514690).
 *
 * Reduction used (Lemma B in REPORT.md): extend a by a_0 = 0.  A permutation
 * a of {1..2^m-1} is good  <=>
 *   (i)  sigma(x) := a_x is a 2-adic isometry of Z/2^m fixing 0, i.e.
 *        sigma(x) = sigma(y) mod 2^k  <=>  x = y mod 2^k   (all k <= m), and
 *   (ii) every proper block of odd length L >= 3 has sum not divisible by L.
 * (Even-length blocks are then automatically fine.)
 *
 * Positions are filled t = 1, 2, ..., n.  With K = floor(log2 t), (i) forces
 *   sigma(t) = sigma(t - 2^K) + 2^K  (mod 2^{K+1}),
 * and leaves the bits K+1..m-1 free: 2^{m-1-K} candidates.  All candidates are
 * enumerated (this is exactly the set of tree automorphisms fixing 0, of size
 * 2^{2^m - 1 - m}) and pruned with (ii) on every odd block ending at t.
 * Every leaf is re-verified against ALL blocks (lengths 2..n-1) before being
 * counted, so the count of solutions is independent of the reasoning that
 * even blocks never fail.  With -e, even blocks are also used for pruning and
 * the number of even-length prunings is reported (expected 0).
 *
 * Build: gcc -O2 -o tree tree.c
 * Usage: ./tree m [-t seconds] [-e] [-h] [-p maxprint] [-o solutions.txt]
 *                [-L l1,l2,...] [-d depth]
 *   -h : halve the search by the complement symmetry a -> n+1-a
 *        (equivalently: require sigma(1) < 2^{m-1}).
 *   -L : EXPERIMENT MODE — only the listed odd block lengths are enforced
 *        (pruning and final check).  Leaves are then "L-set-good" tree
 *        automorphisms, not necessarily good permutations.
 *   -d : print every node at depth >= d together with the length that
 *        killed it (or PASS).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

static int m, n, q;
static int sigma[128];
static int P[129];
static uint64_t used[2];
static unsigned long long nodes = 0, solutions = 0, even_prunes = 0;
static unsigned long long depth_nodes[128];
static unsigned long long kill_by_L[128];
static double time_cap = 0;          /* seconds; 0 = none */
static int use_even = 0, halve = 0, maxprint = 10, restricted = 0, dprint = 1000;
static int allowed[128];
static FILE *solf = NULL;
static clock_t c0;
static int aborted = 0;
static int max_depth = 0;

static int full_check(void) {        /* all proper blocks, lengths 2..n-1 (or the -L set) */
    for (int L = 2; L <= n - 1; L++) {
        if (restricted && !allowed[L]) continue;
        for (int i = 0; i + L <= n; i++)
            if ((P[i + L] - P[i]) % L == 0) return 0;
    }
    return 1;
}

static void print_prefix(FILE *f, int upto) {
    for (int i = 1; i <= upto; i++) fprintf(f, "%d%c", sigma[i], i == upto ? '\n' : ' ');
}

static void progress(void) {
    double secs = (double)(clock() - c0) / CLOCKS_PER_SEC;
    fprintf(stderr, "[%.0fs] nodes=%llu solutions=%llu maxdepth=%d prefix:",
            secs, nodes, solutions, max_depth);
    for (int i = 1; i <= 8 && i <= n; i++) fprintf(stderr, " %d", sigma[i]);
    fprintf(stderr, "\n");
}

static void rec(int t) {
    if (aborted) return;
    if (t > n) {
        if (full_check()) {
            solutions++;
            if (solutions <= (unsigned long long)maxprint) { printf("SOL: "); print_prefix(stdout, n); }
            if (solf) print_prefix(solf, n);
        } else {
            fprintf(stderr, "INTERNAL ERROR: leaf failed full check\n");
            print_prefix(stderr, n);
            exit(2);
        }
        return;
    }
    int K = 31 - __builtin_clz(t);            /* floor(log2 t) */
    int step = 1 << (K + 1);
    int base = (sigma[t - (1 << K)] + (1 << K)) & (step - 1);
    int nch = 1 << (m - 1 - K);
    if (t == 1 && halve) nch >>= 1;           /* sigma(1) < 2^{m-1} */
    for (int h = 0; h < nch; h++) {
        int v = base + h * step;
        nodes++;
        depth_nodes[t]++;
        if ((nodes & 0xFFFFF) == 0) {
            if (time_cap > 0 && (double)(clock() - c0) / CLOCKS_PER_SEC > time_cap) {
                aborted = 1; return;
            }
            if ((nodes & 0x3FFFFFFF) == 0) progress();
        }
        P[t] = P[t - 1] + v;
        int killer = 0;
        int Lmax = t; if (Lmax > n - 1) Lmax = n - 1;
        for (int L = 3; L <= Lmax; L += 2) {
            if (restricted && !allowed[L]) continue;
            if ((P[t] - P[t - L]) % L == 0) { killer = L; break; }
        }
        if (!killer && use_even) {
            for (int L = 2; L <= Lmax; L += 2)
                if ((P[t] - P[t - L]) % L == 0) { killer = L; even_prunes++; break; }
        }
        if (t >= dprint) {
            sigma[t] = v;
            printf("depth %d %s: ", t, killer ? "killed" : "PASS  ");
            if (killer) printf("(L=%d) ", killer);
            print_prefix(stdout, t);
        }
        if (killer) { kill_by_L[killer]++; continue; }
        if (used[v >> 6] & (1ULL << (v & 63))) {
            fprintf(stderr, "INTERNAL ERROR: value %d reused at t=%d\n", v, t); exit(2);
        }
        sigma[t] = v;
        if (t > max_depth) max_depth = t;
        used[v >> 6] |= 1ULL << (v & 63);
        rec(t + 1);
        used[v >> 6] &= ~(1ULL << (v & 63));
        if (aborted) return;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s m [-t secs] [-e] [-h] [-p maxprint] [-o file] [-L l1,l2,..] [-d depth]\n", argv[0]); return 1; }
    m = atoi(argv[1]);
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "-t")) time_cap = atof(argv[++i]);
        else if (!strcmp(argv[i], "-e")) use_even = 1;
        else if (!strcmp(argv[i], "-h")) halve = 1;
        else if (!strcmp(argv[i], "-p")) maxprint = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-o")) solf = fopen(argv[++i], "w");
        else if (!strcmp(argv[i], "-d")) dprint = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-L")) {
            restricted = 1;
            char *s = argv[++i], *tok = strtok(s, ",");
            while (tok) { int L = atoi(tok); if (L >= 2 && L < 128) allowed[L] = 1; tok = strtok(NULL, ","); }
        }
    }
    if (m < 2 || m > 7) { fprintf(stderr, "m out of range\n"); return 1; }
    n = (1 << m) - 1; q = 1 << (m - 1);
    printf("m=%d n=%d candidates(tree automorphisms fixing 0)=2^%d%s", m, n,
           (1 << m) - 1 - m, halve ? " halved by complement symmetry" : "");
    if (restricted) { printf(" RESTRICTED to lengths"); for (int L = 2; L < 128; L++) if (allowed[L]) printf(" %d", L); }
    printf("\n");
    fflush(stdout);
    c0 = clock();
    sigma[0] = 0; P[0] = 0; used[0] = 1; used[1] = 0;
    rec(1);
    double secs = (double)(clock() - c0) / CLOCKS_PER_SEC;
    if (solf) fclose(solf);
    printf("%s m=%d n=%d solutions=%llu nodes=%llu maxdepth=%d time=%.3fs even_prunes=%llu%s\n",
           aborted ? "INCOMPLETE(time cap)" : "COMPLETE", m, n, solutions, nodes, max_depth, secs,
           even_prunes, use_even ? "" : " (even blocks not used for pruning)");
    printf("nodes per depth:");
    for (int t = 1; t <= n; t++) printf(" %d:%llu", t, depth_nodes[t]);
    printf("\nkills by length:");
    for (int L = 2; L <= n; L++) if (kill_by_L[L]) printf(" %d:%llu", L, kill_by_L[L]);
    printf("\n");
    return aborted ? 3 : 0;
}
