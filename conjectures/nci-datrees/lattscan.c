/* lattscan.c — exhaustive winning-da-tree census over all lattices with
 * n = k+2 elements, streaming k-element posets from nauty-genposetg.
 *
 * Pipeline:  nauty-genposetg k t q | ./lattscan k [--sample R] [--hard T]
 *
 * A poset on k points (Hasse diagram, digraph6, topological order) is
 * extended by a global bottom and top; the extension is a lattice iff every
 * incomparable pair {x,y} has a least common upper bound among the interior
 * points, or none (join = top).  Every unlabeled lattice with k+2 elements
 * arises from exactly one generated poset.  (If the digraph6 edge direction
 * is the reverse of what this code assumes, every computation below runs on
 * the dual lattice; since duality is a bijection on unlabeled lattices and
 * winnability of the census as a whole quantifies over all lattices, the
 * census is unaffected.  Individual non-winning hits, if any, are re-checked
 * independently anyway.)
 *
 * Winning da-tree decision (Wilhelm, arXiv:2608.27416, Definition 3.1):
 * buildable states = closure of {0} u { S_v : mu(v) != 0 } under
 *   A,B -> A|B   when A&B == 0        (disjoint union)
 *   A,B -> A^B   when B subset A      (guarded difference)
 * with S_v = down-set of v inside P\{top}, and the lattice is winning iff
 * the full set P\{top} is buildable.  We detect wins early: on inserting a
 * state C we test whether target^C is already present (target = A (+) B).
 *
 * Stages per lattice:
 *   0. unique-coatom fast path (a leaf equals the target)
 *   1. leaf-closure: combine states with LEAVES only (sound for WIN)
 *   2. full pair closure (exact decision; exhaustion == NOT WINNING)
 * Any NOT WINNING lattice is printed immediately (candidate counterexample).
 *
 * Exact integer/bitmask arithmetic throughout; no floating point.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXK 15                 /* interior points */
#define MAXW (MAXK+1)           /* ground set width: interior + bottom */

static int K;                   /* interior size from argv */
static uint32_t anc[MAXK];      /* up-set incl self (interior only) */
static uint32_t desc[MAXK];     /* down-set incl self (interior only) */
static int cov[MAXK];           /* cover rows: bit j set = edge i->j */
static long long mu[MAXW+1];    /* mu over interior 0..K-1, K=bottom, K+1=top */
static uint32_t leaves[MAXW+2];
static int nleaves;

/* closure workspace */
#define MAXSTATES (1<<MAXW)
static uint32_t states[MAXSTATES];
static int      par1[MAXSTATES], par2[MAXSTATES]; /* parents (-1: leaf) */
static uint8_t  seen[1<<MAXW];  /* byte-per-mask; memset per lattice via epoch */
static uint32_t seenep[1<<MAXW];
static uint32_t epoch = 0;
static int      idxof[1<<MAXW];

/* stats */
static long long nposet=0, nlat=0, nwin=0, nstage0=0, nstage1=0, nstage2=0,
                 nnonwin=0;
static long long hist[5];       /* states used: <=10,<=100,<=1000,<=8192,more */
static int maxstates1=0, maxstates2=0;
static char worstline[128];

static inline int seen_get(uint32_t m){ return seenep[m]==epoch; }
static inline void seen_set(uint32_t m){ seenep[m]=epoch; }

/* ---- digraph6 ---- */
static int parse_d6(const char *s, int *rows){
    if(*s!='&') return -1;
    s++;
    int n = s[0]-63; s++;
    if(n<0||n>MAXK) return -1;
    int nb = n*n, bi=0, i;
    for(i=0;i<n;i++) rows[i]=0;
    while(bi<nb){
        int v = *s-63;
        if(*s==0) return -1;
        s++;
        int t;
        for(t=5;t>=0 && bi<nb;t--,bi++)
            if((v>>t)&1) rows[bi/n] |= 1<<(bi%n);
    }
    return n;
}

/* ---- per-poset analysis; returns 1 if lattice ---- */
static int analyze(void){
    int i,j;
    /* transitive closures; edges i->j MUST satisfy i<j (topological order).
       Guard: abort loudly if genposetg's convention ever differs. */
    for(i=K-1;i>=0;i--){
        uint32_t u = 1u<<i, m = (uint32_t)cov[i];
        if(m & ((1u<<(i+1))-1)){
            fprintf(stderr,"FATAL: edge to lower index at vertex %d\n",i);
            exit(4);
        }
        while(m){ j=__builtin_ctz(m); m&=m-1; u|=anc[j]; }
        anc[i]=u;
    }
    /* lattice check */
    for(i=0;i<K;i++) for(j=i+1;j<K;j++){
        if((anc[i]>>j&1)||(anc[j]>>i&1)) continue;
        uint32_t U = anc[i]&anc[j];
        if(!U) continue;
        int m0 = __builtin_ctz(U);
        if(U & ~anc[m0]) return 0;     /* no least upper bound */
    }
    nlat++;
    for(i=0;i<K;i++){
        desc[i] = 1u<<i;
    }
    for(i=0;i<K;i++){
        uint32_t m = (uint32_t)cov[i];
        while(m){ j=__builtin_ctz(m); m&=m-1; desc[j]|=desc[i]; }
    }
    /* wait: desc must accumulate transitively; edges i->j with i<j and we
       process i ascending, so desc[i] is complete before use.  (cov rows
       only point upward, so descendants propagate correctly.) */
    /* mu: top=1; interior descending index; bottom last */
    long long s;
    mu[MAXW]=1; /* use slot MAXW for top regardless of K */
    for(i=K-1;i>=0;i--){
        s = 1; /* top */
        uint32_t m = anc[i] & ~(1u<<i);
        while(m){ j=__builtin_ctz(m); m&=m-1; s+=mu[j]; }
        mu[i]=-s;
    }
    s=1; for(i=0;i<K;i++) s+=mu[i];
    mu[K]=-s; /* bottom */
    /* leaves: S_v for mu!=0, v in interior+bottom; S_v = desc | bottom-bit */
    nleaves=0;
    uint32_t botbit = 1u<<K;
    for(i=0;i<K;i++) if(mu[i]!=0) leaves[nleaves++] = desc[i]|botbit;
    if(mu[K]!=0) leaves[nleaves++] = botbit;
    return 1;
}

