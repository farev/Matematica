/* Doubly saturated (s,t)-Ramsey graphs invariant under a fixed-point-free automorphism of order m.
   Vertices Z_m x [k], n = m*k; sigma(x,i) = (x+1,i).  Circulants are the case k = 1.
   Enumerate all sigma-invariant graphs by choosing, for each orbit of unordered pairs, in/out. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>
typedef uint64_t U;
static int m, k, n, s, t, norb;
static int orb[64][64];                       /* orb[u][v] = orbit index of pair {u,v} */

static inline int hascl(const U *adj, U cand, int kk){
    if (kk <= 0) return 1;
    if (kk == 1) return cand != 0;
    if (__builtin_popcountll(cand) < kk) return 0;
    U c = cand;
    while (c){ int v = __builtin_ctzll(c); c &= c-1;
        if (__builtin_popcountll(c) < kk-1) return 0;
        if (hascl(adj, c & adj[v], kk-1)) return 1; }
    return 0;
}
int main(int argc, char **argv){
    s = atoi(argv[1]); t = atoi(argv[2]); m = atoi(argv[3]); k = atoi(argv[4]);
    n = m*k;
    /* build orbit map */
    int idx[8][8][64]; for(int a=0;a<8;a++)for(int b=0;b<8;b++)for(int d=0;d<64;d++) idx[a][b][d]=-1;
    norb = 0;
    for (int i=0;i<k;i++) for (int j=i;j<k;j++) for (int d=0; d<m; d++){
        if (i==j && d==0) continue;
        if (idx[i][j][d] >= 0) continue;
        int id = norb++;
        idx[i][j][d] = id;  idx[j][i][(m-d)%m] = id;      /* the two descriptions of one orbit */
    }
    for (int u=0;u<n;u++) for (int v=0;v<n;v++){
        if (u==v) continue;
        int xu=u%m, iu=u/m, xv=v%m, iv=v/m;
        orb[u][v] = idx[iu][iv][((xv-xu)%m+m)%m];
    }
    printf("# (s,t)=(%d,%d) m=%d k=%d n=%d orbits=%d  space=2^%d\n", s,t,m,k,n,norb,norb);
    long long good=0, ds=0;
    unsigned long long total = 1ULL << norb;
    #pragma omp parallel for schedule(dynamic,256) reduction(+:good,ds)
    for (long long mask=0; mask<(long long)total; mask++){
        U g[64], h[64];
        U all = (((U)1<<n)-1);
        for (int i=0;i<n;i++) g[i]=0;
        for (int u=0;u<n;u++) for (int v=u+1;v<n;v++)
            if (mask >> orb[u][v] & 1){ g[u] |= (U)1<<v; g[v] |= (U)1<<u; }
        for (int i=0;i<n;i++) h[i] = all & ~g[i] & ~((U)1<<i);
        /* sigma is transitive on each of the k vertex-classes: test cliques through one rep per class */
        int bad=0;
        for (int i=0;i<k && !bad;i++){ int r=i*m;
            if (hascl(g, g[r], s-1)) bad=1;
            if (hascl(h, h[r], t-1)) bad=1; }
        if (bad) continue;
        good++;
        int ok=1;
        for (int i=0;i<k && ok;i++){ int u=i*m;
            for (int v=0; v<n && ok; v++){ if (v==u) continue;
                if (g[u]>>v & 1){ if (!hascl(h, h[u]&h[v], t-2)) ok=0; }
                else            { if (!hascl(g, g[u]&g[v], s-2)) ok=0; } } }
        if (!ok) continue;
        ds++;
        #pragma omp critical
        { printf("HIT m=%d k=%d n=%d mask=%lld\n", m,k,n,mask); fflush(stdout); }
    }
    printf("# n=%d m=%d: good=%lld doubly-saturated=%lld\n", n, m, good, ds);
    return 0;
}
