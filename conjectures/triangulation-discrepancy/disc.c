/* disc.c — exact minimum discrepancy of polychromatic red-blue vertex colourings of plane
 * triangulations read in plantri's planar_code (binary, header ">>planar_code<<").
 * A colouring is polychromatic iff no facial triangle is monochromatic.
 * disc(T) = min over polychromatic colourings of | |R| - |B| |.
 * Method: for each target red-count r (ordered by |2r-n| ascending, one of each complementary
 * pair, i.e. r <= n/2 ... actually we test r from floor(n/2) downwards; complement symmetry
 * means testing |R| = r covers |R| = n-r), a backtracking search assigns vertices in a fixed
 * order with (a) monochromatic-face pruning (a face with two assigned same-coloured vertices
 * forces the third), and (b) counting bounds. Vertex 0 is fixed red (colour exchange).
 * Output: per graph "disc" (or with -h: histogram only). Usage: plantri -T n | ./disc [-q]
 * Also prints, at the end, histogram of disc values and the number of graphs.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 32
#define MAXF 64
static int n, nf;
static int adj[MAXN][MAXN], deg[MAXN];        /* rotation system: adj[v][i] neighbours in cyclic order */
static int faces[MAXF][3];
static int vface[MAXN][MAXN], nvf[MAXN];       /* faces incident to v */
static int col[MAXN];                          /* -1 unassigned, 0 red, 1 blue */
static int order[MAXN];
static int target_r, cnt_r, cnt_b;
static long long nodes;

static int read_graph(FILE *f) {
    int c = fgetc(f);
    if (c == EOF) return 0;
    n = c;
    if (n == 0) return 0;
    for (int v = 0; v < n; v++) {
        deg[v] = 0;
        for (;;) {
            int u = fgetc(f);
            if (u == EOF) return 0;
            if (u == 0) break;
            adj[v][deg[v]++] = u - 1;
        }
    }
    return 1;
}

static void build_faces(void) {
    /* faces of the embedding: each face traced by (v, next-in-rotation rule). For a triangulation
       every face is a triangle: face (v, u, w) with u = adj[v][i], w = successor of v in rotation of u... */
    nf = 0;
    for (int v = 0; v < n; v++) nvf[v] = 0;
    static char seen[MAXN][MAXN];
    memset(seen, 0, sizeof seen);
    for (int v = 0; v < n; v++) for (int i = 0; i < deg[v]; i++) {
        if (seen[v][i]) continue;
        /* trace face starting with dart v -> adj[v][i] */
        int a = v, ai = i, len = 0, fv[8];
        for (;;) {
            seen[a][ai] = 1;
            int b = adj[a][ai];
            fv[len++] = a;
            /* find position of a in rotation of b, then take the previous neighbour (clockwise) */
            int j = 0; while (adj[b][j] != a) j++;
            int jn = (j + deg[b] - 1) % deg[b];   /* next dart of the face */
            a = b; ai = jn;
            if (a == v && ai == i) break;
            if (len > 6) { fprintf(stderr, "non-triangular face?\n"); exit(2); }
        }
        if (len != 3) { fprintf(stderr, "face of length %d (n=%d)\n", len, n); exit(2); }
        faces[nf][0] = fv[0]; faces[nf][1] = fv[1]; faces[nf][2] = fv[2];
        for (int k = 0; k < 3; k++) vface[fv[k]][nvf[fv[k]]++] = nf;
        nf++;
    }
}

/* check whether assigning colour c to v creates a monochromatic face */
static int ok_assign(int v, int c) {
    for (int k = 0; k < nvf[v]; k++) {
        int *fc = faces[vface[v][k]];
        int a = fc[0] == v ? fc[1] : fc[0];
        int b = (fc[2] == v || fc[2] == a) ? (fc[1] == v || fc[1] == a ? fc[0] : fc[1]) : fc[2];
        if (a == v) a = fc[2];
        /* robust: pick the two vertices other than v */
        int x = -1, y = -1;
        for (int t = 0; t < 3; t++) if (fc[t] != v) { if (x < 0) x = fc[t]; else y = fc[t]; }
        if (col[x] == c && col[y] == c) return 0;
    }
    return 1;
}

