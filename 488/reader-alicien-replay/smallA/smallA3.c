/* Erdős #488, small |A|, EXACT decision for every primitive A = {a_1<...<a_k}, a_k <= CMAX.
   f(y) = B(y)/y.  d = density of B (inclusion-exclusion), E = 2^k - 1, so |B(y) - d y| < E for all y.
   (1) For n > N1 = 3E/d:  sup_{m>n} f(m) <= d + E/n < 2(d - E/n) <= 2 f(n): no violation.
   (2) fmin = min_{c<=n<=N1} f(n).  If d >= 2 fmin -> report (violation or boundary case; re-check exactly).
       Else delta = 2 fmin - d > 0, M = max(N1, E/delta) + 2: for m > M, f(m) < d + E/M < 2 fmin <= 2 f(n).
   (3) So a violation exists iff some c <= n <= N1 < m <= M ... or n < m <= M has B(m) n >= 2 B(n) m
       (checked in exact integers against the running suffix maximum of f).
   Also records the largest actual ratio f(m)/f(n) found, and the largest M needed. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
typedef unsigned long long u64; typedef long long i64;
static u64 gcd(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
static int prim(int *a,int k){for(int i=0;i<k;i++)for(int j=i+1;j<k;j++) if(a[j]%a[i]==0) return 0; return 1;}
static long double density(int *a,int k){ long double d=0;
  for(int s=1;s<(1<<k);s++){ int bits=0; u64 L=1; int big=0;
    for(int i=0;i<k;i++) if(s>>i&1){bits++; if(!big){ u64 g=gcd(L,(u64)a[i]); u64 q=(u64)a[i]/g; if(L>(u64)4e18/q) big=1; else L*=q; }}
    if(big) continue; d += ((bits&1)?1.0L:-1.0L)/(long double)L; } return d; }
int main(int argc,char**argv){ int k=atoi(argv[1]), CMIN=atoi(argv[2]), CMAX=atoi(argv[3]); i64 MCAP=atoll(argv[4]); int LP=argc>5?atoi(argv[5]):2, LQ=argc>6?atoi(argv[6]):1; long double lam=(long double)LP/LQ;
  int E=(1<<k)-1; i64 nsets=0, nviol=0, ncap=0; double best=0; int bestA[8]={0}; i64 bestn=0,bestm=0, maxM=0; int maxMA[8]={0};
  #pragma omp parallel
  { int a[8]; int *cnt=malloc(sizeof(int)*(MCAP+2));
    double lbest=0; int lA[8]={0}; i64 ln=0,lm=0,lsets=0,lviol=0,lcap=0,lmaxM=0; int lmA[8]={0};
    #pragma omp for schedule(dynamic,1)
    for(int c=CMIN;c<=CMAX;c++){
      int r=k-1; int idx[8]; for(int i=0;i<r;i++) idx[i]=2+i;
      if(r>0 && 2+r-1>c-1) continue;
      while(1){
        for(int i=0;i<r;i++) a[i]=idx[i]; a[r]=c;
        if(prim(a,k)){ lsets++;
          long double d=density(a,k); i64 N1=(i64)(E*(lam+1)/(d*(lam-1)))+2; if(N1<c) N1=c;
          /* counts up to N1 */
          i64 top=N1; if(top>MCAP){lcap++; goto next;}
          cnt[0]=0; for(i64 y=1;y<=top;y++){ int in=0; for(int i=0;i<k;i++) if(y%a[i]==0){in=1;break;} cnt[y]=cnt[y-1]+in; }
          long double fmin=1e9; for(i64 n=c;n<=N1;n++){ long double f=(long double)cnt[n]/n; if(f<fmin) fmin=f; }
          long double delta=lam*fmin-d; i64 M;
          if(delta<=0){ M=N1+2; lviol++;
            #pragma omp critical
            { printf("DENSITY>=lam*fmin"); for(int i=0;i<k;i++) printf(" %d",a[i]); printf("\n"); fflush(stdout);} }
          else { long double Mm=(long double)E/delta; M=(Mm>(long double)MCAP)? MCAP+1 : (i64)Mm+2; if(M<N1+2) M=N1+2; }
          if(M>MCAP){ lcap++;
            #pragma omp critical
            { printf("CAP"); for(int i=0;i<k;i++) printf(" %d",a[i]); printf(" N1=%lld delta=%Lg\n",N1,delta); fflush(stdout);}
            goto next; }
          if(M>lmaxM){lmaxM=M; memcpy(lmA,a,sizeof(int)*k);}
          for(i64 y=top+1;y<=M;y++){ int in=0; for(int i=0;i<k;i++) if(y%a[i]==0){in=1;break;} cnt[y]=cnt[y-1]+in; }
          /* suffix max over m in (n, M], kept as the argmax index */
          { i64 arg=M; int viol=0; double rbest=0; i64 rn=0, rm=0;
            for(i64 n=M-1;n>=c;n--){ /* arg = argmax_{n<m<=M} f(m) */
              i64 m1=n+1; if((__int128)cnt[m1]*arg > (__int128)cnt[arg]*m1) arg=m1;
              if(n<=N1){ if((__int128)LQ*cnt[arg]*n >= (__int128)LP*cnt[n]*arg){ viol=1; }
                double rr=((double)cnt[arg]/arg)/((double)cnt[n]/n); if(rr>rbest){rbest=rr;rn=n;rm=arg;} } }
            if(viol && delta>0){ lviol++;
              #pragma omp critical
              { printf("VIOLATION"); for(int i=0;i<k;i++) printf(" %d",a[i]); printf("\n"); fflush(stdout);} }
            if(rbest>lbest){lbest=rbest; memcpy(lA,a,sizeof(int)*k); ln=rn; lm=rm;} }
        }
        next:
        if(r==0) break;
        int i=r-1; while(i>=0 && idx[i]==c-1-(r-1-i)) i--; if(i<0) break; idx[i]++; for(int j=i+1;j<r;j++) idx[j]=idx[j-1]+1;
      }
    }
    #pragma omp critical
    { nsets+=lsets; nviol+=lviol; ncap+=lcap; if(lbest>best){best=lbest; memcpy(bestA,lA,sizeof(int)*k); bestn=ln; bestm=lm;}
      if(lmaxM>maxM){maxM=lmaxM; memcpy(maxMA,lmA,sizeof(int)*k);} }
    free(cnt);
  }
  printf("lambda=%d/%d",LP,LQ); printf(" k=%d max A in [%d,%d] primitive_sets=%lld violations=%lld capped(undecided)=%lld largest_ratio=%.9f at A={",k,CMIN,CMAX,nsets,nviol,ncap,best);
  for(int i=0;i<k;i++) printf("%d%s",bestA[i],i<k-1?",":""); printf("} n=%lld m=%lld; largest M used=%lld (A={",bestn,bestm,maxM);
  for(int i=0;i<k;i++) printf("%d%s",maxMA[i],i<k-1?",":""); printf("})\n"); return 0; }
