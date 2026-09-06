// From-definition verifier for a k-edge-colouring of K_n with a claimed proper j-labelling of
// every colour class.  Input (binary): int32 n, int32 k, then n*n bytes col[i*n+j] (colour of
// edge ij, 0..k-1, diagonal ignored), then n*k bytes lab[i*k+c] (label of vertex i in class c).
// Checks: every off-diagonal colour < k and symmetric; no monochromatic triangle (all C(n,3)
// triples); every edge ij of colour c has lab[i][c] != lab[j][c]; reports the number of labels.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb"); if (!f) { perror("open"); return 2; }
    int n, k; if (fread(&n, 4, 1, f) != 1 || fread(&k, 4, 1, f) != 1) return 2;
    unsigned char *col = malloc((size_t)n * n), *lab = malloc((size_t)n * k);
    if (fread(col, 1, (size_t)n * n, f) != (size_t)n * n) { fprintf(stderr, "short col\n"); return 2; }
    if (fread(lab, 1, (size_t)n * k, f) != (size_t)n * k) { fprintf(stderr, "short lab\n"); return 2; }
    fclose(f);
    long long bad = 0; int maxlab = 0;
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (i != j) {
        int c = col[(size_t)i * n + j];
        if (c >= k || c != col[(size_t)j * n + i]) { fprintf(stderr, "bad colour at %d %d\n", i, j); return 1; }
        if (lab[(size_t)i * k + c] == lab[(size_t)j * k + c]) bad++;
    }
    for (int i = 0; i < n; i++) for (int c = 0; c < k; c++) if (lab[(size_t)i * k + c] + 1 > maxlab) maxlab = lab[(size_t)i * k + c] + 1;
    if (bad) { printf("FAIL: %lld improperly labelled edge-ends\n", bad); return 1; }
    long long tri = 0;
    for (int i = 0; i < n; i++) {
        unsigned char *ci = col + (size_t)i * n;
        for (int j = i + 1; j < n; j++) {
            int c = ci[j]; unsigned char *cj = col + (size_t)j * n;
            for (int l = j + 1; l < n; l++) if (ci[l] == c && cj[l] == c) tri++;
        }
    }
    if (tri) { printf("FAIL: %lld monochromatic triangles\n", tri); return 1; }
    printf("VERIFIED: K_%d with %d colours, no monochromatic triangle, every class properly labelled with <= %d labels\n", n, k, maxlab);
    return 0;
}
