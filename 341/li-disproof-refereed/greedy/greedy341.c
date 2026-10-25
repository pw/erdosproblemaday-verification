// greedy341.c — Dickson greedy extension of a seed by bitset. Independent of Li's files.
// usage: greedy341 N tag distinct(0|1) s1 s2 ... sk
// rule equal   (distinct=0): a_{n+1} = least t > a_n with t != a_i + a_j for all i,j<=n (i=j allowed)
// rule distinct(distinct=1): same with i<j only (Queneau variant)
// writes <tag>_elems.u32 (all elements <= N, uint32 LE) and prints a summary.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint64_t *S,*R; static long W;
#define SETB(B,i) (B[(i)>>6] |= (1ULL<<((i)&63)))
#define GETB(B,i) ((B[(i)>>6]>>((i)&63))&1ULL)
static void shift_or(long t){ // R |= S << t, using only words of S up to t (S subset [0,t])
  long q=t>>6, r=t&63, top=t>>6;
  for(long i=0;i<=top;i++){ uint64_t w=S[i]; if(!w) continue;
    if(i+q<W) R[i+q] |= w<<r;
    if(r && i+q+1<W) R[i+q+1] |= w>>(64-r);
  }
}
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 2;}
  long N=atol(argv[1]); const char*tag=argv[2]; int distinct=atoi(argv[3]);
  int ns=argc-4; long *seed=malloc(sizeof(long)*ns); for(int i=0;i<ns;i++) seed[i]=atol(argv[4+i]);
  for(int i=1;i<ns;i++) if(seed[i]<=seed[i-1]){fprintf(stderr,"seed not increasing\n");return 2;}
  W=N/64+3; S=calloc(W,8); R=calloc(W,8);
  uint32_t *el=malloc(sizeof(uint32_t)*(N/2+16)); long ne=0;
  for(int i=0;i<ns;i++){ long t=seed[i]; if(distinct){shift_or(t); SETB(S,t);} else {SETB(S,t); shift_or(t);} el[ne++]=(uint32_t)t; }
  long M=seed[ns-1];
  for(long t=M+1;t<=N;t++){ if(GETB(R,t)) continue; if(distinct){shift_or(t); SETB(S,t);} else {SETB(S,t); shift_or(t);} el[ne++]=(uint32_t)t; }
  char fn[256]; snprintf(fn,256,"%s_elems.u32",tag); FILE*f=fopen(fn,"wb"); fwrite(el,4,ne,f); fclose(f);
  printf("tag=%s N=%ld distinct=%d seed_k=%d max_seed=%ld count=%ld density=%.6f\n",tag,N,distinct,ns,M,ne,(double)ne/N);
  printf("first120:"); for(long i=0;i<ne&&i<120;i++) printf(" %u",el[i]); printf("\n");
  printf("last8:"); for(long i=ne-8;i<ne;i++) if(i>=0) printf(" %u",el[i]); printf("\n");
  // residue census mod 49 for elements > M
  long cen[49]={0}; for(long i=0;i<ne;i++) if(el[i]>M) cen[el[i]%49]++;
  printf("mod49 census (elements>max_seed):"); for(int r=0;r<49;r++) if(cen[r]) printf(" %d:%ld",r,cen[r]); printf("\n");
  // gap sequence period probe on suffixes: smallest period of gap[s..ne-2] via prefix function
  long G=ne-1; uint32_t*g=malloc(4*(G>0?G:1)); for(long i=0;i<G;i++) g[i]=el[i+1]-el[i];
  long maxgap=0; for(long i=0;i<G;i++) if(g[i]>maxgap) maxgap=g[i];
  printf("gaps=%ld maxgap=%ld\n",G,maxgap);
  double fr[3]={0.5,0.75,0.9};
  for(int k=0;k<3;k++){ long s=(long)(G*fr[k]); long L=G-s; if(L<2) continue;
    long *pi=malloc(sizeof(long)*L); pi[0]=0; for(long i=1;i<L;i++){ long j=pi[i-1]; while(j>0 && g[s+i]!=g[s+j]) j=pi[j-1]; if(g[s+i]==g[s+j]) j++; pi[i]=j; }
    long per=L-pi[L-1]; printf("suffix from gap index %ld (len %ld): smallest period %ld %s\n",s,L,per, (per<=L/2)?"(a period of THIS SUFFIX only; says nothing about the infinite sequence)":"(no period <= half the suffix)");
    free(pi); }
  return 0;
}
