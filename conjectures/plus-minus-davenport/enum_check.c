/* enum_check.c — engine E4: from-definition validation for one group.
 *
 * Enumerates plain COMBINATIONS of elements (no DFS, no incremental
 * signed-sum state — nothing shared with dpm_search.c's method) and tests
 * each candidate set for dissociativity by direct iteration over all
 * 3^l sign patterns (early exit on the first vanishing combination).
 * Counts dissociated sets of the requested size.
 *
 * Usage: ./enum_check a b l [--full]
 *   a b : group Z_a x Z_b     l : subset size to enumerate
 *   default universe: sign-representatives (one of {g,-g}, g != 0);
 *   --full: all nonzero elements.
 *
 * Exact integer arithmetic; no floats.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int A, B, N;

static int is_dissociated(const int *set, int l) {
    /* iterate c in {-1,0,1}^l \ {0} via base-3 counter */
    int c[16];
    memset(c, 0, sizeof(c));
    long long total = 1;
    for (int i = 0; i < l; i++) total *= 3;
    for (long long it = 1; it < total; it++) {
        /* increment base-3 counter */
        int pos = 0;
        while (c[pos] == 2) { c[pos] = 0; pos++; }
        c[pos]++;
        /* evaluate: digit 0 -> coeff 0, 1 -> +1, 2 -> -1 */
        int sx = 0, sy = 0;
        for (int i = 0; i < l; i++) {
            if (!c[i]) continue;
            int g = set[i], x = g / B, y = g % B;
            if (c[i] == 1) { sx += x; sy += y; }
            else { sx -= x; sy -= y; }
        }
        if (sx % A == 0 && sy % B == 0) return 0;
    }
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: enum_check a b l [--full]\n"); return 1; }
    A = atoi(argv[1]); B = atoi(argv[2]);
    int l = atoi(argv[3]);
    int full = (argc > 4 && !strcmp(argv[4], "--full"));
    N = A * B;
    int univ[8192], nu = 0;
    for (int g = 1; g < N; g++) {
        int x = g / B, y = g % B;
        int ng = ((A - x) % A) * B + (B - y) % B;
        if (full || g <= ng) univ[nu++] = g;
    }
    /* enumerate combinations of univ of size l */
    int idx[16];
    for (int i = 0; i < l; i++) idx[i] = i;
    long long count = 0, tried = 0;
    int set[16];
    if (l > nu) { printf("%d %d size=%d universe=%d count=0 tried=0\n", A, B, l, nu); return 0; }
    while (1) {
        for (int i = 0; i < l; i++) set[i] = univ[idx[i]];
        tried++;
        if (is_dissociated(set, l)) count++;
        /* next combination */
        int i = l - 1;
        while (i >= 0 && idx[i] == nu - l + i) i--;
        if (i < 0) break;
        idx[i]++;
        for (int j = i + 1; j < l; j++) idx[j] = idx[j-1] + 1;
    }
    printf("%d %d size=%d universe=%d count=%lld tried=%lld\n",
           A, B, l, nu, count, tried);
    return 0;
}
