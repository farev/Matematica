/* checkmorph.c — test whether the fixed point of a cyclic uniform morphism over
 * Z_k is 3-free up to length N.
 *
 * The morphism is phi(r) = (c_0 + r)(c_1 + r)...(c_{b-1} + r) mod k, and the
 * fixed point starting with letter 0 is t_n = sum of c_{d} over the base-b
 * digits d of n, reduced mod k (a generalised Thue–Morse word).
 *
 * usage: ./checkmorph k N c_0 c_1 ... c_{b-1}
 *   or   ./checkmorph k N -f wordfile        (word given as digits, one per char)
 * Prints the first bad pair (alpha, beta, gamma) if any, else "3-free to N".
 * Same incremental check as tf.c; cost is O(N^2 log N)-ish.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KMAX 64
static int k, N;
static unsigned char *w;
static int (*P)[KMAX];

static inline int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    k = atoi(argv[1]); N = atoi(argv[2]);
    w = malloc(N + 1);
    P = malloc((size_t)(N + 1) * sizeof(*P));
    if (strcmp(argv[3], "-f") == 0) {
        FILE *f = fopen(argv[4], "r");
        int n = 0, ch;
        while ((ch = fgetc(f)) != EOF && n < N) {
            if (ch >= '0' && ch <= '9') w[n++] = ch - '0';
            else if (ch >= 'a' && ch <= 'z') w[n++] = ch - 'a' + 10;
            else if (ch >= 'A' && ch <= 'Z') w[n++] = ch - 'A' + 36;
        }
        N = n;
        fclose(f);
    } else {
        int b = argc - 3;
        int c[64];
        for (int i = 0; i < b; i++) c[i] = atoi(argv[3 + i]);
        for (int n = 0; n < N; n++) {
            int m = n, t = 0;
            while (m) { t += c[m % b]; m /= b; }
            w[n] = t % k;
        }
    }
    memset(P[0], 0, sizeof(P[0]));
    for (int n = 0; n < N; n++) {
        int c = w[n];
        /* check append of c at position n */
        int v[KMAX]; for (int i = 0; i < k; i++) v[i] = 0; v[c] = 1;
        for (int beta = n; beta >= 1; beta--) {
            int q = n + 1 - beta;
            int g = 0;
            for (int i = 0; i < k; i++) g = gcd(g, v[i]);
            int s = q / g;
            for (int m = 1; ; m++) {
                int alpha = beta - m * s;
                if (alpha < 0) break;
                int bad = 1;
                for (int i = 0; i < k; i++)
                    if ((P[beta][i] - P[alpha][i]) * g != m * v[i]) { bad = 0; break; }
                if (bad) {
                    printf("BAD PAIR: alpha=%d beta=%d gamma=%d (p=%d q=%d) x=", alpha, beta, n + 1, beta - alpha, q);
                    for (int i = alpha; i < beta; i++) printf("%d,", w[i]);
                    printf(" y=");
                    for (int i = beta; i <= n; i++) printf("%d,", w[i]);
                    printf("\n");
                    return 2;
                }
            }
            v[w[beta - 1]]++;
        }
        for (int i = 0; i < k; i++) P[n + 1][i] = P[n][i];
        P[n + 1][c]++;
    }
    printf("3-free to N=%d (k=%d)\n", N, k);
    return 0;
}
