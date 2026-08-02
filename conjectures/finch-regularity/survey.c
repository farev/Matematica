/* survey.c -- 1-additive (Ulam-type) sequences U(a,b): landscape of even elements.
 *
 * U(a,b): start a < b; each later term is the least integer greater than the
 * previous term with EXACTLY ONE representation as u+v, u<v both earlier terms.
 *
 * All arithmetic is exact integer arithmetic on machine ints; the only
 * "approximation" is the finite horizon N.
 *
 * Usage: ./survey N amin amax bmax
 * Prints one line per coprime pair (a,b), a<b<=bmax, a in [amin,amax]:
 *   a b nterms neven e1 e2 ... (even elements, capped at 64 printed)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int gcd(int x, int y) { while (y) { int t = x % y; x = y; y = t; } return x; }

/* Compute U(a,b) up to N.  terms[] filled, returns count.
 * cnt[] is a saturating-at-2 count of representations. */
static int ulam(int a, int b, int N, int *terms, unsigned char *cnt)
{
    memset(cnt, 0, (size_t)(N + 2));
    int k = 0;
    terms[k++] = a;
    for (int i = 0; i < k; i++) { /* nothing yet */ }
    /* add b */
    if (a + b <= N) cnt[a + b] = 1;
    terms[k++] = b;

    for (int x = b + 1; x <= N; x++) {
        if (cnt[x] != 1) continue;
        /* x joins: bump counts for x + each earlier term */
        for (int i = 0; i < k; i++) {
            int s = terms[i] + x;
            if (s > N) break;               /* terms[] is increasing */
            if (cnt[s] < 2) cnt[s]++;
        }
        terms[k++] = x;
    }
    return k;
}

int main(int argc, char **argv)
{
    int N    = argc > 1 ? atoi(argv[1]) : 20000;
    int amin = argc > 2 ? atoi(argv[2]) : 1;
    int amax = argc > 3 ? atoi(argv[3]) : 20;
    int bmax = argc > 4 ? atoi(argv[4]) : 60;

    int *terms = malloc(sizeof(int) * (size_t)(N + 2));
    unsigned char *cnt = malloc((size_t)(N + 2));
    if (!terms || !cnt) { fprintf(stderr, "oom\n"); return 1; }

    for (int a = amin; a <= amax; a++) {
        for (int b = a + 1; b <= bmax; b++) {
            if (gcd(a, b) != 1) continue;
            int k = ulam(a, b, N, terms, cnt);
            int neven = 0, maxeven = 0;
            for (int i = 0; i < k; i++)
                if ((terms[i] & 1) == 0) { neven++; if (terms[i] > maxeven) maxeven = terms[i]; }
            printf("%d %d %d %d %d", a, b, k, neven, maxeven);
            int printed = 0;
            for (int i = 0; i < k && printed < 64; i++)
                if ((terms[i] & 1) == 0) { printf(" %d", terms[i]); printed++; }
            printf("\n");
        }
        fflush(stdout);
    }
    free(terms); free(cnt);
    return 0;
}
