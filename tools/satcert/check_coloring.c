/* check_coloring.c — independent verifier for Rado-number lower-bound
 * witnesses.  Reads from stdin:
 *   line 1: n k m const mode        (mode: 0=all, 1=not_all_equal, 2=distinct)
 *   line 2: m coefficients a_1..a_m (equation sum a_i x_i + const = 0)
 *   line 3: n colors c_1..c_n       (0-based, for integers 1..n)
 * Enumerates ALL m-tuples in {1..n}^m by nested loops (no solving-for-last:
 * deliberately a different enumeration strategy than the encoder), and
 * reports the first monochromatic solution found, or GOOD if none.
 * Supports m = 2, 3, 4.
 */
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n, k, m, cst, mode;
    if (scanf("%d %d %d %d %d", &n, &k, &m, &cst, &mode) != 5) { fprintf(stderr, "bad header\n"); return 2; }
    if (m < 2 || m > 4) { fprintf(stderr, "m out of range\n"); return 2; }
    long a[4] = {0,0,0,0};
    for (int i = 0; i < m; i++) if (scanf("%ld", &a[i]) != 1) { fprintf(stderr, "bad coeffs\n"); return 2; }
    int *col = malloc(sizeof(int)*(n+1));
    for (int i = 1; i <= n; i++) if (scanf("%d", &col[i]) != 1 ) { fprintf(stderr, "bad colors\n"); return 2; }
    for (int i = 1; i <= n; i++) if (col[i] < 0 || col[i] >= k) { fprintf(stderr, "color out of range at %d\n", i); return 2; }

    long checked = 0, sols = 0;
    int x[4];
    for (x[0] = 1; x[0] <= n; x[0]++)
    for (x[1] = 1; x[1] <= n; x[1]++) {
        if (m == 2) {
            long s = a[0]*x[0] + a[1]*x[1] + cst;
            checked++;
            if (s == 0) goto issol2;
            continue;
        issol2:
            sols++;
            {
                int alleq = (x[0]==x[1]);
                int dist = (x[0]!=x[1]);
                if (mode == 1 && alleq) continue;
                if (mode == 2 && !dist) continue;
                if (col[x[0]] == col[x[1]]) { printf("BAD mono solution: %d %d (color %d)\n", x[0], x[1], col[x[0]]); return 1; }
            }
            continue;
        }
        for (x[2] = 1; x[2] <= n; x[2]++) {
            if (m == 3) {
                long s = a[0]*x[0] + a[1]*x[1] + a[2]*x[2] + cst;
                checked++;
                if (s != 0) continue;
                sols++;
                int alleq = (x[0]==x[1] && x[1]==x[2]);
                int dist = (x[0]!=x[1] && x[0]!=x[2] && x[1]!=x[2]);
                if (mode == 1 && alleq) continue;
                if (mode == 2 && !dist) continue;
                if (col[x[0]] == col[x[1]] && col[x[1]] == col[x[2]]) {
                    printf("BAD mono solution: %d %d %d (color %d)\n", x[0], x[1], x[2], col[x[0]]); return 1;
                }
                continue;
            }
            for (x[3] = 1; x[3] <= n; x[3]++) {
                long s = a[0]*x[0] + a[1]*x[1] + a[2]*x[2] + a[3]*x[3] + cst;
                checked++;
                if (s != 0) continue;
                sols++;
                int alleq = (x[0]==x[1] && x[1]==x[2] && x[2]==x[3]);
                int dist = (x[0]!=x[1] && x[0]!=x[2] && x[0]!=x[3] && x[1]!=x[2] && x[1]!=x[3] && x[2]!=x[3]);
                if (mode == 1 && alleq) continue;
                if (mode == 2 && !dist) continue;
                if (col[x[0]] == col[x[1]] && col[x[1]] == col[x[2]] && col[x[2]] == col[x[3]]) {
                    printf("BAD mono solution: %d %d %d %d (color %d)\n", x[0], x[1], x[2], x[3], col[x[0]]); return 1;
                }
            }
        }
    }
    printf("GOOD: no monochromatic solution; %ld tuples enumerated, %ld solutions checked\n", checked, sols);
    return 0;
}
