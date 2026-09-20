/* morphsearch.c — search cyclic uniform morphisms phi(r) = c + r (mod k) of
 * length L over Z_k whose fixed point (from letter 0) is 3-free to length N.
 * DFS over the image c of 0 (c_0 = 0), pruning on 3-freeness of c itself (a
 * prefix of the fixed point); each completed c is expanded to N letters and
 * checked. usage: ./morphsearch k L N [maxreport]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define KMAX 8
static int k, L, N;
static int c[64];
static unsigned char *w;
static int (*P)[KMAX];
static long candidates = 0, survivors = 0;
static inline int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

/* incremental check of appending w[n]=ch given P[0..n]; returns 1 if ok */
static int ok_append(int n, int ch) {
    if (n > 0 && w[n-1] == ch) return 0;
    int v[KMAX]; for (int i = 0; i < k; i++) v[i] = 0; v[ch] = 1;
    for (int beta = n; beta >= 1; beta--) {
        int q = n + 1 - beta, g = 0;
        for (int i = 0; i < k; i++) g = gcd(g, v[i]);
        int s = q / g;
        for (int m = 1; ; m++) {
            int alpha = beta - m * s;
            if (alpha < 0) break;
            int bad = 1;
            for (int i = 0; i < k; i++)
                if ((P[beta][i] - P[alpha][i]) * g != m * v[i]) { bad = 0; break; }
            if (bad) return 0;
        }
        v[w[beta - 1]]++;
    }
    return 1;
}
static void push(int n, int ch) {
    w[n] = ch;
    for (int i = 0; i < k; i++) P[n + 1][i] = P[n][i];
    P[n + 1][ch]++;
}

static int test_fixed_point(void) {
    /* fixed point: w[n] = sum of c[digit] over base-L digits of n, mod k */
    for (int n = 0; n < N; n++) {
        int m = n, t = 0;
        while (m) { t += c[m % L]; m /= L; }
        int ch = t % k;
        if (!ok_append(n, ch)) return n + 1;
        push(n, ch);
    }
    return N;
}

static void dfs(int j) {
    if (j == L) {
        candidates++;
        /* rebuild prefix from scratch for the fixed point test */
        int r = test_fixed_point();
        if (r >= N) {
            survivors++;
            printf("SURVIVOR k=%d L=%d c=", k, L);
            for (int i = 0; i < L; i++) printf("%d", c[i]);
            printf("\n"); fflush(stdout);
        }
        /* restore prefix P for the DFS (positions 0..L-1 = c) */
        memset(P[0], 0, sizeof(P[0]));
        for (int i = 0; i < L; i++) push(i, c[i]);
        return;
    }
    for (int ch = 0; ch < k; ch++) {
        if (j == 0 && ch != 0) break;
        /* symmetry: after 0, the second letter can be taken as 1 (negation/
           multiplication symmetries of Z_k do not all apply; keep full) */
        if (!ok_append(j, ch)) continue;
        c[j] = ch; push(j, ch);
        dfs(j + 1);
    }
}

int main(int argc, char **argv) {
    k = atoi(argv[1]); L = atoi(argv[2]); N = atoi(argv[3]);
    w = malloc(N + 1);
    P = malloc((size_t)(N + 1) * sizeof(*P));
    memset(P[0], 0, sizeof(P[0]));
    dfs(0);
    printf("k=%d L=%d N=%d candidates=%ld survivors=%ld\n", k, L, N, candidates, survivors);
    return 0;
}