static int search(int idx) {
    nodes++;
    if (cnt_r > target_r || cnt_b > n - target_r) return 0;
    if (idx == n) return cnt_r == target_r;
    int v = order[idx];
    for (int c = 0; c < 2; c++) {
        if (c == 0 && cnt_r == target_r) continue;
        if (c == 1 && cnt_b == n - target_r) continue;
        if (!ok_assign(v, c)) continue;
        col[v] = c; if (c == 0) cnt_r++; else cnt_b++;
        if (search(idx + 1)) return 1;
        col[v] = -1; if (c == 0) cnt_r--; else cnt_b--;
    }
    return 0;
}

static int exists_with_red(int r) {
    for (int v = 0; v < n; v++) col[v] = -1;
    target_r = r; cnt_r = 0; cnt_b = 0;
    /* vertex 0 first, forced red is NOT valid when r counts matter; instead fix col[order[0]]=red and
       rely on complement symmetry: colourings with |R|=r <-> |B|=r. We test both r and n-r via symmetry:
       fixing vertex order[0] red and requiring |R| = r covers exactly the colourings with order[0] red;
       the complementary ones have |R| = n - r. So exists(|R|=r or |R|=n-r) = search(r) || search(n-r) with vertex fixed red.
       We simply do not fix any vertex: a plain search over both colours (factor 2 cost, negligible). */
    return search(0);
}

int main(int argc, char **argv) {
    int quiet = 0, dump = 1000;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-q")) quiet = 1;
        else if (!strcmp(argv[i], "-d") && i + 1 < argc) dump = atoi(argv[++i]);
    }
    /* header */
    char hdr[16]; if (fread(hdr, 1, 15, stdin) != 15 || strncmp(hdr, ">>planar_code<<", 15)) { fprintf(stderr, "bad header\n"); return 2; }
    long long count = 0, hist[MAXN + 1]; memset(hist, 0, sizeof hist);
    long long maxnodes = 0;
    while (read_graph(stdin)) {
        build_faces();
        /* order: BFS from vertex 0 for locality */
        int seen[MAXN] = {0}, q[MAXN], qh = 0, qt = 0; q[qt++] = 0; seen[0] = 1;
        while (qh < qt) { int v = q[qh++]; for (int i = 0; i < deg[v]; i++) { int u = adj[v][i]; if (!seen[u]) { seen[u] = 1; q[qt++] = u; } } }
        for (int i = 0; i < n; i++) order[i] = q[i];
        int d = -1;
        for (int disc = n % 2; disc <= n; disc += 2) {
            int r = (n - disc) / 2;              /* |R| = r, |B| = n - r, |B|-|R| = disc */
            nodes = 0;
            if (exists_with_red(r)) { d = disc; if (nodes > maxnodes) maxnodes = nodes; break; }
            if (nodes > maxnodes) maxnodes = nodes;
        }
        if (d < 0) { fprintf(stderr, "no polychromatic colouring at all?! graph %lld\n", count); return 3; }
        hist[d]++; count++;
        if (!quiet) printf("%d\n", d);
        if (d >= dump) {
            printf("disc=%d n=%d", d, n);
            for (int v = 0; v < n; v++) { printf(" |"); for (int i = 0; i < deg[v]; i++) printf(" %d", adj[v][i]); }
            printf("\n");
        }
    }
    fprintf(stderr, "n=%d graphs=%lld faces/graph=%d maxnodes=%lld\n", n, count, nf, maxnodes);
    for (int d = 0; d <= n; d++) if (hist[d]) fprintf(stderr, "  disc=%d: %lld\n", d, hist[d]);
    return 0;
}
