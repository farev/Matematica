/* sweep.c — certified verifier for Erdős Problem 699 (Erdős–Szekeres,
 * common prime factors of binomial coefficients).
 *
 * Statement (google-deepmind/formal-conjectures ErdosProblems/699.lean,
 * fetched 2026-08-11):
 *   WEAK  (#699):  for all 1 <= i < j <= n/2 there is a prime p >= i
 *                  with p | gcd(C(n,i), C(n,j)).
 *   STRONG (ErSz strengthening): same with p > i, conjecturally with only
 *                  finitely many exceptional triples (n,i,j).
 *
 * Exact integer arithmetic only.  Divisibility p | C(n,k) is decided by the
 * Kummer carry criterion:  p | C(n,k)  <=>  exists t>=1: k mod p^t > n mod p^t.
 *
 * Reduction implemented (proofs in NOTE.md; elementary):
 *   Lemma A: n prime  => p = n divides every C(n,k), 1<=k<=n-1, and n > j,
 *            so every pair (i,j) is satisfied, both versions.  Skip n.
 *   Lemma B: n composite, q = largest prime < n (q > n/2 by Bertrand).
 *            For prime p in (n/2, n]: p | C(n,k) <=> k > n-p  (0<=k<=n/2).
 *            So p = q witnesses every pair with i > g := n - q (q > j > i).
 *            Only rows 2 <= i <= g need checking.
 *   Lemma C: i = 1: n/gcd(n,j) > 1 divides C(n,j) (classical: n | j*C(n,j)),
 *            so some prime divides gcd(C(n,1), C(n,j)) and exceeds i = 1.
 *   Fact D:  in a hard row (i <= g), the primes p > i with p | C(n,i) are
 *            exactly the primes p > i dividing n(n-1)...(n-i+1); all are
 *            <= n/2 (every n-r, r < g, is composite).
 *
 * Per hard row: candidates (Fact D) from SPF factorizations, sorted
 * descending; their patterns S_p = { j : p | C(n,j) } are subtracted from
 * the uncovered set (i, n/2].  Uncovered j = STRONG-exception candidate;
 * then p = i is tested (i prime, i | C(n,i) <=> n mod i^2 < i, carry test
 * for C(n,j)).  If p = i also fails: WEAK counterexample (falsifies #699).
 *
 * Tripwire: Sylvester–Schur guarantees a nonempty candidate list for every
 * hard row; an empty list is reported as SSVIOL (= implementation bug).
 *
 * Engines (cross-checkable):
 *   --engine=bitset    word-parallel bitset over j (simple; default)
 *   --engine=interval  interval-list subtraction (fast at large n;
 *                      falls back to bitset on pathological rows)
 *   --engine=both      run both on every row, report ENGDIFF on mismatch
 *
 * Output:
 *   EXC n i j          strong exception, weak holds via p = i
 *   WEAKFAIL n i j     weak counterexample candidate (re-verify externally!)
 *   SSVIOL n i         Sylvester–Schur assert fired (bug tripwire)
 *   ENGDIFF n i        engine disagreement (bug tripwire)
 *   SUMMARY lo hi composites hard_rows exc_cand exc weakfail maxg secs
 *
 * Usage: sweep LO HI [--engine=bitset|interval|both]
 * Build: gcc -O2 -march=native -o sweep sweep.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
typedef uint32_t u32;
typedef int64_t  i64;

/* ---------------- smallest-prime-factor sieve ---------------- */
static u32 *spf;                 /* spf[m] = smallest prime factor of m */
static void build_spf(u64 N) {
    spf = calloc((size_t)N + 1, sizeof(u32));
    if (!spf) { fprintf(stderr, "spf alloc failed\n"); exit(1); }
    for (u64 i = 2; i <= N; i++) {
        if (!spf[i]) {
            for (u64 j = i; j <= N; j += i)
                if (!spf[j]) spf[j] = (u32)i;
        }
    }
}
static inline int is_prime(u64 m) { return m >= 2 && spf[m] == (u32)m; }

/* ---------------- carry criterion ---------------- */
/* p | C(n,k)  <=>  exists t: k mod p^t > n mod p^t   (0 <= k <= n) */
static inline int carry_div(u64 p, u64 n, u64 k) {
    for (u64 pt = p; pt <= n; ) {
        if (k % pt > n % pt) return 1;
        if (pt > n / p) break;
        pt *= p;
    }
    return 0;
}

