// e488m: rigorous bounds for the FINITE-m check of Erdos 488 pairs.
//   A = {P-smooth a : T < a <= Lambda*T}, n = Lambda*T, m = W*T.
//   |A| = Psi(Lambda T) - Psi(T);  M_A(WT) = sum_{u<W rough} ( Psi(floor(WT/u)) - Psi(T) ).
//   counterexample iff n*M_A(m) > 2*m*|A|  <=>  Lambda*M > 2*W*|A|   (T cancels).
// usage: e488m [-u] y Lambda R T W      (-u = deliberately unsafe negative control)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <quadmath.h>
#include <omp.h>
typedef unsigned __int128 u128;
typedef __float128 f128;
static void pq(const char*k,f128 v){char b[96];quadmath_snprintf(b,sizeof b,"%.34Qe",v);printf("%s %s\n",k,b);}
static void pu(const char*k,u128 v){char b[64];int i=63;b[i]=0;if(!v)b[--i]='0';while(v){b[--i]='0'+(int)(v%10);v/=10;}printf("%s %s\n",k,b+i);}
static int isprime(unsigned long long n){if(n<2)return 0;for(unsigned long long d=2;d*d<=n;d++)if(n%d==0)return 0;return 1;}
static uint64_t *a; static long J;
static f128 RHOMAX,RHOMIN,RQ;
static long Lup(u128 x){return (long)floorq(RHOMAX*RQ*logq((f128)x));}
static long Llo(u128 x){return (long)floorq(RHOMIN*RQ*logq((f128)x));}
static u128 Psi_up(u128 x){long L=Lup(x); if(L>J){fprintf(stderr,"L>J\n");exit(3);} return a[L];}   // a[] is prefix-summed
static u128 Psi_lo(u128 x){long L=Llo(x); if(L<0)return 0; if(L>J){fprintf(stderr,"L>J\n");exit(3);} return a[L];}
int main(int argc,char**argv){
  int unsafe=0,ai=1; if(argc>1&&!strcmp(argv[1],"-u")){unsafe=1;ai=2;}
  if(argc-ai<5){fprintf(stderr,"usage\n");return 1;}
  unsigned long long y=strtoull(argv[ai],0,10),Lam=strtoull(argv[ai+1],0,10); long R=atol(argv[ai+2]);
  u128 T=strtoull(argv[ai+3],0,10); unsigned long long W=strtoull(argv[ai+4],0,10);
  unsigned long long q=y+1; while(!isprime(q))q++;
  if(!(Lam>=y&&Lam<=q&&W>Lam)){fprintf(stderr,"bad params\n");return 1;}
  int np=0; static unsigned long long ps[8192]; for(unsigned long long p=2;p<=y;p++)if(isprime(p))ps[np++]=p;
  double t0=omp_get_wtime(); RQ=R; static long w[8192]; f128 rmax=0,rmin=1e9Q;
  for(int i=0;i<np;i++){ f128 x=RQ*logq((f128)ps[i]); w[i]=unsafe?(long)floorq(x):(long)floorq(x+0.5Q);
    f128 rho=(f128)w[i]/x; if(rho>rmax)rmax=rho; if(rho<rmin)rmin=rho; }
  f128 MG=1e-20Q; if(unsafe){RHOMAX=1;RHOMIN=1;} else {RHOMAX=rmax*(1+MG);RHOMIN=rmin*(1-MG);}
  printf("y %llu\nq %llu\nLambda %llu\nR %ld\nW %llu\nunsafe %d\nnprimes %d\n",y,q,Lam,R,W,unsafe,np);
  pq("rho_max_s",RHOMAX);pq("rho_min_s",RHOMIN); pu("T",T);
  u128 n=(u128)Lam*T, m=(u128)W*T; pu("n",n); pu("m",m);
  long Jn=Lup(n), Jm=Lup(m); J=(Jn>Jm?Jn:Jm)+1;
  a=calloc(J+1,8); if(!a){fprintf(stderr,"alloc\n");return 2;} printf("J %ld\n",J);
  a[0]=1; int ovf=0;
  for(int i=0;i<np;i++){ long wi=w[i];
    for(long st=wi;st<=J;st+=wi){ long en=st+wi; if(en>J+1)en=J+1; int o=0;
      uint64_t *restrict dst=a+st; const uint64_t *restrict src=a+st-wi; long len=en-st;
      #pragma omp parallel for reduction(|:o) schedule(static)
      for(long k=0;k<len;k++){ uint64_t s=dst[k]+src[k]; o|=(s<dst[k]); dst[k]=s; }
      ovf|=o; }
    if(ovf){printf("OVERFLOW 1\n");return 4;} }
  // prefix sums (checked)
  { u128 s=0; for(long j=0;j<=J;j++){ s+=a[j]; if(s>>64){printf("OVERFLOW prefix\n");return 4;} a[j]=(uint64_t)s; } }
  printf("overflow 0\ndp_seconds %.1f\n",omp_get_wtime()-t0);
  u128 pTu=Psi_up(T),pTl=Psi_lo(T),pnu=Psi_up(n),pnl=Psi_lo(n);
  pu("Psi_up_T",pTu);pu("Psi_lo_T",pTl);pu("Psi_up_n",pnu);pu("Psi_lo_n",pnl);
  u128 Aup=pnu-pTl, Alo=pnl>pTu?pnl-pTu:0; pu("A_up",Aup);pu("A_lo",Alo);
  // rough u < W
  unsigned *spf=calloc(W+1,sizeof(unsigned)); for(unsigned long long i=2;i<=W;i++)if(!spf[i])for(unsigned long long j=i;j<=W;j+=i)if(!spf[j])spf[j]=(unsigned)i;
  u128 Mlo=0,Mup=0; long nr=0;
  for(unsigned long long u=1;u<W;u++){ if(u>1&&spf[u]<=y)continue; nr++;
    u128 x=m/u;   // floor(WT/u) >= T since u<W
    u128 hi=Psi_up(x), lo=Psi_lo(x);
    Mlo += (lo>pTu)?lo-pTu:0;
    Mup += hi-pTl; }
  printf("n_rough %ld\n",nr); pu("M_lo",Mlo); pu("M_up",Mup);
  // exact integer test: Lambda*M_lo > 2*W*A_up
  u128 lhs=(u128)Lam*Mlo, rhs=(u128)2*W*Aup; printf("exact_test_lhs_gt_rhs %d\n",lhs>rhs?1:0);
  // ratio_lo = Lambda*M_lo/(W*A_up), 12 decimals, exact integer division (floor)
  u128 den=(u128)W*Aup; u128 sc=(lhs*1000000000000ULL)/den; 
  { char b[64];int i=63;b[i]=0;u128 v=sc;while(v){b[--i]='0'+(int)(v%10);v/=10;} printf("ratio_lo_x1e12 %s\n",b+i); }
  f128 rlo=(f128)lhs/(f128)den; pq("ratio_lo",rlo);
  if(Alo>0){ u128 den2=(u128)W*Alo; pq("ratio_up",(f128)((u128)Lam*Mup)/(f128)den2); }
  printf("certified %s\n",lhs>rhs?"yes":"no"); printf("total_seconds %.1f\n",omp_get_wtime()-t0); return 0; }
