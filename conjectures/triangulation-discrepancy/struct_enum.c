/* struct_enum.c — structural enumeration of potential counterexamples to the refined
 * discrepancy bound disc(T) <= n - 2*ceil((n+2)/3) = 2m-1 at n = 6m+5 (Basti–Cremaschi's open
 * residue class), via the reduction lemmas of NOTE.md:
 *
 *   A counterexample T has a proper 4-colouring with classes (3m+2, m+1, m+1, m+1); with V1 the
 *   big class and W the rest, G = T[W] is a 2-connected plane graph on 3m+3 vertices, properly
 *   3-coloured with classes of size m+1, whose faces are: 3m+2 "occupied" faces (one per V1
 *   vertex, of length deg(v) in {3} u [5, 2m+2]) and empty triangles; every vertex of G lies on an
 *   empty triangle (Lemma "no W-face" ), every occupied face's boundary carries all three colour
 *   pairs (Lemma "plain merge"), and the number h of non-triangular occupied faces satisfies
 *   sum(len-3) <= 2m-1.  Conversely T is recovered from (G, occupied faces) by inserting one vertex
 *   in each occupied face.
 *
 * Input: plantri planar_code on stdin, from  plantri -p -c2 -e<lo>:<hi> -f<2m+2> <3m+3>
 * (all 2-connected plane simple graphs with those edge counts; all embeddings).
 * For each G: enumerate equitable proper 3-colourings (canonical under colour permutation),
 * then all choices of the empty-triangle set covering every vertex, build T, check the
 * fully-mixed condition, and compute disc(T) exactly (backtracking as in disc.c).
 * Reports every T with disc > 2m-1 (a counterexample), and statistics.
 *
 * Usage: plantri ... | ./struct_enum m [-v]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXW 24
#define MAXN 64
#define MAXF 64

static int m, nW, n;                       /* n = 6m+5 vertices of T */
static int adjW[MAXW][MAXW], degW[MAXW];   /* G, rotation system */
static int nfG, faceLen[MAXF], faceV[MAXF][MAXW];
static int col3[MAXW];

/* T structures */
static int adjT[MAXN][MAXN], degT[MAXN];
static int nfT, faceT[MAXF][3], vfaceT[MAXN][MAXN], nvfT[MAXN];
static int colT[MAXN], orderT[MAXN], target_r, cnt_r, cnt_b;
static long long nodes;

static long long stat_graphs, stat_col, stat_cand, stat_fullymixed, stat_h[8];
static int maxdisc_seen = -1;
static int verbose = 0;

static int read_graph(FILE *f) {
    int c = fgetc(f);
    if (c == EOF) return 0;
    nW = c;
    for (int v = 0; v < nW; v++) {
        degW[v] = 0;
        for (;;) {
            int u = fgetc(f);
            if (u == EOF) return 0;
            if (u == 0) break;
            adjW[v][degW[v]++] = u - 1;
        }
    }
    return 1;
}

/* faces of G: dart (v -> adjW[v][i]); next dart of face: at b = adjW[v][i], take the
   neighbour preceding v in b's rotation (same convention as disc.c, verified on Table 2) */
static int build_faces_G(void) {
    static char seen[MAXW][MAXW];
    memset(seen, 0, sizeof seen);
    nfG = 0;
    for (int v = 0; v < nW; v++) for (int i = 0; i < degW[v]; i++) {
        if (seen[v][i]) continue;
        int a = v, ai = i, len = 0;
        for (;;) {
            seen[a][ai] = 1;
            int b = adjW[a][ai];
            if (len >= MAXW) return 0;
            faceV[nfG][len++] = a;
            int j = 0; while (adjW[b][j] != a) j++;
            int jn = (j + degW[b] - 1) % degW[b];
            a = b; ai = jn;
            if (a == v && ai == i) break;
        }
        /* a face boundary must be a cycle with distinct vertices (2-connectedness) */
        for (int x = 0; x < len; x++) for (int y = x + 1; y < len; y++)
            if (faceV[nfG][x] == faceV[nfG][y]) return 0;
        faceLen[nfG] = len;
        nfG++;
        if (nfG >= MAXF) return 0;
    }
    return 1;
}

