/* sweep699.c (v2) — fast exact sweep for Erdos problem #699 (Erdos–Szekeres 1978).
 *
 * Conjecture: for all 1 <= i < j <= floor(n/2) there is a prime p >= i with
 * p | C(n,i) and p | C(n,j).  Strengthening: outside a finite set of
 * (n,i,j) one can take p > i.
 *
 * Facts used (proved in NOTE.md; elementary):
 *  L1. For prime p > i:  p | C(n,i)  <=>  n mod p < i
 *      (C(n,i) = n(n-1)...(n-i+1)/i! and p does not divide i!).
 *      Hence {p > i : p | C(n,i)} = {p > i : p | (n-t) for some 0 <= t < i}.
 *  L2. If some prime lies in (n-i, n], every pair (i,j) is satisfied at it,
 *      with p > i.  Hence any tight/counterexample triple needs
 *      i <= g(n) = n - prevprime(n).
 *  L3. Kummer/Lucas: p | C(n,k) iff some base-p digit of k exceeds that of n.
 *      In particular (k mod p) > (n mod p) is sufficient for p | C(n,k).
 *  L4. p = i prime: i | C(n,i) iff n mod i^2 < i.
 *
 * Algorithm: segmented full factorization; per n, per level i in [1, g(n)]:
 * incremental admissible list A = {(p,t): t<i, p|n-t, p>i at insert time;
 * entries with p <= current i are stale and skipped lazily}; the two
 * strongest congruence filters (min (t+1)/p, tracked incrementally) generate
 * CRT candidates; candidates get exact Kummer tests against all live
 * entries, then the p = i test; survivors are recorded as EXC (tight,
 * conjecture holds only via p = i) or CEX (counterexample).
 * i = 1 doubles as a control: Erdos–Szekeres proved gcd(C(n,1),C(n,j)) > 1,
 * so any i=1 record is an engine bug.
 *
 * Exact integer arithmetic only.  Output: census CSV + stats.
 *
 * Build:  gcc -O2 -march=native -fopenmp -o sweep699 sweep699.c -lm
 * Run:    ./sweep699 N [W]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>

#define MAXF 13
#define GMAX 512         /* max prime gap below 4e9 is 336 */
#define CANDMAX 200000

typedef unsigned __int128 u128;
typedef uint64_t u64;
typedef uint32_t u32;

static u32 *small_primes; static int n_small;

static void sieve_small(u64 lim) {
    int m = (int)lim + 1;
    char *c = calloc(m, 1);
    small_primes = malloc(sizeof(u32) * (m > 16 ? m : 16));
    n_small = 0;
    for (int p = 2; p < m; p++) if (!c[p]) {
        small_primes[n_small++] = p;
        for (long q = (long)p * p; q < m; q += p) c[q] = 1;
    }
    free(c);
}

static inline int pdiv(u64 p, u64 n, u64 k) {   /* p | C(n,k)? (L3, exact) */
    while (k) {
        if (k % p > n % p) return 1;
        k /= p; n /= p;
    }
    return 0;
}

static inline u64 modinv(u64 a, u64 m) {
    long long t = 0, nt = 1, r = (long long)m, nr = (long long)(a % m);
    while (nr) {
        long long q = r / nr, tmp;
        tmp = t - q * nt; t = nt; nt = tmp;
        tmp = r - q * nr; r = nr; nr = tmp;
    }
    if (t < 0) t += m;
    return (u64)t;
}

typedef struct { u64 p; u32 t; } Adm;

typedef struct {
    FILE *out;
    u64 n_danger_pairs, n_candidates, n_exc, n_cex, n_fallback, n_aempty;
    u32 max_g;
} Stats;

static void record(Stats *st, const char *kind, u64 n, u64 i, u64 j) {
    #pragma omp critical(recout)
    {
        fprintf(st->out, "%s,%llu,%llu,%llu\n", kind,
                (unsigned long long)n, (unsigned long long)i, (unsigned long long)j);
        fflush(st->out);
        fprintf(stderr, "  [%s] n=%llu i=%llu j=%llu\n", kind,
                (unsigned long long)n, (unsigned long long)i, (unsigned long long)j);
    }
    if (kind[0] == 'E') st->n_exc++; else st->n_cex++;
}

static inline void check_candidate(Stats *st, u64 n, u64 i, u64 j,
                                   Adm *A, int na) {
    st->n_candidates++;
    for (int a = 0; a < na; a++)
        if (A[a].p > i && pdiv(A[a].p, n, j)) return;   /* covered by p > i */
    /* no live p > i covers j: try p = i (L4) */
    int iprime = (i >= 2);
    for (int a = 0; a < n_small && (u64)small_primes[a] * small_primes[a] <= i; a++)
        if (i % small_primes[a] == 0) { iprime = 0; break; }
    if (i == 1) iprime = 0;
    if (iprime && (n % (i * i)) < i && pdiv(i, n, j)) {
        record(st, "EXC", n, i, j);
    } else {
        record(st, "CEX", n, i, j);
    }
}

