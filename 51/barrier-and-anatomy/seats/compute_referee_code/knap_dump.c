// Independent ell(a) for all a <= A by a multiplicative 0/1 group knapsack over primes
// (NOT a sieve over n): best[a] = least n with phi(n)=a using primes processed so far.
// For each prime p and k>=1: phi(p^k) = (p-1)p^(k-1), extend every a (descending, in place).
// Only even a stored (index a/2); a=1 handled separately. Values uint32, 0 = none, UINT32_MAX = saturated.
// Usage: knap A dumpthresholdR dumpthresholdW outfile
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static uint32_t *best; static uint64_t A;
static inline void upd(uint64_t t, uint64_t cand){ // t even
  uint32_t c = cand >= 0xFFFFFFFFull ? 0xFFFFFFFFu : (uint32_t)cand;
  uint32_t *b=&best[t>>1]; if(*b==0 || c<*b) *b=c; }
int main(int argc,char**argv){
  A=strtoull(argv[1],0,10); double thrR=atof(argv[2]), thrW=atof(argv[3]); FILE*dump=fopen(argv[4],"w");
  uint64_t M=A+1; // primes p <= A+1
  uint8_t *comp=calloc(M/16+2,1); // odd-only bitset
  #define ISC(i) (comp[(i)>>4]&(1<<(((i)>>1)&7)))
  for(uint64_t i=3;i*i<=M;i+=2) if(!ISC(i)) for(uint64_t j=i*i;j<=M;j+=2*i) comp[j>>4]|=1<<((j>>1)&7);
  best=calloc(A/2+1,4); if(!best){fprintf(stderr,"oom\n");return 1;}
  // p = 2: 2^k, k>=2 : phi = 2^(k-1), from a=1 only (nothing else exists yet). 2^1 skipped (phi(2)=phi(1)).
  for(uint64_t k=2;;k++){ uint64_t a2=1ull<<(k-1); if(a2>A)break; upd(a2,1ull<<k); }
  for(uint64_t p=3;p<=M;p+=2){ if(ISC(p)) continue;
    uint64_t hi=A/(p-1); // a*(p-1) <= A
    for(uint64_t a=hi&~1ull; a>=2; a-=2){ uint32_t v=best[a>>1]; if(!v) continue;
      uint64_t m=p-1, pk=p;
      while(1){ u128 t=(u128)a*m; if(t>A)break;
        uint64_t cand = (v==0xFFFFFFFFu)? ~0ull : ((u128)v*pk > 0xFFFFFFFFull ? ~0ull : (uint64_t)v*pk);
        upd((uint64_t)t,cand); if(m>A/p)break; m*=p; pk = (pk>0xFFFFFFFFull)?pk:pk*p; }
    }
    // a = 1 (n=1) last
    { uint64_t m=p-1, pk=p; while(m<=A){ upd(m, pk>0xFFFFFFFFull?~0ull:pk); if(m>A/p)break; m*=p; pk = (pk>0xFFFFFFFFull)?pk:pk*p; } }
  }
  { FILE*bf=fopen("knap_ell.bin","wb"); fwrite(best,4,A/2+1,bf); fclose(bf); }
  // analysis
  static const uint64_t F[5]={3,5,17,257,65537};
  uint64_t cnt=1, viol=0, sat=0, hist[64]={0}, histf[64]={0}; double maxR=1,maxW=1; uint64_t maxRa=1,maxWa=1, maxRn=1, maxWn=1;
  // a=1: n=1, R=1,T=1,W=1 -> hist bin 0
  hist[0]++; histf[0]++;
  for(uint64_t a=2;a<=A;a+=2){ uint32_t v=best[a>>1]; if(!v) continue; cnt++;
    if(v==0xFFFFFFFFu){sat++; continue;}
    uint64_t n=v; uint64_t Tn=1,Td=1; int fs=0;
    for(int j=0;j<5;j++){ if(n%F[j]==0 && (n/F[j])%F[j]!=0){ Tn*=F[j]; Td*=F[j]-1; fs=1; } }
    if(n%4==0){ if(fs) viol++; Tn=2; Td=1; }
    else if(n%2==0){ fprintf(stderr,"n=2 mod 4 least?? a=%llu n=%llu\n",(unsigned long long)a,(unsigned long long)n); }
    double R=(double)n/(double)a; double W=R*(double)Td/(double)Tn;
    // exact bin: floor(32*(W-1)) = floor(32*(n*Td - a*Tn)/(a*Tn))
    u128 num=(u128)n*Td, den=(u128)a*Tn; int b; if(num<den) b=-1; else { u128 q=((num-den)*32)/den; b = q>63?63:(int)q; }
    if(b<0){fprintf(stderr,"W<1 a=%llu\n",(unsigned long long)a); b=0;}
    hist[b]++;
    int bf=(int)((W-1.0)*32.0); if(bf>63)bf=63; if(bf<0)bf=0; histf[bf]++;
    if(R>maxR){maxR=R;maxRa=a;maxRn=n;} if(W>maxW){maxW=W;maxWa=a;maxWn=n;}
    if(R>thrR || W>thrW || n<=1000000) fprintf(dump,"%llu\t%llu\t%.12f\t%.12f\n",(unsigned long long)a,(unsigned long long)n,R,W);
  }
  fclose(dump);
  printf("A=%llu V(A)=%llu saturated=%llu viol=%llu\n",(unsigned long long)A,(unsigned long long)cnt,(unsigned long long)sat,(unsigned long long)viol);
  printf("max R=%.9f at a=%llu (n=%llu); max W=%.9f at a=%llu (n=%llu)\n",maxR,(unsigned long long)maxRa,(unsigned long long)maxRn,maxW,(unsigned long long)maxWa,(unsigned long long)maxWn);
  for(int b=0;b<64;b++) if(hist[b]||histf[b]) printf("  bin %2d [%.4f,%.4f): exact %llu float %llu\n",b,1+b/32.0,1+(b+1)/32.0,(unsigned long long)hist[b],(unsigned long long)histf[b]);
  return 0; }
