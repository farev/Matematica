/* grimm_sweep.c — certified verification of Grimm's conjecture, with a
 * census of critical intervals.
 *
 * Grimm's conjecture (1969): if n+1, ..., n+k are all composite, there exist
 * DISTINCT primes p_1, ..., p_k with p_i | n+i.
 *
 * Reduction (known to Grimm): it suffices to check every maximal run of
 * composites, i.e. every gap (p, q) between consecutive primes: any Grimm
 * window is a subinterval of one, and a system of distinct representatives
 * restricts to subsets.  Within a gap with k = q-p-1 composites, a member m
 * with a prime factor P > k is safe automatically: multiples of P are >= P
 * > k apart, so P divides at most one member of the window, and choosing P
 * for m conflicts neither with other big-prime choices (each unique to its
 * member) nor with small-prime choices (all <= k < P).  The members needing
 * care are the CRITICAL ones:
 *
 *     m in (p, q) is critical  iff  every prime factor of m is <= k.
 *
 * Grimm holds on the gap iff the bipartite graph (critical members) x
 * (primes <= k dividing them) has a matching saturating the criticals
 * (Hall).  This program finds every critical member in a range, computes an
 * explicit matching and the exact Hall margin for every gap that has any,
 * and emits the census as the certificate.  A Hall failure would be a
 * counterexample to Grimm's conjecture and is reported loudly.
 *
 * Method: segmented sieve of Eratosthenes (odd byte map); alongside it a
 * cache-blocked sieve over odd prime powers p^e (p <= BSMALL) accumulates
 * res[m] = prod_{odd p <= BSMALL} p^{v_p(m)}, so
 *     m is BSMALL-smooth  iff  res[m] == m >> ctz(m).
 * The walk streams each segment once: composites that pass the smoothness
 * test (rare) are factored by trial division and buffered; when the closing
 * prime arrives, k is known and buffered candidates with largest prime
 * factor <= k are the gap's criticals (complete for k < BSMALL, since
 * critical => k-smooth => BSMALL-smooth).  If k >= BSMALL the gap is redone
 * from scratch by trial division to BSLOW (complete for k < BSLOW); if
 * k >= BSLOW the program aborts (max gap below 4e18 is 1475 < 2000, so this
 * cannot fire below 10^12; the bound is asserted, not assumed).
 *
 * Exact integer arithmetic throughout; no floating point in any decision.
 *
 * Usage:
 *   grimm_sweep LO HI NTHREADS OUTPREFIX   process gaps with left prime in
 *                                          [LO, HI); sieving continues past
 *                                          HI to close the last gap
 *   grimm_sweep --selftest                 matcher + factor unit tests
 *
 * Outputs:
 *   OUTPREFIX.census.csv   p,k,m,factorization,L,assigned,margin
 *   OUTPREFIX.gaphist.csv  gap length k -> count (left prime in range)
 *   OUTPREFIX.summary.txt  totals, prime count, max gap, verdict, timings
 *   exit 0 iff no Hall failure and no internal consistency abort
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include <time.h>

typedef uint64_t u64;
typedef uint32_t u32;

#define BSMALL 600
#define BSLOW  2000
#define SEGN   ((u64)1 << 22)
#define BLOCK  ((u64)1 << 15)
#define MAXCAND 256
#define MAXCRIT 64

static u64 LO, HI;
static int NTH;
static const char *OUT;

/* ---------- base primes ---------- */
static u32 *bprimes; static int nbp;      /* primes to sqrt bound        */
static u32 sprimes[200]; static int nsp;  /* odd primes <= BSMALL        */
static u32 wprimes[400]; static int nwp;  /* all primes <= BSLOW         */

