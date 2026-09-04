/* witness.c -- extend a fixed partial assignment R (a case-tree leaf) to ALL primes
 * <= T+1 so that no pair (n, n+1) with n < T has both members k-th power residues.
 * Complete DFS over pairs in increasing n with conflict-directed backjumping (CBJ).
 *
 * At pair (n,n+1): DEAD -> next n.  SETTLED (all primes assigned, both residues) ->
 * conflict; blame the deepest decision among the primes of n(n+1), retry it with its
 * next value (resuming the scan at the n where that decision was made), propagating
 * conflict sets upward when a decision is exhausted.  OPEN -> decide the smallest
 * unassigned prime q of the pair; value order = fewest immediate conflicts among the
 * multiples of q whose neighbours are already known residues, then fewest residues
 * created, then numeric.  Complete: every allowed value of every decision is tried.
 *
 * Usage: ./witness k T out.txt [--even q] [--fix q=v,...] [--maxdec N]
 * Output: "q=v" for every prime q <= T+1 (unassigned primes get the first allowed
 * nonzero value; any value works for them).  Verify independently with verify_witness.py.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K; static long T; static int *spf; static signed char *val; static int *level; static char *isfixed, *iseven;
typedef struct { long q; int order[16], nvals, pos; long front; long *conf; int nconf, capconf; } Dec;
static Dec *st; static int top = -1; static long ndec = 0, nconfl = 0, maxdec = -1; static long best_n = 0;

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int allowed(long q, int v) { return !iseven[q] || v % 2 == 0; }
/* factor n: primes fp[], exponents mod k fe[] (nonzero only); returns count */
static int factor(long n, long *fp, int *fe) { int c = 0; while (n > 1) { long p = spf[n]; int e = 0; while (n % p == 0) { n /= p; e++; } e %= K; if (e) { fp[c] = p; fe[c] = e; c++; } } return c; }
/* status of member n: 0 dead, 1 residue, 2 open (*unq = smallest unassigned prime) */
static int status(long n, long *unq) { long fp[24]; int fe[24]; int c = factor(n, fp, fe); int s = 0, d = 0; long un = -1;
    for (int i = 0; i < c; i++) { if (val[fp[i]] >= 0) s += fe[i] * val[fp[i]]; else { d = gcd(d, fe[i] * (iseven[fp[i]] ? 2 : 1)); if (un < 0 || fp[i] < un) un = fp[i]; } }
    d = gcd(d, K); if (s % d) return 0; if (un < 0) return 1; *unq = un; return 2; }
static int residue_known(long n) { if (n < 1) return 0; long u; return status(n, &u) == 1; }
static void conf_add(Dec *D, long q) { for (int i = 0; i < D->nconf; i++) if (D->conf[i] == q) return; if (D->nconf >= D->capconf) { D->capconf = D->capconf ? 2 * D->capconf : 16; D->conf = realloc(D->conf, D->capconf * sizeof(long)); } D->conf[D->nconf++] = q; }

