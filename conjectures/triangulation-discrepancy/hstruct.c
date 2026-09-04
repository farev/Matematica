/* hstruct.c — enumeration of counterexample candidates to the refined discrepancy bound at
 * n = 6m+5 with exactly h high-degree big-class vertices, parametrised by T' = T - D:
 *
 *   If T is a counterexample with big class V1 = D u H (|D| = 3m+2-h degree-3 vertices, |H| = h
 *   vertices of degree in [5, 2m+2] with sum(deg-3) <= 2m-1), then T' = T - D is a triangulation on
 *   3m+3+h vertices in which H is an independent set with those degrees, G = T' - H is the plane
 *   graph of NOTE Lemma 5 (its faces: the h links of H, and the faces of T' not incident to H,
 *   which are the D-triangles and the empty triangles), G has an equitable proper 3-colouring,
 *   every vertex of G lies on an empty triangle, and every link of H shows all three colour pairs.
 *
 * Input: plantri triangulations on 3m+3+h vertices (planar_code) on stdin.
 * For each T': enumerate independent h-sets H with the degree constraints; delete them to get G;
 * enumerate equitable 3-colourings; choose the empty triangles among the faces of G not incident
 * to H (exactly 3m+2-h occupied), covering every vertex; check fully mixed links; build T (= T'
 * plus one vertex in each occupied triangle) and compute disc(T) exactly. Reports any T with
 * disc > 2m-1, and whether each candidate admits a single flip (NOTE Lemma 7).
 *
 * Usage: plantri <3m+3+h> | ./hstruct m h
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXV 32
#define MAXN 72
#define MAXF 96

static int m, h, nTp, nW, n;
static int adjTp[MAXV][MAXV], degTp[MAXV];    /* T' rotation system */
static int adjW[MAXV][MAXV], degW[MAXV];      /* G = T' - H, rotation system, vertices relabelled 0..nW-1 */
static int mapW[MAXV];                        /* T' vertex -> G index or -1 */
static int isH[MAXV];
static int nfG, faceLen[MAXF], faceV[MAXF][MAXV];
static int col3[MAXV];

static int adjT[MAXN][MAXN], degT[MAXN];
static int nfT, faceT[MAXF][3], vfaceT[MAXN][MAXN], nvfT[MAXN];
static int colT[MAXN], orderT[MAXN], target_r, cnt_r, cnt_b;

static long long stat_graphs, stat_hsets, stat_facefilter, stat_col, stat_cand, stat_fullymixed, stat_noflip, stat_nosafe;
static int maxdisc_seen = -1;

static int read_graph(FILE *f) {
    int c = fgetc(f);
    if (c == EOF) return 0;
    nTp = c;
    for (int v = 0; v < nTp; v++) {
        degTp[v] = 0;
        for (;;) {
            int u = fgetc(f);
            if (u == EOF) return 0;
            if (u == 0) break;
            adjTp[v][degTp[v]++] = u - 1;
        }
    }
    return 1;
}

static int build_faces_G(void) {
    static char seen[MAXV][MAXV];
    memset(seen, 0, sizeof seen);
    nfG = 0;
    for (int v = 0; v < nW; v++) for (int i = 0; i < degW[v]; i++) {
        if (seen[v][i]) continue;
        int a = v, ai = i, len = 0;
        for (;;) {
            seen[a][ai] = 1;
            int b = adjW[a][ai];
            if (len >= MAXV) return 0;
            faceV[nfG][len++] = a;
            int j = 0; while (adjW[b][j] != a) j++;
            int jn = (j + degW[b] - 1) % degW[b];
            a = b; ai = jn;
            if (a == v && ai == i) break;
        }
        for (int x = 0; x < len; x++) for (int y = x + 1; y < len; y++)
            if (faceV[nfG][x] == faceV[nfG][y]) return 0;
        faceLen[nfG] = len;
        nfG++;
        if (nfG >= MAXF) return 0;
    }
    return 1;
}

