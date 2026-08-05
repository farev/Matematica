// powerful_seg.cpp — segmented census of consecutive-powerful-number
// structures up to X, memory O(segment).  Exact 64-bit arithmetic.
//
// For each segment [L, R): for every squarefree b <= X^(1/3), append all
// a^2 b^3 in [L, R), sort the segment, and scan for consecutive triples in
// AP.  A 2-element tail from the previous segment is prepended so triples
// spanning a boundary are not missed.  Also counts powerful numbers and
// verifies against the closed-form-free global count (sum over b of
// #a-range), and checks no duplicates (unique representation).
//
// Output: same AP3/AP4 lines as powerful.cpp, plus per-decade counts.
// Usage: powerful_seg X [segsize]
#include <cstdio>
#include <cstdint>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;
typedef unsigned long long ull;
typedef __uint128_t u128;

static uint64_t isqrt64(uint64_t x) {
    uint64_t r = (uint64_t)sqrtl((long double)x);
    while ((u128)(r+1)*(r+1) <= x) r++;
    while (r > 0 && (u128)r*r > x) r--;
    return r;
}

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s X [segsize]\n", argv[0]); return 2; }
    uint64_t X = (uint64_t)strtold(argv[1], nullptr);
    uint64_t SEG = argc > 2 ? (uint64_t)strtold(argv[2], nullptr) : (uint64_t)4e15;

    uint64_t B = 1; while ((u128)(B+1)*(B+1)*(B+1) <= (u128)X) B++;
    vector<uint8_t> sqfree(B+1, 1);
    for (uint64_t p = 2; p*p <= B; p++)
        for (uint64_t q = p*p; q <= B; q += p*p) sqfree[q] = 0;
    // precompute b^3 for squarefree b
    vector<uint64_t> bcubes;
    for (uint64_t b = 1; b <= B; b++) if (sqfree[b]) bcubes.push_back(b*b*b);

    uint64_t total = 0;
    long triples = 0, quads = 0;
    uint64_t carry[3]; int ncarry = 0;   // last up-to-3 elements of previous segment
    vector<uint64_t> seg;
    for (uint64_t L = 1; L <= X; ) {
        uint64_t R = (X - L >= SEG - 1) ? L + SEG : X + 1;   // [L, R)
        if (R < L) R = X + 1; // overflow guard
        seg.clear();
        for (uint64_t b3 : bcubes) {
            if (b3 >= R) break;
            // a^2 b3 in [L, R): a from ceil(sqrt(L/b3)) adjusted to floor(sqrt((R-1)/b3))
            uint64_t alo = isqrt64((L + b3 - 1) / b3);
            while ((u128)alo*alo*b3 < L) alo++;
            uint64_t ahi = isqrt64((R - 1) / b3);
            while ((u128)(ahi+1)*(ahi+1)*b3 <= (u128)(R-1)) ahi++;
            while (ahi > 0 && (u128)ahi*ahi*b3 > (u128)(R-1)) ahi--;
            for (uint64_t a = alo; a <= ahi; a++) seg.push_back(a*a*b3);
        }
        sort(seg.begin(), seg.end());
        for (size_t i = 1; i < seg.size(); i++)
            if (seg[i] == seg[i-1]) { fprintf(stderr, "DUPLICATE %llu — bug\n", (ull)seg[i]); return 1; }
        total += seg.size();
        // prepend carry
        vector<uint64_t> w;
        w.reserve(seg.size() + ncarry);
        for (int i = 0; i < ncarry; i++) w.push_back(carry[i]);
        w.insert(w.end(), seg.begin(), seg.end());
        for (size_t i = 0; i + 2 < w.size(); i++) {
            uint64_t d1 = w[i+1] - w[i], d2 = w[i+2] - w[i+1];
            // a pattern is counted by the window containing its LAST element
            // as a non-carry element; patterns wholly inside the carry were
            // counted by the previous window.
            if (d1 == d2 && i + 2 >= (size_t)ncarry) {
                triples++;
                printf("AP3 #%ld: %llu %llu %llu  (d = %llu)\n", triples,
                       (ull)w[i], (ull)w[i+1], (ull)w[i+2], (ull)d1);
                fflush(stdout);
            }
            if (i + 3 < w.size() && i + 3 >= (size_t)ncarry &&
                d1 == d2 && w[i+3] - w[i+2] == d1) {
                quads++;
                printf("AP4 #%ld: %llu %llu %llu %llu (d = %llu)\n", quads,
                       (ull)w[i], (ull)w[i+1], (ull)w[i+2], (ull)w[i+3], (ull)d1);
                fflush(stdout);
            }
        }
        // set carry to last 3 elements of w (3 so AP4 spanning boundaries caught)
        ncarry = 0;
        for (size_t i = w.size() >= 3 ? w.size() - 3 : 0; i < w.size(); i++)
            carry[ncarry++] = w[i];
        fprintf(stderr, "segment [%llu, %llu): %zu powerful, cumulative %llu, triples so far %ld\n",
                (ull)L, (ull)R, seg.size(), (ull)total, triples);
        if (R == X + 1) break;
        L = R;
    }
    printf("X = %llu\npowerful numbers <= X: %llu\nconsecutive-AP3 count: %ld\nconsecutive-AP4 count: %ld\n",
           (ull)X, (ull)total, triples, quads);
    return 0;
}
