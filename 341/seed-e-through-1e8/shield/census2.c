// census2.c — forced rail dynamics of a Li-type controller for an ARBITRARY doubling cycle P = {x 2^i mod M} in Z/M,
// with the carry of every rail computed (c_i = [2 x_i >= M]), not only the last->first wrap as in erdos341q/census.c.
// Rails sorted by residue; rail j with predecessor i (2 x_i = x_j mod M) obeys Y_j[q] = [q - c_i not in Y_i (+) Y_i]
// for q > q0 (equal rule: +, strict rule: distinct summands). Initial conditions = all rail contents on q <= q0, restricted
// to ICs in which every rail has at least one element (Lemma 5's hypothesis). Reports the period histogram of the
// packed-rail word on the suffix [Q/2, Q) and lists ICs with no period <= Pmax.
// usage: census2 M x L strict q0 Q Pmax
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXL 8
static int M,x,L,strict,q0,Q,Pmax; static int xr[MAXL],pred[MAXL],carry[MAXL];
static uint64_t *Y[MAXL],*S[MAXL]; static unsigned char*W;
static inline int get(uint64_t*b,int i){return (b[i>>6]>>(i&63))&1;}
static inline void set(uint64_t*b,int i){b[i>>6]|=1ULL<<(i&63);}
static void add(int i,int q){ set(Y[i],q); int WQ=(Q+63)/64; int words=(q>>6)+1;
  for(int w=0;w<words;w++){ uint64_t v=Y[i][w]; if(!v) continue; int sh=q&63; int base=(w<<6)+q; uint64_t lo=v<<sh, hi=sh?v>>(64-sh):0;
    int wi=base>>6; if(wi<WQ) S[i][wi]|=lo; if(hi&&wi+1<WQ) S[i][wi+1]|=hi; } }
#define ADD(i,q) do{int qq=(q),tq=2*qq; int was=(tq<Q)?get(S[i],tq):1; add(i,qq); if(strict&&!was&&tq<Q) S[i][tq>>6]&=~(1ULL<<(tq&63));}while(0)
static int run_ic(uint64_t ic){ int WQ=(Q+63)/64; for(int i=0;i<L;i++){memset(Y[i],0,WQ*8);memset(S[i],0,WQ*8);}
  for(int i=0;i<L;i++) for(int q=0;q<=q0;q++) if((ic>>(i*(q0+1)+q))&1) ADD(i,q);
  for(int q=q0+1;q<Q;q++) for(int j=0;j<L;j++){ int i=pred[j]; int qq=q-carry[i]; if(qq>=0 && !get(S[i],qq)) ADD(j,q); }
  for(int q=0;q<Q;q++){unsigned char w=0; for(int i=0;i<L;i++) w|=get(Y[i],q)<<i; W[q]=w;}
  int Lh=Q/2; for(int P=1;P<=Pmax;P++){ int ok=1; for(int q=Lh;q+P<Q;q++) if(W[q]!=W[q+P]){ok=0;break;} if(ok) return P; } return 0; }
int main(int argc,char**argv){ if(argc<8){fprintf(stderr,"usage: census2 M x L strict q0 Q Pmax\n");return 2;}
  M=atoi(argv[1]);x=atoi(argv[2]);L=atoi(argv[3]);strict=atoi(argv[4]);q0=atoi(argv[5]);Q=atoi(argv[6]);Pmax=atoi(argv[7]);
  if(L>MAXL||L*(q0+1)>62){fprintf(stderr,"too big\n");return 2;}
  int res[MAXL]; for(int i=0;i<L;i++) res[i]=(int)(((long)x<<i)%M);
  // sort by residue
  for(int i=0;i<L;i++) for(int j=i+1;j<L;j++) if(res[j]<res[i]){int t=res[i];res[i]=res[j];res[j]=t;}
  for(int i=0;i<L;i++){ xr[i]=res[i]; carry[i]=(2*res[i]>=M); }
  for(int j=0;j<L;j++){ pred[j]=-1; for(int i=0;i<L;i++) if((2*xr[i])%M==xr[j]) pred[j]=i; if(pred[j]<0){fprintf(stderr,"no predecessor\n");return 2;} }
  printf("M=%d x=%d L=%d strict=%d rails:",M,x,L,strict); for(int j=0;j<L;j++) printf(" %d<-%d(c%d)",xr[j],xr[pred[j]],carry[pred[j]]); printf("\n");
  int WQ=(Q+63)/64; for(int i=0;i<L;i++){Y[i]=calloc(WQ,8);S[i]=calloc(WQ,8);} W=calloc(Q,1);
  long nic=1L<<(L*(q0+1)); long hist[64]={0}; long nap=0, tested=0; uint64_t railmask=(1ULL<<(q0+1))-1;
  for(uint64_t ic=0;ic<(uint64_t)nic;ic++){ int ok=1; for(int i=0;i<L;i++) if(!((ic>>(i*(q0+1)))&railmask)) ok=0; if(!ok) continue; tested++;
    int P=run_ic(ic); if(P==0){ nap++; if(nap<=5){ printf("APERIODIC-TO-Q ic=%llu\n",(unsigned long long)ic);} } else if(P<64) hist[P]++; else hist[63]++; }
  printf("ICs tested=%ld (every rail nonempty on q<=%d) aperiodic-to-Q=%ld; period histogram:",tested,q0,nap); for(int p=1;p<64;p++) if(hist[p]) printf(" %d:%ld",p,hist[p]); printf("\n"); return 0; }
