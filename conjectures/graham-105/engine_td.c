/* engine_td.c — top-down interval-pruned enumeration of all terms of
 * OEIS A030979 below 3^L:  n with base-3 digits <= 1, base-5 digits <= 2,
 * base-7 digits <= 3  (equivalently gcd(C(2n,n), 105) = 1, by Kummer).
 * Each term's base-11 digits are also tested (all <= 5 iff additionally
 * gcd(C(2n,n), 1155) = 1 — the flag printed after each term).
 *
 * No bignum library.  The prefix value A (top d base-3 digits fixed) is
 * carried as little-endian digit arrays in bases 5, 7 and 11, updated by
 * exact carry/borrow addition of precomputed digit arrays of 3^k, with
 * per-base counts of over-cap digits at positions >= the current pruning
 * threshold.  Exact integer arithmetic only; every completion of the
 * prefix satisfies A <= n <= A + (3^(L-d)-1)/2.
 *
 * Pruning rule (identical to topdown.py, node for node): at depth d let
 * W = (3^(L-d)+1)/2 and, for base b in {5,7} with digit cap c, let
 * e = e_b(d) = min{e : b^e >= W}.  Every completion n has
 * floor(n / b^e) in {Q, Q+1} with Q = A / b^e, and the base-b digits of n
 * at positions >= e are exactly the digits of floor(n / b^e).  Prune iff
 * Q and Q+1 both contain a digit > c.  Q is invalid iff nbad_b > 0, where
 * nbad_b counts digits > c at positions >= e.  Q+1 is the increment of
 * the digit string at position e: the carry run e..i-1 consists of digits
 * b-1 (each > c, so each counted in nbad_b); after the increment they
 * become 0 and position i becomes dig[i]+1.  Hence, given nbad_b > 0:
 *   Q+1 invalid  iff  dig[i]+1 > c  or  nbad_b > i - e.
 *
 * Modes:
 *   tables  L                   print d, e5(d), e7(d) rows (for diffing)
 *   full    L [pf] [se]         run whole tree; terms to stdout
 *   taskgen L J                 print depth-J prefixes surviving pruning:
 *                               "id hexbits" (bit d of hex = digit of level d)
 *   tasks   L J file start stride count pf se rows.csv terms.txt
 *                               process every stride-th task from `start`,
 *                               one CSV row per task, terms streamed
 * Term print policy: first pf terms (per process), every se-th term (0 =
 * off), and every term with the 1155 flag set.  Fingerprints (nodes,
 * terms, sum of n mod 2^64, xor of n mod 2^64, sum of n mod 1e9+7) print
 * at the end; they are directly comparable with topdown.py's.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;

#define LMAX 801
#define D5  576
#define D7  472
#define D11 384
#define D10 400
#define MODP 1000000007ULL

static int L;

static unsigned char p5[LMAX][D5];   static int l5[LMAX];
static unsigned char p7[LMAX][D7];   static int l7[LMAX];
static unsigned char p11[LMAX][D11]; static int l11[LMAX];
static unsigned char p10[LMAX][D10]; static int l10[LMAX];
static u64 p64[LMAX], pmp[LMAX];
static int e5tab[LMAX + 1], e7tab[LMAX + 1];

static unsigned char dig5[D5 + 8], dig7[D7 + 8], dig11[D11 + 8];
static int nbad5, nbad7, nbad11;
static int ecur5, ecur7;
static u64 a64, amp;
static unsigned char path[LMAX];
static int first_one;

static u64 nodes, terms, n1155, sum64, xor64, summp;
static u64 hist[LMAX + 2];
static u64 print_first, sample_every;
static FILE *term_out;

static void mul3(unsigned char *dst, const unsigned char *src, int slen,
                 int *dlen, int b, int cap) {
    int c = 0, i;
    for (i = 0; i < slen; i++) {
        int v = 3 * src[i] + c;
        dst[i] = (unsigned char)(v % b);
        c = v / b;
    }
    while (c) { dst[i++] = (unsigned char)(c % b); c /= b; }
    *dlen = i;
    if (i >= cap) { fprintf(stderr, "digit overflow\n"); exit(1); }
}

static void build_pows(void) {
    p5[0][0] = p7[0][0] = p11[0][0] = p10[0][0] = 1;
    l5[0] = l7[0] = l11[0] = l10[0] = 1;
    p64[0] = pmp[0] = 1;
    for (int k = 1; k < LMAX; k++) {
        mul3(p5[k],  p5[k-1],  l5[k-1],  &l5[k],  5,  D5);
        mul3(p7[k],  p7[k-1],  l7[k-1],  &l7[k],  7,  D7);
        mul3(p11[k], p11[k-1], l11[k-1], &l11[k], 11, D11);
        mul3(p10[k], p10[k-1], l10[k-1], &l10[k], 10, D10);
        p64[k] = p64[k-1] * 3ULL;
        pmp[k] = (pmp[k-1] * 3ULL) % MODP;
    }
}

/* sign of 3^m - 2*b^e, given the base-b digits of 3^m (equality impossible) */
static int cmp_3m_2be(const unsigned char *dm, int len, int e) {
    if (len - 1 > e) return 1;
    if (len - 1 < e) return -1;
    if (dm[len - 1] != 2) return dm[len - 1] > 2 ? 1 : -1;
    for (int i = len - 2; i >= 0; i--)
        if (dm[i]) return 1;
    fprintf(stderr, "impossible equality 3^m = 2 b^e\n");
    exit(1);
}

