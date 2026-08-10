/* scan699.c (v2) — fast certified sweep for Erdos #699 (Erdos–Szekeres).
 *
 * Question (erdosproblems.com/699; Lean statement in
 * google-deepmind/formal-conjectures): for every 1 <= i < j <= n/2 is there a
 * prime p >= i with p | gcd(C(n,i), C(n,j))?  Strengthening (ErSz 1978):
 * p > i outside a finite exceptional set of triples.
 *
 * Finds, for n in [A,B), ALL triples (n,i,j) with no witness p > i
 * ("strict failures"), each classified:
 *   EXC — saved by p = i (i prime, i | C(n,i), i | C(n,j)): exception to the
 *         strengthening;
 *   CEX — no witness p >= i at all: counterexample to #699.
 *
 * Reductions (proofs in NOTE.md):
 *  R1 (Kummer/Lucas). p | C(n,k) iff some base-p digit of k exceeds n's.
 *  R2. For p > i: p | C(n,i) iff n mod p < i.  So the level-i witness set is
 *      T_i = {p prime > i : n mod p < i} (+ p = i checked separately), and
 *      every p in T_i divides exactly one of n, n-1, ..., n-i+1.
 *  R3. If i > g(n) := n - prevprime(n), the pair has witness prevprime(n).
 *      So only levels 2 <= i <= g(n) matter; n prime => nothing to check.
 *  R4 (level 1 never fails). If p^e || n then base-p domination of j by n
 *      forces p^e | j; over all p | n that forces n | j — impossible for
 *      0 < j <= n/2.  So some prime of n divides C(n,j): skip level 1.
 *  R5. If p^e || n-r (r < i <= g < p), a strict failure at level i forces
 *      j ≡ b (mod p^e) with 0 <= b <= r.  For the two largest prime powers
 *      M1 = p1^e1, M2 = p2^e2 in T_i's window this leaves
 *      (r1+1)(r2+1) <= i^2 CRT classes mod M1*M2 to walk.
 *
 * Fast filter per n: the level-2 window (odd prime powers of n(n-1),
 * residues 0/1, <= 4 CRT classes).  Any survivor or degeneracy escalates to
 * the exact per-level slow path.  All arithmetic exact (u64/u128); no
 * floating point; no randomness.
 *
 * Usage: ./scan699 A B out.csv    (4 <= A < B <= 4e9)
 * out.csv: kind,n,i,j,witness  (witness = i for EXC, 0 for CEX)
 * stderr: stats + any HARD-ERROR (incomplete coverage aborts the run).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>

typedef uint64_t u64;
typedef unsigned __int128 u128;

#define WINDOW 620            /* > max prime gap below 4e9 (336), margin */
#define SEG    (1u<<20)
#define MAXF   12             /* max distinct prime factors below 4e9 is 9 */

static u64 A, B;
static uint32_t *sp; static int nsp;

static void small_sieve(u64 lim) {
    uint32_t L = (uint32_t)lim;
    char *c = calloc(L + 1, 1);
    sp = malloc(sizeof(uint32_t) * (L / 8 + 64)); nsp = 0;
    for (uint32_t p = 2; p <= L; p++) if (!c[p]) {
        if (nsp >= (int)(L / 8 + 64)) { fprintf(stderr, "sieve cap\n"); exit(9); }
        sp[nsp++] = p;
        for (u64 q = (u64)p * p; q <= L; q += p) c[q] = 1;
    }
    free(c);
}

static uint32_t (*fp)[MAXF];   /* distinct primes  */
static uint32_t (*fpe)[MAXF];  /* full powers p^e || m */
static uint8_t *fcnt, *ispr;
static u64 seg_lo;

