/* engine.c — exhaustive enumeration of n with base-3 digits <= 1,
 * base-5 digits <= 2, base-7 digits <= 3  (i.e. gcd(C(2n,n),105)=1,
 * by Kummer).  Each hit is also tested for base-11 digits <= 5
 * (gcd(C(2n,n),1155)=1).  Exact integer arithmetic only.
 *
 * Modes:
 *   rec  T                       recursive DFS with cap T (validation)
 *   grid K W start stride count  production: patterns of powers 3^W..3^(K-1);
 *                                task p covers n = base(p) + (any subset of
 *                                3^0..3^(W-1)); Gray-code walk, 2^W leaves,
 *                                no pruning (every subset in range by design).
 * Output rows (grid):  p,base,leaves,r5pass,f35,elapsed_ms,hits
 *   hits = "-" or space-separated n:flag11 entries.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;
typedef int64_t  i64;

#define P5_8  390625ULL           /* 5^8  */
#define P5_16 152587890625ULL     /* 5^16 */
#define P7_6  117649ULL           /* 7^6  */
#define P7_12 13841287201ULL      /* 7^12 */

static unsigned char valid5[P5_8]; /* all 8 base-5 digits <= 2 */
static unsigned char valid7[P7_6]; /* all 6 base-7 digits <= 3 */

static void build_tables(void){
    for(u64 r=0;r<P5_8;r++){
        u64 x=r; int ok=1;
        for(int i=0;i<8;i++){ if(x%5>2){ok=0;break;} x/=5; }
        valid5[r]=ok;
    }
    for(u64 r=0;r<P7_6;r++){
        u64 x=r; int ok=1;
        for(int i=0;i<6;i++){ if(x%7>3){ok=0;break;} x/=7; }
        valid7[r]=ok;
    }
}

static int full5(u128 n){
    u64 r=(u64)(n%P5_16);
    if(!valid5[r%P5_8]||!valid5[r/P5_8]) return 0;
    u64 q=(u64)(n/P5_16);              /* n < 3^45 => q < 1.94e10, fits */
    while(q){ if(q%5>2) return 0; q/=5; }
    return 1;
}
static int full7(u128 n){
    u64 r=(u64)(n%P7_12);
    if(!valid7[r%P7_6]||!valid7[r/P7_6]) return 0;
    u64 q=(u64)(n/P7_12);              /* n < 3^45 => q < 2.14e11, fits */
    while(q){ if(q%7>3) return 0; q/=7; }
    return 1;
}
static int ok11(u128 n){               /* base-11 digits <= 5 */
    while(n){ if((u64)(n%11)>5) return 0; n/=11; }
    return 1;
}
static void print_u128(FILE*f,u128 n){
    char b[48]; int i=0;
    if(!n){ fputc('0',f); return; }
    while(n){ b[i++]='0'+(char)(u64)(n%10); n/=10; }
    while(i--) fputc(b[i],f);
}
static u128 parse_u128(const char*s){
    u128 v=0; for(;*s;s++){ v=v*10+(u128)(*s-'0'); } return v;
}

/* ---------------- recursive validation mode ---------------- */
static u128 REC_T; static u64 rec_leaves, rec_f35, rec_hits; static FILE* rec_out;
static u128 rec_pows[48]; static int rec_np;
static u128 rec_suffix[49];
static void rec_dfs(int i,u128 s){
    if(i==rec_np){
        rec_leaves++;
        if(full5(s)){ rec_f35++;
            if(full7(s)){ rec_hits++;
                print_u128(rec_out,s); fprintf(rec_out,":%d\n",ok11(s)); } }
        return;
    }
    rec_dfs(i+1,s);
    if(s+rec_pows[i]<=REC_T) rec_dfs(i+1,s+rec_pows[i]);
}

/* ---------------- grid production mode ---------------- */
struct hit { u128 n; int f11; };