static void build_thresholds(void) {
    for (int d = 0; d <= L; d++) {
        int m = L - d, e;
        e = 0;
        while (cmp_3m_2be(p5[m], l5[m], e) > 0) e++;
        e5tab[d] = e;
        e = 0;
        while (cmp_3m_2be(p7[m], l7[m], e) > 0) e++;
        e7tab[d] = e;
    }
    if (e5tab[L] != 0 || e7tab[L] != 0) { fprintf(stderr, "threshold sanity\n"); exit(1); }
}

static inline void add_digits(unsigned char *dig, const unsigned char *p, int plen,
                              int b, int cap, int ecur, int *nbad) {
    int carry = 0, i = 0;
    for (; i < plen || carry; i++) {
        int v = dig[i] + (i < plen ? p[i] : 0) + carry;
        carry = v >= b;
        int nv = carry ? v - b : v;
        if (nv != dig[i] && i >= ecur)
            *nbad += (nv > cap) - (dig[i] > cap);
        dig[i] = (unsigned char)nv;
    }
}
static inline void sub_digits(unsigned char *dig, const unsigned char *p, int plen,
                              int b, int cap, int ecur, int *nbad) {
    int borrow = 0, i = 0;
    for (; i < plen || borrow; i++) {
        int v = dig[i] - (i < plen ? p[i] : 0) - borrow;
        borrow = v < 0;
        int nv = borrow ? v + b : v;
        if (nv != dig[i] && i >= ecur)
            *nbad += (nv > cap) - (dig[i] > cap);
        dig[i] = (unsigned char)nv;
    }
}

static inline void add3k(int k) {
    add_digits(dig5,  p5[k],  l5[k],  5,  2, ecur5, &nbad5);
    add_digits(dig7,  p7[k],  l7[k],  7,  3, ecur7, &nbad7);
    add_digits(dig11, p11[k], l11[k], 11, 5, 0,     &nbad11);
    a64 += p64[k];
    amp += pmp[k]; if (amp >= MODP) amp -= MODP;
}
static inline void sub3k(int k) {
    sub_digits(dig5,  p5[k],  l5[k],  5,  2, ecur5, &nbad5);
    sub_digits(dig7,  p7[k],  l7[k],  7,  3, ecur7, &nbad7);
    sub_digits(dig11, p11[k], l11[k], 11, 5, 0,     &nbad11);
    a64 -= p64[k];
    amp = (amp + MODP - pmp[k]) % MODP;
}

static inline void shift_down(int d) {
    for (int i = e5tab[d]; i < ecur5; i++) nbad5 += dig5[i] > 2;
    ecur5 = e5tab[d];
    for (int i = e7tab[d]; i < ecur7; i++) nbad7 += dig7[i] > 3;
    ecur7 = e7tab[d];
}
static inline void shift_up(int d_child) {
    for (int i = ecur5; i < e5tab[d_child - 1]; i++) nbad5 -= dig5[i] > 2;
    ecur5 = e5tab[d_child - 1];
    for (int i = ecur7; i < e7tab[d_child - 1]; i++) nbad7 -= dig7[i] > 3;
    ecur7 = e7tab[d_child - 1];
}

static inline int prune5(void) {
    if (!nbad5) return 0;
    int i = ecur5;
    while (dig5[i] == 4) i++;
    if (dig5[i] >= 2) return 1;
    if (nbad5 != i - ecur5) return 1;
    return 0;
}
static inline int prune7(void) {
    if (!nbad7) return 0;
    int i = ecur7;
    while (dig7[i] == 6) i++;
    if (dig7[i] >= 3) return 1;
    if (nbad7 != i - ecur7) return 1;
    return 0;
}

