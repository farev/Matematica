/* lambda_coverage.c -- exact segmented Liouville sieve + sign-pattern coverage.
 *
 * Computes lambda(n) = (-1)^Omega(n) for n = 1..X by an exact segmented sieve
 * (pure integer arithmetic; no floating point anywhere in the critical path)
 * and tracks, for each requested window length k, the first occurrence of every
 * one of the 2^k sign patterns of length k.
 *
 *   N_k = the smallest window START index s such that, once the window
 *         lambda(s), lambda(s+1), ..., lambda(s+k-1) has been read, every one
 *         of the 2^k patterns of length k has occurred at some start <= s.
 *
 * Pattern encoding (matches coverage_ext.py, little-endian in window position):
 *
 *   code(s) = sum_{b=0}^{k-1} [lambda(s+b) < 0] * 2^b
 *
 * Sieve.  For a segment [L,R) we keep rem[i] (uint64) and par[i] (uint8).
 * Init: n = L+i, t = ctz(n), rem[i] = n >> t, par[i] = t & 1  (this disposes of
 * p = 2 without a separate pass).  Then for every odd prime p <= sqrt(R-1) and
 * every prime power p^e <= R-1 we walk the multiples of p^e, flipping par and
 * dividing rem by p.  Since Omega(n) = #{(p,e) : p^e | n}, the parity is exact.
 * Division is exact, so we multiply by p^{-1} mod 2^64 (Newton) rather than
 * issuing a hardware divide.  Any n left with rem[i] > 1 carries exactly one
 * prime factor > sqrt(R-1) (its square would exceed n), so one final flip
 * completes Omega(n) mod 2.
 *
 * Usage:
 *   lambda_coverage X k1,k2,...  outprefix [--seg S] [--threads T]
 *                                [--report R] [--endgame E] [--lcheck]
 *
 *   --report R    print an "unseen" line every R values of n (default 2e9)
 *   --endgame E   once fewer than E patterns remain unseen for a given k, log
 *                 every newly-completed pattern (start index + code)
 *   --lcheck      also accumulate L(x) = sum_{n<=x} lambda(n) and print it at
 *                 every power of ten (validation against OEIS A090410 / the
 *                 certified grids in data/)
 *
 * Build:  cc -O2 -fopenmp -march=native -o lambda_coverage lambda_coverage.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>
#include <sys/mman.h>
#include <omp.h>

typedef uint64_t u64;
typedef uint32_t u32;
typedef uint8_t u8;

/* ------------------------------------------------------------------ utils */

static double wall(void) { return omp_get_wtime(); }

/* p^{-1} mod 2^64 by Newton iteration (p odd). */
static u64 inv64(u64 p) {
    u64 x = p;                      /* correct mod 2^3 */
    for (int i = 0; i < 5; i++) x *= 2 - p * x;   /* -> mod 2^64 */
    return x;
}

static u64 isqrt64(u64 n) {
    if (n == 0) return 0;
    u64 x = (u64)1 << ((64 - __builtin_clzll(n) + 1) / 2);
    for (;;) {
        u64 y = (x + n / x) >> 1;
        if (y >= x) break;
        x = y;
    }
    while (x * x > n) x--;
    while ((x + 1) * (x + 1) <= n) x++;
    return x;
}

static void *big_alloc(size_t bytes) {
    void *p = mmap(NULL, bytes, PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(1); }
#ifdef MADV_HUGEPAGE
    madvise(p, bytes, MADV_HUGEPAGE);
#endif
    return p;
}

/* --------------------------------------------------- PRNG control stream */

/* splitmix64 finalizer -- used only by --prng, the negative/positive control:
 * an i.i.d. fair-coin stream pushed through the *identical* window, bitmap and
 * first-occurrence code path, so that any statistic can be calibrated against
 * what genuine randomness produces at the same length. */
static inline u64 sm64(u64 x) {
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}

/* NOTE.  An earlier version used sm64((L+i) ^ seed).  That is wrong as a
 * control: for small seeds, n ^ seed only permutes n inside a short block, so
 * different seeds produce streams with *identical* bit multisets -- every seed
 * gave L(10^8) = +16362 to within 2.  The seed is now pushed through the mixer
 * first and added, which decorrelates the streams properly. */
static void prng_block(u64 L, u64 len, u8 *par, u64 seed) {
    u64 base = sm64(seed * 0x9E3779B97F4A7C15ULL + 0xD1B54A32D192ED03ULL);
    for (u64 i = 0; i < len; i++)
        par[i] = (u8)(sm64(base + L + i) >> 63);
}