/* ---- disc(T) ---- */
static int occupied[MAXF];
static void build_T(void) {
    n = nW;
    for (int v = 0; v < nW; v++) { degT[v] = degW[v]; memcpy(adjT[v], adjW[v], sizeof(int) * degW[v]); }
    for (int f = 0; f < nfG; f++) if (occupied[f]) {
        int x = n++;
        degT[x] = 0;
        for (int k = 0; k < faceLen[f]; k++) adjT[x][degT[x]++] = faceV[f][k];
        for (int k = 0; k < faceLen[f]; k++) { int a = faceV[f][k]; adjT[a][degT[a]++] = x; }
    }
    nfT = 0;
    for (int v = 0; v < n; v++) nvfT[v] = 0;
    int x = nW;
    for (int f = 0; f < nfG; f++) {
        if (!occupied[f]) { faceT[nfT][0] = faceV[f][0]; faceT[nfT][1] = faceV[f][1]; faceT[nfT][2] = faceV[f][2]; nfT++; }
        else {
            for (int k = 0; k < faceLen[f]; k++) { faceT[nfT][0] = x; faceT[nfT][1] = faceV[f][k]; faceT[nfT][2] = faceV[f][(k + 1) % faceLen[f]]; nfT++; }
            x++;
        }
    }
    for (int f = 0; f < nfT; f++) for (int k = 0; k < 3; k++) { int v = faceT[f][k]; vfaceT[v][nvfT[v]++] = f; }
}
static int ok_assign(int v, int c) {
    for (int k = 0; k < nvfT[v]; k++) {
        int *fc = faceT[vfaceT[v][k]];
        int x = -1, y = -1;
        for (int t = 0; t < 3; t++) if (fc[t] != v) { if (x < 0) x = fc[t]; else y = fc[t]; }
        if (colT[x] == c && colT[y] == c) return 0;
    }
    return 1;
}
static int search(int idx) {
    if (cnt_r > target_r || cnt_b > n - target_r) return 0;
    if (idx == n) return cnt_r == target_r;
    int v = orderT[idx];
    for (int c = 0; c < 2; c++) {
        if (c == 0 && cnt_r == target_r) continue;
        if (c == 1 && cnt_b == n - target_r) continue;
        if (!ok_assign(v, c)) continue;
        colT[v] = c; if (c == 0) cnt_r++; else cnt_b++;
        if (search(idx + 1)) return 1;
        colT[v] = -1; if (c == 0) cnt_r--; else cnt_b--;
    }
    return 0;
}
static int disc_T(void) {
    int seen[MAXN] = {0}, q[MAXN], qh = 0, qt = 0; q[qt++] = 0; seen[0] = 1;
    while (qh < qt) { int v = q[qh++]; for (int i = 0; i < degT[v]; i++) { int u = adjT[v][i]; if (!seen[u]) { seen[u] = 1; q[qt++] = u; } } }
    if (qt != n) { fprintf(stderr, "T disconnected?!\n"); exit(3); }
    for (int i = 0; i < n; i++) orderT[i] = q[i];
    for (int d = n % 2; d <= n; d += 2) {
        for (int v = 0; v < n; v++) colT[v] = -1;
        target_r = (n - d) / 2; cnt_r = cnt_b = 0;
        if (search(0)) return d;
    }
    return -1;
}