/* ---- disc(T) computation (as disc.c) ---- */
static void build_T(const int *occupied) {
    /* vertices 0..nW-1 = W, then one vertex per occupied face (in face order) */
    n = nW;
    for (int v = 0; v < nW; v++) { degT[v] = degW[v]; memcpy(adjT[v], adjW[v], sizeof(int) * degW[v]); }
    for (int f = 0; f < nfG; f++) if (occupied[f]) {
        int x = n++;
        degT[x] = 0;
        for (int k = 0; k < faceLen[f]; k++) adjT[x][degT[x]++] = faceV[f][k];
        /* insert x into the rotation of each boundary vertex between its two face-neighbours:
           for boundary vertex a = faceV[f][k], the face dart is a -> faceV[f][k+1]; x is inserted
           right after that dart... rotation order does not matter for the disc computation (only
           the face list does), so we simply append. */
        for (int k = 0; k < faceLen[f]; k++) { int a = faceV[f][k]; adjT[a][degT[a]++] = x; }
    }
    /* faces of T: empty triangles of G (as is) + for each occupied face f with inserted x: triangles (x, a_k, a_{k+1}) */
    nfT = 0;
    for (int v = 0; v < n; v++) nvfT[v] = 0;
    int x = nW;
    for (int f = 0; f < nfG; f++) {
        if (!occupied[f]) {
            faceT[nfT][0] = faceV[f][0]; faceT[nfT][1] = faceV[f][1]; faceT[nfT][2] = faceV[f][2]; nfT++;
        } else {
            for (int k = 0; k < faceLen[f]; k++) {
                faceT[nfT][0] = x; faceT[nfT][1] = faceV[f][k]; faceT[nfT][2] = faceV[f][(k + 1) % faceLen[f]]; nfT++;
            }
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
    nodes++;
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
    /* BFS order from vertex 0 */
    int seen[MAXN] = {0}, q[MAXN], qh = 0, qt = 0; q[qt++] = 0; seen[0] = 1;
    while (qh < qt) { int v = q[qh++]; for (int i = 0; i < degT[v]; i++) { int u = adjT[v][i]; if (!seen[u]) { seen[u] = 1; q[qt++] = u; } } }
    if (qt != n) { fprintf(stderr, "T disconnected?!\n"); exit(3); }
    for (int i = 0; i < n; i++) orderT[i] = q[i];
    for (int d = n % 2; d <= n; d += 2) {
        for (int v = 0; v < n; v++) colT[v] = -1;
        target_r = (n - d) / 2; cnt_r = cnt_b = 0; nodes = 0;
        if (search(0)) return d;
    }
    return -1;
}

/* ---- enumeration of empty-face sets ---- */
static int triFaces[MAXF], nTri, occupied[MAXF], needEmpty;
static int coverCnt[MAXW];

static void print_T_ascii(int d) {
    printf("COUNTEREXAMPLE? disc=%d n=%d m=%d ; G colouring:", d, n, m);
    for (int v = 0; v < nW; v++) printf(" %d", col3[v]);
    printf(" ; occupied faces:");
    for (int f = 0; f < nfG; f++) if (occupied[f]) { printf(" ("); for (int k = 0; k < faceLen[f]; k++) printf("%d%s", faceV[f][k], k + 1 < faceLen[f] ? "," : ""); printf(")"); }
    printf(" ; T adjacency:");
    for (int v = 0; v < n; v++) { printf(" |"); for (int i = 0; i < degT[v]; i++) printf(" %d", adjT[v][i]); }
    printf("\n"); fflush(stdout);
}

static void process_candidate(void) {
    /* fully-mixed check on occupied faces: boundary colour sequence must contain all three pairs */
    for (int f = 0; f < nfG; f++) if (occupied[f]) {
        int has[3] = {0, 0, 0};   /* pair index: (0,1)->2, (0,2)->1, (1,2)->0  i.e. index = 3 - a - b */
        for (int k = 0; k < faceLen[f]; k++) {
            int a = col3[faceV[f][k]], b = col3[faceV[f][(k + 1) % faceLen[f]]];
            has[3 - a - b] = 1;
        }
        if (!(has[0] && has[1] && has[2])) return;
    }
    stat_fullymixed++;
    build_T(occupied);
    int d = disc_T();
    if (d > maxdisc_seen) maxdisc_seen = d;
    if (d > 2 * m - 1) print_T_ascii(d);
    else if (verbose) { printf("candidate disc=%d\n", d); }
}

static void choose_empty(int idx, int chosen) {
    if (chosen == needEmpty) {
        for (int v = 0; v < nW; v++) if (coverCnt[v] == 0) return;
        stat_cand++;
        process_candidate();
        return;
    }
    if (idx == nTri) return;
    if (nTri - idx < needEmpty - chosen) return;
    /* option 1: face triFaces[idx] is empty */
    int f = triFaces[idx];
    occupied[f] = 0;
    for (int k = 0; k < 3; k++) coverCnt[faceV[f][k]]++;
    choose_empty(idx + 1, chosen + 1);
    for (int k = 0; k < 3; k++) coverCnt[faceV[f][k]]--;
    occupied[f] = 1;
    /* option 2: occupied */
    choose_empty(idx + 1, chosen);
}

/* ---- equitable proper 3-colourings, canonical: vertex 0 gets 0, first non-0 colour is 1 ---- */
static int classCnt[3];
static void colour_rec(int v, int maxUsed) {
    if (v == nW) {
        if (classCnt[0] != m + 1 || classCnt[1] != m + 1 || classCnt[2] != m + 1) return;
        stat_col++;
        /* enumerate empty sets */
        for (int f = 0; f < nfG; f++) occupied[f] = 1;
        memset(coverCnt, 0, sizeof coverCnt);
        choose_empty(0, 0);
        return;
    }
    for (int c = 0; c <= (maxUsed + 1 < 2 ? maxUsed + 1 : 2); c++) {
        if (classCnt[c] >= m + 1) continue;
        int ok = 1;
        for (int i = 0; i < degW[v] && ok; i++) { int u = adjW[v][i]; if (u < v && col3[u] == c) ok = 0; }
        if (!ok) continue;
        col3[v] = c; classCnt[c]++;
        colour_rec(v + 1, c > maxUsed ? c : maxUsed);
        classCnt[c]--;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: struct_enum m [-v]\n"); return 2; }
    m = atoi(argv[1]); verbose = argc > 2;
    char hdr[16]; if (fread(hdr, 1, 15, stdin) != 15 || strncmp(hdr, ">>planar_code<<", 15)) { fprintf(stderr, "bad header\n"); return 2; }
    while (read_graph(stdin)) {
        stat_graphs++;
        if (nW != 3 * m + 3) { fprintf(stderr, "wrong vertex count %d\n", nW); return 2; }
        if (!build_faces_G()) continue;             /* not 2-connected-like: skip (cannot be T[W]) */
        /* face constraints */
        int h = 0, excess = 0, ok = 1;
        nTri = 0;
        for (int f = 0; f < nfG; f++) {
            if (faceLen[f] == 3) triFaces[nTri++] = f;
            else if (faceLen[f] == 4 || faceLen[f] > 2 * m + 2) { ok = 0; break; }
            else { h++; excess += faceLen[f] - 3; }
        }
        if (!ok || h > m - 1 || excess > 2 * m - 1) continue;
        needEmpty = nfG - (3 * m + 2);
        if (needEmpty < m + 1 || needEmpty > nTri) continue;
        stat_h[h]++;
        classCnt[0] = classCnt[1] = classCnt[2] = 0;
        colour_rec(0, -1);
    }
    fprintf(stderr, "m=%d n=%d: graphs read %lld; passing face filter by h: %lld %lld %lld %lld; equitable colourings %lld; candidates (empty sets covering) %lld; fully mixed %lld; max disc seen %d; bound U=%d\n",
            m, 6 * m + 5, stat_graphs, stat_h[0], stat_h[1], stat_h[2], stat_h[3], stat_col, stat_cand, stat_fullymixed, maxdisc_seen, 2 * m - 1);
    return 0;
}
