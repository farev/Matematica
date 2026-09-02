/* tree2.c -- exhaustive case tree proving Lambda(k,2) <= L.
 *
 * Model: R: S -> Z/k (S = primes of the trial pairs), n = prod q^e is a k-th power
 * residue iff sum e*R(q) = 0 (mod k).  Optional constraint R(q) even (--even q; for
 * k = 8 the prime 2).  Unit symmetry R -> uR, u in (Z/k)^*, preserves residue status;
 * at each branching only one representative per orbit of the current stabiliser H.
 *
 * Branching (BLL-style "dimension window"): primes are admitted in increasing order;
 * only trial pairs all of whose primes are admitted are examined.  At a node, scan the
 * admitted pairs (n <= L, increasing n): DEAD pairs (some member cannot be a residue
 * under any extension) are skipped, a SETTLED pair (both members residues) closes a
 * leaf, the least OPEN pair is branched on (smallest unassigned prime, one child per
 * H-orbit of allowed values).  If no admitted pair is open, admit the next prime.  If
 * all primes are admitted and no pair is open the leaf is UNSETTLED (a gap): reported.
 *
 * Exhaustiveness: every admissible assignment is, up to units, an extension of exactly
 * one leaf.  If every leaf is settled with a pair n <= L, then for every large prime p
 * some pair (n,n+1), n <= L, consists of k-th power residues, i.e. Lambda(k,2) <= L.
 *
 * Certificate (gzip): one line per leaf "q=v q=v ... | n" (decisions in order; n=-1
 * if unsettled); header carries k, L, the fixed assignment (--fix) and the even list.
 *
 * Usage: ./tree2 k pairsfile L out.gz [--even q] [--fix q=v,q=v,...] [--dry]
 *                [--maxleaves N] [--branch smallest|largest]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXP 8192
static int K; static long L;
static int nprimes; static long primes[MAXP];
static int val[MAXP], step_[MAXP], allowed[MAXP], isfixed[MAXP];
static int npairs; static long *pairn; static int (*moff)[2], (*mlen)[2], *dim;
static int *fq, *fe; static int nf = 0, capf = 0;
static int **lists, *listlen;
static FILE *out = NULL; static int dry = 0, branch_largest = 0; static long maxleaves = -1; static int dmax = 1 << 30;
static long nleaves = 0, nunsettled = 0, nnodes = 0, maxn = -1, maxdepth = 0;
static int path_q[MAXP], path_v[MAXP], depth = 0;
static long *hist, leaves_by_d[MAXP + 2];

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int prime_index(long p) { int lo = 0, hi = nprimes - 1; while (lo <= hi) { int mid = (lo + hi) / 2; if (primes[mid] == p) return mid; if (primes[mid] < p) lo = mid + 1; else hi = mid - 1; } return -1; }

/* 0 dead, 1 residue under current assignment, 2 open (returns an unassigned prime) */
static int member_status(int pi, int m, int *unq) {
    int c = 0, d = 0, off = moff[pi][m], len = mlen[pi][m], un = -1;
    for (int i = 0; i < len; i++) { int q = fq[off + i], e = fe[off + i];
        if (val[q] >= 0) c += e * val[q];
        else { d = gcd(d, e * step_[q]); if (un < 0 || (!branch_largest && q < un) || (branch_largest && q > un)) un = q; } }
    d = gcd(d, K); if (c % d) return 0; if (un < 0) return 1; *unq = un; return 2;
}
static void write_leaf(long n) {
    if (dry) return;
    for (int i = 0; i < depth; i++) fprintf(out, "%s%ld=%d", i ? " " : "", primes[path_q[i]], path_v[i]);
    fprintf(out, " | %ld\n", n);
}
static void solve(int d, int pos, int H, int dskip) {
    nnodes++;
    if (maxleaves >= 0 && nleaves >= maxleaves) return;
    for (;;) {
        int *lst = lists[d], len = listlen[d];
        for (int i = pos; i < len; i++) {
            int pi = lst[i]; if (dim[pi] < dskip) continue;
            int u0 = -1, u1 = -1;
            int s0 = member_status(pi, 0, &u0); if (!s0) continue;
            int s1 = member_status(pi, 1, &u1); if (!s1) continue;
            if (s0 == 1 && s1 == 1) { nleaves++; hist[pi]++; leaves_by_d[d]++; if (pairn[pi] > maxn) maxn = pairn[pi]; write_leaf(pairn[pi]); return; }
            int q = (s0 == 2 && s1 == 2) ? (branch_largest ? (u0 > u1 ? u0 : u1) : (u0 < u1 ? u0 : u1)) : (s0 == 2 ? u0 : u1);
            int covered = 0;
            for (int v = 0; v < K; v++) {
                if (!((allowed[q] >> v) & 1) || ((covered >> v) & 1)) continue;
                int H2 = 0;
                for (int u = 1; u < K; u++) if ((H >> u) & 1) { int w = (u * v) % K; covered |= 1 << w; if (w == v) H2 |= 1 << u; }
                val[q] = v; path_q[depth] = q; path_v[depth] = v; depth++; if (depth > maxdepth) maxdepth = depth;
                solve(d, i, H2, dskip);
                depth--; val[q] = -1;
                if (maxleaves >= 0 && nleaves >= maxleaves) return;
            }
            return;
        }
        if (d == nprimes || d >= dmax) { nleaves++; nunsettled++; leaves_by_d[d]++; write_leaf(-1);
            fprintf(stderr, "UNSETTLED: "); for (int i = 0; i < depth; i++) fprintf(stderr, "%ld=%d ", primes[path_q[i]], path_v[i]); fprintf(stderr, "\n"); return; }
        dskip = d; d++; pos = 0;   /* admit next prime; everything of lower dimension is dead */
    }
}
static void addfact(int pi, int m, char *s) {
    moff[pi][m] = nf; int len = 0; if (strcmp(s, "1") == 0) { mlen[pi][m] = 0; return; }
    char *tok = strtok(s, ",");
    while (tok) { long p; int e; if (sscanf(tok, "%ld^%d", &p, &e) != 2) { fprintf(stderr, "bad token %s\n", tok); exit(1); }
        int q = prime_index(p); if (q < 0) { fprintf(stderr, "prime %ld missing\n", p); exit(1); }
        e %= K; if (e) { if (nf >= capf) { capf = capf ? capf * 2 : 1 << 20; fq = realloc(fq, capf * sizeof(int)); fe = realloc(fe, capf * sizeof(int)); } fq[nf] = q; fe[nf] = e; nf++; len++; if (q > dim[pi]) dim[pi] = q; }
        tok = strtok(NULL, ","); }
    mlen[pi][m] = len;
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: tree2 k pairsfile L out.gz [--even q] [--fix q=v,...] [--dry] [--maxleaves N] [--branch smallest|largest]\n"); return 1; }
    K = atoi(argv[1]); FILE *f = fopen(argv[2], "r"); if (!f) { perror("pairs"); return 1; } L = atol(argv[3]);
    long evenq[16]; int neven = 0; char *fix = NULL;
    for (int i = 5; i < argc; i++) { if (!strcmp(argv[i], "--even")) evenq[neven++] = atol(argv[++i]); else if (!strcmp(argv[i], "--fix")) fix = argv[++i]; else if (!strcmp(argv[i], "--dry")) dry = 1; else if (!strcmp(argv[i], "--maxleaves")) maxleaves = atol(argv[++i]); else if (!strcmp(argv[i], "--branch")) branch_largest = !strcmp(argv[++i], "largest"); else if (!strcmp(argv[i], "--dmax")) dmax = atoi(argv[++i]); }
    static char line[4096], fa[2048], fb[2048]; long n; static unsigned char seen[1 << 25];
    int cnt = 0;
    while (fgets(line, sizeof line, f)) { if (line[0] == '#') continue; if (sscanf(line, "%ld %s %s", &n, fa, fb) != 3) continue; if (n > L) continue; cnt++;
        for (int m = 0; m < 2; m++) { char *s = m ? fb : fa; if (!strcmp(s, "1")) continue; char buf[2048]; strcpy(buf, s); char *tok = strtok(buf, ","); while (tok) { long p; int e; sscanf(tok, "%ld^%d", &p, &e); if (p >= (1L << 25)) { fprintf(stderr, "prime too large\n"); return 1; } seen[p] = 1; tok = strtok(NULL, ","); } } }
    nprimes = 0; for (long p = 2; p < (1L << 25); p++) if (seen[p]) { if (nprimes >= MAXP) { fprintf(stderr, "too many primes\n"); return 1; } primes[nprimes++] = p; }
    for (int i = 0; i < nprimes; i++) { val[i] = -1; step_[i] = 1; allowed[i] = (1 << K) - 1; isfixed[i] = 0; for (int j = 0; j < neven; j++) if (primes[i] == evenq[j]) { step_[i] = 2; allowed[i] = 0; for (int v = 0; v < K; v += 2) allowed[i] |= 1 << v; } }
    pairn = malloc(cnt * sizeof(long)); moff = malloc(cnt * sizeof *moff); mlen = malloc(cnt * sizeof *mlen); dim = malloc(cnt * sizeof(int));
    rewind(f); npairs = 0;
    while (fgets(line, sizeof line, f)) { if (line[0] == '#') continue; if (sscanf(line, "%ld %s %s", &n, fa, fb) != 3) continue; if (n > L) continue;
        pairn[npairs] = n; dim[npairs] = -1; addfact(npairs, 0, fa); addfact(npairs, 1, fb); npairs++; }
    fclose(f);
    for (int i = 1; i < npairs; i++) if (pairn[i] <= pairn[i - 1]) { fprintf(stderr, "pairs not sorted\n"); return 1; }
    lists = malloc((nprimes + 1) * sizeof(int *)); listlen = calloc(nprimes + 1, sizeof(int));
    for (int d = 0; d <= nprimes; d++) { int c = 0; for (int i = 0; i < npairs; i++) if (dim[i] < d) c++; lists[d] = malloc((c + 1) * sizeof(int)); c = 0; for (int i = 0; i < npairs; i++) if (dim[i] < d) lists[d][c++] = i; listlen[d] = c; }
    hist = calloc(npairs, sizeof(long));
    int H = 0; for (int u = 1; u < K; u++) if (gcd(u, K) == 1) H |= 1 << u;
    if (fix) { char buf[4096]; strcpy(buf, fix); char *tok = strtok(buf, ","); while (tok) { long p; int v; if (sscanf(tok, "%ld=%d", &p, &v) != 2) { fprintf(stderr, "bad fix %s\n", tok); return 1; } int q = prime_index(p); if (q < 0) { fprintf(stderr, "fixed prime %ld not in pair list\n", p); return 1; } if (!((allowed[q] >> v) & 1)) { fprintf(stderr, "fix value not allowed\n"); return 1; } val[q] = v; isfixed[q] = 1; int H2 = 0; for (int u = 1; u < K; u++) if ((H >> u) & 1 && (u * v) % K == v) H2 |= 1 << u; H = H2; tok = strtok(NULL, ","); } }
    if (!dry) { char cmd[4200]; snprintf(cmd, sizeof cmd, "gzip -1 > %s", argv[4]); out = popen(cmd, "w"); if (!out) { perror("gzip"); return 1; }
        fprintf(out, "# k=%d L=%ld pairs=%s nprimes=%d npairs=%d branch=%s\n# even:", K, L, argv[2], nprimes, npairs, branch_largest ? "largest" : "smallest"); for (int j = 0; j < neven; j++) fprintf(out, " %ld", evenq[j]); fprintf(out, "\n# fix:"); for (int i = 0; i < nprimes; i++) if (isfixed[i]) fprintf(out, " %ld=%d", primes[i], val[i]); fprintf(out, "\n"); }
    fprintf(stderr, "k=%d L=%ld primes=%d pairs(n<=L)=%d even=%d fix=%s dry=%d\n", K, L, nprimes, npairs, neven, fix ? fix : "-", dry);
    solve(0, 0, H, 0);
    if (out) pclose(out);
    printf("k=%d L=%ld: nodes=%ld leaves=%ld unsettled=%ld maxdepth=%ld max_settling_n=%ld%s\n", K, L, nnodes, nleaves, nunsettled, maxdepth, maxn, (maxleaves >= 0 && nleaves >= maxleaves) ? " [ABORTED at maxleaves]" : "");
    printf("largest settling values (n:count):"); int shown = 0; for (int pi = npairs - 1; pi >= 0 && shown < 10; pi--) if (hist[pi]) { printf(" %ld:%ld", pairn[pi], hist[pi]); shown++; } printf("\n");
    printf("leaves by window d:"); for (int d = 0; d <= nprimes; d++) if (leaves_by_d[d]) printf(" %d:%ld", d, leaves_by_d[d]); printf("\n");
    return 0;
}
