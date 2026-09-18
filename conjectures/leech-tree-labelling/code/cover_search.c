/* cover2.c -- exhaustive search for Leech's covering tree problem (OEIS A007187), engine 2.
 * Does a tree on n vertices with positive integer edge weights exist whose path sums
 * cover 1..k?  B = C(n,2)-k is the excess budget (pairs whose distance is > k or
 * repeats another pair's distance).  Edges are exposed in nondecreasing weight order.
 *
 * Soundness facts used (proofs in NOTE.md):
 *  L1 (weight window)  next weight q in [q_prev, mex], mex = least uncovered value.
 *  L2 (monotone excess) excess of a prefix forest never decreases; prune if > B.
 *  L3 (parity)         odd-distance pairs number a(n-a) for the distance-parity
 *                      bipartition; need ceil(k/2) <= a(n-a) <= ceil(k/2)+B and
 *                      floor(k/2) <= N-a(n-a) <= floor(k/2)+B.
 *  L4 (edge load)      an edge joining K_i,K_j carries >= min(|K_i|(n-|K_i|),|K_j|(n-|K_j|))
 *                      paths, all of length >= q, and at most k-q+1+B pairs have distance >= q.
 *  L5 (block bound)    cross distances of a component pair are {d(x,p)+L+d(p',y)},
 *                      L >= q_prev; future excess >= sum over pairs of min block excess;
 *                      and every uncovered value must lie in some admissible block.
 *  S1 (symmetry)       components with equal canonical weighted-tree form are
 *                      interchangeable: only the first of each class is used.
 * Usage: ./cover_search n k [split_depth worker nworkers] [-nb] [-np] [-ns] [-nw] [-nh]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
#define MAXN 16
#define MAXK 120
#define ONE ((u128)1)

static int n, k, N, B;
static int dist[MAXN][MAXN];
static int csize[MAXN];
static int cmem[MAXN][MAXN];
static int ncomp;
static u128 uncov;            /* bit d set iff value d in 1..k uncovered */
static u128 maskk;            /* bits 1..k */
static long long nodes = 0;
static int eu[MAXN], ev[MAXN], ew[MAXN], nedges = 0;
static int found = 0;
static int split_depth = -1, worker = 0, nworkers = 1;
static long long prefix_counter = 0;
static int use_block = 1, use_parity = 1, use_sym = 1, use_wbound = 1, use_hall = 1;
static int allowed_a[MAXN+1];
static long long pruned_parity = 0, pruned_block = 0, pruned_hall = 0;
static int adjw[MAXN][MAXN];  /* adjacency weights within forest, 0 if none */

static inline int popc128(u128 x) { return __builtin_popcountll((unsigned long long)x) + __builtin_popcountll((unsigned long long)(x >> 64)); }

static int mex(void) {
    if (uncov == 0) return k + 1;
    unsigned long long lo = (unsigned long long)uncov;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((unsigned long long)(uncov >> 64));
}

static int parity_ok(void) {
    static char reach[2][MAXN+1];
    int cur = 0;
    memset(reach[cur], 0, sizeof(reach[cur]));
    reach[cur][0] = 1;
    for (int c = 0; c < n; c++) {
        if (csize[c] == 0) continue;
        int r = cmem[c][0], c0 = 0, c1 = 0;
        for (int i = 0; i < csize[c]; i++) { if (dist[r][cmem[c][i]] & 1) c1++; else c0++; }
        int nxt = cur ^ 1;
        memset(reach[nxt], 0, sizeof(reach[nxt]));
        for (int s = 0; s <= n; s++) if (reach[cur][s]) {
            if (s + c0 <= n) reach[nxt][s + c0] = 1;
            if (s + c1 <= n) reach[nxt][s + c1] = 1;
        }
        cur = nxt;
    }
    for (int a = 0; a <= n; a++) if (reach[cur][a] && allowed_a[a]) return 1;
    return 0;
}