/* handle level (n,i); A has na entries, some possibly stale (p <= i);
 * b1, b2 = indices of the two best live filters (score (t+1)/p), or -1. */
static void handle_level(Stats *st, u64 n, u64 i, Adm *A, int na,
                         int b1, int b2) {
    u64 nh = n / 2;
    st->n_danger_pairs++;
    if (b1 < 0) {                        /* no live admissible prime */
        st->n_aempty++;
        for (u64 j = i + 1; j <= nh; j++) check_candidate(st, n, i, j, A, na);
        return;
    }
    u64 p1 = A[b1].p, t1 = A[b1].t;
    if (b2 < 0) {                        /* single live prime */
        u64 cnt = (t1 + 1) * (nh / p1 + 1);
        if (cnt <= CANDMAX) {
            for (u64 a = 0; a <= t1; a++)
                for (u64 j = a ? a : p1; j <= nh; j += p1)
                    if (j > i) check_candidate(st, n, i, j, A, na);
        } else {
            st->n_fallback++;
            for (u64 j = i + 1; j <= nh; j++)
                if (j % p1 <= t1) check_candidate(st, n, i, j, A, na);
        }
        return;
    }
    u64 p2 = A[b2].p, t2 = A[b2].t;
    u128 M = (u128)p1 * p2;
    u64 est = (t1 + 1) * (t2 + 1) * (u64)(M > nh ? 1 : nh / (u64)M + 1);
    if (est > CANDMAX) {
        st->n_fallback++;
        for (u64 j = i + 1; j <= nh; j++)
            if (j % p1 <= t1 && j % p2 <= t2) check_candidate(st, n, i, j, A, na);
        return;
    }
    if (t1 == 0 && t2 == 0) {            /* j ≡ 0 (mod p1 p2): no inverse needed */
        if (M <= nh)
            for (u64 j = (u64)M; j <= nh; j += (u64)M)
                if (j > i) check_candidate(st, n, i, j, A, na);
        return;
    }
    static _Thread_local u64 c_p1 = 0, c_p2 = 0, c_inv = 0;   /* inv cache */
    u64 inv;
    if (c_p1 == p1 && c_p2 == p2) inv = c_inv;
    else { inv = modinv(p1 % p2, p2); c_p1 = p1; c_p2 = p2; c_inv = inv; }
    for (u64 a = 0; a <= t1; a++) {
        for (u64 b = 0; b <= t2; b++) {
            u64 d = (b + p2 - a % p2) % p2;
            u128 j0 = (u128)a + (u128)p1 * ((u128)d * inv % p2);
            for (u128 j = j0; j <= nh; j += M) {
                u64 jj = (u64)j;
                if (jj > i) check_candidate(st, n, i, jj, A, na);
            }
        }
    }
}

