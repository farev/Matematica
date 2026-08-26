/* kernel.c — hot loop of the t=2 closure for prefix products P < 2^62.
 *
 * For the node (P, A, D = P - A, eps), a valid second-to-last prime q must
 * make u = D*q - P a positive divisor of Nstar = P*P + eps*D  (proved in
 * NOTE.md: gcd(u, D) = 1, so u | P*q + eps  <=>  u | Nstar).
 *
 * This kernel scans ALL odd q in [q0, q0 + 2*(count-1)] and reports the
 * indices whose u divides Nstar.  No primality here: the caller screens
 * the (very few) passers exactly.  All arithmetic is unsigned 128-bit;
 * the caller guarantees P < 2^62 and q_hi < 2^63 so nothing overflows:
 * D*q < 2^125, Nstar < 2^125.
 *
 * Returns the number of passers written to out (capped at outcap; if the
 * cap is hit the caller must rescan — with outcap 4096 this never happens
 * in practice, since passers correspond to divisors of Nstar).
 *
 * build: gcc -O2 -shared -fPIC -o kernel.so kernel.c
 */
#include <stdint.h>
#include <string.h>

typedef unsigned __int128 u128;

/* ---------------------------------------------------------------------
 * t2_scan2: same contract as t2_scan, ~5-10x faster.
 *   - wheel filter: for each small prime p with p NOT dividing Nstar,
 *     indices with p | u are skipped (u = D*q - P moves in an arithmetic
 *     progression mod p, so those indices form a residue class);
 *   - u < 2^64 always holds here (u <= sqrt(Nstar) + 2D < 2^63 for
 *     P < 2^62), so the divisibility test is a 128/64 remainder.
 * Soundness: only candidates with some small prime p | u, p ∤ Nstar are
 * skipped, and such u can never divide Nstar.
 * ------------------------------------------------------------------- */
#define BLK (1 << 20)
static uint8_t alive[BLK];
static const uint64_t SP[] = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                              37, 41, 43, 47, 53, 59, 61};
#define NSP (sizeof(SP) / sizeof(SP[0]))

static inline uint64_t mod128_64(u128 n, uint64_t d)
{
    return (uint64_t)(n % d);
}

long t2_scan2(uint64_t n_hi, uint64_t n_lo,
              uint64_t d_hi, uint64_t d_lo,
              uint64_t p_hi, uint64_t p_lo,
              uint64_t q0, long count,
              long *out, long outcap)
{
    u128 N = ((u128)n_hi << 64) | n_lo;
    u128 D = ((u128)d_hi << 64) | d_lo;
    u128 P = ((u128)p_hi << 64) | p_lo;
    long found = 0;

    /* progression of u mod p: u(i) = u0 + s*i with u0 = D*q0 - P, s = 2D
       (as residues; u(i) may be negative early — those fail uq > P and
       the wheel still only ever *skips* indices, so no issue) */
    uint64_t u0m[NSP], sm[NSP], nm[NSP], inv[NSP];
    int use[NSP];
    for (unsigned k = 0; k < NSP; k++) {
        uint64_t p = SP[k];
        nm[k] = mod128_64(N, p);
        uint64_t dm = mod128_64(D, p);
        uint64_t pm = mod128_64(P, p);
        uint64_t s = (2 * dm) % p;
        uint64_t u0 = ((dm * (q0 % p)) % p + p - pm) % p;
        u0m[k] = u0; sm[k] = s;
        use[k] = 0;
        if (nm[k] != 0) {
            if (s == 0) {
                if (u0 == 0) return 0;   /* every u divisible by p, p∤N */
            } else {
                /* inverse of s mod p by Fermat (p prime, tiny) */
                uint64_t x = 1, b = s, e = p - 2;
                while (e) { if (e & 1) x = (x * b) % p; b = (b * b) % p; e >>= 1; }
                inv[k] = x;
                use[k] = 1;
            }
        }
    }

    u128 step = D << 1;
    for (long base = 0; base < count; base += BLK) {
        long len = count - base < BLK ? count - base : BLK;
        memset(alive, 1, len);
        for (unsigned k = 0; k < NSP; k++) {
            if (!use[k]) continue;
            uint64_t p = SP[k];
            /* first j in block with u(base+j) ≡ 0 (mod p):
               j ≡ -(u0 + s*base) * inv  (mod p) */
            uint64_t r = (u0m[k] + (sm[k] * ((uint64_t)base % p)) % p) % p;
            uint64_t j0 = ((p - r) % p * inv[k]) % p;
            for (long j = (long)j0; j < len; j += p) alive[j] = 0;
        }
        u128 uq = D * (u128)(q0 + 2 * (uint64_t)base);
        for (long j = 0; j < len; j++, uq += step) {
            if (!alive[j] || uq <= P) continue;
            u128 u128v = uq - P;
            uint64_t u = (uint64_t)u128v;   /* u < 2^63 guaranteed */
            if (mod128_64(N, u) == 0) {
                if (found >= outcap) return -1;
                out[found++] = base + j;
            }
        }
    }
    return found;
}

long t2_scan(uint64_t n_hi, uint64_t n_lo,   /* Nstar */
             uint64_t d_hi, uint64_t d_lo,   /* D     */
             uint64_t p_hi, uint64_t p_lo,   /* P     */
             uint64_t q0, long count,
             long *out, long outcap)
{
    u128 N = ((u128)n_hi << 64) | n_lo;
    u128 D = ((u128)d_hi << 64) | d_lo;
    u128 P = ((u128)p_hi << 64) | p_lo;
    long found = 0;
    u128 uq = D * (u128)q0;          /* D*q, advanced by 2D per step */
    u128 step = D << 1;
    for (long i = 0; i < count; i++) {
        if (uq > P) {
            u128 u = uq - P;
            if (N % u == 0) {
                if (found >= outcap) return -1;
                out[found++] = i;
            }
        }
        uq += step;
    }
    return found;
}
