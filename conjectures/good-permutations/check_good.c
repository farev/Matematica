/*
 * check_good.c — independent from-definition checker for good permutations.
 *
 * Reads permutations from stdin, one per line (n integers separated by spaces;
 * n is inferred from the line).  For each line it verifies (1) the line is a
 * permutation of {1..n} and (2) no proper consecutive block of length L in
 * [2, n-1] has sum divisible by L.  Prints one verdict line per input line:
 *   "GOOD n=<n>"  or  "BAD n=<n> block start=<s> len=<L> avg=<sum/L>"  or "NOTPERM n=<n>".
 * Exit status 0 iff every line is GOOD.
 *
 * Also accepts "construction <p>" as a line: it then builds the permutation
 * 1, p-1, p, p-3, p-2, ..., 2, 3 (p odd) and checks it, printing
 * "CONSTRUCTION p=<p> GOOD|BAD ...".
 *
 * Exact 64-bit integer arithmetic; O(n^2) time, no floating point.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 2000000

static long long a[MAXN + 2], pre[MAXN + 2];
static unsigned char seen[MAXN + 2];

static int check(long long n, const char *tag, long long p) {
    for (long long i = 0; i <= n; i++) seen[i] = 0;
    for (long long i = 1; i <= n; i++) {
        if (a[i] < 1 || a[i] > n || seen[a[i]]) { printf("NOTPERM n=%lld%s\n", n, tag); return 0; }
        seen[a[i]] = 1;
    }
    pre[0] = 0;
    for (long long i = 1; i <= n; i++) pre[i] = pre[i - 1] + a[i];
    for (long long L = 2; L <= n - 1; L++) {
        for (long long s = 1; s + L - 1 <= n; s++) {
            long long S = pre[s + L - 1] - pre[s - 1];
            if (S % L == 0) {
                if (p) printf("CONSTRUCTION p=%lld BAD block start=%lld len=%lld avg=%lld\n", p, s, L, S / L);
                else printf("BAD n=%lld block start=%lld len=%lld avg=%lld\n", n, s, L, S / L);
                return 0;
            }
        }
    }
    if (p) printf("CONSTRUCTION p=%lld GOOD\n", p); else printf("GOOD n=%lld%s\n", n, tag);
    return 1;
}

int main(void) {
    static char line[1 << 24];
    int allgood = 1;
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '\n' || line[0] == '#') continue;
        if (strncmp(line, "construction", 12) == 0) {
            long long p = atoll(line + 12);
            if (p < 3 || p % 2 == 0 || p > MAXN) { printf("CONSTRUCTION p=%lld INVALID\n", p); allgood = 0; continue; }
            long long t = 1; a[t++] = 1;
            for (long long x = p - 1; x >= 2; x -= 2) { a[t++] = x; a[t++] = x + 1; }
            if (!check(p, "", p)) allgood = 0;
            continue;
        }
        long long n = 0; char *s = line;
        while (*s) {
            while (*s == ' ' || *s == '\t') s++;
            if (*s == '\n' || *s == 0) break;
            a[++n] = strtoll(s, &s, 10);
            if (n > MAXN) { printf("TOOLONG\n"); return 2; }
        }
        if (n == 0) continue;
        if (!check(n, "", 0)) allgood = 0;
    }
    return allgood ? 0 : 1;
}