int main(int argc, char **argv) {
    u64 N = argc > 1 ? strtoull(argv[1], 0, 10) : 1000000;
    u64 IMIN = argc > 2 ? strtoull(argv[2], 0, 10) : 1;
    u64 W = argc > 3 ? strtoull(argv[3], 0, 10) : (1ull << 21);
    /* IMIN = 2 is justified by NOTE Prop 0 (Erdos–Szekeres gcd > 1 theorem):
     * level i = 1 can produce neither a counterexample (some prime >= 2 > ...
     * >= 1 always divides the gcd) nor a tight triple (that prime is > 1).
     * Validation runs use IMIN = 1 so the theorem doubles as an engine
     * control. */
    u64 lim = (u64)sqrt((double)N) + 2;
    sieve_small(lim);
    {   /* sieve controls */
        u64 checks[5][2] = {{100,25},{1000,168},{10000,1229},{100000,9592},{1000000,78498}};
        for (int c = 0; c < 5; c++) if (checks[c][0] <= lim) {
            int cnt = 0;
            for (int a = 0; a < n_small && small_primes[a] <= checks[c][0]; a++) cnt++;
            if ((u64)cnt != checks[c][1]) { fprintf(stderr, "SIEVE CONTROL FAIL at %llu\n",
                (unsigned long long)checks[c][0]); return 1; }
        }
        fprintf(stderr, "sieve control ok (%d primes up to %llu)\n", n_small,
                (unsigned long long)lim);
    }

    FILE *out = fopen("census699.csv", "w");
    fprintf(out, "# kind,n,i,j  kinds: EXC (tight: only p=i works), CEX (counterexample)\n");
    Stats total; memset(&total, 0, sizeof total); total.out = out;

    double T0 = omp_get_wtime();
    u64 nseg = (N + W) / W + 1;
    u64 segs_done = 0;

    #pragma omp parallel
    {
        u32 (*fac)[MAXF] = malloc(sizeof(u32[MAXF]) * (W + GMAX));
        unsigned char *nfac = malloc(W + GMAX);
        u64 *cof = malloc(sizeof(u64) * (W + GMAX));
        unsigned char *ispr = malloc(W + GMAX);
        Adm A[MAXF * GMAX];
        Stats st; memset(&st, 0, sizeof st); st.out = out;

        #pragma omp for schedule(dynamic)
        for (u64 seg = 0; seg < nseg; seg++) {
            u64 base = seg * W;
            u64 lo = base > (u64)GMAX ? base - GMAX : 2;
            u64 hi = base + W; if (hi > N + 1) hi = N + 1;
            if (lo >= hi) continue;
            u64 len = hi - lo;
            for (u64 x = 0; x < len; x++) { nfac[x] = 0; cof[x] = lo + x; }
            for (int a = 0; a < n_small; a++) {
                u64 p = small_primes[a];
                if (p * p >= hi) break;
                u64 s = (lo + p - 1) / p * p; if (s < p * p) s = p * p;
                for (u64 m = s; m < hi; m += p) {
                    u64 x = m - lo;
                    fac[x][nfac[x]++] = (u32)p;
                    while (cof[x] % p == 0) cof[x] /= p;
                }
            }
            for (u64 x = 0; x < len; x++) {
                if (cof[x] > 1 && cof[x] < lo + x) fac[x][nfac[x]++] = (u32)cof[x];
                ispr[x] = (cof[x] == lo + x && lo + x >= 2);
                if (ispr[x]) { fac[x][0] = (u32)(lo + x); nfac[x] = 1; }
            }
            u64 nstart = (seg == 0) ? 4 : base;
            for (u64 n = nstart; n < hi; n++) {
                u64 xn = n - lo;
                if (ispr[xn]) continue;             /* g(n)=0 */
                u64 g = 1;
                while (g <= xn && !ispr[xn - g]) g++;
                if (g > xn) { fprintf(stderr, "window underrun n=%llu\n",
                    (unsigned long long)n); exit(2); }
                if (g >= GMAX) { fprintf(stderr, "gap >= GMAX at n=%llu\n",
                    (unsigned long long)n); exit(2); }
                if (g > st.max_g) st.max_g = (u32)g;
                u64 nh = n / 2;
                if (nh < 2) continue;
                u64 imax = g; if (imax > nh - 1) imax = nh - 1;
                /* incremental admissible list + best-two tracking */
                int na = 0, b1 = -1, b2 = -1;
                double s1 = 1e300, s2 = 1e300;
                for (u64 i = 1; i <= imax; i++) {
                    /* insert factors of n-(i-1) with p > i */
                    u64 xt = xn - (i - 1);
                    for (int f = 0; f < nfac[xt]; f++) {
                        u64 p = fac[xt][f];
                        if (p > i) {
                            A[na].p = p; A[na].t = (u32)(i - 1);
                            double s = (double)i / (double)p;   /* (t+1)/p */
                            if (s < s1) { s2 = s1; b2 = b1; s1 = s; b1 = na; }
                            else if (s < s2) { s2 = s; b2 = na; }
                            na++;
                        }
                    }
                    if (i < IMIN) continue;   /* level settled by Prop 0 */
                    /* refresh best pair if stale (p <= i) */
                    if ((b1 >= 0 && A[b1].p <= i) || (b2 >= 0 && A[b2].p <= i)) {
                        b1 = b2 = -1; s1 = s2 = 1e300;
                        for (int a = 0; a < na; a++) {
                            if (A[a].p <= i) continue;
                            double s = (double)(A[a].t + 1) / (double)A[a].p;
                            if (s < s1) { s2 = s1; b2 = b1; s1 = s; b1 = a; }
                            else if (s < s2) { s2 = s; b2 = a; }
                        }
                    }
                    handle_level(&st, n, i, A, na, b1, b2);
                }
            }
            #pragma omp critical(prog)
            {
                segs_done++;
                FILE *sf = fopen("segments_done.log", "a");
                if (sf) { fprintf(sf, "%llu\n", (unsigned long long)seg); fclose(sf); }
                if (segs_done % 128 == 0)
                    fprintf(stderr, "  ... %llu/%llu segments, %.0fs\n",
                        (unsigned long long)segs_done, (unsigned long long)nseg,
                        omp_get_wtime() - T0);
            }
        }
        #pragma omp critical(stats)
        {
            total.n_danger_pairs += st.n_danger_pairs;
            total.n_candidates += st.n_candidates;
            total.n_exc += st.n_exc; total.n_cex += st.n_cex;
            total.n_fallback += st.n_fallback; total.n_aempty += st.n_aempty;
            if (st.max_g > total.max_g) total.max_g = st.max_g;
        }
        free(fac); free(nfac); free(cof); free(ispr);
    }
    double T1 = omp_get_wtime();
    fprintf(stderr,
        "N=%llu danger_pairs=%llu candidates=%llu EXC=%llu CEX=%llu "
        "fallbacks=%llu Aempty=%llu max_gap=%u wall=%.1fs threads=%d\n",
        (unsigned long long)N, (unsigned long long)total.n_danger_pairs,
        (unsigned long long)total.n_candidates, (unsigned long long)total.n_exc,
        (unsigned long long)total.n_cex, (unsigned long long)total.n_fallback,
        (unsigned long long)total.n_aempty, total.max_g, T1 - T0,
        omp_get_max_threads());
    fclose(out);
    return 0;
}