int main(int argc,char**argv){
    build_tables();
    if(argc>=3 && !strcmp(argv[1],"rec")){
        REC_T=parse_u128(argv[2]); rec_out=stdout;
        u128 p=1; rec_np=0;
        while(p<=REC_T){ rec_pows[rec_np++]=p; p*=3; }
        /* descending */
        for(int i=0;i<rec_np/2;i++){u128 t=rec_pows[i];rec_pows[i]=rec_pows[rec_np-1-i];rec_pows[rec_np-1-i]=t;}
        rec_dfs(0,0);
        fprintf(stderr,"rec T="); print_u128(stderr,REC_T);
        fprintf(stderr," leaves=%llu f35=%llu hits=%llu\n",
            (unsigned long long)rec_leaves,(unsigned long long)rec_f35,(unsigned long long)rec_hits);
        return 0;
    }
    if(argc>=8 && !strcmp(argv[1],"grid")){
        int K=atoi(argv[2]), W=atoi(argv[3]);
        u64 start=strtoull(argv[4],0,10), stride=strtoull(argv[5],0,10), count=strtoull(argv[6],0,10);
        FILE*out=fopen(argv[7],"a");
        if(!out){perror("out");return 1;}
        int J=K-W;                      /* top pattern bits */
        if(J<1||J>63||W<1||W>34){fprintf(stderr,"bad K/W\n");return 1;}
        u128 topw[64]; u128 pw3=1;
        for(int i=0;i<W;i++) pw3*=3;    /* 3^W */
        topw[0]=pw3;
        for(int i=1;i<J;i++) topw[i]=topw[i-1]*3;
        u64 pwlo[35]; pwlo[0]=1;
        for(int i=1;i<W;i++) pwlo[i]=pwlo[i-1]*3;
        i64 m5[35];
        for(int i=0;i<W;i++) m5[i]=(i64)(pwlo[i]%P5_8);
        struct hit hits[256];
        for(u64 ti=0;ti<count;ti++){
            u64 p=start+ti*stride;
            if(p>=(1ULL<<J)) break;
            struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
            u128 base=0;
            for(int i=0;i<J;i++) if(p>>i&1) base+=topw[i];
            u64 nh=0, r5pass=0, f35=0;
            u64 s=0, mask=0;
            i64 r5=(i64)(u64)(base%P5_8);
            /* leaf for state 0 */
            if(valid5[r5]){ r5pass++; u128 n=base;
                if(full5(n)){ f35++; if(full7(n)){ hits[nh].n=n; hits[nh].f11=ok11(n); nh++; } } }
            const u64 NL=1ULL<<W;
            for(u64 t=1;t<NL;t++){
                int j=__builtin_ctzll(t);
                u64 b=1ULL<<j; mask^=b;
                if(mask&b){ s+=pwlo[j]; r5+=m5[j]; r5-=(r5>=(i64)P5_8)?(i64)P5_8:0; }
                else      { s-=pwlo[j]; r5-=m5[j]; r5+=(r5<0)?(i64)P5_8:0; }
                if(__builtin_expect(valid5[r5],0)){
                    r5pass++; u128 n=base+s;
                    if(full5(n)){ f35++;
                        if(full7(n)){ if(nh<256){hits[nh].n=n;hits[nh].f11=ok11(n);nh++;} } }
                }
            }
            clock_gettime(CLOCK_MONOTONIC,&t1);
            long ms=(t1.tv_sec-t0.tv_sec)*1000+(t1.tv_nsec-t0.tv_nsec)/1000000;
            fprintf(out,"%llu,",(unsigned long long)p);
            print_u128(out,base);
            fprintf(out,",%llu,%llu,%llu,%ld,",(unsigned long long)NL,
                (unsigned long long)r5pass,(unsigned long long)f35,ms);
            if(!nh) fputc('-',out);
            for(u64 i=0;i<nh;i++){ if(i)fputc(' ',out); print_u128(out,hits[i].n); fprintf(out,":%d",hits[i].f11); }
            fputc('\n',out); fflush(out);
        }
        fclose(out);
        return 0;
    }
    fprintf(stderr,"usage: engine rec T | engine grid K W start stride count outfile\n");
    return 1;
}