static void base_sieve(u32 lim) {
    char *c = calloc((size_t)lim + 1, 1);
    for (u32 i = 2; (u64)i * i <= lim; i++)
        if (!c[i]) for (u64 j = (u64)i * i; j <= lim; j += i) c[j] = 1;
    int n = 0;
    for (u32 i = 2; i <= lim; i++) if (!c[i]) n++;
    bprimes = malloc((size_t)n * sizeof(u32));
    nbp = nsp = nwp = 0;
    for (u32 i = 2; i <= lim; i++) if (!c[i]) {
        bprimes[nbp++] = i;
        if (i > 2 && i <= BSMALL) sprimes[nsp++] = i;
        if (i <= BSLOW) wprimes[nwp++] = i;
    }
    free(c);
}

/* factor m by trial division over primes <= bound.  Returns 0 if a factor
 * > bound remains (then largest prime factor > bound), else 1 with the
 * distinct prime factors and the largest one. */
static int factor_small(u64 m, u32 bound, u32 *pf, int *npf, u32 *lpf) {
    u64 r = m; *npf = 0; *lpf = 0;
    for (int i = 0; i < nwp && wprimes[i] <= bound; i++) {
        u32 p = wprimes[i];
        if ((u64)p * p > r) break;
        if (r % p == 0) {
            pf[(*npf)++] = p; if (p > *lpf) *lpf = p;
            do r /= p; while (r % p == 0);
        }
    }
    if (r > 1) {
        if (r > bound) return 0;
        pf[(*npf)++] = (u32)r; if ((u32)r > *lpf) *lpf = (u32)r;
    }
    return 1;
}

/* ---------- criticals and matching ---------- */
typedef struct {
    u64 m;
    u32 pf[16]; int npf;
    u32 lpf;
    u32 assigned;
} crit;

static int match_try(int u, crit *cr, int s, u32 *primeof, int nslots,
                     int *seen, int *owner) {
    for (int i = 0; i < cr[u].npf; i++) {
        u32 p = cr[u].pf[i];
        int slot = -1;
        for (int t = 0; t < nslots; t++) {
            if (primeof[t] == p) { slot = t; break; }
            if (primeof[t] == 0) { primeof[t] = p; slot = t; break; }
        }
        if (slot < 0 || seen[slot]) continue;
        seen[slot] = 1;
        if (owner[slot] < 0 ||
            match_try(owner[slot], cr, s, primeof, nslots, seen, owner)) {
            owner[slot] = u; cr[u].assigned = p; return 1;
        }
    }
    return 0;
}

static int match_gap(crit *cr, int s) {
    int nslots = s * 16;
    u32 primeof[MAXCRIT * 16]; int owner[MAXCRIT * 16], seen[MAXCRIT * 16];
    memset(primeof, 0, sizeof(u32) * nslots);
    for (int t = 0; t < nslots; t++) owner[t] = -1;
    int msz = 0;
    for (int u = 0; u < s; u++) {
        memset(seen, 0, sizeof(int) * nslots);
        cr[u].assigned = 0;
        if (match_try(u, cr, s, primeof, nslots, seen, owner)) msz++;
    }
    return msz;
}

/* exact Hall margin min_{T nonempty} |N(T)| - |T| over critical subsets */
static int hall_margin(crit *cr, int s) {
    if (s > 20) return -99;   /* sentinel: not computed exhaustively */
    int best = 1 << 30;
    for (u32 T = 1; T < (1u << s); T++) {
        u32 uni[MAXCRIT * 16]; int nu = 0, sz = 0;
        for (int u = 0; u < s; u++) if (T >> u & 1) {
            sz++;
            for (int i = 0; i < cr[u].npf; i++) {
                u32 p = cr[u].pf[i]; int f = 0;
                for (int j = 0; j < nu; j++) if (uni[j] == p) { f = 1; break; }
                if (!f) uni[nu++] = p;
            }
        }
        if (nu - sz < best) best = nu - sz;
    }
    return best;
}

/* ---------- per-thread state ---------- */
typedef struct {
    int id;
    u64 lo, hi;
    u64 first_prime, last_right;
    u64 nprimes;
    u64 maxgap, maxgap_p;
    u64 ncrit, ngaps_crit, ncand;
    int max_s, min_margin; u64 min_margin_p;
    u64 *gaphist;
    int hall_fail;
    FILE *cf;
    double secs;
} tstate;