/* ---------------- bitset engine ---------------- */
static inline void bs_clear_range(u64 *B, i64 lo, i64 hi) {
    if (lo > hi) return;
    i64 wl = lo >> 6, wh = hi >> 6;
    u64 ml = ~0ULL << (lo & 63);
    u64 mh = ((hi & 63) == 63) ? ~0ULL : ((1ULL << ((hi & 63) + 1)) - 1);
    if (wl == wh) { B[wl] &= ~(ml & mh); return; }
    B[wl] &= ~ml;
    for (i64 w = wl + 1; w < wh; w++) B[w] = 0;
    B[wh] &= ~mh;
}
static inline void bs_set_range(u64 *B, i64 lo, i64 hi) {
    if (lo > hi) return;
    i64 wl = lo >> 6, wh = hi >> 6;
    u64 ml = ~0ULL << (lo & 63);
    u64 mh = ((hi & 63) == 63) ? ~0ULL : ((1ULL << ((hi & 63) + 1)) - 1);
    if (wl == wh) { B[wl] |= (ml & mh); return; }
    B[wl] |= ml;
    for (i64 w = wl + 1; w < wh; w++) B[w] = ~0ULL;
    B[wh] |= mh;
}
/* clear from M every j with p | C(n,j) */
static void bs_subtract_Sp(u64 *M, u64 p, u64 n, i64 half) {
    for (u64 pt = p; pt <= n; ) {
        i64 r = (i64)(n % pt);
        if (r < (i64)pt - 1) {
            for (i64 base = 0; base <= half; base += (i64)pt) {
                i64 lo = base + r + 1, hi = base + (i64)pt - 1;
                if (lo > half) break;
                if (hi > half) hi = half;
                bs_clear_range(M, lo, hi);
            }
        }
        if (pt > n / p) break;
        pt *= p;
    }
}

static int row_bitset(u64 n, u64 i, i64 half, int nc, const u64 *C,
                      u64 *M, i64 *excj, int excap) {
    i64 words = (half >> 6) + 1;
    memset(M, 0, (size_t)words * 8);
    bs_set_range(M, (i64)i + 1, half);
    i64 firstw = ((i64)i + 1) >> 6;
    for (int s = 0; s < nc; s++) {
        bs_subtract_Sp(M, C[s], n, half);
        while (firstw < words && M[firstw] == 0) firstw++;
        if (firstw == words) return 0;
    }
    int ne = 0;
    for (i64 w = firstw; w < words; w++) {
        u64 x = M[w];
        while (x) {
            i64 j = (w << 6) + __builtin_ctzll(x);
            x &= x - 1;
            if (ne < excap) excj[ne] = j;
            ne++;
        }
    }
    return ne;
}

/* ---------------- interval engine ---------------- */
typedef struct { i64 a, b; } iv;
#define IVCAP 8192
static iv rowlist[IVCAP], sc1[IVCAP], sc2[IVCAP];

/* keep positions with residue mod q <= r; result into O; -1 on overflow */
static int iv_subtract_layer(const iv *L, int m, i64 q, i64 r, iv *O) {
    int om = 0;
    for (int s = 0; s < m; s++) {
        i64 a = L[s].a, b = L[s].b;
        for (i64 base = (a / q) * q; base <= b; base += q) {
            i64 lo = base, hi = base + r;
            if (lo < a) lo = a;
            if (hi > b) hi = b;
            if (lo <= hi) {
                if (om >= IVCAP) return -1;
                O[om].a = lo; O[om].b = hi; om++;
            }
        }
    }
    return om;
}

/* L := L \ S_p.  Returns new length, or -1 on overflow with L UNTOUCHED. */
static int iv_subtract_Sp(u64 p, u64 n, iv *L, int m) {
    if (m == 0) return 0;
    memcpy(sc1, L, (size_t)m * sizeof(iv));
    iv *cur = sc1, *nxt = sc2;
    for (u64 pt = p; pt <= n && m > 0; ) {
        i64 r = (i64)(n % pt);
        if (r < (i64)pt - 1) {
            int nm = iv_subtract_layer(cur, m, (i64)pt, r, nxt);
            if (nm < 0) return -1;
            iv *t = cur; cur = nxt; nxt = t;
            m = nm;
        }
        if (pt > n / p) break;
        pt *= p;
    }
    memcpy(L, cur, (size_t)m * sizeof(iv));
    return m;
}

#define MAXC 4096
/* returns exception-candidate count; may fall back to bitset engine */
static int row_interval(u64 n, u64 i, i64 half, int nc, const u64 *C,
                        u64 *M, i64 *excj, int excap) {
    rowlist[0].a = (i64)i + 1; rowlist[0].b = half;
    int m = 1, nd = 0;
    u64 defer[MAXC];
    for (int s = 0; s < nc && m > 0; s++) {
        u64 p = C[s];
        i64 est = 2 * m;
        for (int t = 0; t < m; t++)
            est += (rowlist[t].b - rowlist[t].a + 1) / (i64)p;
        if (est > IVCAP - 8) { defer[nd++] = p; continue; }
        int nm = iv_subtract_Sp(p, n, rowlist, m);
        if (nm < 0) { defer[nd++] = p; continue; }
        m = nm;
    }
    if (m == 0) return 0;
    i64 total = 0;
    for (int t = 0; t < m; t++) total += rowlist[t].b - rowlist[t].a + 1;
    if (total > 200000)                    /* pathological: exact fallback */
        return row_bitset(n, i, half, nc, C, M, excj, excap);
    int ne = 0;
    for (int t = 0; t < m; t++)
        for (i64 j = rowlist[t].a; j <= rowlist[t].b; j++) {
            int covered = 0;
            for (int s = 0; s < nd; s++)
                if (carry_div(defer[s], n, (u64)j)) { covered = 1; break; }
            if (!covered) { if (ne < excap) excj[ne] = j; ne++; }
        }
    return ne;
}

