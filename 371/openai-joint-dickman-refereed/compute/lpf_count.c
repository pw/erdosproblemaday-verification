// Segmented largest-prime-factor sieve; counts for Erdős #371 / OpenAI family 012.
// For 2 <= n <= X: inc = #{P(n) < P(n+1)}, dec = #{P(n+1) < P(n)}; 2D histogram of
// (u,v) = (log P(n)/log n, log P(n+1)/log n), bin k = ceil(100*u) in 0..100 (so #{u <= k/100} = sum bins <= k).
// Checkpoints at X in {1,2,5}*10^k. Output: one line per checkpoint (inc dec) + hist dump at each 10^k.
// usage: lpf_count N_MAX threads
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <omp.h>
#define SEG (1<<22)
typedef unsigned long long u64;
static u64 *primes; static long np;
static u64 lpf_of(u64 n){ // direct trial division, used only for the segment-end sentinel cross-check
  u64 best=1; for(long i=0;i<np && primes[i]*primes[i]<=n;i++){u64 p=primes[i]; if(n%p==0){best=p; while(n%p==0)n/=p;}} if(n>1)best=n; return best; }
int main(int argc,char**argv){
  u64 N=strtoull(argv[1],0,10); int T=atoi(argv[2]); omp_set_num_threads(T);
  u64 R=(u64)sqrtl((long double)(N+2))+2; char*c=calloc(R+1,1); primes=malloc(sizeof(u64)*(R/2+10)); np=0;
  for(u64 i=2;i<=R;i++){ if(!c[i]){primes[np++]=i; for(u64 j=i*i;j<=R;j+=i)c[j]=1;} }
  // checkpoints
  u64 cps[64]; int ncp=0; for(u64 p=10;p<=N;p*=10){ u64 m[3]={1,2,5}; for(int k=0;k<3;k++){ if(p*m[k]<=N) cps[ncp++]=p*m[k]; } }
  long nseg=(N+SEG-1)/SEG;  // segment s covers n in [s*SEG, (s+1)*SEG) ; we need P at n and n+1
  // per-segment results stored, then prefix-summed into checkpoints
  u64 *seg_inc=calloc(nseg,8),*seg_dec=calloc(nseg,8);
  // histograms per checkpoint decade: we accumulate per segment into a global hist with atomic adds per decade bucket index
  int ndec=0; u64 decs[32]; for(u64 p=10;p<=N;p*=10) decs[ndec++]=p;
  u64 *H=calloc((size_t)ndec*101*101,8); // H[d][i][j]: counts for n <= decs[d] (cumulative later); we store per-n into smallest d with n<=decs[d]
  // checkpoint partials: counts strictly inside segment up to checkpoint handled by per-n check
  u64 *cp_inc=calloc(ncp,8),*cp_dec=calloc(ncp,8);
  #pragma omp parallel
  {
    u64 *rem=malloc(8*(SEG+1)), *P=malloc(8*(SEG+1));
    u64 *Hl=calloc((size_t)ndec*101*101,8); u64 *ci=calloc(ncp,8),*cd=calloc(ncp,8);
    #pragma omp for schedule(dynamic,1)
    for(long s=0;s<nseg;s++){
      u64 lo=(u64)s*SEG; u64 len=SEG+1; // n in [lo, lo+SEG]
      for(u64 i=0;i<len;i++){rem[i]=lo+i; P[i]=1;}
      for(long k=0;k<np;k++){ u64 p=primes[k]; if(p*p>lo+len) break;
        u64 st=(lo%p==0)?0:(p-lo%p);
        for(u64 i=st;i<len;i+=p){ u64 r=rem[i]; if(r==0) continue; do{r/=p;}while(r%p==0); rem[i]=r; P[i]=p; } }
      for(u64 i=0;i<len;i++){ if(rem[i]>1) P[i]=rem[i]; }
      u64 inc=0,dec=0; int qlo=0,qhi=0; // checkpoints inside this segment get per-n treatment; later ones get the segment total below
      while(qlo<ncp && cps[qlo]<lo) qlo++; qhi=qlo; while(qhi<ncp && cps[qhi]<lo+SEG) qhi++;
      for(u64 i=0;i<SEG;i++){ u64 n=lo+i; if(n<2||n>N) continue;
        u64 a=P[i], b=P[i+1];
        if(a<b) inc++; else if(b<a) dec++;
        for(int q=qlo;q<qhi;q++) if(n<=cps[q]){ if(a<b) ci[q]++; else if(b<a) cd[q]++; }
        double ln=log((double)n); double u=log((double)a)/ln, v=log((double)b)/ln;
        int bi=(int)ceil(100.0*u-1e-12), bj=(int)ceil(100.0*v-1e-12); if(bi<0)bi=0; if(bj<0)bj=0; if(bi>100)bi=100; if(bj>100)bj=100;
        int d=0; while(d<ndec && n>decs[d]) d++; if(d<ndec) Hl[((size_t)d*101+bi)*101+bj]++;
      }
      seg_inc[s]=inc; seg_dec[s]=dec;
      for(int q=qhi;q<ncp;q++){ ci[q]+=inc; cd[q]+=dec; } // whole segment lies below checkpoints q>=qhi
    }
    #pragma omp critical
    { for(size_t z=0;z<(size_t)ndec*101*101;z++) H[z]+=Hl[z]; for(int q=0;q<ncp;q++){cp_inc[q]+=ci[q]; cp_dec[q]+=cd[q];} }
  }
  u64 ti=0,td=0; for(long s=0;s<nseg;s++){ti+=seg_inc[s]; td+=seg_dec[s];}
  printf("TOTAL N=%llu inc=%llu dec=%llu sum=%llu expect=%llu\n",N,ti,td,ti+td,N-1);
  for(int q=0;q<ncp;q++) printf("CP X=%llu inc=%llu dec=%llu inc/X=%.9f dec/X=%.9f\n",cps[q],cp_inc[q],cp_dec[q],(double)cp_inc[q]/cps[q],(double)cp_dec[q]/cps[q]);
  // sentinel cross-check: direct trial division at a few n
  u64 test[6]={N/3+1,N/2+7,N-1,N,999999937ULL<N?999999937ULL:N-2, 2*3*5*7*11*13ULL};
  for(int t=0;t<6;t++) printf("SENTINEL n=%llu P=%llu\n",test[t],lpf_of(test[t]));
  FILE*f=fopen(argv[3]?argv[3]:"hist.bin","wb"); fwrite(&ndec,4,1,f); fwrite(decs,8,ndec,f); fwrite(H,8,(size_t)ndec*101*101,f); fclose(f);
  return 0;
}
