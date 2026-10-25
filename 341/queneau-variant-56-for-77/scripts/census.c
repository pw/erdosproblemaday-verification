// Census of rail initial conditions for the m-gate Li controller under EQUAL or STRICT rule.
// usage: ./census m strict q0 Q Pmax   (enumerates all 2^(m*(q0+1)) ICs; prints period histogram + aperiodic candidates)
//        ./census m strict q0 Q Pmax icmask   (single IC, prints rails)
// Bits: ic bit (i*(q0+1)+q) = Y_i[q].  Period test on the suffix [Q/2, Q): smallest P ≤ Pmax with W[q+P]==W[q] there.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXM 4
static int m, strict, q0, Q, Pmax;
static uint64_t *Y[MAXM], *S[MAXM]; // bitsets of length Q
static unsigned char *W;             // packed rails per q
static inline int get(uint64_t*b,int i){return (b[i>>6]>>(i&63))&1;}
static inline void set(uint64_t*b,int i){b[i>>6]|=1ULL<<(i&63);}
static void add(int i,int q){ // Y_i[q]=1; sums += q + u for u in Y_i (u!=q if strict)
  set(Y[i],q);
  // OR shifted copy of Y_i[0..q] into S[i] at offset q: S |= Y_i << q, restricted to indices <= 2q and < Q
  int words=(q>>6)+1;
  for(int w=0;w<words;w++){ uint64_t x=Y[i][w]; if(!x) continue;
    // position of this word after shifting by q
    int sh=q&63; int base=(w<<6)+q; // bit (w*64+b) goes to base+b
    uint64_t lo=x<<sh, hi= sh? x>>(64-sh):0;
    int wi=base>>6; if(wi<(Q+63)/64) S[i][wi]|=lo; if(hi && wi+1<(Q+63)/64) S[i][wi+1]|=hi; }
  if(strict){ // remove the double 2q (only if it was NOT already present from a distinct pair)
    // careful: 2q may be a sum u+v with u!=v, u,v<=q, (u,v)!=(q,q) — it was already in S before this add iff so.
    // So: recompute membership of 2q from distinct pairs: it is in S_before OR comes from (q,q). We saved nothing, so
    // handle by checking before OR-ing: done in caller via 'was' flag.
  }
}
static int run_ic(uint64_t ic){
  int WQ=(Q+63)/64;
  for(int i=0;i<m;i++){memset(Y[i],0,WQ*8);memset(S[i],0,WQ*8);}
  // strict rule: we must not insert 2q from the pair (q,q).  Implement add as: was=get(S,2q); add(); if strict && !was: clear(2q).
  #define ADD(i,q) do{ int qq=(q); int tq=2*qq; int was=(tq<Q)?get(S[i],tq):1; add(i,qq); if(strict && !was && tq<Q) S[i][tq>>6]&=~(1ULL<<(tq&63)); }while(0)
  for(int i=0;i<m;i++) for(int q=0;q<=q0;q++) if((ic>>(i*(q0+1)+q))&1) ADD(i,q);
  for(int q=q0+1;q<Q;q++){
    if(!get(S[m-1],q-1)) ADD(0,q);
    for(int i=1;i<m;i++) if(!get(S[i-1],q)) ADD(i,q);
  }
  for(int q=0;q<Q;q++){unsigned char w=0; for(int i=0;i<m;i++) w|=get(Y[i],q)<<i; W[q]=w;}
  // suffix period
  int L=Q/2;
  for(int P=1;P<=Pmax;P++){ int ok=1; for(int q=L;q+P<Q;q++) if(W[q]!=W[q+P]){ok=0;break;} if(ok) return P; }
  return 0;
}
int main(int argc,char**argv){
  m=atoi(argv[1]); strict=atoi(argv[2]); q0=atoi(argv[3]); Q=atoi(argv[4]); Pmax=atoi(argv[5]);
  int WQ=(Q+63)/64; for(int i=0;i<m;i++){Y[i]=calloc(WQ,8);S[i]=calloc(WQ,8);} W=calloc(Q,1);
  if(argc>6){ uint64_t ic=strtoull(argv[6],0,0); int P=run_ic(ic); printf("ic=%llu period=%d\n",(unsigned long long)ic,P);
    if(argc>7 && !strcmp(argv[7],"runs")){ for(int i=0;i<m;i++){ printf("Y%d runs:",i); int q=0; while(q<Q){ if(get(Y[i],q)){int s=q; while(q<Q&&get(Y[i],q)) q++; printf(" (%d,%d)",s,q-1);} else q++; } printf("\n"); } return 0; }
    for(int i=0;i<m;i++){printf("Y%d: ",i); for(int q=0;q<(Q<200?Q:200);q++) putchar(get(Y[i],q)?'1':'0'); putchar('\n');} return 0; }
  int nb=m*(q0+1); uint64_t n=1ULL<<nb; int *hist=calloc(Pmax+1,sizeof(int)); int nap=0;
  for(uint64_t ic=0;ic<n;ic++){ int P=run_ic(ic); hist[P]++; if(P==0){ nap++; printf("APERIODIC-TO-Q ic=%llu bits=",(unsigned long long)ic);
      for(int i=0;i<m;i++){ for(int q=0;q<=q0;q++) putchar(((ic>>(i*(q0+1)+q))&1)?'1':'0'); if(i<m-1) putchar(','); } putchar('\n'); fflush(stdout);} }
  printf("m=%d strict=%d q0=%d Q=%d Pmax=%d ICs=%llu aperiodic-to-Q=%d\n",m,strict,q0,Q,Pmax,(unsigned long long)n,nap);
  printf("period histogram (P:count):"); for(int P=1;P<=Pmax;P++) if(hist[P]) printf(" %d:%d",P,hist[P]); printf("\n");
  return 0;
}
