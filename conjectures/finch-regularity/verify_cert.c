/* verify_cert.c -- independent verifier for regularity certificates of the
 * 1-additive sequence U(a,b).  Written from the statement of the theorem, not
 * ported from cert2.py: exact phase is the same definition but the cycle is
 * found by Brent's algorithm (O(1) memory) rather than by a hash table, and
 * the residue/finite checks are re-derived here.
 *
 * Usage: ./verify_cert a b X0 [MAXB]      (MAXB caps the memory: ~5 bytes/unit)
 * Prints:  a b PASS W X1 P nR B   or   a b FAIL <reason>
 *
 * All arithmetic is exact integer arithmetic.  No floating point.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;

static long X0, Wid, HALF, NW;      /* window: HALF bits, NW 64-bit words */
static int  nE, offs[64];           /* bit offsets of the even elements    */

/* ---------- window state helpers ---------- */
static inline int getbit(const u64 *s, long i){ return (s[i>>6] >> (i&63)) & 1ULL; }

/* one automaton step: returns the new element bit, updates state in place */
static inline int step(u64 *s)
{
    int c = 0;
    for (int i = 0; i < nE; i++) { if (getbit(s, offs[i])) { if (++c > 1) break; } }
    int hit = (c == 1);
    /* shift left by one bit across NW words, insert hit at bit 0 */
    u64 carry = (u64)hit;
    for (long w = 0; w < NW; w++) {
        u64 nc = s[w] >> 63;
        s[w] = (s[w] << 1) | carry;
        carry = nc;
    }
    long top = HALF & 63;                    /* mask off bits >= HALF */
    if (top) s[NW-1] &= (1ULL << top) - 1ULL;
    return hit;
}

