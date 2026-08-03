/* evens.c -- exact even elements of U(a,b) up to N.  Usage: ./evens a b N */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv){
    int a=atoi(argv[1]), b=atoi(argv[2]); long N=atol(argv[3]);
    int *terms=malloc(sizeof(int)*(size_t)(N+2));
    unsigned char *cnt=calloc((size_t)(N+2),1);
    if(!terms||!cnt){fprintf(stderr,"oom\n");return 1;}
    int k=0; terms[k++]=a;
    if((long)a+b<=N) cnt[a+b]=1;
    terms[k++]=b;
    for(long x=b+1;x<=N;x++){
        if(cnt[x]!=1) continue;
        for(int i=0;i<k;i++){ long s=(long)terms[i]+x; if(s>N) break; if(cnt[s]<2) cnt[s]++; }
        terms[k++]=(int)x;
    }
    int neven=0; for(int i=0;i<k;i++) if((terms[i]&1)==0) neven++;
    printf("%d %d %ld %d %d",a,b,N,k,neven);
    for(int i=0;i<k;i++) if((terms[i]&1)==0) printf(" %d",terms[i]);
    printf("\n");
    return 0;
}