/* close the gap (p, q): decide criticals from buffered candidates (fast
 * path) or full trial division (slow path), match, record. */
static void close_gap(tstate *T, u64 p, u64 q, crit *cand, int ncand) {
    u64 k = q - p - 1;
    if (k < BSLOW) T->gaphist[k]++;
    else { fprintf(stderr, "ABORT: gap k=%llu >= BSLOW at p=%llu\n",
                   (unsigned long long)k, (unsigned long long)p); exit(3); }
    if (k > T->maxgap) { T->maxgap = k; T->maxgap_p = p; }
    if (k == 0) return;

    crit cr[MAXCRIT]; int s = 0;
    if (k < BSMALL) {
        for (int i = 0; i < ncand; i++)
            if (cand[i].lpf <= k) {
                if (s >= MAXCRIT) { fprintf(stderr, "ABORT: criticals overflow p=%llu\n",
                                            (unsigned long long)p); exit(3); }
                cr[s++] = cand[i];
            }
    } else {
        /* slow path: re-derive members by trial division to BSLOW */
        for (u64 m = p + 1; m < q; m++) {
            u32 pf[16]; int npf; u32 lpf;
            if (!factor_small(m, BSLOW, pf, &npf, &lpf)) continue;
            if (lpf > k) continue;
            if (s >= MAXCRIT) { fprintf(stderr, "ABORT: criticals overflow p=%llu\n",
                                        (unsigned long long)p); exit(3); }
            cr[s].m = m; cr[s].npf = npf; cr[s].lpf = lpf;
            memcpy(cr[s].pf, pf, sizeof(u32) * npf);
            s++;
        }
    }
    if (!s) return;
    T->ncrit += s; T->ngaps_crit++;
    if (s > T->max_s) T->max_s = s;
    int msz = match_gap(cr, s);
    int margin = hall_margin(cr, s);
    if (msz < s) {
        T->hall_fail = 1;
        fprintf(stderr, "*** HALL FAILURE (Grimm counterexample?!) p=%llu k=%llu "
                        "criticals=%d matched=%d ***\n",
                (unsigned long long)p, (unsigned long long)k, s, msz);
    }
    if (margin != -99 && margin < T->min_margin) {
        T->min_margin = margin; T->min_margin_p = p;
    }
    for (int u = 0; u < s; u++) {
        fprintf(T->cf, "%llu,%llu,%llu,", (unsigned long long)p,
                (unsigned long long)k, (unsigned long long)cr[u].m);
        for (int i = 0; i < cr[u].npf; i++)
            fprintf(T->cf, "%s%u", i ? "*" : "", cr[u].pf[i]);
        fprintf(T->cf, ",%u,%u,%d\n", cr[u].lpf, cr[u].assigned, margin);
    }
}