/* returns 1 win, 0 not winning; fills *used with states explored */
static int decide(uint32_t target, int *used, int *stage){
    int i,j;
    epoch++;
    int ns=0;
    /* dedupe leaves, fast path */
    for(i=0;i<nleaves;i++){
        uint32_t L=leaves[i];
        if(L==target){ *used=1; *stage=0; return 1; }
        if(!seen_get(L)){ seen_set(L); idxof[L]=ns; par1[ns]=-1; states[ns++]=L; }
    }
    /* empty state is always available; harmless to include */
    if(!seen_get(0)){ seen_set(0); idxof[0]=ns; par1[ns]=-1; states[ns++]=0; }
    int nl=ns;
    /* stage 1: combine with initial leaf block only */
    for(i=0;i<ns;i++){
        uint32_t A=states[i];
        if(seen_get(target^A)){ *used=ns; *stage=1; return 1; }
        for(j=0;j<nl;j++){
            uint32_t B=states[j], C; uint32_t ab=A&B;
            if(ab==0) C=A|B;
            else if(ab==B) C=A^B;
            else if(ab==A) C=B^A;
            else continue;
            if(!seen_get(C)){
                seen_set(C); idxof[C]=ns; par1[ns]=i; par2[ns]=j; states[ns++]=C;
                if(C==target || seen_get(target^C)){ *used=ns; *stage=1; return 1; }
            }
        }
    }
    if(ns>maxstates1) maxstates1=ns;
    /* stage 2: full pair closure over everything discovered so far */
    for(i=0;i<ns;i++){
        uint32_t A=states[i];
        for(j=0;j<=i;j++){
            uint32_t B=states[j], C; uint32_t ab=A&B;
            if(ab==0) C=A|B;
            else if(ab==B) C=A^B;
            else if(ab==A) C=B^A;
            else continue;
            if(!seen_get(C)){
                seen_set(C); idxof[C]=ns; par1[ns]=i; par2[ns]=j; states[ns++]=C;
                if(C==target || seen_get(target^C)){ *used=ns; *stage=2; return 1; }
            }
        }
    }
    *used=ns; *stage=2;
    return 0;
}

int main(int argc, char **argv){
    if(argc<2){ fprintf(stderr,"usage: lattscan k [--stats-every N]\n"); return 2; }
    K = atoi(argv[1]);
    if(K<1||K>MAXK){ fprintf(stderr,"bad k\n"); return 2; }
    long long stats_every = 0;
    for(int a=2;a<argc;a++)
        if(!strcmp(argv[a],"--stats-every") && a+1<argc) stats_every=atoll(argv[++a]);
    uint32_t target = (1u<<(K+1))-1;
    char line[256];
    while(fgets(line,sizeof line,stdin)){
        if(line[0]!='&') continue;
        nposet++;
        int n = parse_d6(line,cov);
        if(n!=K){ fprintf(stderr,"parse error: %s",line); return 3; }
        if(!analyze()) continue;
        int used=0, stage=0;
        int win = decide(target,&used,&stage);
        if(win){
            nwin++;
            if(stage==0) nstage0++; else if(stage==1) nstage1++; else nstage2++;
        } else {
            nnonwin++;
            /* candidate counterexample — print immediately, keep going */
            int len=strlen(line); if(line[len-1]=='\n') line[len-1]=0;
            printf("NONWINNING %s\n",line); fflush(stdout);
        }
        if(used>maxstates2){ maxstates2=used;
            int len=strlen(line); if(len>120) len=120;
            memcpy(worstline,line,len); worstline[len]=0;
            char *nl=strchr(worstline,'\n'); if(nl)*nl=0; }
        hist[ used<=10?0 : used<=100?1 : used<=1000?2 : used<=8192?3 : 4 ]++;
        if(stats_every && nposet%stats_every==0)
            fprintf(stderr,"[progress] posets=%lld lattices=%lld win=%lld\n",
                    nposet,nlat,nwin);
    }
    printf("RESULT k=%d n=%d posets=%lld lattices=%lld winning=%lld nonwinning=%lld\n",
           K,K+2,nposet,nlat,nwin,nnonwin);
    printf("STAGES fastpath=%lld leafclosure=%lld fullclosure=%lld\n",
           nstage0,nstage1,nstage2);
    printf("STATES hist(<=10,<=100,<=1000,<=8192,more)=%lld,%lld,%lld,%lld,%lld maxleaf=%d maxfull=%d\n",
           hist[0],hist[1],hist[2],hist[3],hist[4],maxstates1,maxstates2);
    printf("WORST %s\n",worstline);
    return nnonwin?1:0;
}