/* ---------------- candidate collection ---------------- */
static u64 cand[MAXC];
static int cmp_desc(const void *x, const void *y) {
    u64 a = *(const u64 *)x, b = *(const u64 *)y;
    return (a < b) - (a > b);
}
/* distinct primes p > i dividing any of n, n-1, ..., n-i+1 */
static int collect_candidates(u64 n, u64 i, u64 *out) {
    int c = 0;
    for (u64 r = 0; r < i; r++) {
        u64 m = n - r;
        while (m > 1) {
            u64 p = spf[m];
            if (p > i) {
                int seen = 0;
                for (int s = 0; s < c; s++) if (out[s] == p) { seen = 1; break; }
                if (!seen) {
                    if (c >= MAXC) { fprintf(stderr, "cand overflow\n"); exit(1); }
                    out[c++] = p;
                }
            }
            while (m % p == 0) m /= p;
        }
    }
    qsort(out, (size_t)c, sizeof(u64), cmp_desc);
    return c;
}

/* ---------------- main sweep ---------------- */
int main(int argc, char **argv) {
    u64 nums[2]; int nn = 0;
    int eng = 0; /* 0 bitset, 1 interval, 2 both */
    for (int a = 1; a < argc; a++) {
        if (!strncmp(argv[a], "--engine=", 9)) {
            if (!strcmp(argv[a] + 9, "interval")) eng = 1;
            else if (!strcmp(argv[a] + 9, "both")) eng = 2;
            else eng = 0;
        } else if (nn < 2) nums[nn++] = strtoull(argv[a], 0, 10);
    }
    if (nn == 0) { fprintf(stderr, "usage: sweep [LO] HI [--engine=...]\n"); return 1; }
    u64 lo = (nn == 2) ? nums[0] : 4, hi = (nn == 2) ? nums[1] : nums[0];
    if (lo < 4) lo = 4;

    clock_t t0 = clock();
    build_spf(hi);

    i64 maxhalf = (i64)(hi / 2);
    u64 *M = malloc((size_t)((maxhalf >> 6) + 2) * 8);
    if (!M) { fprintf(stderr, "bitset alloc failed\n"); return 1; }

    u64 lastp = 0;
    for (u64 m = lo - 1; m >= 2; m--) if (is_prime(m)) { lastp = m; break; }

    u64 composites = 0, hardrows = 0, excand = 0, excn = 0, weakn = 0, maxg = 0;
    static i64 excj1[IVCAP], excj2[IVCAP];

    for (u64 n = lo; n <= hi; n++) {
        if (is_prime(n)) { lastp = n; continue; }          /* Lemma A */
        composites++;
        u64 g = n - lastp;
        if (g > maxg) maxg = g;
        i64 half = (i64)(n / 2);
        u64 imax = g;
        if ((i64)imax > half - 1) imax = (u64)(half - 1);
        for (u64 i = 2; i <= imax; i++) {                  /* Lemmas B, C */
            hardrows++;
            int nc = collect_candidates(n, i, cand);
            if (nc == 0) {
                printf("SSVIOL %llu %llu\n",
                       (unsigned long long)n, (unsigned long long)i);
                fflush(stdout);
                continue;
            }
            int ne;
            if (eng == 0)
                ne = row_bitset(n, i, half, nc, cand, M, excj1, IVCAP);
            else if (eng == 1)
                ne = row_interval(n, i, half, nc, cand, M, excj1, IVCAP);
            else {
                ne = row_bitset(n, i, half, nc, cand, M, excj1, IVCAP);
                int ne2 = row_interval(n, i, half, nc, cand, M, excj2, IVCAP);
                int bad = (ne != ne2);
                if (!bad)
                    for (int s = 0; s < ne && s < IVCAP; s++)
                        if (excj1[s] != excj2[s]) { bad = 1; break; }
                if (bad) {
                    printf("ENGDIFF %llu %llu\n",
                           (unsigned long long)n, (unsigned long long)i);
                    fflush(stdout);
                }
            }
            for (int s = 0; s < ne && s < IVCAP; s++) {
                i64 j = excj1[s];
                excand++;
                int weak_ok = is_prime(i) && (n % (i * i)) < i
                              && carry_div(i, n, (u64)j);
                if (weak_ok) {
                    printf("EXC %llu %llu %lld\n", (unsigned long long)n,
                           (unsigned long long)i, (long long)j);
                    excn++;
                } else {
                    printf("WEAKFAIL %llu %llu %lld\n", (unsigned long long)n,
                           (unsigned long long)i, (long long)j);
                    weakn++;
                }
                fflush(stdout);
            }
        }
    }
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("SUMMARY %llu %llu %llu %llu %llu %llu %llu %llu %.2f\n",
           (unsigned long long)lo, (unsigned long long)hi,
           (unsigned long long)composites, (unsigned long long)hardrows,
           (unsigned long long)excand, (unsigned long long)excn,
           (unsigned long long)weakn, (unsigned long long)maxg, secs);
    free(M); free(spf);
    return 0;
}
