/* codings.c — apply every set partition of the 8 letters of a base word (file
 * of digits 0..7) and report which coded words remain 3-free up to length N.
 * usage: ./codings wordfile N
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define KMAX 8
static int N;
static unsigned char *base;
static unsigned char *w;
static int (*P)[KMAX];
static inline int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

/* returns first length at which coded word fails, or N if 3-free to N */
static int check(int k) {
    memset(P[0], 0, sizeof(P[0]));
    for (int n = 0; n < N; n++) {
        int c = w[n];
        int v[KMAX]; for (int i = 0; i < k; i++) v[i] = 0; v[c] = 1;
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
                if (bad) return n + 1;
            }
            v[w[beta - 1]]++;
        }
        for (int i = 0; i < k; i++) P[n + 1][i] = P[n][i];
        P[n + 1][c]++;
    }
    return N;
}

static int rgs[8];
static long total = 0;
static void enumerate(int pos, int maxsofar) {
    if (pos == 8) {
        int k = maxsofar + 1;
        if (k == 8 || k < 3) return;
        for (int n = 0; n < N; n++) w[n] = rgs[base[n]];
        int r = check(k);
        total++;
        if (r >= N) {
            printf("SURVIVES k=%d coding=", k);
            for (int i = 0; i < 8; i++) printf("%d", rgs[i]);
            printf("\n");
            fflush(stdout);
        }
        return;
    }
    for (int c = 0; c <= maxsofar + 1; c++) {
        rgs[pos] = c;
        enumerate(pos + 1, c > maxsofar ? c : maxsofar);
    }
}

int main(int argc, char **argv) {
    N = atoi(argv[2]);
    base = malloc(N + 1); w = malloc(N + 1);
    P = malloc((size_t)(N + 1) * sizeof(*P));
    FILE *f = fopen(argv[1], "r"); int n = 0, ch;
    while ((ch = fgetc(f)) != EOF && n < N) if (ch >= '0' && ch <= '7') base[n++] = ch - '0';
    N = n; fclose(f);
    rgs[0] = 0;
    enumerate(1, 0);
    fprintf(stderr, "partitions tested: %ld\n", total);
    return 0;
}
