/* Erdős #416 / OpenAI family 24 — exact totient-value census by prime-power DFS (route A).
   Marks every v = phi(n) <= N in a bitset (n ranges over ALL n with phi(n) <= N, generated as products of prime powers
   with increasing primes). Also records the least preimage ell(v) for v <= NL (uint64), checks nothing else.
   Usage: vdfs N NL outprefix   (writes <prefix>.bits (bitset), <prefix>.ell (uint64[NL+1]))  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint64_t N, NL; static uint8_t *bits; static uint64_t *ell; static uint32_t *pr; static uint64_t np; static uint64_t nodes=0;
static inline void mark(uint64_t v, uint64_t n){ bits[v>>3] |= (uint8_t)(1u<<(v&7)); if(v<=NL && n<ell[v]) ell[v]=n; nodes++; }
static void dfs(uint64_t v, uint64_t n, uint64_t idx){
  for(uint64_t i=idx;i<np;i++){ uint64_t p=pr[i]; if(v*(p-1)>N) break;
    uint64_t v2=v*(p-1), n2=n*p;
    for(;;){ mark(v2,n2); dfs(v2,n2,i+1); if(v2>N/p) break; v2*=p; n2*=p; } }
}
int main(int argc,char**argv){
  N=strtoull(argv[1],0,10); NL=strtoull(argv[2],0,10); const char*pre=argv[3];
  uint64_t M=N+1; uint8_t *comp=calloc(M/2+1,1); /* odd sieve */
  for(uint64_t i=3;i*i<=M;i+=2) if(!comp[i/2]) for(uint64_t j=i*i;j<=M;j+=2*i) comp[j/2]=1;
  uint64_t cnt=1; for(uint64_t i=3;i<=M;i+=2) if(!comp[i/2]) cnt++;
  if(cnt>0xffffffffULL||M>0xffffffffULL){fprintf(stderr,"N too big for uint32 primes\n");return 1;}
  pr=malloc(cnt*4); np=0; pr[np++]=2; for(uint64_t i=3;i<=M;i+=2) if(!comp[i/2]) pr[np++]=(uint32_t)i; free(comp);
  fprintf(stderr,"primes<=%llu: %llu\n",(unsigned long long)M,(unsigned long long)np);
  bits=calloc(N/8+1,1); ell=malloc((NL+1)*8); for(uint64_t i=0;i<=NL;i++) ell[i]=UINT64_MAX;
  mark(1,1); /* phi(1)=1 */ dfs(1,1,0);
  fprintf(stderr,"nodes=%llu\n",(unsigned long long)nodes);
  char fn[512]; snprintf(fn,512,"%s.bits",pre); FILE*f=fopen(fn,"wb"); fwrite(bits,1,N/8+1,f); fclose(f);
  snprintf(fn,512,"%s.ell",pre); f=fopen(fn,"wb"); fwrite(ell,8,NL+1,f); fclose(f);
  return 0;
}
