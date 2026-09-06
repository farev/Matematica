// Independent implementation of OEIS A398259 from its definition:
// a(1)=0; for n>=2, s = digit sum of a(n-1); if s = a(m) for some m < n-1, take the greatest
// such m and set a(n) = n-1-m; otherwise a(n) = 0.   (1-indexed as in the OEIS)
// Reports all zeros up to N, the checkpoint values a(10^4), a(10^5), a(10^6), and a(N).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc, char **argv) {
    long long N = atoll(argv[1]);
    // last[v] = greatest index m (1-based) with a(m) = v among terms processed so far; 0 = never.
    // values are bounded by N, so an array of size N+1 suffices.
    uint32_t *last = calloc((size_t)N + 2, sizeof(uint32_t));
    if (!last) { fprintf(stderr, "alloc failed\n"); return 1; }
    long long prev = 0;   // a(1) = 0
    long long nzeros = 0; long long zeros_listed = 0;
    printf("zeros:");
    // a(1) = 0 is a zero
    printf(" 1"); nzeros++;
    for (long long n = 2; n <= N; n++) {
        // record a(n-1) = prev at index n-1 AFTER using it for lookup of s (m < n-1 required)
        long long s = 0, t = prev; while (t) { s += t % 10; t /= 10; }
        long long a;
        if (s <= N && last[s] != 0) a = (n - 1) - (long long)last[s]; else a = 0;
        last[prev] = (uint32_t)(n - 1);
        if (a == 0) { nzeros++; if (nzeros <= 40) printf(" %lld", n); }
        if (n == 10000 || n == 100000 || n == 1000000) printf("\n  a(%lld) = %lld", n, a);
        if (n == N) printf("\n  a(%lld) = %lld", n, a);
        if (n >= 700000440 && n <= 700000443) printf("\n  a(%lld) = %lld", n, a);
        prev = a;
    }
    printf("\ntotal zeros up to %lld: %lld\n", N, nzeros);
    return 0;
}
