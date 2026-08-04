/* Census of doubly saturated (s,t)-Ramsey circulants, n <= 64.
   G = Cay(Z_n, S), S = -S.  Vertex-transitivity lets us:
     - test K_s-freeness by looking only for a K_{s-1} inside N(0);
     - test the two saturation conditions only for the pairs (0,d), d = 1..n/2,
       since x -> x+1 and x -> -x are automorphisms.
   Conditions (see ds.c): (A) non-edge {u,v} : N_G(u) & N_G(v) has a K_{s-2}
                          (B) edge     {u,v} : N_H(u) & N_H(v) has a K_{t-2}, H = complement.
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>

typedef uint64_t U;

static inline int hascl(const U *adj, U cand, int k){
    if (k <= 0) return 1;
    if (k == 1) return cand != 0;
    if (__builtin_popcountll(cand) < k) return 0;
    U c = cand;
    while (c) {
        int v = __builtin_ctzll(c);
        c &= c - 1;
        if (__builtin_popcountll(c) < k-1) return 0;
        if (hascl(adj, c & adj[v], k-1)) return 1;
    }
    return 0;
}

int main(int argc, char **argv){
    int s = atoi(argv[1]), t = atoi(argv[2]);
    int nlo = atoi(argv[3]), nhi = atoi(argv[4]);
    for (int n = nlo; n <= nhi; n++){
        int nd = n/2;
        long long ngood = 0, nds = 0;
        unsigned long long total = 1ULL << nd;
        #pragma omp parallel for schedule(dynamic,64) reduction(+:ngood,nds)
        for (long long mask = 0; mask < (long long)total; mask++){
            U g[64], h[64];
            U all = (n==64)? ~(U)0 : (((U)1<<n)-1);
            for (int i = 0; i < n; i++) g[i] = 0;
            for (int d = 1; d <= nd; d++){
                if (!(mask >> (d-1) & 1)) continue;
                for (int i = 0; i < n; i++){
                    int j = (i+d) % n;
                    g[i] |= (U)1 << j; g[j] |= (U)1 << i;
                }
            }
            for (int i = 0; i < n; i++) h[i] = all & ~g[i] & ~((U)1<<i);
            if (hascl(g, g[0], s-1)) continue;      /* K_s through vertex 0 */
            if (hascl(h, h[0], t-1)) continue;      /* independent t-set through 0 */
            ngood++;
            int ok = 1;
            for (int d = 1; d <= nd && ok; d++){
                if (g[0] >> d & 1) { if (!hascl(h, h[0] & h[d], t-2)) ok = 0; }
                else               { if (!hascl(g, g[0] & g[d], s-2)) ok = 0; }
            }
            if (!ok) continue;
            nds++;
            #pragma omp critical
            { printf("HIT (s,t)=(%d,%d) n=%2d S={", s, t, n);
              for (int d = 1; d <= nd; d++) if (mask>>(d-1)&1) printf("%d%s", d, (d<nd)?"":"");
              printf("} mask=%lld deg=%d\n", mask, __builtin_popcountll(g[0])); fflush(stdout); }
        }
        printf("# (s,t)=(%d,%d) n=%2d  masks=%llu  good=%lld  doubly-saturated=%lld\n",
               s, t, n, total, ngood, nds);
        fflush(stdout);
    }
    return 0;
}
