// powerful.cpp — exact census of 3-term arithmetic progressions of
// CONSECUTIVE powerful numbers up to a bound X.
//
// A powerful number is n such that p | n implies p^2 | n. Every powerful
// number is uniquely n = a^2 * b^3 with b squarefree. We enumerate all of
// them up to X (64-bit integer arithmetic only), sort, verify uniqueness
// (no duplicates — a representation-correctness self-test), then scan the
// sorted list for consecutive triples in arithmetic progression, i.e.
// indices i with P[i+1]-P[i] == P[i+2]-P[i+1]. Also reports consecutive
// 4-term APs and pairs with gap 1 (calibration against OEIS A060355).
//
// Usage: powerful X [--pairs]
// Compile: g++ -O2 -o powerful powerful.cpp
#include <cstdio>
#include <cstdint>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s X [--pairs]\n", argv[0]); return 2; }
    long double Xd = strtold(argv[1], nullptr);
    uint64_t X = (uint64_t)Xd;
    bool show_pairs = argc > 2 && !strcmp(argv[2], "--pairs");

    // cube root bound for b
    uint64_t B = 1; while ((__uint128_t)(B+1)*(B+1)*(B+1) <= (__uint128_t)X) B++;

    // squarefree sieve up to B
    vector<uint8_t> sqfree(B+1, 1);
    for (uint64_t p = 2; p*p <= B; p++) {
        if (!sqfree[p*p] && p > 2) { /* p*p already marked; p may be non-prime, harmless */ }
        for (uint64_t q = p*p; q <= B; q += p*p) sqfree[q] = 0;
    }

    // enumerate a^2 b^3 <= X, b squarefree
    vector<uint64_t> P;
    {
        // estimate count ~ 2.1732 * sqrt(X)
        double est = 2.1732 * sqrt((double)X) * 1.02 + 1000;
        P.reserve((size_t)est);
    }
    for (uint64_t b = 1; b <= B; b++) {
        if (!sqfree[b]) continue;
        uint64_t b3 = b*b*b;
        if (b3 > X) break;
        uint64_t amax = (uint64_t)sqrtl((long double)(X / b3));
        while ((__uint128_t)(amax+1)*(amax+1)*b3 <= (__uint128_t)X) amax++;
        while (amax > 0 && (__uint128_t)amax*amax*b3 > (__uint128_t)X) amax--;
        for (uint64_t a = 1; a <= amax; a++) P.push_back(a*a*b3);
    }
    sort(P.begin(), P.end());

    // uniqueness self-test: representation a^2 b^3 (b squarefree) is a
    // bijection onto powerful numbers, so duplicates indicate a bug.
    for (size_t i = 1; i < P.size(); i++)
        if (P[i] == P[i-1]) { fprintf(stderr, "DUPLICATE at %llu — bug\n", (unsigned long long)P[i]); return 1; }

    printf("X = %llu\n", (unsigned long long)X);
    printf("powerful numbers <= X: %zu\n", P.size());

    // pairs with gap 1 (A060355 calibration)
    if (show_pairs) {
        int shown = 0;
        for (size_t i = 0; i + 1 < P.size() && shown < 10; i++)
            if (P[i+1] - P[i] == 1) { printf("pair: (%llu, %llu)\n", (unsigned long long)P[i], (unsigned long long)P[i+1]); shown++; }
    }

    // consecutive triples in AP
    long triples = 0;
    for (size_t i = 0; i + 2 < P.size(); i++) {
        uint64_t d1 = P[i+1] - P[i], d2 = P[i+2] - P[i+1];
        if (d1 == d2) {
            triples++;
            printf("AP3 #%ld: %llu %llu %llu  (d = %llu)\n", triples,
                   (unsigned long long)P[i], (unsigned long long)P[i+1],
                   (unsigned long long)P[i+2], (unsigned long long)d1);
        }
    }
    printf("consecutive-AP3 count: %ld\n", triples);

    // consecutive 4-term APs (free readout)
    long quads = 0;
    for (size_t i = 0; i + 3 < P.size(); i++) {
        uint64_t d1 = P[i+1] - P[i], d2 = P[i+2] - P[i+1], d3 = P[i+3] - P[i+2];
        if (d1 == d2 && d2 == d3) {
            quads++;
            printf("AP4 #%ld: %llu %llu %llu %llu (d = %llu)\n", quads,
                   (unsigned long long)P[i], (unsigned long long)P[i+1],
                   (unsigned long long)P[i+2], (unsigned long long)P[i+3],
                   (unsigned long long)d1);
        }
    }
    printf("consecutive-AP4 count: %ld\n", quads);
    return 0;
}
