/* Independent witness checker for reciprocal Rado colorings, in C.
   Reads a witness file: line 1 "n r k", line 2: n colors in 0..r-1.
   Verifies NO color class contains x_1 <= ... <= x_k, y (all in class)
   with sum 1/x_i = 1/y.  Exact arithmetic in unsigned __int128 with gcd
   reduction (headroom: denominators can reach ~10^24 at k = 8; 128-bit
   holds ~3.4e38; overflow is detected and aborts rather than wraps).
   Same mathematical contract as verify_witness.py; independent code.
   Usage: check_class witness_file [--all]
     default: print first violation and exit 1, or "WITNESS OK" exit 0.
     --all:   print every violation (capped at 1000), exit 1 if any.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;
typedef unsigned long long u64;

static int n, r, k, dmax;    /* dmax: max distinct x-values (k = full) */
static int *col;
static u64 *cls;             /* current class, sorted */
static int cn;               /* class size */
static u64 xs[64];
static int print_all, nviol = 0;

static u128 gcd128(u128 a, u128 b) {
    while (b) { u128 t = a % b; a = b; b = t; }
    return a;
}

static void print_viol(int c, u64 y, int depth) {
    printf("VIOLATION in color %d: ", c);
    for (int i = 0; i < depth; i++)
        printf("%s1/%llu", i ? " + " : "", xs[i]);
    printf(" = 1/%llu  (all in class)\n", y);
    nviol++;
}

/* find smallest index in cls with value >= v */
static int lower_idx(u64 v) {
    int lo = 0, hi = cn;
    while (lo < hi) { int m = (lo + hi) / 2; if (cls[m] < v) lo = m + 1; else hi = m; }
    return lo;
}

static int in_class(u64 v) {
    int i = lower_idx(v);
    return i < cn && cls[i] == v;
}

/* j terms remain from cls[idx..], nondecreasing, remainder a/b exact,
   nd = distinct values used so far.  Returns 1 iff stop everything. */
static int dfs(int j, int idx, u128 a, u128 b, u64 y, int c, int nd) {
    if (a == 0) return 0;
    if (j == 1) {
        if (b % a == 0) {
            u128 x128 = b / a;
            if (x128 <= (u128)n) {
                u64 x = (u64)x128;
                u64 last = (k >= 2) ? xs[k - 2] : 0;    /* nondecreasing */
                int nd2 = nd + (x != last || k < 2);
                if (x > y && x >= last && nd2 <= dmax && in_class(x)) {
                    xs[k - 1] = x;
                    print_viol(c, y, k);
                    if (!print_all || nviol >= 1000) return 1;
                }
            }
        }
        return 0;
    }
    /* x > b/a strictly (j-1 positive terms remain), and j/x >= a/b */
    u128 xmin = b / a + 1;
    int start = idx;
    if (start >= cn) return 0;
    if (xmin > (u128)cls[start]) {
        if (xmin > (u128)cls[cn - 1]) return 0;
        start = lower_idx((u64)xmin);
    }
    u64 last = (k - j >= 1) ? xs[k - j - 1] : 0;
    for (int i = start; i < cn; i++) {
        u128 x = cls[i];
        if (a * x > (u128)j * b) break;          /* even j copies too small */
        int nd2 = nd + ((u64)x != last);
        if (nd2 > dmax) {
            if ((u64)x != last) break;           /* all further x also new */
            continue;
        }
        u128 na = a * x - b, nb = b * x;
        u128 g = gcd128(na, nb);
        if (g) { na /= g; nb /= g; }
        xs[k - j] = (u64)x;
        if (dfs(j - 1, i, na, nb, y, c, nd2)) return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: check_class witness [--all] [--dmax=D]\n");
        return 2;
    }
    dmax = 0;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--all")) print_all = 1;
        else if (!strncmp(argv[i], "--dmax=", 7)) dmax = atoi(argv[i] + 7);
    }
    FILE *f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 2; }
    if (fscanf(f, "%d %d %d", &n, &r, &k) != 3) { return 2; }
    col = malloc(n * sizeof *col);
    for (int i = 0; i < n; i++)
        if (fscanf(f, "%d", &col[i]) != 1) {
            fprintf(stderr, "BAD WITNESS: short color list\n"); return 1;
        }
    fclose(f);
    for (int i = 0; i < n; i++)
        if (col[i] < 0 || col[i] >= r) {
            fprintf(stderr, "BAD WITNESS: color out of range\n"); return 1;
        }
    if (dmax <= 0 || dmax > k) dmax = k;
    cls = malloc(n * sizeof *cls);
    for (int c = 0; c < r; c++) {
        cn = 0;
        for (int i = 0; i < n; i++)
            if (col[i] == c) cls[cn++] = (u64)(i + 1);
        for (int yi = 0; yi < cn; yi++) {
            u64 y = cls[yi];
            int start = lower_idx(y + 1);
            if (start >= cn) continue;
            if (dfs(k, start, (u128)1, (u128)y, y, c, 0)) goto done;
        }
    }
done:
    if (nviol == 0) {
        if (dmax < k)
            printf("NO VIOLATION up to dmax=%d  (n=%d, r=%d, k=%d) — PARTIAL\n",
                   dmax, n, r, k);
        else
            printf("WITNESS OK  (n=%d, r=%d, k=%d)\n", n, r, k);
        return 0;
    }
    return 1;
}
