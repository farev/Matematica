/* dval.c -- exact d(A) for sets read from stdin (one set per line, whitespace-separated
 * positive integers, lines starting with '#' ignored).
 *
 * d(A) = size of the largest dissociated subset.  The family of dissociated
 * subsets is closed under taking subsets (the subset sums of B' ⊂ B are among
 * those of B, so a collision in B' is a collision in B), so a DFS that extends a
 * dissociated subset by a larger element, and prunes as soon as a subset sum
 * collides, visits exactly the dissociated subsets.  d(A) is the maximum depth.
 * Output line:  d=<d> n=<n> witness: <elements>   | <input set>
 *
 * Build: gcc -O2 -o dval dval.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 64
#define MAXD 16   /* sums[][] is (MAXD+1) * 2^MAXD ints; d(A) <= 16 for every set here (W <= 65536) */

static int n, A[MAXN];
static int best, bestw[MAXD], cur[MAXD];
static int sums[MAXD + 1][1 << MAXD]; /* sums[depth] = sorted subset sums of cur[0..depth) */
static long long visited;

/* merge sums[d] (size 2^d) with sums[d]+x into sums[d+1]; return 0 on collision */
static int extend(int d, int x) {
    int nn = 1 << d; const int *s = sums[d]; int *t = sums[d + 1];
    int p = 0, q = 0, o = 0;
    while (p < nn && q < nn) {
        int s1 = s[p], s2 = s[q] + x;
        if (s1 == s2) return 0;
        if (s1 < s2) t[o++] = s[p++]; else t[o++] = s[q++] + x;
    }
    while (p < nn) t[o++] = s[p++];
    while (q < nn) t[o++] = s[q++] + x;
    return 1;
}

static void dfs(int d, int start) {
    if (d > best) { best = d; memcpy(bestw, cur, d * sizeof(int)); }
    if (d >= MAXD) return;
    if (d + (n - start) <= best) return;  /* cannot beat best */
    for (int i = start; i < n; i++) {
        if (d + (n - i) <= best) return;
        if (extend(d, A[i])) {
            visited++;
            cur[d] = A[i];
            dfs(d + 1, i + 1);
        }
    }
}

static int cmpint(const void *x, const void *y) { return *(const int *)x - *(const int *)y; }

int main(void) {
    char line[65536];
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '#' || line[0] == '\n') { fputs(line, stdout); continue; }
        n = 0; char *p = line;
        while (*p) {
            while (*p == ' ' || *p == '\t' || *p == ',' || *p == '\n' || *p == '\r') p++;
            if (!*p) break;
            char *e; long v = strtol(p, &e, 10);
            if (e == p) { p++; continue; }
            if (n < MAXN) A[n++] = (int)v;
            p = e;
        }
        if (n == 0) continue;
        qsort(A, n, sizeof(int), cmpint);
        for (int i = 1; i < n; i++) if (A[i] == A[i - 1] || A[0] <= 0) { fprintf(stderr, "bad set (dup/nonpositive)\n"); exit(1); }
        best = 0; visited = 0; sums[0][0] = 0;
        dfs(0, 0);
        printf("d=%d n=%d witness:", best, n);
        for (int i = 0; i < best; i++) printf(" %d", bestw[i]);
        printf("   |");
        for (int i = 0; i < n; i++) printf(" %d", A[i]);
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
