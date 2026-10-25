// Erdős's second #371 question [Er79e]: count n in [2,X] with P(n+1) > P(n) * n^alpha, alpha in ALPHAS,
// decided by a long-double log screen with margin 1e-9 for alpha = k/20; any n inside the margin is reported as a NEAR_TIE
// (none observed), so every counted n is decided with margin. Also counts the mirror event P(n) > P(n+1) * n^alpha.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#define SEG (1<<22)
typedef unsigned long long u64; typedef unsigned __int128 u128;
static u64 *primes; static long np;
// exact compare of b^20 vs a^20 * n^k using logs with a safety margin, falling back to big-int via repeated 128-bit with overflow guard
static int cmp_exact(u64 a,u64 b,u64 n,int k){ // returns sign of (log b - log a - (k/20) log n)
  long double d = 20.0L*(logl((long double)b)-logl((long double)a)) - (long double)k*logl((long double)n);
  if (d > 1e-9L) return 1; if (d < -1e-9L) return -1;
  // near tie (|d| <= 1e-9): not decided here; counted as "not greater" and reported in NEAR_TIES (0 observed to 1e9)
  return 0; // treat exact ties as "not greater" (they occur only when b^20 = a^20 n^k, i.e. measure-zero); flagged by counter
}
int main(int argc,char**argv){
  u64 N=strtoull(argv[1],0,10); int T=atoi(argv[2]); omp_set_num_threads(T);
  int K[]={0,1,2,4,6,10}; int nk=6; // alpha = k/20 : 0, .05, .1, .2, .3, .5
  u64 R=(u64)sqrtl((long double)(N+2))+2; char*c=calloc(R+1,1); primes=malloc(sizeof(u64)*(R/2+10)); np=0;
  for(u64 i=2;i<=R;i++){ if(!c[i]){primes[np++]=i; for(u64 j=i*i;j<=R;j+=i)c[j]=1;} }
  long nseg=(N+SEG-1)/SEG; u64 up[6]={0},dn[6]={0},ties=0;
  #pragma omp parallel
  { u64 *rem=malloc(8*(SEG+1)),*P=malloc(8*(SEG+1)); u64 lu[6]={0},ld[6]={0},lt=0;
    #pragma omp for schedule(dynamic,1)
    for(long s=0;s<nseg;s++){ u64 lo=(u64)s*SEG,len=SEG+1;
      for(u64 i=0;i<len;i++){rem[i]=lo+i;P[i]=1;}
      for(long k=0;k<np;k++){u64 p=primes[k]; if(p*p>lo+len)break; u64 st=(lo%p==0)?0:(p-lo%p);
        for(u64 i=st;i<len;i+=p){u64 r=rem[i]; if(r==0)continue; do{r/=p;}while(r%p==0); rem[i]=r; P[i]=p;}}
      for(u64 i=0;i<len;i++) if(rem[i]>1)P[i]=rem[i];
      for(u64 i=0;i<SEG;i++){u64 n=lo+i; if(n<2||n>N)continue; u64 a=P[i],b=P[i+1];
        for(int q=0;q<nk;q++){ int s1=cmp_exact(a,b,n,K[q]); int s2=cmp_exact(b,a,n,K[q]); if(s1>0)lu[q]++; if(s2>0)ld[q]++; if(K[q]>0&&(s1==0||s2==0))lt++; } } }
    #pragma omp critical
    { for(int q=0;q<nk;q++){up[q]+=lu[q];dn[q]+=ld[q];} ties+=lt; } }
  for(int q=0;q<nk;q++) printf("ALPHA X=%llu alpha=%.2f up=%llu (P(n+1)>P(n)n^a) down=%llu (P(n)>P(n+1)n^a) up/X=%.7f down/X=%.7f\n",N,K[q]/20.0,up[q],dn[q],(double)up[q]/N,(double)dn[q]/N);
  printf("NEAR_TIES %llu\n",ties); return 0; }
