/* vdw_check.c — independent good-partition verifier for w(2;s,t) witnesses.
 *
 * Reads: s t on argv, witness bits (one line of 0/1, '#' comments skipped)
 * on stdin. A witness is GOOD iff no s-AP is all-0 and no t-AP is all-1.
 * Enumerates every AP by nested (start, difference) loops from the
 * definition; shares no code with the Python encoder or verifier.
 *
 * Exit 0 and print "GOOD n=<n>" iff good; exit 1 with the violating AP
 * otherwise.
 *
 *   gcc -O2 -o vdw_check vdw_check.c
 *   ./vdw_check 5 8 < data/witness_5_8_n292_persat_p74ext.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: vdw_check s t < bits\n"); return 2; }
    int s = atoi(argv[1]), t = atoi(argv[2]);
    static char line[1 << 20];
    static int col[1 << 19];
    int n = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '#') continue;
        for (char *c = line; *c; ++c) {
            if (*c == '0' || *c == '1') col[++n] = *c - '0';
            else if (*c != '\n' && *c != '\r' && *c != ' ') {
                fprintf(stderr, "bad character '%c'\n", *c); return 2;
            }
        }
        if (n > 0) break;   /* first bit line only */
    }
    if (n == 0) { fprintf(stderr, "no bits read\n"); return 2; }

    /* s-APs all colored 0 */
    for (int d = 1; (s - 1) * d <= n - 1; ++d)
        for (int a = 1; a + (s - 1) * d <= n; ++a) {
            int all0 = 1;
            for (int i = 0; i < s; ++i)
                if (col[a + i * d]) { all0 = 0; break; }
            if (all0) {
                printf("BAD: %d-AP start=%d diff=%d all color 0\n", s, a, d);
                return 1;
            }
        }
    /* t-APs all colored 1 */
    for (int d = 1; (t - 1) * d <= n - 1; ++d)
        for (int a = 1; a + (t - 1) * d <= n; ++a) {
            int all1 = 1;
            for (int i = 0; i < t; ++i)
                if (!col[a + i * d]) { all1 = 0; break; }
            if (all1) {
                printf("BAD: %d-AP start=%d diff=%d all color 1\n", t, a, d);
                return 1;
            }
        }
    printf("GOOD n=%d\n", n);
    return 0;
}