static void print_current(FILE *f, int flag) {
    static unsigned char dec[D10 + 8];
    int top = 0;
    memset(dec, 0, sizeof dec);
    for (int d = 0; d < L; d++)
        if (path[d]) {
            int k = L - 1 - d, carry = 0, i = 0;
            for (; i < l10[k] || carry; i++) {
                int v = dec[i] + (i < l10[k] ? p10[k][i] : 0) + carry;
                carry = v >= 10;
                dec[i] = (unsigned char)(carry ? v - 10 : v);
            }
            if (i > top) top = i;
        }
    if (!top) { fprintf(f, "0:%d\n", flag); return; }
    for (int i = top - 1; i >= 0; i--) fputc('0' + dec[i], f);
    fprintf(f, ":%d\n", flag);
}

static void leaf(void) {
    if (nbad5 || nbad7) return;
    int flag = nbad11 == 0;
    terms++;
    sum64 += a64;
    xor64 ^= a64;
    summp += amp; if (summp >= MODP) summp -= MODP;
    hist[first_one < 0 ? 0 : L - first_one]++;
    if (flag) n1155++;
    if (term_out && (terms <= print_first ||
                     (sample_every && terms % sample_every == 0) || flag))
        print_current(term_out, flag);
}

static void rec(int d) {
    nodes++;
    if (d == L) { leaf(); return; }
    if (prune5() || prune7()) return;
    shift_down(d + 1);
    path[d] = 0;
    rec(d + 1);
    path[d] = 1;
    int saved = first_one;
    if (first_one < 0) first_one = d;
    add3k(L - 1 - d);
    rec(d + 1);
    sub3k(L - 1 - d);
    first_one = saved;
    path[d] = 0;
    shift_up(d + 1);
}

static void reset_state(void) {
    memset(dig5, 0, sizeof dig5);
    memset(dig7, 0, sizeof dig7);
    memset(dig11, 0, sizeof dig11);
    memset(path, 0, sizeof path);
    nbad5 = nbad7 = nbad11 = 0;
    ecur5 = e5tab[0]; ecur7 = e7tab[0];
    a64 = 0; amp = 0; first_one = -1;
}

/* rec_max: explore the 1-branch first; the first term reached is the
 * largest term below 3^L (every value in the 1-subtree exceeds every value
 * in the 0-subtree).  Pruning is order-independent, so soundness carries. */
static u64 max_nodes;
static int rec_max(int d) {
    max_nodes++;
    if (d == L) {
        if (nbad5 || nbad7) return 0;
        printf("MAX ");
        print_current(stdout, nbad11 == 0);
        return 1;
    }
    if (prune5() || prune7()) return 0;
    shift_down(d + 1);
    path[d] = 1;
    int saved = first_one;
    if (first_one < 0) first_one = d;
    add3k(L - 1 - d);
    int hit = rec_max(d + 1);
    if (!hit) {
        sub3k(L - 1 - d);
        first_one = saved;
        path[d] = 0;
        hit = rec_max(d + 1);
        if (!hit) { shift_up(d + 1); return 0; }
    }
    return 1;   /* leave state as-is; process exits after the first hit */
}

static int TG_J;
static u64 tg_id, tg_nodes;   /* tg_nodes = entries at depth < J (matches rec's) */
static void rec_taskgen(int d) {
    if (d == TG_J) {
        int nhex = (TG_J + 3) / 4;
        printf("%llu ", (unsigned long long)tg_id++);
        for (int h = 0; h < nhex; h++) {
            int v = 0;
            for (int b = 0; b < 4; b++) {
                int lvl = h * 4 + b;
                if (lvl < TG_J && path[lvl]) v |= 1 << b;
            }
            putchar(v < 10 ? '0' + v : 'a' + v - 10);
        }
        putchar('\n');
        return;
    }
    tg_nodes++;
    if (prune5() || prune7()) return;
    shift_down(d + 1);
    path[d] = 0;
    rec_taskgen(d + 1);
    path[d] = 1;
    add3k(L - 1 - d);
    rec_taskgen(d + 1);
    sub3k(L - 1 - d);
    path[d] = 0;
    shift_up(d + 1);
}