/* ------------------------------------------------------------ small primes */

static u64 *primes = NULL;
static u64 *pinv = NULL;
static size_t nprimes = 0;

static void build_primes(u64 limit) {
    u8 *c = calloc(limit + 1, 1);
    if (!c) { perror("calloc"); exit(1); }
    for (u64 i = 2; i * i <= limit; i++)
        if (!c[i]) for (u64 j = i * i; j <= limit; j += i) c[j] = 1;
    size_t cnt = 0;
    for (u64 i = 3; i <= limit; i += 2) if (!c[i]) cnt++;
    primes = malloc(cnt * sizeof(u64));
    pinv = malloc(cnt * sizeof(u64));
    size_t m = 0;
    for (u64 i = 3; i <= limit; i += 2)
        if (!c[i]) { primes[m] = i; pinv[m] = inv64(i); m++; }
    nprimes = m;                     /* odd primes only; p=2 done in init */
    free(c);
}

/* ------------------------------------------------------------------ sieve */

/* Fill par[0..len) with Omega(L+i) mod 2. */
static void sieve_block(u64 L, u64 len, u8 *par, u64 *rem) {
    for (u64 i = 0; i < len; i++) {
        u64 n = L + i;
        int t = __builtin_ctzll(n);
        rem[i] = n >> t;
        par[i] = (u8)(t & 1);
    }
    if (L == 1) { rem[0] = 1; par[0] = 0; }      /* n = 1: Omega = 0 */

    u64 hi = L + len - 1;
    u64 plim = isqrt64(hi);
    for (size_t pi = 0; pi < nprimes; pi++) {
        u64 p = primes[pi];
        if (p > plim) break;
        u64 iv = pinv[pi];
        u64 pe = p;
        for (;;) {
            u64 first = ((L + pe - 1) / pe) * pe;
            if (first <= hi) {
                for (u64 j = first - L; j < len; j += pe) {
                    rem[j] *= iv;
                    par[j] ^= 1;
                }
            }
            if (pe > hi / p) break;
            pe *= p;
        }
    }
    for (u64 i = 0; i < len; i++)
        if (rem[i] > 1) par[i] ^= 1;             /* the one large prime factor */
}

/* ------------------------------------------------------- coverage tracking */

typedef struct {
    int k;
    u8 *bits;            /* 2^k bits */
    u64 *first;          /* optional: first-occurrence start index per pattern */
    const char *firstpath;
    u64 remaining;       /* patterns not yet seen */
    u64 win;             /* current window code (little-endian in position) */
    int filled;          /* how many bits of the window are valid */
    u64 Nk;              /* result: completing window start (0 = not yet) */
    u64 lastcode;
    FILE *endlog;
    u64 endgame;
} Track;

static void track_init(Track *t, int k, u64 endgame, FILE *endlog) {
    t->k = k;
    size_t bytes = ((size_t)1 << k) / 8;
    if (k < 3) bytes = 1;
    t->bits = big_alloc(bytes);
    memset(t->bits, 0, bytes);
    t->first = NULL;
    t->firstpath = NULL;
    t->remaining = (u64)1 << k;
    t->win = 0;
    t->filled = 0;
    t->Nk = 0;
    t->lastcode = 0;
    t->endlog = endlog;
    t->endgame = endgame;
}