/* value ordering heuristic for prime q */
static void order_values(Dec *D) {
    long q = D->q; long bad[16] = {0}, res[16] = {0};
    for (long m = q; m <= T + 1; m += q) {
        long fp[24]; int fe[24]; int c = factor(m, fp, fe); int s = 0, eq = 0, ok = 1;
        for (int i = 0; i < c; i++) { if (fp[i] == q) eq = fe[i]; else if (val[fp[i]] >= 0) s += fe[i] * val[fp[i]]; else { ok = 0; break; } }
        if (!ok) continue;
        int nb = (m <= T && residue_known(m - 1)) || (m < T && residue_known(m + 1));
        for (int v = 0; v < K; v++) { if (!allowed(q, v)) continue; if ((s + eq * v) % K == 0) { res[v]++; if (nb) bad[v]++; } }
    }
    int n = 0; for (int v = 0; v < K; v++) if (allowed(q, v)) D->order[n++] = v; D->nvals = n;
    for (int i = 1; i < n; i++) { int v = D->order[i], j = i - 1; while (j >= 0 && (bad[D->order[j]] > bad[v] || (bad[D->order[j]] == bad[v] && res[D->order[j]] > res[v]))) { D->order[j + 1] = D->order[j]; j--; } D->order[j + 1] = v; }
}
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: witness k T out.txt [--even q] [--fix q=v,...] [--maxdec N]\n"); return 1; }
    K = atoi(argv[1]); T = atol(argv[2]); char *outname = argv[3]; char *fix = NULL; long evenq[16]; int neven = 0;
    for (int i = 4; i < argc; i++) { if (!strcmp(argv[i], "--even")) evenq[neven++] = atol(argv[++i]); else if (!strcmp(argv[i], "--fix")) fix = argv[++i]; else if (!strcmp(argv[i], "--maxdec")) maxdec = atol(argv[++i]); }
    long N = T + 2; spf = malloc(N * sizeof(int)); val = malloc(N); level = malloc(N * sizeof(int)); isfixed = calloc(N, 1); iseven = calloc(N, 1);
    for (long i = 0; i < N; i++) { spf[i] = 0; val[i] = -1; level[i] = -1; }
    for (long i = 2; i < N; i++) if (!spf[i]) { spf[i] = i; for (long j = i * i; j < N; j += i) if (!spf[j]) spf[j] = i; }
    for (int j = 0; j < neven; j++) iseven[evenq[j]] = 1;
    if (fix) { char *buf = strdup(fix); char *tok = strtok(buf, ","); while (tok) { long p; int v; sscanf(tok, "%ld=%d", &p, &v); if (p < N) { if (!allowed(p, v)) { fprintf(stderr, "fix not allowed\n"); return 1; } val[p] = v; isfixed[p] = 1; } tok = strtok(NULL, ","); } }
    for (int i = 4; i < argc; i++) if (!strcmp(argv[i], "--fixfile")) { FILE *ff = fopen(argv[i + 1], "r"); char ln[256]; long nfx = 0; while (fgets(ln, sizeof ln, ff)) { long p; int v; if (ln[0] != '#' && sscanf(ln, "%ld=%d", &p, &v) == 2 && p < N && allowed(p, v)) { val[p] = v; isfixed[p] = 1; nfx++; } } fclose(ff); fprintf(stderr, "fixed %ld primes from %s\n", nfx, argv[i + 1]); }
    st = calloc(N, sizeof(Dec));
    long n = 1;
    while (n < T) {
        if (n > best_n) best_n = n;
        long u0 = -1, u1 = -1; int s0 = status(n, &u0); if (!s0) { n++; continue; } int s1 = status(n + 1, &u1); if (!s1) { n++; continue; }
        if (s0 == 1 && s1 == 1) {   /* conflict */
            nconfl++;
            long C[48]; int nc = 0; long fp[24]; int fe[24]; int c = factor(n, fp, fe); for (int i = 0; i < c; i++) C[nc++] = fp[i]; c = factor(n + 1, fp, fe); for (int i = 0; i < c; i++) C[nc++] = fp[i];
            for (;;) {
                int best = -1; for (int i = 0; i < nc; i++) if (level[C[i]] > best) best = level[C[i]];
                if (best < 0) { printf("FAIL: pair (%ld,%ld) settled with no decision to blame (fixed assignment forces it); best_n=%ld decisions=%ld conflicts=%ld\n", n, n + 1, best_n, ndec, nconfl); return 2; }
                while (top > best) { val[st[top].q] = -1; level[st[top].q] = -1; top--; }
                Dec *D = &st[best]; for (int i = 0; i < nc; i++) if (C[i] != D->q) conf_add(D, C[i]);
                D->pos++;
                if (D->pos < D->nvals) { val[D->q] = D->order[D->pos]; n = D->front; break; }
                nc = 0; for (int i = 0; i < D->nconf; i++) C[nc++] = D->conf[i]; /* conf never contains D->q */
                val[D->q] = -1; level[D->q] = -1; D->nconf = 0; top--;
            }
            continue;
        }
        long q = (s0 == 2 && s1 == 2) ? (u0 < u1 ? u0 : u1) : (s0 == 2 ? u0 : u1);
        ndec++; if (maxdec >= 0 && ndec > maxdec) { printf("ABORT: decision limit; best_n=%ld decisions=%ld conflicts=%ld\n", best_n, ndec, nconfl); return 3; }
        top++; Dec *D = &st[top]; D->q = q; D->pos = 0; D->front = n; D->nconf = 0; order_values(D); val[q] = D->order[0]; level[q] = top;
    }
    /* success: write full assignment */
    FILE *o = fopen(outname, "w"); fprintf(o, "# k=%d T=%ld witness: no pair (n,n+1), n<T, of k-th power residues; decisions=%ld conflicts=%ld\n", K, T, ndec, nconfl);
    long nun = 0; for (long p = 2; p <= T + 1; p++) if (spf[p] == p) { int v = val[p]; if (v < 0) { v = iseven[p] ? 2 : 1; nun++; } fprintf(o, "%ld=%d\n", p, v); }
    fclose(o);
    printf("SUCCESS: witness written to %s (decisions=%ld conflicts=%ld unassigned-primes-defaulted=%ld)\n", outname, ndec, nconfl, nun);
    return 0;
}
