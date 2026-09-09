/* family.c — generalised Gaussian-digit walks: at binary level l choose a sign
 * s_l in {+1,-1} and an order rule o_l in {fixed, alternating}.
 *   fixed:       t(2m)   = T(m),            t(2m+1) = T(m) + s
 *   alternating: t(2m)   = T(m) + s*[m odd], t(2m+1) = T(m) + s*[m even]
 * where T is the state under the rules shifted by one level. Rules are periodic
 * with period p. The transition word is w_n = (t_n, t_{n+1}) over Z_4 x Z_4.
 * For each pattern we report the transition alphabet and the smallest number of
 * classes of a letter-to-letter coding that is 3-free to length N (exhaustive
 * over set partitions with at most MAXC classes, alphabet size <= 10).
 * usage: ./family N maxperiod MAXC
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define KMAX 16
static int N, MAXC;
static int *T[8];
static unsigned char *w;      /* coded word */
static unsigned char *tw;     /* transition letters 0..A-1 */
static int (*P)[KMAX];
static inline int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

static int check(int k) {
    memset(P[0], 0, sizeof(P[0]));
    for (int n = 0; n < N; n++) {
        int c = w[n];
        if (n > 0 && w[n-1] == c) return n + 1;
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

static int A;             /* alphabet size of transition word */
static int rgs[16];
static int bestk;
static int bestrgs[16];
static long tested;
static void enumerate(int pos, int maxsofar) {
    if (maxsofar + 1 > MAXC) return;
    if (maxsofar + 1 >= bestk) return;      /* cannot improve */
    if (pos == A) {
        int k = maxsofar + 1;
        for (int n = 0; n < N; n++) w[n] = rgs[tw[n]];
        tested++;
        if (check(k) >= N) { bestk = k; memcpy(bestrgs, rgs, sizeof(rgs)); }
        return;
    }
    for (int c = 0; c <= maxsofar + 1; c++) {
        rgs[pos] = c;
        enumerate(pos + 1, c > maxsofar ? c : maxsofar);
    }
}

int main(int argc, char **argv) {
    N = atoi(argv[1]); int maxp = atoi(argv[2]); MAXC = atoi(argv[3]);
    w = malloc(N + 2); tw = malloc(N + 2);
    P = malloc((size_t)(N + 2) * sizeof(*P));
    for (int l = 0; l < 8; l++) T[l] = malloc((N + 2) * sizeof(int));
    for (int p = 1; p <= maxp; p++) {
        int npat = 1; for (int i = 0; i < p; i++) npat *= 4;
        for (int pat = 0; pat < npat; pat++) {
            int s[8], o[8], x = pat;
            for (int l = 0; l < p; l++) { s[l] = (x & 1) ? -1 : 1; o[l] = (x >> 1) & 1; x >>= 2; }
            if (s[0] == -1) continue;   /* global conjugation symmetry */
            /* skip patterns that are repetitions of a shorter period */
            int rep = 0;
            for (int d = 1; d < p; d++) if (p % d == 0) {
                int ok = 1; for (int l = 0; l < p; l++) if (s[l] != s[l % d] || o[l] != o[l % d]) ok = 0;
                if (ok) rep = 1;
            }
            if (rep) continue;
            for (int l = 0; l < p; l++) T[l][0] = 0;
            for (int n = 1; n <= N; n++) for (int l = 0; l < p; l++) {
                int m = n >> 1, e = n & 1, par = (l + 1) % p;
                int base = T[par][m], add;
                if (o[l] == 0) add = e ? s[l] : 0;
                else add = e ? (m & 1 ? 0 : s[l]) : (m & 1 ? s[l] : 0);
                T[l][n] = ((base + add) % 4 + 4) % 4;
            }
            /* transition alphabet */
            int map[16]; for (int i = 0; i < 16; i++) map[i] = -1;
            A = 0;
            for (int n = 0; n < N; n++) {
                int tr = 4 * T[0][n] + T[0][n + 1];
                if (map[tr] < 0) map[tr] = A++;
                tw[n] = map[tr];
            }
            printf("p=%d pattern=", p);
            for (int l = 0; l < p; l++) printf("%c%c", s[l] > 0 ? '+' : '-', o[l] ? 'A' : 'F');
            printf(" transitions=%d {", A);
            for (int i = 0; i < 16; i++) if (map[i] >= 0) printf("%d%d ", i / 4, i % 4);
            printf("}");
            if (A > 12 || (A > 10 && MAXC > 5)) { printf(" (skipped)\n"); continue; }
            bestk = 99; tested = 0;
            enumerate(1, 0);
            if (bestk < 99) {
                printf(" min3free=%d coding=", bestk);
                for (int i = 0; i < A; i++) printf("%d", bestrgs[i]);
            } else printf(" min3free>%d", MAXC);
            printf(" tested=%ld\n", tested);
            fflush(stdout);
        }
    }
    return 0;
}
