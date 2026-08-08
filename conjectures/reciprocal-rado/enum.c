/* Fast exact enumerator of canonical solutions of
       1/x_1 + ... + 1/x_k = 1/y,   y < x_1 <= ... <= x_k <= n.
   Usage: enum k n [--count]
   Emits one line per solution: "y x1 ... xk"; with --count, only the total.
   All arithmetic in unsigned 64-bit / __int128 where products appear; the
   remainder is kept as a reduced fraction a/b. Overflow safety: b <= lcm of
   at most k denominators <= n^k can exceed 64 bits for large k, so the
   remainder is reduced at every step and products use __int128 with an
   explicit range check (abort on overflow rather than wrap).
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t g_n;
static int g_k, g_count_only;
static uint64_t g_count = 0;
static uint64_t g_xs[64];

static uint64_t gcd64(uint64_t a, uint64_t b) {
    while (b) { uint64_t t = a % b; a = b; b = t; }
    return a;
}

static void emit(uint64_t y) {
    g_count++;
    if (!g_count_only) {
        printf("%llu", (unsigned long long)y);
        for (int i = 0; i < g_k; i++)
            printf(" %llu", (unsigned long long)g_xs[i]);
        putchar('\n');
    }
}

/* j terms remain, each denom in [lo, n], summing exactly to a/b (reduced). */
static void dfs(int j, uint64_t lo, uint64_t a, uint64_t b, uint64_t y) {
    if (j == 1) {
        if (a > 0 && b % a == 0) {
            uint64_t x = b / a;
            if (x >= lo && x <= g_n) { g_xs[g_k - 1] = x; emit(y); }
        }
        return;
    }
    uint64_t xlo = b / a + 1;            /* 1/x < a/b strictly */
    if (lo > xlo) xlo = lo;
    unsigned __int128 jb = (unsigned __int128)j * b;
    uint64_t xhi = (uint64_t)(jb / a);   /* j/x >= a/b */
    if (xhi > g_n) xhi = g_n;
    for (uint64_t x = xlo; x <= xhi; x++) {
        unsigned __int128 na128 = (unsigned __int128)a * x - b;
        unsigned __int128 nb128 = (unsigned __int128)b * x;
        if (na128 >> 64 || nb128 >> 64) {
            fprintf(stderr, "OVERFLOW at k=%d n=%llu\n", g_k,
                    (unsigned long long)g_n);
            exit(3);
        }
        uint64_t na = (uint64_t)na128, nb = (uint64_t)nb128;
        uint64_t g = gcd64(na, nb);
        g_xs[g_k - j] = x;
        dfs(j - 1, x, na / g, nb / g, y);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: enum k n [--count]\n"); return 2; }
    g_k = atoi(argv[1]);
    g_n = strtoull(argv[2], 0, 10);
    g_count_only = (argc > 3 && !strcmp(argv[3], "--count"));
    for (uint64_t y = 1; y < g_n; y++)
        dfs(g_k, y + 1, 1, y, y);
    if (g_count_only)
        printf("%llu\n", (unsigned long long)g_count);
    fprintf(stderr, "total %llu\n", (unsigned long long)g_count);
    return 0;
}
