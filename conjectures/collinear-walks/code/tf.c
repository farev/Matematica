/* tf.c — exhaustive search for 3-free words (no two adjacent nonempty blocks
 * with proportional Parikh vectors) over k letters.
 *
 * A word b_0 b_1 ... over {0..k-1} is 3-free iff the unit-step walk
 * P_n = sum_{j<n} e_{b_j} in N^k has no three collinear points
 * (Shallit, arXiv:2609.05780, Prop. 1; Korsky, arXiv:2608.07906, Sec. 2).
 *
 * usage: ./tf k maxlen [countcap]
 *   Depth-first search over canonical words (letters introduced in increasing
 *   order: the first letter is 0 and a new letter is always the smallest unused
 *   one). Prints, for each length n, the number of canonical 3-free words of
 *   length n (search is exhaustive unless a count cap is hit at some depth).
 *   Exits with the largest length reached; if the search finishes with no word
 *   of length maxlen, L(k) < maxlen and the last nonzero length is L(k).
 *
 * Incremental check when appending letter c at position n (new length n+1):
 *   for every beta in [1, n]: y = b[beta..n], q = n+1-beta, v = Parikh(y),
 *   g = gcd(v), v0 = v/g, s = q/g = |v0|_1. A bad partner x = b[alpha..beta-1]
 *   must have Parikh(x) = m*v0, hence length m*s, hence alpha = beta - m*s.
 *   Check P[beta] - P[alpha] == m*v0 for m = 1, 2, ... while alpha >= 0.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KMAX 16
#define NMAX 100000

static int k, maxlen;
static unsigned char w[NMAX + 1];
static int P[NMAX + 1][KMAX];   /* prefix Parikh vectors */
static unsigned long long cnt[NMAX + 2];
static unsigned long long nodes = 0;
static unsigned long long countcap = 0; /* 0 = no cap */
static int best = 0;
static unsigned char bestw[NMAX + 1];

static inline int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

/* returns 1 if appending c at position n keeps the word 3-free */
static int ok_append(int n, int c) {
    int v[KMAX];
    for (int i = 0; i < k; i++) v[i] = 0;
    v[c] = 1;
    /* P[n+1] = P[n] + e_c is implicit: P[n+1]-P[beta] = v maintained below */
    for (int beta = n; beta >= 1; beta--) {
        /* v = Parikh(b[beta..n]) */
        int q = n + 1 - beta;
        int g = 0;
        for (int i = 0; i < k; i++) g = gcd(g, v[i]);
        int s = q / g;
        for (int m = 1; ; m++) {
            int alpha = beta - m * s;
            if (alpha < 0) break;
            int bad = 1;
            for (int i = 0; i < k; i++) {
                if ((P[beta][i] - P[alpha][i]) * g != m * v[i]) { bad = 0; break; }
            }
            if (bad) return 0;
        }
        v[w[beta - 1]]++;
    }
    return 1;
}

static void dfs(int n, int used) {
    nodes++;
    cnt[n]++;
    if (n > best) { best = n; memcpy(bestw, w, n); }
    if (n >= maxlen) return;
    if (countcap && cnt[n] > countcap) return;
    int lim = used < k ? used + 1 : k;   /* canonical: new letter = smallest unused */
    for (int c = 0; c < lim; c++) {
        if (n > 0 && w[n - 1] == c) continue; /* xx is a bad pair (1,1) */
        if (!ok_append(n, c)) continue;
        w[n] = c;
        for (int i = 0; i < k; i++) P[n + 1][i] = P[n][i];
        P[n + 1][c]++;
        dfs(n + 1, c == used ? used + 1 : used);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s k maxlen [countcap]\n", argv[0]); return 1; }
    k = atoi(argv[1]); maxlen = atoi(argv[2]);
    if (argc > 3) countcap = strtoull(argv[3], 0, 10);
    if (k > KMAX || maxlen > NMAX) { fprintf(stderr, "limits\n"); return 1; }
    memset(P, 0, sizeof(P));
    memset(cnt, 0, sizeof(cnt));
    dfs(0, 0);
    printf("k=%d maxlen=%d nodes=%llu best=%d\n", k, maxlen, nodes, best);
    for (int n = 0; n <= best; n++) printf("n=%d count=%llu\n", n, cnt[n]);
    printf("longest: ");
    for (int i = 0; i < best; i++) printf("%d", bestw[i]);
    printf("\n");
    return 0;
}