static void *worker(void *arg) {
    tstate *T = arg;
    struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
    unsigned char *map = malloc(SEGN / 2);
    u64 *res = malloc(SEGN * 8);
    u64 *bcur = malloc((size_t)nbp * 8);
    /* odd prime powers p^e <= HI + slack, with persistent cursors */
    enum { MAXPP = 4096 };
    static _Thread_local u32 sp_p[MAXPP];
    static _Thread_local u64 sp_pe[MAXPP], sp_cur[MAXPP];
    int nspp = 0;
    u64 pplim = T->hi + 64 * BSLOW;
    for (int i = 0; i < nsp; i++) {
        u32 p = sprimes[i];
        for (u64 pe = p; ; pe *= p) {
            sp_p[nspp] = p; sp_pe[nspp] = pe; nspp++;
            if (pe > pplim / p) break;
        }
    }
    u64 base = T->lo < 2 ? 2 : T->lo;
    for (int i = 0; i < nbp; i++) {
        u64 p = bprimes[i];
        if (p == 2) { bcur[i] = UINT64_MAX; continue; }  /* evens by parity */
        u64 st = p * p;
        if (st < base) {
            st = (base + p - 1) / p * p;
            if ((st & 1) == 0) st += p;
        }
        bcur[i] = st;
    }
    for (int i = 0; i < nspp; i++)
        sp_cur[i] = (base + sp_pe[i] - 1) / sp_pe[i] * sp_pe[i];

    crit cand[MAXCAND]; int ncand = 0;
    u64 prev = 0;
    T->first_prime = 0;
    T->min_margin = 1 << 30;
    int done = 0;
    u64 seg_lo = base;
    while (!done) {
        u64 seg_hi = seg_lo + SEGN;
        /* primality map for odds in [seg_lo, seg_hi) */
        memset(map, 0, SEGN / 2);
        for (int i = 0; i < nbp; i++) {
            u64 p = bprimes[i], m = bcur[i];
            for (; m < seg_hi; m += 2 * p) map[(m - seg_lo) >> 1] = 1;
            bcur[i] = m;
        }
        /* odd smooth parts, cache-blocked */
        for (u64 j = 0; j < SEGN; j++) res[j] = 1;
        for (u64 blk = seg_lo; blk < seg_hi; blk += BLOCK) {
            u64 bhi = blk + BLOCK; if (bhi > seg_hi) bhi = seg_hi;
            for (int i = 0; i < nspp; i++) {
                u64 pe = sp_pe[i], m = sp_cur[i]; u32 p = sp_p[i];
                for (; m < bhi; m += pe) res[m - seg_lo] *= p;
                sp_cur[i] = m;
            }
        }
        /* walk */
        for (u64 m = seg_lo; m < seg_hi; m++) {
            int isp;
            if (m < 2) continue;
            else if (m == 2) isp = 1;
            else if ((m & 1) == 0) isp = 0;
            else isp = !map[(m - seg_lo) >> 1];
            if (isp) {
                if (!T->first_prime) {
                    T->first_prime = m; prev = m;
                    if (m >= T->lo && m < T->hi) T->nprimes++;
                    continue;
                }
                close_gap(T, prev, m, cand, ncand);
                ncand = 0;
                prev = m;
                if (m >= T->hi) { T->last_right = m; done = 1; break; }
                T->nprimes++;
            } else if (prev) {
                /* composite inside the open gap: buffer if BSMALL-smooth */
                u64 odd = m >> __builtin_ctzll(m);
                if (res[m - seg_lo] == odd) {
                    T->ncand++;
                    if (ncand >= MAXCAND) { fprintf(stderr, "ABORT: cand overflow near %llu\n",
                                                    (unsigned long long)m); exit(3); }
                    crit *c = &cand[ncand];
                    if (!factor_small(m, BSMALL, c->pf, &c->npf, &c->lpf)) {
                        fprintf(stderr, "ABORT: smooth-part contradiction at %llu\n",
                                (unsigned long long)m); exit(3);
                    }
                    c->m = m;
                    ncand++;
                }
            }
        }
        seg_lo = seg_hi;
        if (!done && seg_lo > T->hi + 100 * BSLOW) {
            fprintf(stderr, "ABORT: no closing prime within %d past hi\n", 100 * BSLOW);
            exit(3);
        }
    }
    free(map); free(res); free(bcur);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    T->secs = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    return NULL;
}