/* Feed par[0..len) (bits for n = L..L+len-1).  Returns 1 if k completed. */
static int track_feed(Track *t, u64 L, const u8 *par, u64 len, u64 *wbuf) {
    const int k = t->k;
    const u64 mask = (k == 64) ? ~(u64)0 : (((u64)1 << k) - 1);
    const u64 top = (u64)1 << (k - 1);
    u8 *bits = t->bits;
    u64 w = t->win;
    int filled = t->filled;
    u64 i = 0;

    /* prime the window if this is the very start of the stream */
    while (filled < k - 1 && i < len) {
        w = (w >> 1) | ((u64)(par[i] & 1) * top);
        filled++;
        i++;
    }
    if (filled < k - 1) { t->win = w; t->filled = filled; return 0; }

    /* Two-stage loop: precompute window codes for a chunk (sequential, cheap),
       then walk the chunk with software prefetch so the random bitmap probes
       overlap.  This is what makes the 2^32-entry table affordable. */
    const u64 CH = 4096;
    const u64 PF = 24;
    while (i < len) {
        u64 m = len - i; if (m > CH) m = CH;
        for (u64 j = 0; j < m; j++) {
            w = (w >> 1) | ((u64)(par[i + j] & 1) * top);
            wbuf[j] = w & mask;
        }
        for (u64 j = 0; j < m; j++) {
            if (j + PF < m) __builtin_prefetch(&bits[wbuf[j + PF] >> 3], 1, 0);
            u64 c = wbuf[j];
            u8 msk = (u8)(1u << (c & 7));
            u8 *slot = &bits[c >> 3];
            if (!(*slot & msk)) {
                *slot |= msk;
                t->remaining--;
                u64 start = L + i + j - (u64)(k - 1);
                if (t->first) t->first[c] = start;
                if (t->endlog && t->remaining < t->endgame)
                    fprintf(t->endlog, "%d %" PRIu64 " %" PRIu64 " %" PRIu64 "\n",
                            k, t->remaining, start, c);
                if (t->remaining == 0) {
                    t->Nk = start;
                    t->lastcode = c;
                    t->win = w; t->filled = k - 1 + 1;
                    return 1;
                }
            }
        }
        i += m;
    }
    t->win = w;
    t->filled = k;                    /* saturated */
    return 0;
}