/* block bound: returns lower bound on future excess; also fills *cover with union of admissible blocks */
static int block_bound(int q_prev, int remaining, u128 *cover) {
    int total = 0;
    u128 cov = 0;
    int ids[MAXN], m = 0;
    for (int c = 0; c < n; c++) if (csize[c] > 0) ids[m++] = c;
    for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) {
        int ci = ids[a], cj = ids[b];
        int si = csize[ci], sj = csize[cj];
        int pairs = si * sj;
        int best = pairs;             /* L > k: all excess */
        u128 covij = 0;
        for (int pi = 0; pi < si; pi++) {
            int p = cmem[ci][pi];
            u128 Mi = 0;
            for (int x = 0; x < si; x++) Mi |= ONE << dist[cmem[ci][x]][p];
            for (int pj = 0; pj < sj; pj++) {
                int pp = cmem[cj][pj];
                u128 S = 0;
                for (int y = 0; y < sj; y++) { int b2 = dist[pp][cmem[cj][y]]; if (b2 < MAXK) S |= Mi << b2; }
                if (pairs - popc128(S) >= best) continue;
                for (int L = q_prev; L <= k; L++) {
                    u128 blk = (S << L) & uncov;
                    int newd = popc128(blk);
                    int ex = pairs - newd;
                    if (ex < best) best = ex;
                    if (ex + total <= remaining) covij |= blk;
                }
            }
        }
        total += best;
        if (total > remaining) { *cover = 0; return total; }
        cov |= covij;
    }
    *cover = cov;
    return total;
}



/* Combined block analysis for few components (c <= CMAX_EXACT):
   candidates per pair = blocks with excess <= rem; sum of per-pair minima (L5), Hall union,
   then an exact DFS with suffix-minima look-ahead and a step cap (fail-open). */
