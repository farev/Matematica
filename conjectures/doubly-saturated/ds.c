/* Doubly saturated Ramsey graphs.
   G on n<=32 vertices is (s,t)-good if G has no K_s and complement H has no K_t.
   G is doubly saturated if additionally
     (A) every non-edge uv of G:  N_G(u) & N_G(v) contains a K_{s-2}
     (B) every edge     uv of G:  N_H(u) & N_H(v) contains a K_{t-2}
   (A) = adding uv creates a K_s ; (B) = deleting uv creates an independent t-set.
   Note G doubly-sat for (s,t)  <=>  H doubly-sat for (t,s).
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint32_t U;
static int N;

/* does the induced subgraph on vertex set `cand` (in graph adj[]) contain a K_k ? */
static int hasclique(const U *adj, U cand, int k){
    if (k <= 0) return 1;
    if (k == 1) return cand != 0;
    U c = cand;
    while (c) {
        int v = __builtin_ctz(c);
        c &= c - 1;
        /* only look at neighbours after v to avoid repeats */
        if (hasclique(adj, cand & adj[v] & ~((U)0) & (~(((U)1<<(v+1))-1)), k-1)) return 1;
        if (__builtin_popcount(c) < k-1) return 0;
    }
    return 0;
}

static int good(const U *g, const U *h, int s, int t){
    for (int v = 0; v < N; v++){
        U later = ~(((U)1<<(v+1))-1);
        if (hasclique(g, g[v] & later, s-1)) return 0;
        if (hasclique(h, h[v] & later, t-1)) return 0;
    }
    return 1;
}

static int doubly(const U *g, const U *h, int s, int t){
    for (int u = 0; u < N; u++)
        for (int v = u+1; v < N; v++){
            if (g[u] >> v & 1){
                if (!hasclique(h, h[u] & h[v], t-2)) return 0;
            } else {
                if (!hasclique(g, g[u] & g[v], s-2)) return 0;
            }
        }
    return 1;
}

static void build_circ(U *g, U *h, int n, unsigned mask){
    for (int i = 0; i < n; i++) g[i] = 0;
    for (int d = 1; d <= n/2; d++){
        if (!(mask >> (d-1) & 1)) continue;
        for (int i = 0; i < n; i++){
            int j = (i+d) % n;
            g[i] |= (U)1 << j;  g[j] |= (U)1 << i;
        }
    }
    U all = (n==32)? ~(U)0 : (((U)1<<n)-1);
    for (int i = 0; i < n; i++) h[i] = all & ~g[i] & ~((U)1<<i);
}

int main(int argc, char **argv){
    int s = atoi(argv[1]), t = atoi(argv[2]);
    int nlo = atoi(argv[3]), nhi = atoi(argv[4]);
    for (int n = nlo; n <= nhi; n++){
        N = n;
        int nd = n/2, found = 0, ngood = 0;
        U g[32], h[32];
        for (unsigned mask = 0; mask < (1u<<nd); mask++){
            build_circ(g, h, n, mask);
            if (!good(g, h, s, t)) continue;
            ngood++;
            if (!doubly(g, h, s, t)) continue;
            found++;
            printf("n=%2d  DOUBLY SATURATED (%d,%d)  S={", n, s, t);
            for (int d = 1; d <= nd; d++) if (mask>>(d-1)&1) printf("%d,", d);
            printf("}\n");
        }
        printf("# n=%2d (s,t)=(%d,%d): circulants scanned %u, (s,t)-good %d, doubly saturated %d\n",
               n, s, t, 1u<<nd, ngood, found);
        fflush(stdout);
    }
    return 0;
}
