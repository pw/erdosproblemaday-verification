/* Erdős #416 — seed search to N: for thresholds t_i, mark S_i = { phi(n) <= N : n <= t_i * phi(n) }.
   A totient d (bit in V) NOT in S_i has every preimage n > t_i d, i.e. ell(d) > t_i d. Writes <prefix>.V and <prefix>.S<i>. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static uint64_t N; static uint8_t *V,*S[3]; static double T[3]={2.0414,2.5,3.0}; static uint32_t *pr; static uint64_t np;
static inline void setb(uint8_t*b,uint64_t v){ b[v>>3]|=(uint8_t)(1u<<(v&7)); }
static inline void mark(uint64_t v,uint64_t n){ setb(V,v); for(int i=0;i<3;i++) if((double)n<=T[i]*(double)v) setb(S[i],v); }
static void dfs(uint64_t v,uint64_t n,uint64_t idx){
  for(uint64_t i=idx;i<np;i++){ uint64_t p=pr[i]; if(v*(p-1)>N) break; uint64_t v2=v*(p-1),n2=n*p;
    for(;;){ mark(v2,n2); dfs(v2,n2,i+1); if(v2>N/p) break; v2*=p; n2*=p; } } }
int main(int argc,char**argv){ N=strtoull(argv[1],0,10); const char*pre=argv[2]; uint64_t M=N+1;
  uint8_t*c=calloc(M/2+1,1); for(uint64_t i=3;i*i<=M;i+=2) if(!c[i/2]) for(uint64_t j=i*i;j<=M;j+=2*i) c[j/2]=1;
  uint64_t cnt=1; for(uint64_t i=3;i<=M;i+=2) if(!c[i/2]) cnt++; pr=malloc(cnt*4); np=0; pr[np++]=2;
  for(uint64_t i=3;i<=M;i+=2) if(!c[i/2]) pr[np++]=(uint32_t)i; free(c);
  V=calloc(N/8+1,1); for(int i=0;i<3;i++) S[i]=calloc(N/8+1,1);
  mark(1,1); dfs(1,1,0);
  char fn[512]; FILE*f; snprintf(fn,512,"%s.V",pre); f=fopen(fn,"wb"); fwrite(V,1,N/8+1,f); fclose(f);
  for(int i=0;i<3;i++){ snprintf(fn,512,"%s.S%d",pre,i); f=fopen(fn,"wb"); fwrite(S[i],1,N/8+1,f); fclose(f);} return 0; }
