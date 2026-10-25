/* Erdős #416 — route B (decorrelated): linear totient sieve phi[n] for n <= M = ceil(6.6*N), then mark phi(n) <= N and the least n.
   Bound used: n/phi(n) < e^gamma loglog n + 3/loglog n < 6.55 for 3 <= n <= 1e10 (Rosser–Schoenfeld 1962, Thm 15) => every n with
   phi(n) <= N has n <= 6.55 N. Writes <prefix>.bits and <prefix>.ell (uint64[N+1]). Usage: vsieve N prefix */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char**argv){
  uint64_t N=strtoull(argv[1],0,10); const char*pre=argv[2]; uint64_t M=(uint64_t)(6.6*(double)N)+10;
  uint32_t *phi=malloc((M+1)*4); uint32_t *pr=malloc(((M/8)+1000)*4); uint64_t np=0;
  for(uint64_t i=0;i<=M;i++) phi[i]=0; phi[1]=1;
  for(uint64_t i=2;i<=M;i++){ if(phi[i]==0){ phi[i]=(uint32_t)(i-1); pr[np++]=(uint32_t)i; }
    for(uint64_t j=0;j<np;j++){ uint64_t p=pr[j], ip=i*p; if(ip>M) break;
      if(i%p==0){ phi[ip]=phi[i]*(uint32_t)p; break; } else phi[ip]=phi[i]*(uint32_t)(p-1); } }
  uint8_t*bits=calloc(N/8+1,1); uint64_t*ell=malloc((N+1)*8); for(uint64_t i=0;i<=N;i++) ell[i]=UINT64_MAX;
  uint64_t maxratio_n=0;
  for(uint64_t n=1;n<=M;n++){ uint64_t v=phi[n]; if(v<=N){ bits[v>>3]|=(uint8_t)(1u<<(v&7)); if(n<ell[v]) ell[v]=n; if(n> maxratio_n && n>5*v) maxratio_n=n; } }
  /* guard: the largest n/phi(n) seen among n<=M must stay below 6.55 for the bound to cover */
  double mx=0; for(uint64_t n=3;n<=M;n++){ double r=(double)n/phi[n]; if(r>mx) mx=r; }
  fprintf(stderr,"M=%llu max n/phi(n) on [3,M] = %.6f (bound 6.55 needed)\n",(unsigned long long)M,mx);
  char fn[512]; snprintf(fn,512,"%s.bits",pre); FILE*f=fopen(fn,"wb"); fwrite(bits,1,N/8+1,f); fclose(f);
  snprintf(fn,512,"%s.ell",pre); f=fopen(fn,"wb"); fwrite(ell,8,N+1,f); fclose(f);
  return mx<6.55?0:3;
}