int main(int argc, char **argv)
{
    int a = atoi(argv[1]), b = atoi(argv[2]);
    X0 = atol(argv[3]);
    long MAXB = argc > 4 ? atol(argv[4]) : 200000000L;

    /* ---------- (1) exact U(a,b) on [0,X0] ---------- */
    int *terms = malloc(sizeof(int)*(size_t)(X0+2));
    unsigned char *cnt = calloc((size_t)(X0+2),1);
    if(!terms||!cnt){ printf("%d %d FAIL oom\n",a,b); return 1; }
    int k=0; terms[k++]=a;
    if ((long)a+b<=X0) cnt[a+b]=1;
    terms[k++]=b;
    for (long x=b+1; x<=X0; x++){
        if (cnt[x]!=1) continue;
        for (int i=0;i<k;i++){ long s=(long)terms[i]+x; if(s>X0) break; if(cnt[s]<2) cnt[s]++; }
        terms[k++]=(int)x;
    }
    free(cnt);

    long E[64]; nE=0;
    for (int i=0;i<k;i++) if((terms[i]&1)==0){ if(nE<64) E[nE++]=terms[i]; }
    if (nE==0){ printf("%d %d FAIL no-even-elements\n",a,b); return 1; }
    Wid = E[nE-1];
    if (Wid*4 > X0){ printf("%d %d FAIL W=%ld too close to X0=%ld\n",a,b,Wid,X0); return 1; }
    HALF = Wid/2; NW = (HALF+63)/64;
    for (int i=0;i<nE;i++) offs[i] = (int)(E[i]/2 - 1);

    /* ---------- (2) seed the window at the first odd x > X0 ---------- */
    /* membership on [0,X0] as a bitmap for seeding */
    unsigned char *inSmall = calloc((size_t)(X0+2),1);
    for (int i=0;i<k;i++) inSmall[terms[i]]=1;
    long xstart = (X0%2==0)? X0+1 : X0+2;
    u64 *s0 = calloc((size_t)NW,8);
    for (long j=0;j<HALF;j++){ long y = xstart - 2*(j+1); if (y>0 && y<=X0 && inSmall[y]) s0[j>>6] |= 1ULL<<(j&63); }

    /* ---------- (3) Brent cycle detection on the state map ---------- */
    u64 *tort = malloc((size_t)NW*8), *hare = malloc((size_t)NW*8), *tmp = malloc((size_t)NW*8);
    memcpy(tort, s0, (size_t)NW*8);
    memcpy(hare, s0, (size_t)NW*8); step(hare);
    long power=1, lam=1;
    while (memcmp(tort,hare,(size_t)NW*8)!=0){
        if (power==lam){ memcpy(tort,hare,(size_t)NW*8); power*=2; lam=0; }
        step(hare); lam++;
        if (lam > 1500000000L){ printf("%d %d FAIL no-cycle-within-step-budget\n",a,b); return 1; }
    }
    /* find mu */
    memcpy(tort,s0,(size_t)NW*8);
    memcpy(hare,s0,(size_t)NW*8);
    for (long i=0;i<lam;i++) step(hare);
    long mu=0;
    while (memcmp(tort,hare,(size_t)NW*8)!=0){ step(tort); step(hare); mu++; }

    long X1 = xstart + 2*mu, P = 2*lam;
    long B  = 2*X1 + 4*P + 2*Wid + 4;
    if (B > MAXB){ printf("%d %d FAIL B=%ld exceeds MAXB=%ld (X1=%ld P=%ld)\n",a,b,B,MAXB,X1,P); return 1; }

    /* ---------- (4) materialise U* on [0,B] ---------- */
    unsigned char *inU = calloc((size_t)(B+2),1);
    if(!inU){ printf("%d %d FAIL oom-B=%ld\n",a,b,B); return 1; }
    for (int i=0;i<k;i++) inU[terms[i]]=1;
    memcpy(tmp,s0,(size_t)NW*8);
    for (long x=xstart; x<=B; x+=2){ if (step(tmp)) inU[x]=1; }
    /* NOTE: step() computes the bit for x from the window *before* the shift,
       so the value returned at loop iteration x is exactly [x in U*]. */

    /* ---------- (5) residue analysis ---------- */
    unsigned char *inR = calloc((size_t)P,1);
    long nR=0;
    for (long y=X1; y<X1+P; y+=2) if (inU[y]) { inR[y%P]=1; nR++; }

    /* small odd elements: odd members of U* below X1 */
    long nsmall=0;
    long *small = malloc(sizeof(long)*(size_t)(X1/2+2));
    for (long y=1; y<X1; y+=2) if (inU[y]) small[nsmall++]=y;

    /* sumset R+R over Z_P, computed by enumerating pairs and stopping as soon
       as every even class is covered (the generic case) */
    long *Rl = malloc(sizeof(long)*(size_t)(nR+1)); long nl=0;
    for (long r=0;r<P;r++) if (inR[r]) Rl[nl++]=r;
    unsigned char *hit = calloc((size_t)P,1);
    long unhit = P/2;
    for (long i=0;i<nl && unhit;i++)
        for (long j=0;j<nl;j++){
            long c = Rl[i]+Rl[j]; if (c>=P) c-=P;
            if (!hit[c]){ hit[c]=1; if(--unhit==0) break; }
        }

    long badclass=-1;
    for (long c=0; c<P; c+=2){
        if (hit[c]) continue;                        /* A(x) >= 2 for x >= B */
        long beta=0;
        for (long i=0;i<nsmall;i++){ long t=((c-small[i])%P+P)%P; if(inR[t]) if(++beta>1) break; }
        if (beta==1){ badclass=c; break; }           /* beta==0 is fine: no reps at all */
    }
    if (badclass>=0){ printf("%d %d FAIL residue-class-%ld-has-exactly-one-rep\n",a,b,badclass); return 1; }

    /* ---------- (6) finite check: even x in (X0,B] must have != 1 reps ---------- */
    long *pos = malloc(sizeof(long)*(size_t)(B/2+4)); long np=0;
    for (long y=1;y<=B;y++) if (inU[y]) pos[np++]=y;
    long badx=-1;
    for (long x=(X0%2==0? X0+2 : X0+1); x<=B; x+=2){
        long c2=0;
        for (long i=0;i<np;i++){ long u=pos[i]; if (2*u>=x) break; if (inU[x-u]) { if(++c2>1) break; } }
        if (c2==1){ badx=x; break; }
    }
    if (badx>=0){ printf("%d %d FAIL even-%ld-has-exactly-one-rep\n",a,b,badx); return 1; }

    printf("%d %d PASS W=%ld X0=%ld X1=%ld P=%ld nR=%ld B=%ld E=",a,b,Wid,X0,X1,P,nR,B);
    for (int i=0;i<nE;i++) printf("%s%ld", i?",":"", E[i]);
    printf("\n");
    return 0;
}