/* ---------- unit tests ---------- */
static int selftest(void) {
    int bad = 0;
    crit cr[3];
    /* Hall failure: three criticals over primes {2,3} */
    cr[0] = (crit){12, {2,3}, 2, 3, 0};
    cr[1] = (crit){18, {2,3}, 2, 3, 0};
    cr[2] = (crit){24, {2,3}, 2, 3, 0};
    int m = match_gap(cr, 3), h = hall_margin(cr, 3);
    if (m != 2 || h != -1) { printf("FAIL hall-neg: match=%d margin=%d\n", m, h); bad = 1; }
    /* matchable */
    cr[0] = (crit){4,  {2},   1, 2, 0};
    cr[1] = (crit){6,  {2,3}, 2, 3, 0};
    cr[2] = (crit){15, {3,5}, 2, 5, 0};
    m = match_gap(cr, 3); h = hall_margin(cr, 3);
    int distinct = cr[0].assigned && cr[1].assigned && cr[2].assigned &&
                   cr[0].assigned != cr[1].assigned &&
                   cr[1].assigned != cr[2].assigned &&
                   cr[0].assigned != cr[2].assigned;
    if (m != 3 || h != 0 || !distinct) { printf("FAIL hall-pos: %d %d %d\n", m, h, distinct); bad = 1; }
    /* factor_small */
    u32 pf[16]; int npf; u32 lpf;
    if (!factor_small(2ULL*2*3*5*541, BSMALL, pf, &npf, &lpf) || lpf != 541 || npf != 4)
        { printf("FAIL factor 1\n"); bad = 1; }
    if (factor_small(999983ULL * 4, BSMALL, pf, &npf, &lpf))
        { printf("FAIL factor 2 (big factor accepted)\n"); bad = 1; }
    if (!factor_small(1ULL << 40, BSMALL, pf, &npf, &lpf) || lpf != 2 || npf != 1)
        { printf("FAIL factor 3 (power of two)\n"); bad = 1; }
    printf(bad ? "selftest FAILED\n" : "selftest PASSED\n");
    return bad;
}

