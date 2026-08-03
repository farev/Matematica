/* dejean_morph.c -- search for q-uniform alpha^+-free-preserving morphisms
 * on Sigma_n = Z_n of the shift-equivariant ("cyclic") form
 *
 *      h(a)[i] = (h0[i] + a) mod n,     h0 in Sigma_n^q,  h0[0] = 0.
 *
 * Such an h automatically satisfies
 *   (H1) a -> h(a)[0]   injective,
 *   (H2) a -> h(a)[q-1] injective,
 * so by Theorem M (see NOTE.md) it suffices to check
 *   (H3) synchronization: h(c) never occurs in h(ab) at an offset 0<i<q,
 *   (H4) h(v) is alpha^+-free for every alpha^+-free v with |v| <= N0.
 *
 * With alpha = n/(n-1) (n >= 5), N0 = 2n+2 suffices; the program uses
 * N0 = ceil((alpha*P0+1)/q)+1 with P0 = ceil(2q/(alpha-1)), computed exactly
 * in integers, and takes the max with 2n+2 for safety.
 *
 * By shift-equivariance h(v+c) = h(v)+c and alpha^+-freeness is invariant
 * under adding a constant to every letter, so (H4) need only be checked for
 * v with v[0] = 0.
 *
 * Build:  gcc -O3 -march=native -o dejean_morph dejean_morph.c
 * Usage:  ./dejean_morph n qlo qhi [alpha_num alpha_den] [maxhits]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N;              /* alphabet size */
static long AN, AD;        /* alpha = AN/AD */
static int Q;              /* morphism length */
static int N0;             /* (H4) depth */
static long long checked = 0, syncpass = 0, hits = 0;
static long long MAXHITS = 20;

/* q(p) = floor(alpha*p)+1-p, the number of equalities in the shortest
 * factor of period p and exponent > alpha. */
static int qq(int p) { return (int)((AN * (long)p) / AD) + 1 - p; }

static int *QQ;            /* QQ[p] cached */
static int QQMAX;

/* alpha^+-free test, straight from the definition of the forbidden window. */
static int afree(const int *w, int L)
{
    for (int p = 1; p < L; p++) {
        int q = (p <= QQMAX) ? QQ[p] : qq(p);
        if (p + q > L) break;
        int run = 0;
        int lim = L - p;
        for (int i = 0; i < lim; i++) {
            if (w[i] == w[i + p]) { if (++run >= q) return 0; }
            else run = 0;
        }
    }
    return 1;
}

static int h0[512];

/* (H3'): for every a,b with ab alpha^+-free, every c, and every 0 < i < Q,
 * h(c) must not equal (h(a)h(b))[i..i+Q-1].  Restricting to alpha^+-free ab
 * is what the proof of Theorem M actually needs: the offending occurrence
 * always sits across two consecutive letters of an alpha^+-free word.
 *
 * With the cyclic form, (h(a)h(b))[i..i+Q-1] = h(c) forces
 *   h0[i+j]-h0[j]   = c-a  constant in j (0 <= j < Q-i)   AND
 *   h0[j]-h0[Q-i+j] = c-b  constant in j (0 <= j < i),
 * and then a-b = d2-d1, so a = b iff d1 = d2.  For alpha < 2 the word aa is
 * not alpha^+-free, so a collision with d1 == d2 is harmless.
 * Returns 1 if synchronizing (in this relativised sense). */
static int synchronizing(void)
{
    int aa_free = (AN >= 2 * AD);      /* is "aa" alpha^+-free? (alpha >= 2) */
    for (int i = 1; i < Q; i++) {
        int d1 = ((h0[i] - h0[0]) % N + N) % N, ok1 = 1;
        for (int j = 1; j < Q - i; j++)
            if (((h0[i + j] - h0[j]) % N + N) % N != d1) { ok1 = 0; break; }
        if (!ok1) continue;
        int d2 = ((h0[0] - h0[Q - i]) % N + N) % N, ok2 = 1;
        for (int j = 1; j < i; j++)
            if (((h0[j] - h0[Q - i + j]) % N + N) % N != d2) { ok2 = 0; break; }
        if (!ok2) continue;
        if (d1 != d2 || aa_free) return 0;   /* genuine collision */
    }
    return 1;
}

/* ---- (H4): DFS over alpha^+-free v with v[0]=0, |v| <= N0 ---- */
static int vbuf[64];
static int img[64 * 512];

static int h4dfs(int t)          /* v has length t, img holds h(v) */
{
    if (t == N0) return 1;
    for (int c = 0; c < N; c++) {
        vbuf[t] = c;
        if (!afree(vbuf, t + 1)) continue;          /* v must be alpha^+-free */
        for (int i = 0; i < Q; i++)
            img[t * Q + i] = (h0[i] + c) % N;
        if (!afree(img, (t + 1) * Q)) return 0;     /* h(v) must be too */
        if (!h4dfs(t + 1)) return 0;
    }
    return 1;
}

static int check_h4(void)
{
    vbuf[0] = 0;
    for (int i = 0; i < Q; i++) img[i] = h0[i];
    if (!afree(img, Q)) return 0;
    return h4dfs(1);
}

static void report(void)
{
    hits++;
    printf("HIT n=%d q=%d alpha=%ld/%ld h0=", N, Q, AN, AD);
    for (int i = 0; i < Q; i++) printf("%d", h0[i]);
    printf("\n");
    fflush(stdout);
}

/* DFS over alpha^+-free h0 with h0[0]=0 */
static void h0dfs(int t)
{
    if (hits >= MAXHITS) return;
    if (t == Q) {
        checked++;
        if (!synchronizing()) return;
        syncpass++;
        if (check_h4()) report();
        return;
    }
    for (int c = 0; c < N; c++) {
        h0[t] = c;
        if (afree(h0, t + 1)) h0dfs(t + 1);
    }
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "usage: %s n qlo qhi [anum aden] [maxhits]\n", argv[0]);
        return 1;
    }
    N = atoi(argv[1]);
    int qlo = atoi(argv[2]), qhi = atoi(argv[3]);
    if (argc >= 6) { AN = atol(argv[4]); AD = atol(argv[5]); }
    else if (N == 3) { AN = 7; AD = 4; }
    else if (N == 4) { AN = 7; AD = 5; }
    else { AN = N; AD = N - 1; }
    if (argc >= 7) MAXHITS = atoll(argv[6]);

    QQMAX = 4096;
    QQ = malloc((QQMAX + 1) * sizeof(int));
    for (int p = 1; p <= QQMAX; p++) QQ[p] = qq(p);

    for (Q = qlo; Q <= qhi; Q++) {
        /* P0 = ceil(2q/(alpha-1)) = ceil(2q*AD/(AN-AD)) */
        long P0 = (2L * Q * AD + (AN - AD) - 1) / (AN - AD);
        /* N0 = ceil((alpha*P0+1)/q)+1 */
        long num = AN * P0 + AD;                 /* (alpha*P0+1) = num/AD */
        long N0a = (num + (long)Q * AD - 1) / ((long)Q * AD) + 1;
        N0 = (int)(N0a > 2 * N + 2 ? N0a : 2 * N + 2);
        if (N0 > 60) N0 = 60;
        checked = syncpass = hits = 0;
        h0dfs(1);
        fprintf(stderr, "n=%d q=%d N0=%d P0=%ld: h0 candidates=%lld sync=%lld hits=%lld\n",
                N, Q, N0, P0, checked, syncpass, hits);
        fflush(stderr);
    }
    return 0;
}
