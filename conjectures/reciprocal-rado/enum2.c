/* Divisor-based enumerator for k=2: all solutions of 1/x + 1/y = 1/z with
   z < x <= y <= n. Parametrization: x = z + d1, y = z + d2 where d1*d2 = z^2,
   d1 <= z <= d2. Independent of the DFS in enum.c (different algorithm).
   Divisors of z^2 from the prime factorization of z via an SPF sieve.
   Usage: enum2 n [--count]      output lines: "z x y"
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: enum2 n [--count]\n"); return 2; }
    uint64_t n = strtoull(argv[1], 0, 10);
    int count_only = (argc > 2 && !strcmp(argv[2], "--count"));
    uint32_t *spf = malloc((n + 1) * sizeof *spf);
    if (!spf) { fprintf(stderr, "OOM\n"); return 3; }
    for (uint64_t i = 0; i <= n; i++) spf[i] = 0;
    for (uint64_t i = 2; i <= n; i++)
        if (!spf[i])
            for (uint64_t j = i; j <= n; j += i)
                if (!spf[j]) spf[j] = (uint32_t)i;
    uint64_t count = 0;
    uint64_t divs[16384];
    for (uint64_t z = 1; z < n; z++) {
        /* factor z, build divisors of z^2 (exponents doubled) */
        int nd = 1; divs[0] = 1;
        uint64_t m = z;
        while (m > 1) {
            uint64_t p = spf[m];
            int e = 0;
            while (m % p == 0) { m /= p; e++; }
            int e2 = 2 * e, base = nd;
            uint64_t pw = 1;
            for (int t = 1; t <= e2; t++) {
                pw *= p;
                for (int i = 0; i < base; i++) {
                    if (nd >= 16384) { fprintf(stderr, "divisor overflow\n"); return 4; }
                    divs[nd++] = divs[i] * pw;
                }
            }
        }
        for (int i = 0; i < nd; i++) {
            uint64_t d1 = divs[i];
            if (d1 > z) continue;                 /* d1 <= z <= d2 */
            uint64_t d2 = (z * z) / d1;
            uint64_t x = z + d1, y = z + d2;
            if (y <= n) {
                count++;
                if (!count_only)
                    printf("%llu %llu %llu\n", (unsigned long long)z,
                           (unsigned long long)x, (unsigned long long)y);
            }
        }
    }
    if (count_only) printf("%llu\n", (unsigned long long)count);
    fprintf(stderr, "total %llu\n", (unsigned long long)count);
    free(spf);
    return 0;
}
