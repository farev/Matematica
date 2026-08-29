// Count loop-graphs on [n] with n edges, every component unicyclic
// (equal #V=#E per component), by exhaustive C(slots, n) enumeration.
#include <stdio.h>
#include <stdint.h>
int n;
int eu[40], ev[40], ns;
int comb[40];
long long count = 0;
int parent[16];
int find(int x){ while(parent[x]!=x){ parent[x]=parent[parent[x]]; x=parent[x];} return x;}
void check(void){
    int nv[16], ne[16];
    for(int i=0;i<n;i++){parent[i]=i;}
    for(int k=0;k<n;k++){
        int ru=find(eu[comb[k]]), rv=find(ev[comb[k]]);
        if(ru!=rv) parent[ru]=rv;
    }
    for(int i=0;i<n;i++){nv[i]=0; ne[i]=0;}
    for(int i=0;i<n;i++) nv[find(i)]++;
    for(int k=0;k<n;k++) ne[find(eu[comb[k]])]++;
    for(int i=0;i<n;i++) if(nv[i] && nv[i]!=ne[i]) return;
    count++;
}
void rec(int pos, int start){
    if(pos==n){ check(); return; }
    for(int s=start; s<ns-(n-1-pos); s++){ comb[pos]=s; rec(pos+1, s+1); }
}
int main(int argc, char**argv){
    n = atoi(argv[1]); ns=0;
    for(int i=0;i<n;i++){ eu[ns]=i; ev[ns]=i; ns++; }
    for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ eu[ns]=i; ev[ns]=j; ns++; }
    rec(0,0);
    printf("u(%d) = %lld\n", n, count);
    return 0;
}
