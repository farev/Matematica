/* check_peaceable.c — independent verifier for peaceable-queens witnesses.
 *
 * Written from the definition, sharing no code or geometry helpers with
 * the CNF encoder: reads a placement, re-derives all attacks by scanning
 * every white-black pair, checks the army sizes.
 *
 * Input (stdin):
 *   line 1: n m            (board size, claimed army size)
 *   then n lines of n characters:  '.' empty, 'W' white queen, 'B' black.
 *
 * Exit 0 and print "s WITNESS VERIFIED" iff:
 *   #W >= m, #B >= m, and no W and B share a row, column, or diagonal.
 * Any violation: exit 1 with a diagnostic.
 *
 * Build: gcc -O2 -o check_peaceable check_peaceable.c
 */
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2 || n < 1 || n > 1024) {
        fprintf(stderr, "bad header\n");
        return 1;
    }
    static char g[1024][1026];
    for (int r = 0; r < n; r++) {
        if (scanf("%1025s", g[r]) != 1) {
            fprintf(stderr, "bad row %d\n", r);
            return 1;
        }
    }
    int nw = 0, nb = 0;
    static int wr[1048576], wc[1048576], br[1048576], bc[1048576];
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) {
            if (g[r][c] == 'W') { wr[nw] = r; wc[nw] = c; nw++; }
            else if (g[r][c] == 'B') { br[nb] = r; bc[nb] = c; nb++; }
            else if (g[r][c] != '.') {
                fprintf(stderr, "bad char '%c' at (%d,%d)\n", g[r][c], r, c);
                return 1;
            }
        }
    if (nw < m || nb < m) {
        fprintf(stderr, "army too small: %d white, %d black, need %d\n",
                nw, nb, m);
        return 1;
    }
    long attacks = 0;
    for (int i = 0; i < nw; i++)
        for (int j = 0; j < nb; j++) {
            int dr = wr[i] - br[j], dc = wc[i] - bc[j];
            if (dr == 0 || dc == 0 || dr == dc || dr == -dc) {
                fprintf(stderr, "attack: W(%d,%d) vs B(%d,%d)\n",
                        wr[i], wc[i], br[j], bc[j]);
                attacks++;
            }
        }
    if (attacks) {
        fprintf(stderr, "%ld attacking pairs\n", attacks);
        return 1;
    }
    printf("s WITNESS VERIFIED  n=%d white=%d black=%d (need %d)\n",
           n, nw, nb, m);
    return 0;
}