/* ---- Lemma 7 single flip / safe flip ---- */
static int single_flip_exists(void) {
    for (int F = 0; F < 3; F++) for (int S = 0; S < 3; S++) {
        if (S == F) continue;
        int B = 3 - F - S;
        for (int u = 0; u < nW; u++) {
            if (col3[u] != F) continue;
            int occ = 0, p = 0, q = 0, blocked = 0;
            for (int f = 0; f < nfG && !blocked; f++) {
                if (!occupied[f]) continue;
                int L = faceLen[f];
                if (L == 3) { for (int k = 0; k < 3; k++) if (faceV[f][k] == u) occ++; continue; }
                int pos = -1;
                for (int k = 0; k < L; k++) if (faceV[f][k] == u) pos = k;
                int adjS = 0, fbElsewhere = 0, fbAny = 0;
                if (pos >= 0) {
                    int pc = col3[faceV[f][(pos + L - 1) % L]], nc = col3[faceV[f][(pos + 1) % L]];
                    if (pc == S || nc == S) adjS = 1;
                }
                for (int k = 0; k < L; k++) {
                    int a = faceV[f][k], b = faceV[f][(k + 1) % L];
                    int ca = col3[a], cb = col3[b];
                    if ((ca == F && cb == B) || (ca == B && cb == F)) { fbAny = 1; if (a != u && b != u) fbElsewhere = 1; }
                }
                if (pos >= 0 && adjS) { q++; if (fbElsewhere) blocked = 1; }
                if (fbAny && !fbElsewhere) p++;
            }
            if (blocked) continue;
            if (occ + p >= 2 && occ + q <= 2 * m + 1) return 1;
        }
    }
    return 0;
}
static int safe_flip_exists(void) {
    for (int u = 0; u < nW; u++) {
        int occ = 0, onH = 0;
        for (int f = 0; f < nfG; f++) {
            if (!occupied[f]) continue;
            for (int k = 0; k < faceLen[f]; k++) if (faceV[f][k] == u) { if (faceLen[f] == 3) occ++; else onH = 1; }
        }
        if (!onH && occ >= 2 && occ <= 2 * m + 1) return 1;
    }
    return 0;
}

static void print_T(int d) {
    printf("COUNTEREXAMPLE? disc=%d n=%d m=%d h=%d ; G colouring:", d, n, m, h);
    for (int v = 0; v < nW; v++) printf(" %d", col3[v]);
    printf(" ; occupied faces:");
    for (int f = 0; f < nfG; f++) if (occupied[f]) { printf(" ("); for (int k = 0; k < faceLen[f]; k++) printf("%d%s", faceV[f][k], k + 1 < faceLen[f] ? "," : ""); printf(")"); }
    printf(" ; T adjacency:");
    for (int v = 0; v < n; v++) { printf(" |"); for (int i = 0; i < degT[v]; i++) printf(" %d", adjT[v][i]); }
    printf("\n"); fflush(stdout);
}

static void process_candidate(void) {
    for (int f = 0; f < nfG; f++) if (occupied[f] && faceLen[f] > 3) {
        int has[3] = {0, 0, 0};
        for (int k = 0; k < faceLen[f]; k++) { int a = col3[faceV[f][k]], b = col3[faceV[f][(k + 1) % faceLen[f]]]; has[3 - a - b] = 1; }
        if (!(has[0] && has[1] && has[2])) return;
    }
    stat_fullymixed++;
    int flip = single_flip_exists();
    if (!flip) { stat_noflip++; }
    if (!safe_flip_exists()) stat_nosafe++;
    build_T();
    int d = disc_T();
    if (d > maxdisc_seen) maxdisc_seen = d;
    if (d > 2 * m - 1) print_T(d);
    else if (!flip) { printf("no-flip candidate with disc=%d: ", d); print_T(d); }
}

static int triFaces[MAXF], nTri, needEmpty, coverCnt[MAXV];
static void choose_empty(int idx, int chosen) {
    if (chosen == needEmpty) {
        for (int v = 0; v < nW; v++) if (coverCnt[v] == 0) return;
        stat_cand++; process_candidate(); return;
    }
    if (idx == nTri) return;
    if (nTri - idx < needEmpty - chosen) return;
    int f = triFaces[idx];
    occupied[f] = 0; for (int k = 0; k < 3; k++) coverCnt[faceV[f][k]]++;
    choose_empty(idx + 1, chosen + 1);
    for (int k = 0; k < 3; k++) coverCnt[faceV[f][k]]--; occupied[f] = 1;
    choose_empty(idx + 1, chosen);
}

