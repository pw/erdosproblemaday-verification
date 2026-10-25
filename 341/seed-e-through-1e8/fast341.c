// fast341.c — Dickson (equal) / Queneau (distinct) greedy extension of a seed by bitset.
// Second implementation, written 2026-10-15 for the E = {1,4,8,10,11,12} run: carry-form branchless shift-or,
// inner loop truncated at min(t, N-t) (sums beyond N are never read), so the cost is ~ density*N^2/256 word-ops.
// Output format identical to greedy341.c (<tag>_elems.u32, uint32 LE) so the two binaries can be cmp'd.
// usage: fast341 N tag distinct(0|1) s1 ... sk
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage: fast341 N tag distinct s1..sk\n");return 2;}
  long N=atol(argv[1]); const char*tag=argv[2]; int distinct=atoi(argv[3]);
  int ns=argc-4; long seed[64]; if(ns>64){fprintf(stderr,"seed too long\n");return 2;}
  for(int i=0;i<ns;i++){ seed[i]=atol(argv[4+i]); if(i&&seed[i]<=seed[i-1]){fprintf(stderr,"seed not increasing\n");return 2;} }
  long W=N/64+4; uint64_t*S=calloc(W,8),*R=calloc(W,8);
  uint32_t*el=malloc(4*(N/2+64)); long ne=0; long M=seed[ns-1];
  #define SETB(B,i) (B[(i)>>6] |= (1ULL<<((i)&63)))
  #define GETB(B,i) ((B[(i)>>6]>>((i)&63))&1ULL)
  for(long t=1;t<=N;t++){
    int in;
    if(t<=M){ in=0; for(int i=0;i<ns;i++) if(seed[i]==t) in=1; if(!in) continue; }
    else { if(GETB(R,t)) continue; }
    // add t: equal rule sets S first (so 2t is forbidden); distinct rule ORs first (2t stays allowed by this pair)
    if(!distinct) SETB(S,t);
    long lim = (N-t < t) ? (N-t) : t;          // only sums t+s with s <= N-t matter, and s <= t covers all of S
    long top = lim>>6; long q=t>>6; int r=t&63;
    if(r==0){ for(long i=0;i<=top;i++) R[i+q] |= S[i]; }
    else { uint64_t prev=0; for(long i=0;i<=top;i++){ uint64_t w=S[i]; R[i+q] |= (w<<r) | (prev>>(64-r)); prev=w; } R[top+1+q] |= prev>>(64-r); }
    if(distinct) SETB(S,t);
    el[ne++]=(uint32_t)t;
  }
  char fn[256]; snprintf(fn,256,"%s_elems.u32",tag); FILE*f=fopen(fn,"wb"); fwrite(el,4,ne,f); fclose(f);
  printf("tag=%s N=%ld distinct=%d seed_k=%d max_seed=%ld count=%ld density=%.6f\n",tag,N,distinct,ns,M,ne,(double)ne/N);
  long G=ne-1; uint32_t*g=malloc(4*(G>0?G:1)); long maxgap=0; for(long i=0;i<G;i++){ g[i]=el[i+1]-el[i]; if(g[i]>maxgap) maxgap=g[i]; }
  printf("gaps=%ld maxgap=%ld last8:",G,maxgap); for(long i=ne-8;i<ne;i++) if(i>=0) printf(" %u",el[i]); printf("\n");
  double fr[3]={0.5,0.75,0.9};
  for(int k=0;k<3;k++){ long s=(long)(G*fr[k]); long L=G-s; if(L<2) continue;
    long*pi=malloc(sizeof(long)*L); pi[0]=0; for(long i=1;i<L;i++){ long j=pi[i-1]; while(j>0&&g[s+i]!=g[s+j]) j=pi[j-1]; if(g[s+i]==g[s+j]) j++; pi[i]=j; }
    long per=L-pi[L-1]; printf("suffix from gap index %ld (len %ld): smallest period %ld %s\n",s,L,per,(per<=L/2)?"(period of THIS SUFFIX only)":"(no period <= half the suffix)"); free(pi);}
  return 0;
}
