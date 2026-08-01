/* firstocc_stats.c -- statistics of a first-occurrence spectrum.
 *
 * Input: a `*_firstocc_k<K>.bin` file written by lambda_coverage: a raw array
 * of 2^K uint64, entry c = the START index of the first window whose sign
 * pattern is c (0 = never occurred within the scanned range).
 *
 * The point of the exercise.  For an i.i.d. fair-coin sequence the expected
 * waiting time until the first occurrence of a fixed word w of length K is
 * given *exactly* by Conway's leading-number (Solov'ev) formula
 *
 *     A(w) = sum_{j=1..K}  delta_j(w) * 2^j ,
 *     delta_j(w) = 1 iff the length-j prefix of w equals its length-j suffix,
 *
 * measured at the position of the last letter.  Our spectrum stores the START
 * index s(w), so the model prediction is E[s(w)] = A(w) - (K-1).
 *
 * This is a parameter-free, per-pattern prediction: 2^K separate predictions
 * with no fitted constant anywhere.  The statistic reported is
 *
 *     R(w) = (s(w) + K - 1) / A(w),        model: E[R] = 1.
 *
 * A(w) varies by a factor of two across patterns (from 2^K for a word with no
 * self-overlap up to 2^{K+1}-2 for a constant word), so R is a much sharper
 * instrument than the raw s(w): it removes the entire self-overlap effect,
 * which is the dominant non-uniformity and has nothing to do with lambda.
 *
 * Aggregates emitted: overall, by popcount (number of -1's in the window),
 * and by overlap class (A(w)/2^K rounded into bins).  Run the same tool on a
 * --prng spectrum from lambda_coverage to calibrate: R is a ratio of order
 * statistics from a single stream, so its sampling error is NOT sigma/sqrt(2^K)
 * and must be read off the control, not assumed.
 *
 * Usage:  firstocc_stats FILE.bin K label
 * Build:  cc -O2 -o firstocc_stats firstocc_stats.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include <math.h>

typedef uint64_t u64;

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s FILE.bin K label\n", argv[0]); return 1; }
    int K = atoi(argv[2]);
    const char *label = argv[3];
    size_t N = (size_t)1 << K;

    u64 *s = malloc(N * sizeof(u64));
    if (!s) { perror("malloc"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("fopen"); return 1; }
    if (fread(s, sizeof(u64), N, f) != N) { fprintf(stderr, "short read\n"); return 1; }
    fclose(f);

    /* per-popcount and per-overlap-class accumulators */
    double *pc_sum = calloc(K + 1, sizeof(double));
    u64 *pc_cnt = calloc(K + 1, sizeof(u64));
    double *pc_sq = calloc(K + 1, sizeof(double));
    /* overlap class: index by the number of nontrivial overlaps (0..K-1) */
    double *ov_sum = calloc(K + 1, sizeof(double));
    u64 *ov_cnt = calloc(K + 1, sizeof(u64));

    double tot = 0, totsq = 0;
    u64 totn = 0, missing = 0;
    double rmin = 1e300, rmax = -1e300;
    u64 argmax = 0, argmin = 0;
    u64 smax = 0, argsmax = 0;

    for (size_t c = 0; c < N; c++) {
        if (s[c] == 0) { missing++; continue; }
        /* Conway leading number A(w) and the count of nontrivial overlaps */
        double A = 0;
        int novl = 0;
        for (int j = 1; j <= K; j++) {
            u64 m = ((u64)1 << j) - 1;          /* prefix_j == suffix_j ? */
            if ((c & m) == (((u64)c >> (K - j)) & m)) {
                A += ldexp(1.0, j);
                if (j < K) novl++;
            }
        }
        double R = ((double)s[c] + (K - 1)) / A;
        int pc = __builtin_popcountll(c);
        pc_sum[pc] += R; pc_sq[pc] += R * R; pc_cnt[pc]++;
        ov_sum[novl] += R; ov_cnt[novl]++;
        tot += R; totsq += R * R; totn++;
        if (R > rmax) { rmax = R; argmax = c; }
        if (R < rmin) { rmin = R; argmin = c; }
        if (s[c] > smax) { smax = s[c]; argsmax = c; }
    }

    double mean = tot / totn;
    double var = totsq / totn - mean * mean;
    printf("# %s  k=%d  patterns=%zu  missing=%" PRIu64 "\n", label, K, N, missing);
    printf("# R = (first-occurrence start + k-1) / Conway A(w);  model E[R]=1\n");
    printf("stat,label,k,value\n");
    printf("mean_R,%s,%d,%.6f\n", label, K, mean);
    printf("sd_R,%s,%d,%.6f\n", label, K, sqrt(var));
    printf("naive_se_R,%s,%d,%.6f\n", label, K, sqrt(var / (double)totn));
    printf("max_R,%s,%d,%.6f\n", label, K, rmax);
    printf("argmax_R_code,%s,%d,%" PRIu64 "\n", label, K, argmax);
    printf("min_R,%s,%d,%.8f\n", label, K, rmin);
    printf("argmin_R_code,%s,%d,%" PRIu64 "\n", label, K, argmin);
    printf("N_k,%s,%d,%" PRIu64 "\n", label, K, smax);
    printf("N_k_code,%s,%d,%" PRIu64 "\n", label, K, argsmax);

    printf("\npopcount,count,mean_R,sd_R\n");
    for (int p = 0; p <= K; p++)
        if (pc_cnt[p]) {
            double m = pc_sum[p] / pc_cnt[p];
            double v = pc_sq[p] / pc_cnt[p] - m * m;
            printf("%d,%" PRIu64 ",%.6f,%.6f\n", p, pc_cnt[p], m, sqrt(v > 0 ? v : 0));
        }

    printf("\nnontrivial_overlaps,count,mean_R\n");
    for (int o = 0; o <= K; o++)
        if (ov_cnt[o])
            printf("%d,%" PRIu64 ",%.6f\n", o, ov_cnt[o], ov_sum[o] / ov_cnt[o]);
    return 0;
}
