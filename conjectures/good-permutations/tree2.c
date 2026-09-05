/* tree2.c — same algorithm as tree.c (structured exhaustive search over
 * 2-adic tree automorphisms fixing 0, pruned by odd-length blocks; see the
 * header of tree.c and Lemma B in REPORT.md), generalised to m <= 12
 * (n <= 4095) and with a selectable candidate order.
 *
 * Candidate order at position t (K = floor(log2 t)): the admissible values are
 * v = base + h*2^{K+1}, h = 0..2^{m-1-K}-1.
 *   default : h ascending at every t.
 *   -c      : h ascending at t = 1, descending at t >= 2.  With this order the
 *             asker's construction 1, n-1, n, n-3, n-2, ..., 2, 3 is the very
 *             first leaf visited, so a witness for prime n is found at once.
 * Everything else (pruning on odd blocks, full re-verification of every leaf
 * against ALL block lengths, node counting, time cap) is as in tree.c.
 *
 * Build: gcc -O2 -o tree2 tree2.c
 * Usage: ./tree2 m [-t seconds] [-c] [-p maxprint] [-o solutions.txt] [-s maxsol]
 *   -s : stop after maxsol solutions have been found.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define MAXN 4096
static int m, n;
static int sigma[MAXN + 1];
static long P[MAXN + 2];
static uint64_t used[MAXN / 64 + 1];
static unsigned long long nodes = 0, solutions = 0;
static unsigned long long depth_nodes[MAXN + 1];
static double time_cap = 0;
static int cfirst = 0, maxprint = 4;
static unsigned long long maxsol = 0;
static FILE *solf = NULL;
static clock_t c0;
static int aborted = 0, max_depth = 0;

static int full_check(void) {
    for (int L = 2; L <= n - 1; L++)
        for (int i = 0; i + L <= n; i++)
            if ((P[i + L] - P[i]) % L == 0) return 0;
    return 1;
}

static void print_perm(FILE *f) {
    for (int i = 1; i <= n; i++) fprintf(f, "%d%c", sigma[i], i == n ? '\n' : ' ');
}

static void progress(void) {
    double secs = (double)(clock() - c0) / CLOCKS_PER_SEC;
    fprintf(stderr, "[%.0fs] nodes=%llu solutions=%llu maxdepth=%d prefix:", secs, nodes, solutions, max_depth);
    for (int i = 1; i <= 8 && i <= n; i++) fprintf(stderr, " %d", sigma[i]);
    fprintf(stderr, "\n");
}

static void rec(int t) {
    if (aborted) return;
    if (t > n) {
        if (full_check()) {
            solutions++;
            if (solutions <= maxsol || maxsol == 0) {
                if (solutions <= (unsigned long long)maxprint) { printf("SOL: "); print_perm(stdout); fflush(stdout); }
                if (solf) { print_perm(solf); fflush(solf); }
            }
            if (maxsol && solutions >= maxsol) aborted = 2;
        } else {
            fprintf(stderr, "INTERNAL ERROR: leaf failed full check\n"); print_perm(stderr); exit(2);
        }
        return;
    }
    int K = 31 - __builtin_clz(t);
    int step = 1 << (K + 1);
    int base = (sigma[t - (1 << K)] + (1 << K)) & (step - 1);
    int nch = 1 << (m - 1 - K);
    int desc = (cfirst && t >= 2);
    for (int hh = 0; hh < nch; hh++) {
        int h = desc ? nch - 1 - hh : hh;
        int v = base + h * step;
        nodes++;
        depth_nodes[t]++;
        if ((nodes & 0xFFFFF) == 0) {
            if (time_cap > 0 && (double)(clock() - c0) / CLOCKS_PER_SEC > time_cap) { aborted = 1; return; }
            if ((nodes & 0x3FFFFFFF) == 0) progress();
        }
        P[t] = P[t - 1] + v;
        int ok = 1;
        int Lmax = t; if (Lmax > n - 1) Lmax = n - 1;
        for (int L = 3; L <= Lmax; L += 2)
            if ((P[t] - P[t - L]) % L == 0) { ok = 0; break; }
        if (!ok) continue;
        if (used[v >> 6] & (1ULL << (v & 63))) { fprintf(stderr, "INTERNAL ERROR: reuse\n"); exit(2); }
        sigma[t] = v;
        if (t > max_depth) max_depth = t;
        used[v >> 6] |= 1ULL << (v & 63);
        rec(t + 1);
        used[v >> 6] &= ~(1ULL << (v & 63));
        if (aborted) return;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s m [-t secs] [-c] [-p maxprint] [-o file] [-s maxsol]\n", argv[0]); return 1; }
    m = atoi(argv[1]);
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "-t")) time_cap = atof(argv[++i]);
        else if (!strcmp(argv[i], "-c")) cfirst = 1;
        else if (!strcmp(argv[i], "-p")) maxprint = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-o")) solf = fopen(argv[++i], "w");
        else if (!strcmp(argv[i], "-s")) maxsol = strtoull(argv[++i], NULL, 10);
    }
    if (m < 2 || m > 12) { fprintf(stderr, "m out of range (2..12)\n"); return 1; }
    n = (1 << m) - 1;
    printf("tree2 m=%d n=%d candidates=2^%d order=%s\n", m, n, (1 << m) - 1 - m, cfirst ? "construction-first" : "ascending");
    fflush(stdout);
    c0 = clock();
    sigma[0] = 0; P[0] = 0; memset(used, 0, sizeof used); used[0] = 1;
    rec(1);
    double secs = (double)(clock() - c0) / CLOCKS_PER_SEC;
    if (solf) fclose(solf);
    printf("%s tree2 m=%d n=%d solutions=%llu nodes=%llu maxdepth=%d time=%.3fs\n",
           aborted == 1 ? "INCOMPLETE(time cap)" : aborted == 2 ? "STOPPED(maxsol reached)" : "COMPLETE",
           m, n, solutions, nodes, max_depth, secs);
    printf("nodes per depth (first 40):");
    for (int t = 1; t <= n && t <= 40; t++) printf(" %d:%llu", t, depth_nodes[t]);
    printf("\n");
    return aborted;
}
