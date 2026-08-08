/* Weighted enumerator: all solutions of sum_t w_t / x_t = 1/y with
   x_1 < x_2 < ... < x_d <= n, over every composition (w_1..w_d) arising
   from partitions of k into at most dmax parts (all weight orderings).
   Output lines: "y w1 x1 w2 x2 ..." — i.e. solutions of the reciprocal
   Rado equation with at most dmax distinct x-values.
   Usage: enumw k n dmax [--count]
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t g_n, g_count = 0;
static int g_k, g_dmax, g_count_only, g_d;
static int g_wv[16];
static uint64_t g_xs[16];
static uint64_t g_suffix[16];

static uint64_t gcd64(uint64_t a, uint64_t b) {
    while (b) { uint64_t t = a % b; a = b; b = t; }
    return a;
}

static void dfs(int t, uint64_t lo, uint64_t a, uint64_t b, uint64_t y) {
    uint64_t w = (uint64_t)g_wv[t];
    if (t == g_d - 1) {
        unsigned __int128 wb = (unsigned __int128)w * b;
        if (a > 0 && wb % a == 0) {
            uint64_t x = (uint64_t)(wb / a);
            if (x >= lo && x <= g_n) {
                g_xs[t] = x;
                g_count++;
                if (!g_count_only) {
                    printf("%llu", (unsigned long long)y);
                    for (int i = 0; i < g_d; i++)
                        printf(" %d %llu", g_wv[i], (unsigned long long)g_xs[i]);
                    putchar('\n');
                }
            }
        }
        return;
    }
    unsigned __int128 wb = (unsigned __int128)w * b;
    uint64_t xlo = (uint64_t)(wb / a) + 1;          /* w/x < a/b strictly */
    if (lo > xlo) xlo = lo;
    unsigned __int128 sb = (unsigned __int128)g_suffix[t] * b;
    uint64_t xhi = (uint64_t)(sb / a);              /* suffix/x >= a/b */
    if (xhi > g_n) xhi = g_n;
    for (uint64_t x = xlo; x <= xhi; x++) {
        unsigned __int128 na128 = (unsigned __int128)a * x - wb;
        unsigned __int128 nb128 = (unsigned __int128)b * x;
        if (na128 >> 64 || nb128 >> 64) { fprintf(stderr, "OVERFLOW\n"); exit(3); }
        uint64_t na = (uint64_t)na128, nb = (uint64_t)nb128;
        uint64_t g = gcd64(na, nb);
        g_xs[t] = x;
        dfs(t + 1, x + 1, na / g, nb / g, y);
    }
}

static void run_perm(void) {
    for (int t = g_d - 1; t >= 0; t--)
        g_suffix[t] = (t == g_d - 1 ? 0 : g_suffix[t + 1]) + (uint64_t)g_wv[t];
    for (uint64_t y = 1; y < g_n; y++)
        dfs(0, y + 1, 1, y, y);
}

/* generate all distinct permutations of parts[] via recursion with dedup */
static int parts[16], nparts;
static int used[16];
static void perms(int pos) {
    if (pos == nparts) { g_d = nparts; run_perm(); return; }
    int prev = -1;
    for (int i = 0; i < nparts; i++) {
        if (used[i] || parts[i] == prev) continue;
        used[i] = 1; prev = parts[i];
        g_wv[pos] = parts[i];
        perms(pos + 1);
        used[i] = 0;
    }
}

static void partitions(int rem, int maxpart, int depth) {
    if (rem == 0) {
        nparts = depth;
        memset(used, 0, sizeof used);
        perms(0);
        return;
    }
    if (depth == g_dmax) return;
    int cap = rem < maxpart ? rem : maxpart;
    for (int p = cap; p >= 1; p--) {
        parts[depth] = p;
        partitions(rem - p, p, depth + 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: enumw k n dmax [--count]\n"); return 2; }
    g_k = atoi(argv[1]);
    g_n = strtoull(argv[2], 0, 10);
    g_dmax = atoi(argv[3]);
    g_count_only = (argc > 4 && !strcmp(argv[4], "--count"));
    partitions(g_k, g_k, 0);
    fprintf(stderr, "total %llu\n", (unsigned long long)g_count);
    return 0;
}
