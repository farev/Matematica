/* Test a single circulant for double saturation.  Usage: ./one n s t d1,d2,... */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t U;
static int n;
static inline int hascl(const U *adj, U cand, int k){
    if (k<=0) return 1;  if (k==1) return cand!=0;
    if (__builtin_popcountll(cand)<k) return 0;
    U c=cand;
    while(c){ int v=__builtin_ctzll(c); c&=c-1;
        if(__builtin_popcountll(c)<k-1) return 0;
        if(hascl(adj,c&adj[v],k-1)) return 1; }
    return 0;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); int s=atoi(argv[2]), t=atoi(argv[3]);
    U g[64],h[64]; for(int i=0;i<n;i++) g[i]=0;
    char *p=strtok(argv[4],","); int nd=0;
    while(p){ int d=atoi(p); nd++;
        for(int i=0;i<n;i++){ int j=(i+d)%n; g[i]|=(U)1<<j; g[j]|=(U)1<<i; }
        p=strtok(NULL,","); }
    U all=(n==64)?~(U)0:(((U)1<<n)-1);
    for(int i=0;i<n;i++) h[i]=all&~g[i]&~((U)1<<i);
    int deg=__builtin_popcountll(g[0]);
    if(hascl(g,g[0],s-1)){ printf("n=%2d (%d,%d) deg=%2d : HAS K%d\n",n,s,t,deg,s); return 1; }
    if(hascl(h,h[0],t-1)){ printf("n=%2d (%d,%d) deg=%2d : HAS independent %d-set\n",n,s,t,deg,t); return 1; }
    for(int d=1;d<=n/2;d++){
        if(g[0]>>d&1){ if(!hascl(h,h[0]&h[d],t-2)){ printf("n=%2d (%d,%d) deg=%2d : edge 0-%d NOT deletion-critical\n",n,s,t,deg,d); return 1; } }
        else         { if(!hascl(g,g[0]&g[d],s-2)){ printf("n=%2d (%d,%d) deg=%2d : non-edge 0-%d NOT saturated\n",n,s,t,deg,d); return 1; } }
    }
    printf("n=%2d (%d,%d) deg=%2d : DOUBLY SATURATED\n",n,s,t,deg); return 0;
}
