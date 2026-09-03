/* grundy_check.c -- exhaustive check of the Bit Deletion closed forms.
 *
 * For every n < 2^K computes, straight from the game definition,
 *   (i)  the normal-play Sprague-Grundy value G(n)  (stored in bits 0-1),
 *   (ii) the misere outcome W(n) = 1 iff the player to move wins under the
 *        rule "whoever removes the last nonzero digit LOSES" (bit 2),
 * and compares them with the closed forms of NOTE.md:
 *   G(n) = (L mod 2) + 2*[t odd],   misere P-position  <=>  G(n) = 1,
 * where L = bit length and t = number of initial odd-length zero-blocks of
 * the binary expansion after the leading 1.
 *
 * All options of an L-bit number are (L-1)-bit or shorter, so each bit-length
 * level depends only on the previous levels and is computed in parallel.
 * If any Grundy value exceeded 3 the packed storage would be invalid; the
 * program detects this and aborts (it never happens: Theorem 1).
 *
 * Build:  gcc -O3 -march=native -fopenmp -o grundy_check grundy_check.c
 * Run:    ./grundy_check 32        (2^32 positions, 4 GB RAM, ~minutes on 4 cores)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <omp.h>

static inline int closed_form(uint64_t n) {
    /* returns (L mod 2) + 2*[t odd] */
    int L = 64 - __builtin_clzll(n);
    int t = 0, run = 0, broken = 0;
    /* scan bits below the leading one, from the top */
    for (int i = L - 2; i >= 0; --i) {
        int bit = (n >> i) & 1;
        if (bit == 0) { run++; }
        else {
            if (!broken) { if (run & 1) t++; else broken = 1; }
            run = 0;
        }
    }
    if (!broken) { if (run & 1) t++; }   /* last block (may be empty) */
    return (L & 1) + 2 * (t & 1);
}

int main(int argc, char **argv) {
    int K = (argc > 1) ? atoi(argv[1]) : 24;
    uint64_t N = 1ULL << K;
    uint8_t *tab = (uint8_t *)malloc(N);
    if (!tab) { fprintf(stderr, "alloc failed\n"); return 2; }
    tab[0] = 0 | 4;               /* G(0)=0; misere: player to move at 0 has already won -> W=1 */
    uint64_t mism_g = 0, mism_m = 0, overflow = 0;
    double t0 = omp_get_wtime();
    for (int L = 1; L <= K; ++L) {
        uint64_t lo = 1ULL << (L - 1), hi = 1ULL << L;
        uint64_t cnt[4] = {0, 0, 0, 0}, mp = 0;
        uint64_t mg = 0, mm = 0, ov = 0;
#pragma omp parallel for schedule(static) reduction(+:mg,mm,ov,mp) reduction(+:cnt[:4])
        for (uint64_t n = lo; n < hi; ++n) {
            unsigned mask = 0;           /* option Grundy values present */
            int misere_win = 0;
            for (int i = 0; i < L; ++i) {
                /* delete bit i counted from the top (i = 0 = leading one) */
                uint64_t top = n >> (L - i);
                uint64_t bot = n & ((1ULL << (L - i - 1)) - 1);
                uint64_t m = (top << (L - i - 1)) | bot;
                uint8_t v = tab[m];
                mask |= 1u << (v & 3);
                if (!(v & 4)) misere_win = 1;   /* an option that is a misere P-position */
            }
            int g = 0;
            while (mask >> g & 1) g++;
            if (g > 3) { ov++; g = 3; }
            tab[n] = (uint8_t)(g | (misere_win ? 4 : 0));
            int cf = closed_form(n);
            if (g != cf) mg++;
            /* misere P  <=> G == 1 */
            if ((misere_win == 0) != (g == 1)) mm++;
            cnt[g]++;
            if (!misere_win) mp++;
        }
        mism_g += mg; mism_m += mm; overflow += ov;
        printf("L=%2d  G-counts {0:%llu 1:%llu 2:%llu 3:%llu}  misere-P %llu  mismatches G:%llu misere:%llu  overflow:%llu  %.1fs\n",
               L, (unsigned long long)cnt[0], (unsigned long long)cnt[1], (unsigned long long)cnt[2],
               (unsigned long long)cnt[3], (unsigned long long)mp, (unsigned long long)mg,
               (unsigned long long)mm, (unsigned long long)ov, omp_get_wtime() - t0);
        fflush(stdout);
    }
    printf("DONE K=%d: positions checked %llu; Grundy mismatches %llu; misere mismatches %llu; values>3: %llu; threads %d; %.1fs\n",
           K, (unsigned long long)N, (unsigned long long)mism_g, (unsigned long long)mism_m,
           (unsigned long long)overflow, omp_get_max_threads(), omp_get_wtime() - t0);
    /* spot check against OEIS A398916 data */
    static const int oeis[34] = {0,1,2,0,1,3,1,1,2,0,0,2,0,0,0,0,1,3,1,1,3,1,3,3,1,1,1,1,1,1,1,1,2,0};
    int ok = 1;
    for (int i = 0; i < 34 && i < (int)N; ++i) if ((tab[i] & 3) != oeis[i]) ok = 0;
    printf("OEIS A398916 first 34 terms reproduced: %s\n", ok ? "yes" : "NO");
    free(tab);
    return (mism_g || mism_m || overflow) ? 1 : 0;
}