int main(int argc, char **argv) {
    if (argc == 2 && !strcmp(argv[1], "--selftest")) { base_sieve(4000); return selftest(); }
    if (argc != 5) { fprintf(stderr, "usage: %s LO HI NTHREADS OUTPREFIX | --selftest\n", argv[0]); return 2; }
    LO = strtoull(argv[1], 0, 10); HI = strtoull(argv[2], 0, 10);
    NTH = atoi(argv[3]); OUT = argv[4];
    if (NTH < 1 || NTH > 64) { fprintf(stderr, "bad NTHREADS\n"); return 2; }
    u64 sq = 1; while (sq * sq < HI + 200 * BSLOW) sq++;
    base_sieve((u32)(sq + 1000));
    struct timespec w0, w1; clock_gettime(CLOCK_MONOTONIC, &w0);

    pthread_t th[64]; static tstate ts[64];
    u64 span = (HI - LO) / NTH;
    char fn[512];
    for (int t = 0; t < NTH; t++) {
        memset(&ts[t], 0, sizeof(tstate));
        ts[t].id = t;
        ts[t].lo = LO + span * t;
        ts[t].hi = (t == NTH - 1) ? HI : LO + span * (t + 1);
        ts[t].gaphist = calloc(BSLOW, 8);
        snprintf(fn, sizeof fn, "%s.census.t%d.csv", OUT, t);
        ts[t].cf = fopen(fn, "w");
        if (!ts[t].cf) { perror("census"); return 2; }
        pthread_create(&th[t], 0, worker, &ts[t]);
    }
    u64 nprimes = 0, ncrit = 0, ngc = 0, maxgap = 0, maxgap_p = 0, nsc = 0;
    int max_s = 0, minmarg = 1 << 30, fail = 0; u64 minmarg_p = 0;
    for (int t = 0; t < NTH; t++) {
        pthread_join(th[t], 0);
        fclose(ts[t].cf);
        nprimes += ts[t].nprimes; ncrit += ts[t].ncrit; ngc += ts[t].ngaps_crit;
        nsc += ts[t].ncand;
        if (ts[t].maxgap > maxgap) { maxgap = ts[t].maxgap; maxgap_p = ts[t].maxgap_p; }
        if (ts[t].max_s > max_s) max_s = ts[t].max_s;
        if (ts[t].min_margin < minmarg) { minmarg = ts[t].min_margin; minmarg_p = ts[t].min_margin_p; }
        fail |= ts[t].hall_fail;
    }
    for (int t = 0; t + 1 < NTH; t++)
        if (ts[t].last_right != ts[t + 1].first_prime) {
            fprintf(stderr, "ABORT: continuity break t%d: %llu vs %llu\n", t,
                    (unsigned long long)ts[t].last_right,
                    (unsigned long long)ts[t + 1].first_prime);
            return 3;
        }
    clock_gettime(CLOCK_MONOTONIC, &w1);
    double wall = (w1.tv_sec - w0.tv_sec) + 1e-9 * (w1.tv_nsec - w0.tv_nsec);

    snprintf(fn, sizeof fn, "%s.census.csv", OUT);
    FILE *cf = fopen(fn, "w");
    fprintf(cf, "p,k,m,factorization,L,assigned,margin\n");
    for (int t = 0; t < NTH; t++) {
        char fn2[512]; snprintf(fn2, sizeof fn2, "%s.census.t%d.csv", OUT, t);
        FILE *f = fopen(fn2, "r"); char buf[1 << 16]; size_t r;
        while ((r = fread(buf, 1, sizeof buf, f)) > 0) fwrite(buf, 1, r, cf);
        fclose(f); remove(fn2);
    }
    fclose(cf);
    snprintf(fn, sizeof fn, "%s.gaphist.csv", OUT);
    FILE *gh = fopen(fn, "w"); fprintf(gh, "k,count\n");
    for (int k = 0; k < BSLOW; k++) {
        u64 c = 0; for (int t = 0; t < NTH; t++) c += ts[t].gaphist[k];
        if (c) fprintf(gh, "%d,%llu\n", k, (unsigned long long)c);
    }
    fclose(gh);
    snprintf(fn, sizeof fn, "%s.summary.txt", OUT);
    FILE *sf = fopen(fn, "w");
    fprintf(sf, "grimm_sweep LO=%llu HI=%llu threads=%d BSMALL=%d BSLOW=%d\n",
            (unsigned long long)LO, (unsigned long long)HI, NTH, BSMALL, BSLOW);
    fprintf(sf, "primes_in_range=%llu\n", (unsigned long long)nprimes);
    fprintf(sf, "first_prime=%llu last_right_prime=%llu\n",
            (unsigned long long)ts[0].first_prime,
            (unsigned long long)ts[NTH - 1].last_right);
    fprintf(sf, "max_gap_k=%llu at_p=%llu\n", (unsigned long long)maxgap,
            (unsigned long long)maxgap_p);
    fprintf(sf, "smooth_candidates=%llu criticals=%llu gaps_with_criticals=%llu "
            "max_criticals_in_gap=%d\n", (unsigned long long)nsc,
            (unsigned long long)ncrit, (unsigned long long)ngc, max_s);
    fprintf(sf, "min_hall_margin=%d at_p=%llu\n", minmarg == (1 << 30) ? 999 : minmarg,
            (unsigned long long)minmarg_p);
    fprintf(sf, "hall_failures=%d\nwall_secs=%.1f\nthread_secs=", fail, wall);
    for (int t = 0; t < NTH; t++) fprintf(sf, "%.1f ", ts[t].secs);
    fprintf(sf, "\nVERDICT: %s\n", fail ? "HALL FAILURE FOUND — CHECK CENSUS"
                                        : "GRIMM HOLDS ON ALL GAPS IN RANGE");
    fclose(sf);
    printf("done [%llu,%llu): primes=%llu maxgap=%llu(at %llu) cand=%llu "
           "criticals=%llu gaps_w_crit=%llu max_s=%d min_margin=%d wall=%.1fs %s\n",
           (unsigned long long)LO, (unsigned long long)HI,
           (unsigned long long)nprimes, (unsigned long long)maxgap,
           (unsigned long long)maxgap_p, (unsigned long long)nsc,
           (unsigned long long)ncrit, (unsigned long long)ngc, max_s,
           minmarg == (1 << 30) ? 999 : minmarg, wall, fail ? "FAIL" : "OK");
    return fail ? 1 : 0;
}