#define CMAX_EXACT 4
#define CAND_CAP 3000
#define DFS_CAP 5000
static int exact_rem_max = 2; static double prod_cap = 2e5;
static long long pruned_exact = 0, exact_capped = 0;
static int use_exact = 1;
typedef struct { u128 mask; int ex; short L, p, pp; } cand_t;
static cand_t candbuf_all[MAXN][10][CAND_CAP];
static int ncand_all[MAXN][10], minex[10], order[10], sufmin[11];
static int npairs_all[MAXN];
static int pair_ci_all[MAXN][10], pair_cj_all[MAXN][10];
#define candbuf (candbuf_all[nedges])
#define ncand (ncand_all[nedges])
#define npairs_e (npairs_all[nedges])
#define pair_ci (pair_ci_all[nedges])
#define pair_cj (pair_cj_all[nedges])
static long long dfs_steps;
static int exact_dfs(int idx, u128 uni, int exsum, int rem) {
    if (exsum + sufmin[idx] > rem) return 0;
    if (idx == npairs_e) return 1;
    if (++dfs_steps > DFS_CAP) return 1; /* fail open */
    int pr = order[idx];
    for (int t = 0; t < ncand[pr]; t++) {
        cand_t *c = &candbuf[pr][t];
        int overlap = popc128(c->mask & uni);
        if (exsum + c->ex + overlap + sufmin[idx+1] > rem) continue;
        if (exact_dfs(idx + 1, uni | c->mask, exsum + c->ex + overlap, rem)) return 1;
        if (dfs_steps > DFS_CAP) return 1;
    }
    return 0;
}
/* returns 0 if the node is refuted, 1 otherwise */
static int few_component_check(int q_prev, int rem) {
    int ids[MAXN], m = 0;
    for (int c = 0; c < n; c++) if (csize[c] > 0) ids[m++] = c;
    npairs_e = 0;
    int total_min = 0;
    u128 cov = 0;
    for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) {
        int ci = ids[a], cj = ids[b];
        int si = csize[ci], sj = csize[cj], pairs = si * sj;
        int nc = 0, best = pairs + 1;
        u128 covij = 0;
        pair_ci[npairs_e] = ci; pair_cj[npairs_e] = cj;
        if (pairs <= rem) { candbuf[npairs_e][nc].mask = 0; candbuf[npairs_e][nc].ex = pairs; candbuf[npairs_e][nc].L = 0; nc++; best = pairs; }
        int capped = 0;
        for (int pi = 0; pi < si && !capped; pi++) {
            int p = cmem[ci][pi];
            u128 Mi = 0;
            for (int x = 0; x < si; x++) Mi |= ONE << dist[cmem[ci][x]][p];
            for (int pj = 0; pj < sj && !capped; pj++) {
                int pp = cmem[cj][pj];
                u128 S = 0;
                for (int y = 0; y < sj; y++) { int b2 = dist[pp][cmem[cj][y]]; if (b2 < MAXK) S |= Mi << b2; }
                if (pairs - popc128(S) > rem) continue;
                for (int L = q_prev; L <= k; L++) {
                    u128 blk = (S << L) & uncov;
                    int ex = pairs - popc128(blk);
                    if (ex <= rem) {
                        if (ex < best) best = ex;
                        covij |= blk;
                        if (nc < CAND_CAP) { candbuf[npairs_e][nc].mask = blk; candbuf[npairs_e][nc].ex = ex; candbuf[npairs_e][nc].L = L; candbuf[npairs_e][nc].p = p; candbuf[npairs_e][nc].pp = pp; nc++; }
                        else { capped = 1; break; }
                    }
                }
            }
        }
        if (nc == 0) return 0;              /* no admissible block for this pair */
        total_min += best;
        if (total_min > rem) return 0;      /* sum of minima */
        cov |= covij;
        ncand[npairs_e] = nc; minex[npairs_e] = best;
        if (capped) { exact_capped++; ncand[npairs_e] = -1; }
        npairs_e++;
    }
    if (use_hall && (uncov & ~cov) != 0) { pruned_hall++; return 0; }
    if (!use_exact || m > CMAX_EXACT) return 1;
    /* if any pair capped, skip exact DFS (fail open) */
    for (int i = 0; i < npairs_e; i++) if (ncand[i] < 0) return 1;
    if (rem > exact_rem_max) return 1;
    { double prod = 1; for (int i = 0; i < npairs_e; i++) prod *= ncand[i]; if (prod > prod_cap) return 1; }
    /* order by candidate count ascending */
    for (int i = 0; i < npairs_e; i++) order[i] = i;
    for (int i = 0; i < npairs_e; i++) for (int j = i + 1; j < npairs_e; j++) if (ncand[order[j]] < ncand[order[i]]) { int t = order[i]; order[i] = order[j]; order[j] = t; }
    sufmin[npairs_e] = 0;
    for (int i = npairs_e - 1; i >= 0; i--) sufmin[i] = sufmin[i+1] + minex[order[i]];
    dfs_steps = 0;
    if (!exact_dfs(0, 0, 0, rem)) { pruned_exact++; return 0; }
    return 1;
}
/* canonical form of weighted tree component (AHU strings, rooted at hop-center) */
static char cbuf_all[MAXN][MAXN][2048];
#define cbuf (cbuf_all[nedges])
static int canon_rec(int v, int parent, char *out) {
    /* collect children strings */
    char kids[MAXN][1024]; int nk = 0;
    for (int c = 0; c < n; c++) if (adjw[v][c] && c != parent) {
        char tmp[1024]; int len = canon_rec(c, v, tmp);
        snprintf(kids[nk], 1024, "%03d%s", adjw[v][c], tmp); (void)len; nk++;
    }
    /* sort kids */
    for (int i = 0; i < nk; i++) for (int j = i + 1; j < nk; j++) if (strcmp(kids[i], kids[j]) > 0) { char t[1024]; strcpy(t, kids[i]); strcpy(kids[i], kids[j]); strcpy(kids[j], t); }
    int pos = 0; out[pos++] = '(';
    for (int i = 0; i < nk; i++) { int l = strlen(kids[i]); if (pos + l + 2 >= 1000) { fprintf(stderr, "canon overflow\n"); exit(3); } memcpy(out + pos, kids[i], l); pos += l; }
    out[pos++] = ')'; out[pos] = 0; return pos;
}
static void canon_component(int c, char *out) {
    int s = csize[c];
    if (s == 1) { strcpy(out, "."); return; }
    /* hop center: repeatedly strip leaves */
    int deg[MAXN], alive[MAXN], cnt_alive = s;
    for (int i = 0; i < s; i++) { int v = cmem[c][i]; alive[v] = 1; deg[v] = 0; for (int j = 0; j < s; j++) if (adjw[v][cmem[c][j]]) deg[v]++; }
    while (cnt_alive > 2) {
        int leaves[MAXN], nl = 0;
        for (int i = 0; i < s; i++) { int v = cmem[c][i]; if (alive[v] && deg[v] == 1) leaves[nl++] = v; }
        for (int i = 0; i < nl; i++) { int v = leaves[i]; alive[v] = 0; cnt_alive--; for (int j = 0; j < s; j++) { int u = cmem[c][j]; if (alive[u] && adjw[v][u]) deg[u]--; } }
    }
    int centers[2], nc = 0;
    for (int i = 0; i < s; i++) if (alive[cmem[c][i]]) centers[nc++] = cmem[c][i];
    if (nc == 1) { char t[1024]; canon_rec(centers[0], -1, t); snprintf(out, 2048, "C%s", t); }
    else {
        char t1[1024], t2[1024]; canon_rec(centers[0], centers[1], t1); canon_rec(centers[1], centers[0], t2);
        if (strcmp(t1, t2) > 0) { char tt[1024]; strcpy(tt, t1); strcpy(t1, t2); strcpy(t2, tt); }
        snprintf(out, 2048, "B%03d%s%s", adjw[centers[0]][centers[1]], t1, t2);
    }
}

