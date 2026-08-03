/* dejean_fixpoint.c -- search for shift-equivariant q-uniform morphisms
 *      h(a)[i] = (h0[i] + a) mod n,   h0[0] = 0
 * whose FIXED POINT u = h^omega(0) is alpha^+-free.
 *
 * This is the weaker criterion (Theorem M', see NOTE.md): it does NOT ask h
 * to preserve alpha^+-freeness of arbitrary words, only that u itself has no
 * short over-exponent factor.  The program is a *candidate filter*: hits are
 * re-verified rigorously by pump.py (fixpoint over Fac(u)), which shares no
 * code with this file.
 *
 * Filters, cheapest first:
 *   F1  h0 is alpha^+-free                       (enforced in the DFS)
 *   F2  h0.(h0+d) is alpha^+-free for every difference d = h0[i+1]-h0[i]
 *       occurring in h0.  Necessary: the pair (0,d) occurs in u, hence
 *       h(0)h(d) is a factor of u.
 *   F3  h^2(0) is alpha^+-free
 *   F4  h^3(0) is alpha^+-free  (truncated at LMAX letters)
 *
 * Build: gcc -O3 -march=native -o dejean_fixpoint dejean_fixpoint.c
 * Usage: ./dejean_fixpoint n qlo qhi [anum aden] [maxhits]
 */
#include <stdio.h>
#include <stdlib.h>

#define LMAX 200000

static int N, Q;
static long AN, AD;
static long long MAXHITS = 20;
static int h0[512];
static int *buf, *buf2;
static long long cand, f2p, f3p, hits;

static int qq(int p) { return (int)((AN * (long)p) / AD) + 1 - p; }

static int afree(const int *w, int L)
{
    for (int p = 1; p < L; p++) {
        int q = qq(p);
        if (p + q > L) break;
        int run = 0, lim = L - p;
        for (int i = 0; i < lim; i++) {
            if (w[i] == w[i + p]) { if (++run >= q) return 0; }
            else run = 0;
        }
    }
    return 1;
}

/* write h(src[0..sl-1]) into dst, truncated at cap; return length written */
static int apply(const int *src, int sl, int *dst, int cap)
{
    int L = 0;
    for (int t = 0; t < sl && L + Q <= cap; t++) {
        int a = src[t];
        for (int i = 0; i < Q; i++) dst[L + i] = (h0[i] + a) % N;
        L += Q;
    }
    return L;
}

static void report(void)
{
    hits++;
    printf("HIT n=%d q=%d alpha=%ld/%ld h0=", N, Q, AN, AD);
    for (int i = 0; i < Q; i++) printf("%d", h0[i]);
    printf("\n");
    fflush(stdout);
}

static void leaf(void)
{
    cand++;
    /* F2 */
    int seen[64] = {0};
    for (int i = 0; i + 1 < Q; i++) {
        int d = ((h0[i + 1] - h0[i]) % N + N) % N;
        if (seen[d]) continue;
        seen[d] = 1;
        if (d == 0) return;                      /* h0 would have a square */
        for (int t = 0; t < Q; t++) { buf[t] = h0[t]; buf[Q + t] = (h0[t] + d) % N; }
        if (!afree(buf, 2 * Q)) return;
    }
    f2p++;
    /* F3 : h^2(0) */
    int L = apply(h0, Q, buf, LMAX);
    if (!afree(buf, L)) return;
    f3p++;
    /* F4 : h^3(0), truncated */
    int L2 = apply(buf, L, buf2, LMAX);
    if (!afree(buf2, L2)) return;
    report();
}

static void dfs(int t)
{
    if (hits >= MAXHITS) return;
    if (t == Q) { leaf(); return; }
    for (int c = 0; c < N; c++) {
        h0[t] = c;
        if (afree(h0, t + 1)) dfs(t + 1);
    }
}

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: %s n qlo qhi [anum aden] [maxhits]\n", argv[0]); return 1; }
    N = atoi(argv[1]);
    int qlo = atoi(argv[2]), qhi = atoi(argv[3]);
    if (argc >= 6) { AN = atol(argv[4]); AD = atol(argv[5]); }
    else if (N == 3) { AN = 7; AD = 4; }
    else if (N == 4) { AN = 7; AD = 5; }
    else { AN = N; AD = N - 1; }
    if (argc >= 7) MAXHITS = atoll(argv[6]);
    buf = malloc(sizeof(int) * LMAX);
    buf2 = malloc(sizeof(int) * LMAX);
    for (Q = qlo; Q <= qhi; Q++) {
        cand = f2p = f3p = hits = 0;
        h0[0] = 0;
        dfs(1);
        fprintf(stderr, "n=%d q=%d: cand=%lld F2ok=%lld F3ok=%lld hits=%lld\n",
                N, Q, cand, f2p, f3p, hits);
        fflush(stderr);
    }
    return 0;
}