/* ------------------------------------------------------------------- main */

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "usage: %s X k1,k2,... outprefix "
                        "[--seg S] [--threads T] [--report R] [--endgame E] [--lcheck]\n",
                argv[0]);
        return 1;
    }
    u64 X = (u64)strtod(argv[1], NULL);
    int ks[64], nk = 0;
    for (char *s = strtok(argv[2], ","); s && nk < 64; s = strtok(NULL, ","))
        ks[nk++] = atoi(s);
    const char *outpfx = argv[3];

    u64 SEG = 1u << 24;              /* per-thread sub-segment length */
    int T = 4;
    u64 report = 2000000000ULL;
    u64 endgame = 64;
    int lcheck = 0;
    int fo[64], nfo = 0;
    u64 prng_seed = 0;
    int use_prng = 0;
    for (int a = 4; a < argc; a++) {
        if (!strcmp(argv[a], "--firstocc") && a + 1 < argc) {
            for (char *s = strtok(argv[++a], ","); s && nfo < 64; s = strtok(NULL, ","))
                fo[nfo++] = atoi(s);
        }
        else if (!strcmp(argv[a], "--prng") && a + 1 < argc) {
            prng_seed = strtoull(argv[++a], NULL, 0); use_prng = 1;
        }
        else if (!strcmp(argv[a], "--seg") && a + 1 < argc) SEG = (u64)strtod(argv[++a], NULL);
        else if (!strcmp(argv[a], "--threads") && a + 1 < argc) T = atoi(argv[++a]);
        else if (!strcmp(argv[a], "--report") && a + 1 < argc) report = (u64)strtod(argv[++a], NULL);
        else if (!strcmp(argv[a], "--endgame") && a + 1 < argc) endgame = (u64)strtod(argv[++a], NULL);
        else if (!strcmp(argv[a], "--lcheck")) lcheck = 1;
        else { fprintf(stderr, "unknown arg %s\n", argv[a]); return 1; }
    }

    char path[512];
    snprintf(path, sizeof path, "%s_endgame.txt", outpfx);
    FILE *endlog = fopen(path, "w");
    if (endlog) setvbuf(endlog, NULL, _IOLBF, 0);   /* line-buffered: a killed
        run must not lose the endgame certificate lines still in the buffer */
    snprintf(path, sizeof path, "%s_coverage.csv", outpfx);
    FILE *csv = fopen(path, "w");
    fprintf(csv, "k,N_k,last_pattern_code\n");
    fflush(csv);

    double t0 = wall();
    u64 plim = isqrt64(X + (u64)SEG * T + 64);
    build_primes(plim);
    fprintf(stderr, "# odd primes <= %" PRIu64 ": %zu  (%.1fs)\n",
            plim, nprimes, wall() - t0);

    u64 span = SEG * (u64)T;
    u8 *par = big_alloc(span);
    u64 **rems = malloc(T * sizeof(u64 *));
    for (int t = 0; t < T; t++) rems[t] = big_alloc(SEG * sizeof(u64));

    Track *tr = calloc(nk, sizeof(Track));
    u64 **wbufs = malloc(nk * sizeof(u64 *));
    for (int j = 0; j < nk; j++) {
        track_init(&tr[j], ks[j], endgame, endlog);
        wbufs[j] = malloc(4096 * sizeof(u64));
        for (int q = 0; q < nfo; q++)
            if (fo[q] == ks[j]) {
                tr[j].first = big_alloc(((size_t)1 << ks[j]) * sizeof(u64));
                memset(tr[j].first, 0, ((size_t)1 << ks[j]) * sizeof(u64));
                fprintf(stderr, "# first-occurrence spectrum enabled for k=%d "
                        "(%.2f GB)\n", ks[j],
                        (double)((size_t)1 << ks[j]) * 8 / 1e9);
            }
    }
    int ndone = 0;

    int64_t Lsum = 0;
    u64 nextpow = 10;
    u64 nextreport = report;
    double t_sieve = 0, t_track = 0;

    for (u64 L = 1; L <= X && ndone < nk; L += span) {
        u64 len = span;
        if (L + len - 1 > X) len = X - L + 1;

        double ta = wall();
        #pragma omp parallel for num_threads(T) schedule(static, 1)
        for (int t = 0; t < T; t++) {
            u64 off = (u64)t * SEG;
            if (off < len) {
                u64 l = SEG;
                if (off + l > len) l = len - off;
                if (use_prng) prng_block(L + off, l, par + off, prng_seed);
                else          sieve_block(L + off, l, par + off, rems[t]);
            }
        }
        t_sieve += wall() - ta;

        if (lcheck) {
            /* L(x) at every power of ten -- validation only, exact integers */
            for (u64 i = 0; i < len; i++) {
                Lsum += par[i] ? -1 : 1;
                if (L + i == nextpow) {
                    fprintf(stderr, "# L(%" PRIu64 ") = %" PRId64 "\n", nextpow, Lsum);
                    fflush(stderr);
                    nextpow = (nextpow > X / 10) ? ~(u64)0 : nextpow * 10;
                }
            }
        }

        ta = wall();
        #pragma omp parallel for num_threads(nk < T ? nk : T) schedule(dynamic, 1)
        for (int j = 0; j < nk; j++) {
            if (tr[j].Nk) continue;
            if (track_feed(&tr[j], L, par, len, wbufs[j])) {
                #pragma omp critical
                {
                    ndone++;
                    fprintf(stderr, "# k=%d: N_k = %" PRIu64 "  last pattern code = %"
                            PRIu64 "  (%.0fs)\n", tr[j].k, tr[j].Nk, tr[j].lastcode,
                            wall() - t0);
                    fprintf(csv, "%d,%" PRIu64 ",%" PRIu64 "\n",
                            tr[j].k, tr[j].Nk, tr[j].lastcode);
                    fflush(csv);
                }
            }
        }
        t_track += wall() - ta;

        if (L + len - 1 >= nextreport) {
            fprintf(stderr, "  at x=%.3e unseen:", (double)(L + len - 1));
            for (int j = 0; j < nk; j++)
                if (!tr[j].Nk)
                    fprintf(stderr, " k%d:%" PRIu64, tr[j].k, tr[j].remaining);
            fprintf(stderr, "   [sieve %.0fs track %.0fs]\n", t_sieve, t_track);
            fflush(stderr);
            while (nextreport <= L + len - 1) nextreport += report;
        }
    }

    for (int j = 0; j < nk; j++)
        if (!tr[j].Nk)
            fprintf(stderr, "# k=%d: INCOMPLETE at X=%" PRIu64 ", %" PRIu64
                    " patterns still unseen\n", tr[j].k, X, tr[j].remaining);

    /* first-occurrence spectra: raw little-endian uint64 array, index = code.
       A zero entry means the pattern had not occurred by X. */
    for (int j = 0; j < nk; j++) {
        if (!tr[j].first) continue;
        snprintf(path, sizeof path, "%s_firstocc_k%d.bin", outpfx, tr[j].k);
        FILE *fb = fopen(path, "wb");
        if (!fb) { perror("fopen firstocc"); continue; }
        size_t nent = (size_t)1 << tr[j].k;
        if (fwrite(tr[j].first, sizeof(u64), nent, fb) != nent)
            fprintf(stderr, "# WARNING: short write on %s\n", path);
        fclose(fb);
        fprintf(stderr, "# wrote %s (%zu entries)\n", path, nent);
    }

    fprintf(stderr, "# done %.1fs (sieve %.0fs, track %.0fs)\n",
            wall() - t0, t_sieve, t_track);
    fclose(csv);
    if (endlog) fclose(endlog);
    return 0;
}