static void factor_segment(u64 lo, u64 len) {
    seg_lo = lo;
    static u64 *rem = NULL; static u64 cap = 0;
    if (len > cap) {
        free(rem); rem = malloc(len * 8);
        free(fp);  fp  = malloc(len * sizeof(*fp));
        free(fpe); fpe = malloc(len * sizeof(*fpe));
        free(fcnt); fcnt = malloc(len); free(ispr); ispr = malloc(len);
        if (!rem || !fp || !fpe || !fcnt || !ispr) { fprintf(stderr, "oom\n"); exit(9); }
        cap = len;
    }
    for (u64 t = 0; t < len; t++) { rem[t] = lo + t; fcnt[t] = 0; }
    for (int s = 0; s < nsp; s++) {
        u64 p = sp[s];
        if (p * p > lo + len - 1) break;
        u64 start = (lo + p - 1) / p * p;
        for (u64 m = start; m < lo + len; m += p) {
            u64 t = m - lo;
            if (rem[t] % p == 0) {
                if (fcnt[t] >= MAXF) { fprintf(stderr, "MAXF %" PRIu64 "\n", m); exit(9); }
                u64 pe = 1;
                do { rem[t] /= p; pe *= p; } while (rem[t] % p == 0);
                fp[t][fcnt[t]] = (uint32_t)p;
                if (pe >> 32) { fprintf(stderr, "pe ovf\n"); exit(9); }
                fpe[t][fcnt[t]++] = (uint32_t)pe;
            }
        }
    }
    for (u64 t = 0; t < len; t++) {
        if (rem[t] > 1) {
            if (rem[t] >> 32) { fprintf(stderr, "fac ovf\n"); exit(9); }
            if (fcnt[t] >= MAXF) { fprintf(stderr, "MAXF2\n"); exit(9); }
            fp[t][fcnt[t]] = (uint32_t)rem[t];
            fpe[t][fcnt[t]++] = (uint32_t)rem[t];
        }
        /* m prime <=> exactly one prime factor p with p^1 = m (covers both
           the small-prime case, where m was divided down to 1 by itself,
           and the big-cofactor case). */
        ispr[t] = (fcnt[t] == 1 && fpe[t][0] == lo + t && fp[t][0] == fpe[t][0]
                   && lo + t > 1);
    }
}
static inline int getf(u64 m, const uint32_t **p, const uint32_t **pe) {
    u64 t = m - seg_lo; *p = fp[t]; *pe = fpe[t]; return fcnt[t];
}
static inline int isprime(u64 m) { return ispr[m - seg_lo]; }

static inline int div_binom(u64 p, u64 n, u64 k) {   /* p | C(n,k)? */
    while (k) { if (k % p > n % p) return 1; k /= p; n /= p; }
    return 0;
}
static inline int dominated(u64 p, u64 n, u64 j) { return !div_binom(p, n, j); }

static u64 inv_mod(u64 a, u64 m) {
    long long g = (long long)m, x = 0, x1 = 1, aa = (long long)(a % m), t, q;
    while (aa) { q = g / aa; t = g - q * aa; g = aa; aa = t;
                 t = x - q * x1; x = x1; x1 = t; }
    return (u64)((x % (long long)m + (long long)m) % (long long)m);
}

static FILE *out;
static u64 n_strict, n_cex, n_flag, n_walkcand, n_slowdirect;