static void report_witness(void) {
    printf("WITNESS n=%d k=%d edges:", n, k);
    for (int i = 0; i < nedges; i++) printf(" (%d,%d,%d)", eu[i], ev[i], ew[i]);
    printf("\n"); fflush(stdout);
}

static void rec(int x, int q_prev) {
    if (found) return;
    nodes++;
    int m = mex();
    if (m > k) {
        found = 1;
        int ids[MAXN], cm = 0;
        for (int c = 0; c < n; c++) if (csize[c] > 0) ids[cm++] = c;
        for (int i = 1; i < cm; i++) { eu[nedges] = cmem[ids[0]][0]; ev[nedges] = cmem[ids[i]][0]; ew[nedges] = 1000 + i; nedges++; }
        report_witness();
        nedges -= (cm - 1);
        return;
    }
    if (ncomp == 1) return;
    if (use_parity && !parity_ok()) { pruned_parity++; return; }
    if (use_block) {
        if (ncomp <= CMAX_EXACT) { if (!few_component_check(q_prev, B - x)) { pruned_block++; return; } }
        else {
            u128 cover = maskk;
            int lb = block_bound(q_prev, B - x, &cover);
            if (x + lb > B) { pruned_block++; return; }
            if (use_hall && (uncov & ~cover) != 0) { pruned_hall++; return; }
        }
    }
    if (split_depth >= 0 && nedges == split_depth) {
        long long id = prefix_counter++;
        if (id % nworkers != worker) return;
    }
    /* candidate components: first of each isomorphism class */
    int cand[MAXN], nc = 0;
    if (use_sym) {
        int ids[MAXN], m2 = 0;
        for (int c = 0; c < n; c++) if (csize[c] > 0) ids[m2++] = c;
        for (int i = 0; i < m2; i++) canon_component(ids[i], cbuf[ids[i]]);
        /* class representatives: first with each string; but pairs within a class need the first two */
        int used[MAXN] = {0};
        for (int i = 0; i < m2; i++) {
            int c = ids[i];
            int rep = -1, second = -1;
            for (int j = 0; j < i; j++) if (!strcmp(cbuf[ids[j]], cbuf[c])) { if (rep < 0) rep = ids[j]; else if (second < 0) second = ids[j]; }
            if (rep < 0) { cand[nc++] = c; used[c] = 1; }
            else if (second < 0) { cand[nc++] = c; used[c] = 2; }
        }
    } else {
        for (int c = 0; c < n; c++) if (csize[c] > 0) cand[nc++] = c;
    }
    int use_cands = (use_block && ncomp <= CMAX_EXACT);
    if (use_cands) for (int i = 0; i < npairs_e; i++) if (ncand[i] < 0) use_cands = 0;
    if (use_cands) {
        /* class-representative filter on pairs, as below */
        for (int t = 0; t < npairs_e && !found; t++) {
            int ci = pair_ci[t], cj = pair_cj[t];
            int ok = 0;
            for (int a = 0; a < nc && !ok; a++) for (int b = a + 1; b < nc && !ok; b++) if (cand[a] == ci && cand[b] == cj) ok = 1;
            if (!ok) continue;
            if (use_sym) {
                int same = !strcmp(cbuf[ci], cbuf[cj]);
                if (!same) {
                    int fi = 1, fj = 1;
                    for (int c = 0; c < ci; c++) if (csize[c] > 0 && !strcmp(cbuf[c], cbuf[ci])) fi = 0;
                    for (int c = 0; c < cj; c++) if (csize[c] > 0 && !strcmp(cbuf[c], cbuf[cj])) fj = 0;
                    if (!fi || !fj) continue;
                }
            }
            int si = csize[ci], sj = csize[cj];
            int qmax = m;
            if (use_wbound) { int li = si * (n - si), lj = sj * (n - sj); int load = li < lj ? li : lj; int wb = k + 1 + B - load; if (wb < qmax) qmax = wb; }
            for (int c2 = 0; c2 < ncand[t] && !found; c2++) {
                cand_t *cd = &candbuf[t][c2];
                int q = cd->L;
                if (q < q_prev || q > qmax) continue;
                int ex = cd->ex;
                if (x + ex > B) continue;
                int u = cd->p, v = cd->pp;
                u128 addmask = cd->mask;
                uncov &= ~addmask;
                int old_si = si;
                for (int xx = 0; xx < si; xx++) for (int yy = 0; yy < sj; yy++) {
                    int d = dist[cmem[ci][xx]][u] + q + dist[v][cmem[cj][yy]];
                    dist[cmem[ci][xx]][cmem[cj][yy]] = d; dist[cmem[cj][yy]][cmem[ci][xx]] = d;
                }
                for (int yy = 0; yy < sj; yy++) cmem[ci][si + yy] = cmem[cj][yy];
                csize[ci] = si + sj; csize[cj] = 0; ncomp--;
                adjw[u][v] = adjw[v][u] = q;
                eu[nedges] = u; ev[nedges] = v; ew[nedges] = q; nedges++;
                rec(x + ex, q);
                nedges--;
                adjw[u][v] = adjw[v][u] = 0;
                ncomp++; csize[cj] = sj; csize[ci] = old_si;
                for (int xx = 0; xx < old_si; xx++) for (int yy = 0; yy < sj; yy++) {
                    dist[cmem[ci][xx]][cmem[cj][yy]] = -1; dist[cmem[cj][yy]][cmem[ci][xx]] = -1;
                }
                uncov |= addmask;
            }
        }
        return;
    }
    for (int q = q_prev; q <= m && !found; q++) {
        for (int a = 0; a < nc && !found; a++) for (int b = a + 1; b < nc && !found; b++) {
            int ci = cand[a], cj = cand[b];
            if (use_sym) {
                /* skip pairs of two "second" representatives, or second-of-class with a different class's first? no:
                   allowed: (first_X, first_Y) for X != Y; (first_X, second_X). Disallow (second_X, first_Y) and (second_X, second_Y). */
                int same = !strcmp(cbuf[ci], cbuf[cj]);
                if (!same) {
                    /* require both to be firsts */
                    int fi = 1, fj = 1;
                    for (int c = 0; c < ci; c++) if (csize[c] > 0 && !strcmp(cbuf[c], cbuf[ci])) fi = 0;
                    for (int c = 0; c < cj; c++) if (csize[c] > 0 && !strcmp(cbuf[c], cbuf[cj])) fj = 0;
                    if (!fi || !fj) continue;
                }
            }
            int si = csize[ci], sj = csize[cj];
            if (use_wbound) {
                int li = si * (n - si), lj = sj * (n - sj);
                int load = li < lj ? li : lj;
                if (q > k + 1 + B - load) continue;
            }
            for (int pi = 0; pi < si && !found; pi++) for (int pj = 0; pj < sj && !found; pj++) {
                int u = cmem[ci][pi], v = cmem[cj][pj];
                int ex = 0;
                u128 addmask = 0;
                for (int xx = 0; xx < si; xx++) for (int yy = 0; yy < sj; yy++) {
                    int d = dist[cmem[ci][xx]][u] + q + dist[v][cmem[cj][yy]];
                    if (d > k || !((uncov >> d) & 1)) ex++; else { uncov &= ~(ONE << d); addmask |= ONE << d; }
                }
                if (x + ex <= B) {
                    int old_si = si;
                    for (int xx = 0; xx < si; xx++) for (int yy = 0; yy < sj; yy++) {
                        int d = dist[cmem[ci][xx]][u] + q + dist[v][cmem[cj][yy]];
                        dist[cmem[ci][xx]][cmem[cj][yy]] = d; dist[cmem[cj][yy]][cmem[ci][xx]] = d;
                    }
                    for (int yy = 0; yy < sj; yy++) cmem[ci][si + yy] = cmem[cj][yy];
                    csize[ci] = si + sj; csize[cj] = 0; ncomp--;
                    adjw[u][v] = adjw[v][u] = q;
                    eu[nedges] = u; ev[nedges] = v; ew[nedges] = q; nedges++;
                    rec(x + ex, q);
                    nedges--;
                    adjw[u][v] = adjw[v][u] = 0;
                    ncomp++; csize[cj] = sj; csize[ci] = old_si;
                    for (int xx = 0; xx < old_si; xx++) for (int yy = 0; yy < sj; yy++) {
                        dist[cmem[ci][xx]][cmem[cj][yy]] = -1; dist[cmem[cj][yy]][cmem[ci][xx]] = -1;
                    }
                }
                uncov |= addmask;
            }
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s n k [split_depth worker nworkers] [-nb] [-np] [-ns] [-nw] [-nh]\n", argv[0]); return 1; }
    n = atoi(argv[1]); k = atoi(argv[2]);
    int ai = 3;
    if (argc >= 6 && argv[3][0] != '-') { split_depth = atoi(argv[3]); worker = atoi(argv[4]); nworkers = atoi(argv[5]); ai = 6; }
    for (; ai < argc; ai++) {
        if (!strcmp(argv[ai], "-nb")) use_block = 0; if (!strcmp(argv[ai], "-np")) use_parity = 0;
        if (!strcmp(argv[ai], "-ns")) use_sym = 0; if (!strcmp(argv[ai], "-nw")) use_wbound = 0; if (!strcmp(argv[ai], "-nh")) use_hall = 0; if (!strcmp(argv[ai], "-ne")) use_exact = 0; if (!strncmp(argv[ai], "-rem", 4)) exact_rem_max = atoi(argv[ai]+4); if (!strncmp(argv[ai], "-prod", 5)) prod_cap = atof(argv[ai]+5);
    }
    if (k > MAXK) { fprintf(stderr, "k too large\n"); return 1; }
    N = n * (n - 1) / 2; B = N - k;
    if (B < 0) { printf("RESULT n=%d k=%d found=0 (k > N)\n", n, k); return 0; }
    int odd_needed = (k + 1) / 2, even_needed = k / 2;
    for (int a = 0; a <= n; a++) {
        int ab = a * (n - a);
        allowed_a[a] = (ab >= odd_needed && ab <= odd_needed + B && (N - ab) >= even_needed && (N - ab) <= even_needed + B);
    }
    for (int i = 0; i < n; i++) { for (int j = 0; j < n; j++) { dist[i][j] = (i == j) ? 0 : -1; adjw[i][j] = 0; } csize[i] = 1; cmem[i][0] = i; }
    ncomp = n;
    maskk = 0; for (int d = 1; d <= k; d++) maskk |= ONE << d;
    uncov = maskk;
    clock_t t0 = clock();
    rec(0, 1);
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("RESULT n=%d k=%d B=%d worker=%d/%d split=%d found=%d nodes=%lld pruned_parity=%lld pruned_block=%lld pruned_hall=%lld pruned_exact=%lld exact_capped=%lld secs=%.2f\n",
           n, k, B, worker, nworkers, split_depth, found, nodes, pruned_parity, pruned_block, pruned_hall, pruned_exact, exact_capped, secs);
    return 0;
}
