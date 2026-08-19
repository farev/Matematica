/* witness_hunt.c — randomized search for a dissociated set of target size
 * in Z_a x Z_b. One-sided tool: a found witness (verified independently by
 * verify_witness.py) proves maxdiss >= L, which together with the proved
 * cap maxdiss <= floor(log2 |G|) can DECIDE D± for cap-gap groups too large
 * for exhaustive search. A failed hunt proves nothing and is never cited as
 * evidence of absence.
 *
 * Greedy randomized restarts; deterministic given --seed. Exact integer
 * arithmetic (the LCG is arithmetic on uint64, not randomness-critical).
 *
 * Usage: ./witness_hunt a b L [--seed S] [--restarts R]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int A, B, N, W;
static uint64_t *T;
static int *neg;

static inline int getbit(const uint64_t *t, int i) { return (int)((t[i>>6]>>(i&63))&1ULL); }
static inline void setbit(uint64_t *t, int i) { t[i>>6] |= 1ULL<<(i&63); }

static uint64_t rng;
static inline uint64_t nextr(void) {
    rng = rng * 6364136223846793005ULL + 1442695040888963407ULL;
    return rng >> 11;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: witness_hunt a b L [--seed S] [--restarts R]\n"); return 1; }
    A = atoi(argv[1]); B = atoi(argv[2]);
    int L = atoi(argv[3]);
    long long restarts = 100000000LL;
    rng = 88172645463325252ULL;
    for (int i = 4; i < argc; i++) {
        if (!strcmp(argv[i], "--seed")) rng = strtoull(argv[++i], 0, 10);
        else if (!strcmp(argv[i], "--restarts")) restarts = atoll(argv[++i]);
    }
    N = A * B; W = (N + 63) / 64;
    T = malloc(sizeof(uint64_t) * (size_t)W * (L + 2));
    neg = malloc(sizeof(int) * N);
    for (int g = 0; g < N; g++) {
        int x = g / B, y = g % B;
        neg[g] = ((A - x) % A) * B + (B - y) % B;
    }
    int *seq = malloc(sizeof(int) * (L + 2));
    for (long long r = 0; r < restarts; r++) {
        uint64_t *t0 = T;
        memset(t0, 0, sizeof(uint64_t) * (size_t)W);
        int depth = 0;
        while (depth < L) {
            /* pick a random legal element (rejection; fallback scan) */
            int g = -1;
            for (int tries = 0; tries < 64; tries++) {
                int cand = (int)(nextr() % (N - 1)) + 1;
                if (!getbit(t0, cand)) { g = cand; break; }
            }
            if (g < 0) {
                for (int cand = 1; cand < N; cand++)
                    if (!getbit(t0, cand)) { g = cand; break; }
                if (g < 0) break;
            }
            /* T' = T ∪ T+g ∪ T-g ∪ {g,-g} */
            uint64_t *t1 = t0 + W;
            memcpy(t1, t0, sizeof(uint64_t) * (size_t)W);
            setbit(t1, g); setbit(t1, neg[g]);
            for (int w = 0; w < W; w++) {
                uint64_t v = t0[w];
                while (v) {
                    int i = (w << 6) + __builtin_ctzll(v);
                    v &= v - 1;
                    /* i + g and i - g via coordinates (no big addtab at this N) */
                    int ix = i / B, iy = i % B;
                    int gx = g / B, gy = g % B;
                    setbit(t1, ((ix + gx) % A) * B + (iy + gy) % B);
                    int nx = (ix + A - gx) % A, ny = (iy + B - gy) % B;
                    setbit(t1, nx * B + ny);
                }
            }
            if (t1[0] & 1ULL) break;  /* safety: 0 appeared (cannot if legal) */
            seq[depth++] = g;
            t0 = t1;
        }
        if (depth >= L) {
            printf("FOUND %d %d L=%d after %lld restarts:", A, B, L, r);
            for (int i = 0; i < L; i++)
                printf(" (%d,%d)", seq[i] / B, seq[i] % B);
            printf("\n");
            return 0;
        }
        if ((r & 0xFFFFF) == 0xFFFFF)
            fprintf(stderr, "restart %lld...\n", r + 1);
    }
    printf("NOT-FOUND %d %d L=%d after %lld restarts (proves nothing)\n", A, B, L, restarts);
    return 3;
}