static int classCnt[3];
static void colour_rec(int v, int maxUsed) {
    if (v == nW) {
        if (classCnt[0] != m + 1 || classCnt[1] != m + 1 || classCnt[2] != m + 1) return;
        stat_col++;
        for (int f = 0; f < nfG; f++) occupied[f] = 1;
        memset(coverCnt, 0, sizeof coverCnt);
        choose_empty(0, 0);
        return;
    }
    int lim = maxUsed + 1 < 2 ? maxUsed + 1 : 2;
    for (int c = 0; c <= lim; c++) {
        if (classCnt[c] >= m + 1) continue;
        int ok = 1;
        for (int i = 0; i < degW[v] && ok; i++) { int u = adjW[v][i]; if (u < v && col3[u] == c) ok = 0; }
        if (!ok) continue;
        col3[v] = c; classCnt[c]++;
        colour_rec(v + 1, c > maxUsed ? c : maxUsed);
        classCnt[c]--;
    }
}

static int Hset[MAXV];
static void process_Hset(void) {
    stat_hsets++;
    /* G = T' - H */
    nW = 0;
    for (int v = 0; v < nTp; v++) mapW[v] = isH[v] ? -1 : nW++;
    for (int v = 0; v < nTp; v++) {
        if (isH[v]) continue;
        int g = mapW[v]; degW[g] = 0;
        for (int i = 0; i < degTp[v]; i++) { int u = adjTp[v][i]; if (!isH[u]) adjW[g][degW[g]++] = mapW[u]; }
        if (degW[g] < 2) return;
    }
    if (!build_faces_G()) return;
    /* face filter: non-triangular faces must be exactly h faces of length in [5, 2m+2] (the links) */
    int hh = 0; nTri = 0;
    for (int f = 0; f < nfG; f++) {
        if (faceLen[f] == 3) triFaces[nTri++] = f;
        else if (faceLen[f] == 4 || faceLen[f] > 2 * m + 2) return;
        else hh++;
    }
    if (hh != h) return;
    needEmpty = nfG - (3 * m + 2);
    if (needEmpty < m + 1 || needEmpty > nTri) return;
    stat_facefilter++;
    classCnt[0] = classCnt[1] = classCnt[2] = 0;
    colour_rec(0, -1);
}

/* choose independent h-sets of vertices with degree in [5, 2m+2] and sum(deg-3) <= 2m-1 */
static void choose_H(int start, int chosen, int excess) {
    if (chosen == h) { process_Hset(); return; }
    for (int v = start; v < nTp; v++) {
        int d = degTp[v];
        if (d < 5 || d > 2 * m + 2) continue;
        if (excess + d - 3 > 2 * m - 1) continue;
        int ok = 1;
        for (int i = 0; i < degTp[v] && ok; i++) if (isH[adjTp[v][i]]) ok = 0;
        if (!ok) continue;
        isH[v] = 1; Hset[chosen] = v;
        choose_H(v + 1, chosen + 1, excess + d - 3);
        isH[v] = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: hstruct m h\n"); return 2; }
    m = atoi(argv[1]); h = atoi(argv[2]);
    char hdr[16]; if (fread(hdr, 1, 15, stdin) != 15 || strncmp(hdr, ">>planar_code<<", 15)) { fprintf(stderr, "bad header\n"); return 2; }
    while (read_graph(stdin)) {
        stat_graphs++;
        if (nTp != 3 * m + 3 + h) { fprintf(stderr, "wrong vertex count %d (expected %d)\n", nTp, 3 * m + 3 + h); return 2; }
        memset(isH, 0, sizeof isH);
        choose_H(0, 0, 0);
    }
    fprintf(stderr, "m=%d h=%d n=%d: T' read %lld; independent H-sets with the degree constraints %lld; passing face filter %lld; equitable colourings %lld; candidates %lld; fully mixed %lld; without single flip %lld; without safe flip %lld; max disc %d; bound U=%d\n",
            m, h, 6 * m + 5, stat_graphs, stat_hsets, stat_facefilter, stat_col, stat_cand, stat_fullymixed, stat_noflip, stat_nosafe, maxdisc_seen, 2 * m - 1);
    return 0;
}
