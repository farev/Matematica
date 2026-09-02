/* casetest.c -- BLL64 "case test" (Sec. 4-5) generalised: extend a fixed partial
 * assignment (a case-tree leaf) to all primes <= T+1 and push the first pair of
 * consecutive k-th power residues as far as possible (target: beyond T).
 *
 * State: R(q) for every prime (fixed values from --fix, default value otherwise) and
 * the array R[n] = sum e R(q) mod k for all n <= T+1, updated incrementally.
 * Loop: find the least "zero pair" (R[n]=R[n+1]=0) with n >= F (F = frontier: no zero
 * pair below F).  Repair it: for the primes q of n(n+1) (largest first; never fixed
 * or currently locked), for each alternative allowed value v: change R(q), update the
 * multiples of q, and accept iff no zero pair (j,j+1) with j <= n exists among the
 * multiples of q (so the frontier advances to n+1); the change is pushed on a stack
 * and q is locked.  If no (q,v) works: impasse -> backtrack: pop the last change,
 * restore, unlock, and resume that frame's remaining (q,v) options.  Depth-first,
 * with a step limit.  On success writes the full assignment (all primes <= T+1).
 *
 * Usage: ./casetest k T out.txt [--even q] [--fix q=v,...] [--default v] [--vals v,v,..]
 *        [--maxsteps N] [--quiet]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K; static long T, N; static int *spf; static signed char *R, *val; static char *isfixed, *iseven, *locked;
static int dflt = 1, vals[16], nvals = 0; static long maxsteps = 200000000; static int quiet = 0;
typedef struct { long n; long cands[48]; int ncand, ci, vi, pass; long q; int oldv; } Frame;
static Frame *stk; static int sp = 0; static long steps = 0, best_n = 0; static int allow_break = 1;

static int allowed(long q, int v) { return !iseven[q] || v % 2 == 0; }
static void bump(long q, int delta) {   /* R[m] += e*delta for all multiples m = q^e * ... */
    if (delta == 0) return; delta = ((delta % K) + K) % K;
    for (long pw = q; pw <= N - 1; pw *= q) for (long m = pw; m <= N - 1; m += pw) { int r = R[m] + delta; if (r >= K) r -= K; R[m] = r; }
}
static int factor_primes(long n, long *fp) { int c = 0; while (n > 1) { long p = spf[n]; int e = 0; while (n % p == 0) { n /= p; e++; } if (e % K) fp[c++] = p; } return c; }
static long check_multiples(long q, long n) {   /* least j <= n with q | j(j+1) and R[j]=R[j+1]=0, or -1 */
    for (long m = q; m <= n + 1; m += q) { if (m - 1 >= 1 && m - 1 <= n && R[m - 1] == 0 && R[m] == 0) return m - 1; if (m <= n && R[m] == 0 && R[m + 1] == 0) return m; }
    return -1;
}
static long next_zero_pair(long F) { for (long j = F; j < T; j++) if (R[j] == 0 && R[j + 1] == 0) return j; return -1; }
static int cmpdesc(const void *a, const void *b) { long x = *(long *)a, y = *(long *)b; return x < y ? 1 : x > y ? -1 : 0; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    K = atoi(argv[1]); T = atol(argv[2]); char *outname = argv[3]; char *fix = NULL; long evenq[16]; int neven = 0; char *initfile = NULL;
    for (int i = 4; i < argc; i++) { if (!strcmp(argv[i], "--even")) evenq[neven++] = atol(argv[++i]); else if (!strcmp(argv[i], "--fix")) fix = argv[++i]; else if (!strcmp(argv[i], "--default")) dflt = atoi(argv[++i]); else if (!strcmp(argv[i], "--maxsteps")) maxsteps = atol(argv[++i]); else if (!strcmp(argv[i], "--quiet")) quiet = 1; else if (!strcmp(argv[i], "--nobreak")) allow_break = 0; else if (!strcmp(argv[i], "--init")) initfile = argv[++i];
        else if (!strcmp(argv[i], "--vals")) { char *tok = strtok(argv[++i], ","); while (tok) { vals[nvals++] = atoi(tok); tok = strtok(NULL, ","); } } }
    if (!nvals) { for (int v = 0; v < K; v++) vals[nvals++] = v; }
    N = T + 2; spf = malloc(N * sizeof(int)); R = calloc(N, 1); val = malloc(N); isfixed = calloc(N, 1); iseven = calloc(N, 1); locked = calloc(N, 1);
    for (long i = 0; i < N; i++) { spf[i] = 0; val[i] = -1; }
    for (long i = 2; i < N; i++) if (!spf[i]) { spf[i] = i; if (i * i < N) for (long j = i * i; j < N; j += i) if (!spf[j]) spf[j] = i; }
    for (int j = 0; j < neven; j++) iseven[evenq[j]] = 1;
    if (fix) { char *buf = strdup(fix); char *tok = strtok(buf, ","); while (tok) { long p; int v; sscanf(tok, "%ld=%d", &p, &v); if (p < N) { if (!allowed(p, v)) { fprintf(stderr, "fix not allowed\n"); return 1; } val[p] = v; isfixed[p] = 1; } tok = strtok(NULL, ","); } }
    if (initfile) { FILE *fi = fopen(initfile, "r"); char ln[256]; while (fgets(ln, sizeof ln, fi)) { long p; int v; if (ln[0] == '#') continue; if (sscanf(ln, "%ld=%d", &p, &v) == 2 && p < N && val[p] < 0 && allowed(p, v)) val[p] = v; } fclose(fi); }
    for (long p = 2; p < N; p++) if (spf[p] == p && val[p] < 0) val[p] = iseven[p] ? (dflt % 2 ? 2 : dflt) : dflt;
    for (long p = 2; p < N; p++) if (spf[p] == p) bump(p, val[p]);
    stk = malloc(1000000 * sizeof(Frame));
    long F = 1; int status = -1;
    for (;;) {
        long n = next_zero_pair(F);
        if (n < 0) { status = 0; break; }               /* reached T */
        if (n > best_n) best_n = n;
        /* new frame for pair n */
        Frame *f = &stk[sp]; f->n = n; long fp[24]; f->ncand = 0;
        int c = factor_primes(n, fp); for (int i = 0; i < c; i++) f->cands[f->ncand++] = fp[i];
        c = factor_primes(n + 1, fp); for (int i = 0; i < c; i++) f->cands[f->ncand++] = fp[i];
        qsort(f->cands, f->ncand, sizeof(long), cmpdesc); f->ci = 0; f->vi = 0; f->q = -1; f->pass = 0;
        for (;;) {   /* try options of the top frame; on impasse pop */
            f = &stk[sp]; int found = 0; long newF = f->n + 1;
            /* pass 0: changes that create no earlier zero pair; pass 1: allow breaking an
               earlier pair (the frontier moves back to it and it is repaired next) */
            while (f->pass < 2 && !found) {
                while (f->ci < f->ncand) {
                    long q = f->cands[f->ci];
                    if (isfixed[q] || locked[q]) { f->ci++; f->vi = 0; continue; }
                    while (f->vi < nvals) {
                        int v = vals[f->vi++]; if (v == val[q] || !allowed(q, v)) continue;
                        steps++; if (steps > maxsteps) { status = 3; goto done; }
                        int oldv = val[q]; bump(q, v - oldv); val[q] = v;
                        long bad = check_multiples(q, f->n);
                        if (bad < 0 || (f->pass == 1 && allow_break && bad < f->n)) { f->q = q; f->oldv = oldv; locked[q] = 1; found = 1; if (bad >= 0) newF = bad; break; }
                        bump(q, oldv - v); val[q] = oldv;
                    }
                    if (found) break;
                    f->ci++; f->vi = 0;
                }
                if (!found) { f->pass++; f->ci = 0; f->vi = 0; }
            }
            if (found) { if (!quiet) fprintf(stderr, "pair %ld: R(%ld) %d->%d (depth %d)%s\n", f->n, f->q, f->oldv, val[f->q], sp + 1, newF <= f->n ? " [breaks earlier pair]" : ""); F = newF; sp++; break; }
            /* impasse at this frame */
            if (sp == 0) { status = 2; goto done; }
            sp--; Frame *g = &stk[sp]; bump(g->q, g->oldv - val[g->q]); val[g->q] = g->oldv; locked[g->q] = 0; F = g->n;
            if (!quiet) fprintf(stderr, "backtrack to pair %ld (depth %d)\n", g->n, sp);
            /* the popped frame's pair g->n is the next zero pair again; continue its options */
        }
        if (status >= 0) break;
    }
done:
    if (status == 0) { FILE *o = fopen(outname, "w"); fprintf(o, "# k=%d T=%ld casetest witness: no zero pair below T; changes=%d steps=%ld\n", K, T, sp, steps);
        for (long p = 2; p <= T + 1; p++) if (spf[p] == p) fprintf(o, "%ld=%d\n", p, val[p]); fclose(o);
        printf("SUCCESS T=%ld: no pair (n,n+1), n<T, of k-th power residues; changes=%d steps=%ld -> %s\n", T, sp, steps, outname);
        printf("changed primes:"); for (int i = 0; i < sp; i++) printf(" %ld:%d->%d@%ld", stk[i].q, stk[i].oldv, val[stk[i].q], stk[i].n); printf("\n"); }
    else printf("%s: best_n=%ld steps=%ld depth=%d\n", status == 2 ? "IMPASSE (search exhausted under greedy rule)" : "STEP LIMIT", best_n, steps, sp);
    return status;
}