static void record(u64 n, u64 i, u64 j) {
    int saved = 0;
    if (i >= 2) {
        int ip = 1; for (u64 d = 2; d * d <= i; d++) if (i % d == 0) { ip = 0; break; }
        if (ip && div_binom(i, n, i) && div_binom(i, n, j)) saved = 1;
    }
    n_strict++;
    if (saved) fprintf(out, "EXC,%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 "\n", n, i, j, i);
    else { n_cex++;
        fprintf(out, "CEX,%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",0\n", n, i, j);
        fprintf(stderr, "*** COUNTEREXAMPLE (%" PRIu64 ",%" PRIu64 ",%" PRIu64 ")\n", n, i, j);
    }
    fflush(out);
}

/* exact level-i analysis. T/PE/R: witness primes > i with full powers and
   residues r = n mod p < i.  Finds every j in (i, n/2] dominated for all. */
static void slow_level(u64 n, u64 i, const u64 *T, const u64 *PE, const u64 *R, int nt) {
    u64 half = n / 2;
    if (nt == 0) {
        if (half > 2000000) { fprintf(stderr, "HARD-ERROR empty-T n=%" PRIu64 " i=%" PRIu64 "\n", n, i); exit(8); }
        for (u64 j = i + 1; j <= half; j++) record(n, i, j);   /* tiny n only */
        return;
    }
    int a1 = 0; for (int t = 1; t < nt; t++) if (PE[t] > PE[a1]) a1 = t;
    if (nt == 1) {
        /* single witness prime p: j ≡ b (mod p^e), b <= r, upper digits of j
           dominated by digits of n above e.  Enumerate by digit odometer. */
        u64 p = T[0], pe = PE[0], r = R[0];
        u64 digs[64]; int nd = 0;
        for (u64 nn = n / pe; nn; nn /= p) digs[nd++] = nn % p;
        u128 cnt = r + 1; for (int d = 0; d < nd; d++) { cnt *= digs[d] + 1; if (cnt > 4000000) break; }
        if (cnt > 4000000) {
            if (half <= 4000000) { n_slowdirect++;   /* direct scan fallback */
                for (u64 j = i + 1; j <= half; j++) if (dominated(p, n, j)) record(n, i, j);
                return;
            }
            fprintf(stderr, "HARD-ERROR 1-prime n=%" PRIu64 " i=%" PRIu64 "\n", n, i); exit(8);
        }
        u64 idx[64]; memset(idx, 0, sizeof idx);
        for (;;) {
            u64 up = 0, pw = pe;
            for (int d = 0; d < nd; d++) { up += idx[d] * pw; pw *= p; }
            for (u64 b = 0; b <= r; b++) {
                u64 j = up + b;
                if (j > i && j <= half) record(n, i, j);
            }
            int d = 0;
            while (d < nd && idx[d] == digs[d]) idx[d++] = 0;
            if (d == nd) break;
            idx[d]++;
        }
        return;
    }
    int a2 = -1; for (int t = 0; t < nt; t++) if (t != a1 && (a2 < 0 || PE[t] > PE[a2])) a2 = t;
    int a3 = -1; for (int t = 0; t < nt; t++) if (t != a1 && t != a2 && (a3 < 0 || PE[t] > PE[a3])) a3 = t;
    u64 M1 = PE[a1], r1 = R[a1], M2 = PE[a2], r2 = R[a2];
    u64 P3 = a3 >= 0 ? T[a3] : 0;
    u64 inv = inv_mod(M1 % M2, M2);
    u128 M = (u128)M1 * M2;
    u64 per = (M > half) ? 1 : (u64)(half / M) + 1;
    if ((u128)(r1 + 1) * (r2 + 1) * per > 5000000) {
        if (half <= 4000000) { n_slowdirect++;
            u64 p1 = T[a1], p2 = T[a2];
            for (u64 j = i + 1; j <= half; j++) {
                if (!dominated(p1, n, j) || !dominated(p2, n, j)) continue;
                int all = 1;
                for (int t = 0; t < nt; t++) if (!dominated(T[t], n, j)) { all = 0; break; }
                if (all) record(n, i, j);
            }
            return;
        }
        fprintf(stderr, "HARD-ERROR combos n=%" PRIu64 " i=%" PRIu64 "\n", n, i); exit(8);
    }
    for (u64 b1 = 0; b1 <= r1; b1++) for (u64 b2 = 0; b2 <= r2; b2++) {
        u64 d = (b2 + M2 - b1 % M2) % M2;
        u64 j0 = b1 + M1 * ((u64)(((u128)d * inv) % M2));
        for (u128 j = j0; j <= half; j += M) {
            u64 jj = (u64)j;
            if (jj <= i) continue;
            n_walkcand++;
            if (P3 && !dominated(P3, n, jj)) continue;
            int all = 1;
            for (int t = 0; t < nt; t++) if (!dominated(T[t], n, jj)) { all = 0; break; }
            if (all) record(n, i, jj);
        }
    }
}

static void slow_n(u64 n, u64 g) {
    u64 half = n / 2;
    u64 T[WINDOW * MAXF], PE[WINDOW * MAXF], R[WINDOW * MAXF];
    for (u64 i = 2; i <= g && i + 1 <= half; i++) {
        int nt = 0;
        for (u64 r = 0; r < i; r++) {
            const uint32_t *p, *pe; int c = getf(n - r, &p, &pe);
            for (int t = 0; t < c; t++) if (p[t] > i) { T[nt] = p[t]; PE[nt] = pe[t]; R[nt] = r; nt++; }
        }
        slow_level(n, i, T, PE, R, nt);
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s A B out.csv\n", argv[0]); return 1; }
    A = strtoull(argv[1], 0, 10); B = strtoull(argv[2], 0, 10);
    if (B > 4000000000ULL) { fprintf(stderr, "B too large for u32 prime powers\n"); return 1; }
    out = fopen(argv[3], "w");
    if (!out) { perror("out"); return 1; }
    fprintf(out, "kind,n,i,j,witness\n");
    u64 rt = 2; while (rt * rt < B) rt++;
    small_sieve(rt + 2);
    u64 lo = A >= WINDOW + 4 ? A - WINDOW : 4;
    u64 last_prime = 0;
    for (u64 base = lo < A ? A : lo, first = 1; base < B; first = 0) {
        u64 blk_lo = first ? lo : base;
        u64 len = SEG; if (base + len > B) len = B - base;
        u64 flo = blk_lo > lo ? blk_lo - WINDOW : lo;
        factor_segment(flo, base + len - flo);
        if (first) for (u64 m = flo; m < base && m < B; m++) if (isprime(m) && m <= base) last_prime = m;
        for (u64 n = base; n < base + len; n++) {
            if (isprime(n)) { last_prime = n; continue; }
            if (n < A || n < 8) continue;
            if (last_prime < 2) continue;                    /* n in {4,6} handled below anyway */
            u64 g = n - last_prime;
            if (g >= WINDOW) { fprintf(stderr, "gap>%d at %" PRIu64 "\n", WINDOW, n); return 9; }
            if (g < 2) continue;                             /* R3: only i>=2 matter, i<=g */
            u64 half = n / 2;
            if (half < 3) continue;
            /* ---- fast filter over primes > g of n(n-1): these lie in T_i
               for EVERY level 2 <= i <= g, so "no j dominated by all of
               them" clears every level at once.  Primes <= g must NOT be
               used here (they are absent from T_i for i >= p). ---- */
            const uint32_t *p0, *pe0, *p1, *pe1;
            int c0 = getf(n, &p0, &pe0), c1 = getf(n - 1, &p1, &pe1);
            u64 T2[2 * MAXF], PE2[2 * MAXF], R2[2 * MAXF]; int nt = 0;
            for (int t = 0; t < c0; t++) if (p0[t] > g) { T2[nt] = p0[t]; PE2[nt] = pe0[t]; R2[nt] = 0; nt++; }
            for (int t = 0; t < c1; t++) if (p1[t] > g) { T2[nt] = p1[t]; PE2[nt] = pe1[t]; R2[nt] = 1; nt++; }
            int deep = 0;
            if (nt < 2) deep = 1;
            else {
                int a1 = 0; for (int t = 1; t < nt; t++) if (PE2[t] > PE2[a1]) a1 = t;
                int a2 = -1; for (int t = 0; t < nt; t++) if (t != a1 && (a2 < 0 || PE2[t] > PE2[a2])) a2 = t;
                u64 M1 = PE2[a1], M2 = PE2[a2];
                if ((u128)M1 * M2 <= half) deep = 1;
                else {
                    u64 r1 = R2[a1], r2 = R2[a2];
                    u64 inv = inv_mod(M1 % M2, M2);
                    u128 M = (u128)M1 * M2;
                    for (u64 b1 = 0; b1 <= r1 && !deep; b1++)
                    for (u64 b2 = 0; b2 <= r2 && !deep; b2++) {
                        u64 d = (b2 + M2 - b1 % M2) % M2;
                        u64 j0 = b1 + M1 * ((u64)(((u128)d * inv) % M2));
                        for (u128 j = j0; j <= half; j += M) {
                            u64 jj = (u64)j; if (jj < 3) continue;
                            int all = 1;
                            for (int t = 0; t < nt; t++) if (!dominated(T2[t], n, jj)) { all = 0; break; }
                            if (all) { deep = 1; break; }
                        }
                    }
                }
            }
            if (deep) { n_flag++; slow_n(n, g); }
        }
        base += len;
    }
    fprintf(stderr, "range [%" PRIu64 ",%" PRIu64 "): strict=%" PRIu64 " cex=%" PRIu64 " flagged=%" PRIu64 " walkcand=%" PRIu64 " slowdirect=%" PRIu64 "\n",
            A, B, n_strict, n_cex, n_flag, n_walkcand, n_slowdirect);
    fclose(out);
    return n_cex ? 2 : 0;
}