static void print_fingerprint(FILE *f) {
    fprintf(f, "FINGERPRINT L=%d nodes=%llu terms=%llu sum64=%llu xor64=%llu summodp=%llu\n",
            L, (unsigned long long)nodes, (unsigned long long)terms,
            (unsigned long long)sum64, (unsigned long long)xor64,
            (unsigned long long)summp);
    fprintf(f, "HIST");
    for (int i = 0; i <= L; i++)
        if (hist[i]) fprintf(f, " %d:%llu", i, (unsigned long long)hist[i]);
    fprintf(f, "\nN1155=%llu\n", (unsigned long long)n1155);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: see header comment\n"); return 1; }
    L = atoi(argv[2]);
    if (L < 1 || L >= LMAX) { fprintf(stderr, "bad L\n"); return 1; }
    build_pows();
    build_thresholds();

    if (!strcmp(argv[1], "tables")) {
        for (int d = 0; d <= L; d++)
            printf("%d %d %d\n", d, e5tab[d], e7tab[d]);
        return 0;
    }

    if (!strcmp(argv[1], "full")) {
        print_first = argc > 3 ? strtoull(argv[3], 0, 10) : ~0ULL;
        sample_every = argc > 4 ? strtoull(argv[4], 0, 10) : 0;
        term_out = stdout;
        reset_state();
        rec(0);
        print_fingerprint(stderr);
        return 0;
    }

    if (!strcmp(argv[1], "max")) {
        reset_state();
        if (!rec_max(0)) printf("MAX none\n");
        fprintf(stderr, "max_nodes=%llu\n", (unsigned long long)max_nodes);
        return 0;
    }

    if (!strcmp(argv[1], "taskgen")) {
        if (argc < 4) { fprintf(stderr, "taskgen L J\n"); return 1; }
        TG_J = atoi(argv[3]);
        if (TG_J < 1 || TG_J > L) { fprintf(stderr, "bad J\n"); return 1; }
        reset_state();
        rec_taskgen(0);
        fprintf(stderr, "TGNODES %llu TASKS %llu\n",
                (unsigned long long)tg_nodes, (unsigned long long)tg_id);
        return 0;
    }

    if (!strcmp(argv[1], "tasks")) {
        if (argc < 11) { fprintf(stderr, "tasks L J file start stride count pf se rows terms\n"); return 1; }
        int J = atoi(argv[3]);
        FILE *tf = fopen(argv[4], "r");
        if (!tf) { perror("tasks file"); return 1; }
        u64 start = strtoull(argv[5], 0, 10), stride = strtoull(argv[6], 0, 10),
            count = strtoull(argv[7], 0, 10);
        print_first = strtoull(argv[8], 0, 10);
        sample_every = strtoull(argv[9], 0, 10);
        FILE *rows = fopen(argv[10], "a");
        term_out = argc > 11 ? fopen(argv[11], "a") : NULL;
        if (!rows || (argc > 11 && !term_out)) { perror("out"); return 1; }
        char line[LMAX / 4 + 64];
        u64 done = 0, want = start;
        while (fgets(line, sizeof line, tf) && done < count) {
            unsigned long long id;
            char hex[LMAX / 4 + 8];
            if (sscanf(line, "%llu %s", &id, hex) != 2) continue;
            if (id != want) continue;
            want += stride; done++;
            reset_state();
            for (int d = 0; d < J; d++) {
                int v = hex[d / 4] <= '9' ? hex[d / 4] - '0' : hex[d / 4] - 'a' + 10;
                path[d] = (unsigned char)((v >> (d % 4)) & 1);
            }
            u64 nodes0 = nodes, terms0 = terms;
            struct timespec t0, t1;
            clock_gettime(CLOCK_MONOTONIC, &t0);
            for (int d = 0; d < J; d++) {
                shift_down(d + 1);
                if (path[d]) {
                    if (first_one < 0) first_one = d;
                    add3k(L - 1 - d);
                }
            }
            rec(J);
            clock_gettime(CLOCK_MONOTONIC, &t1);
            long ms = (t1.tv_sec - t0.tv_sec) * 1000 + (t1.tv_nsec - t0.tv_nsec) / 1000000;
            fprintf(rows, "%llu,%llu,%llu,%llu,%llu,%llu,%llu,%ld\n",
                    id, (unsigned long long)(nodes - nodes0),
                    (unsigned long long)(terms - terms0),
                    (unsigned long long)sum64, (unsigned long long)xor64,
                    (unsigned long long)summp, (unsigned long long)n1155, ms);
            fflush(rows);
            if (term_out) fflush(term_out);
        }
        fprintf(rows, "TOTAL,%llu,%llu,%llu,%llu,%llu,%llu,END\n",
                (unsigned long long)nodes, (unsigned long long)terms,
                (unsigned long long)sum64, (unsigned long long)xor64,
                (unsigned long long)summp, (unsigned long long)n1155);
        fflush(rows);
        print_fingerprint(stderr);
        return 0;
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}
