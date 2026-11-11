// e488c: rigorous one-sided bounds for Erdos 488 pair (y,T) via integer log-lattice DP.
// usage: e488c [-u] y R E T1 [T2 ...]
//   y prime, R = lattice resolution (weights ~ R*ln p), E = extra ln-range kept for tail sum.
//   -u : DELIBERATELY UNSAFE variant (negative control): floor weights, rho forced to 1, no margins.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <quadmath.h>
#include <omp.h>
#include <time.h>
typedef unsigned __int128 u128;
typedef __float128 f128;

static void pq(const char*k,f128 v){char b[96];quadmath_snprintf(b,sizeof b,"%.34Qe",v);printf("%s %s\n",k,b);}
static void pu(const char*k,u128 v){char b[64];int i=63;b[i]=0;if(!v)b[--i]='0';while(v){b[--i]='0'+(int)(v%10);v/=10;}printf("%s %s\n",k,b+i);}
static int isprime(unsigned long long n){if(n<2)return 0;for(unsigned long long d=2;d*d<=n;d++)if(n%d==0)return 0;return 1;}

static uint64_t *a; static long J;

static u128 Ncount(long L){ // number of lattice multisets with weight <= L
  if(L<0)return 0; if(L>J){fprintf(stderr,"L>J\n");exit(3);}
  u128 s=0; for(long j=0;j<=L;j++) s+=a[j]; return s; }

// sum_{j=j0}^{j1} a_j * exp(-j/D), quad precision, chunked; returns sum (no safety margin applied)
static f128 expsum(long j0,long j1,f128 D){
  if(j1>J)j1=J; if(j0>j1)return 0;
  const long CH=1<<14; long nch=(j1-j0)/CH+1;
  f128 *part=malloc(sizeof(f128)*nch);
  #pragma omp parallel for schedule(dynamic,4)
  for(long c=0;c<nch;c++){
    long lo=j0+c*CH, hi=lo+CH-1; if(hi>j1)hi=j1; f128 s=0;
    // block recurrence: exp(-j/D) = base_b * r^(j-jb), blocks of BL terms, base via expq (error <= ~4*BL ulp)
    const int BL=64; f128 r=expq(-1/D);
    for(long jb=lo;jb<=hi;jb+=BL){ f128 e=expq(-(f128)jb/D); long je=jb+BL-1; if(je>hi)je=hi;
      for(long j=jb;j<=je;j++){ if(a[j]) s+=(f128)a[j]*e; e*=r; } }
    part[c]=s; }
  f128 t=0; for(long c=0;c<nch;c++)t+=part[c]; free(part); return t; }

int main(int argc,char**argv){
  int unsafe=0,ai=1; if(argc>1&&!strcmp(argv[1],"-u")){unsafe=1;ai=2;}
  if(argc-ai<4){fprintf(stderr,"usage\n");return 1;}
  unsigned long long y=strtoull(argv[ai],0,10); long R=atol(argv[ai+1]); double E=atof(argv[ai+2]);
  int nT=argc-ai-3; unsigned long long T[16]; for(int i=0;i<nT;i++)T[i]=strtoull(argv[ai+3+i],0,10);
  unsigned long long q=y+1; while(!isprime(q))q++;
  int np=0; unsigned long long ps[4096]; for(unsigned long long p=2;p<=y;p++)if(isprime(p))ps[np++]=p;
  double t0=omp_get_wtime();
  f128 Rq=R; long w[4096]; f128 rmax=0,rmin=1e9Q; f128 Pi=1;
  for(int i=0;i<np;i++){
    f128 x=Rq*logq((f128)ps[i]);
    w[i]= unsafe ? (long)floorq(x) : (long)floorq(x+0.5Q);
    f128 rho=(f128)w[i]/x; if(rho>rmax)rmax=rho; if(rho<rmin)rmin=rho;
    Pi*=((f128)ps[i]-1)/(f128)ps[i]; }
  f128 MG=1e-20Q; // safety margin used throughout
  f128 rmax_s,rmin_s,Pi_lo;
  if(unsafe){rmax_s=1;rmin_s=1;Pi_lo=Pi;} else {rmax_s=rmax*(1+MG);rmin_s=rmin*(1-MG);Pi_lo=Pi*(1-MG);}
  printf("y %llu\nq %llu\nR %ld\nE %g\nnprimes %d\nunsafe %d\n",y,q,R,E,np,unsafe);
  pq("rho_max_raw",rmax);pq("rho_min_raw",rmin);pq("rho_max_s",rmax_s);pq("rho_min_s",rmin_s);pq("Pi_lo",Pi_lo);
  pq("invPi",1/Pi);
  // lattice extent
  long Lup_n[16],Llo_n[16],Lup_T[16],Llo_T[16],Lthr[16]; f128 lnT[16],lnn[16]; u128 n[16];
  long Jneed=0;
  for(int i=0;i<nT;i++){
    n[i]=(u128)q*T[i]; lnT[i]=logq((f128)T[i]); lnn[i]=logq((f128)n[i]);
    Lup_n[i]=(long)floorq(rmax_s*Rq*lnn[i]); Llo_n[i]=(long)floorq(rmin_s*Rq*lnn[i]);
    Lup_T[i]=(long)floorq(rmax_s*Rq*lnT[i]); Llo_T[i]=(long)floorq(rmin_s*Rq*lnT[i]);
    Lthr[i]=Lup_T[i]+1;
    long jt=(long)ceilq(Rq*(lnT[i]+(f128)E)); if(jt>Jneed)Jneed=jt; if(Lup_n[i]>Jneed)Jneed=Lup_n[i]; }
  J=Jneed+1; a=calloc(J+1,8); if(!a){fprintf(stderr,"alloc fail\n");return 2;}
  printf("J %ld\n",J);
  a[0]=1; int ovf=0;
  for(int i=0;i<np;i++){
    long wi=w[i];
    for(long st=wi;st<=J;st+=wi){ long en=st+wi; if(en>J+1)en=J+1; int o=0;
      uint64_t *restrict dst=a+st; const uint64_t *restrict src=a+st-wi; long len=en-st;
      #pragma omp parallel for reduction(|:o) schedule(static)
      for(long k=0;k<len;k++){ uint64_t s=dst[k]+src[k]; o|=(s<dst[k]); dst[k]=s; }
      ovf|=o; }
    if(ovf){fprintf(stderr,"UINT64 OVERFLOW\n");printf("OVERFLOW 1\n");return 4;} }
  double t1=omp_get_wtime();
  printf("overflow 0\ndp_seconds %.1f\n",t1-t0);
  for(int i=0;i<nT;i++){
    printf("--- T %llu\n",T[i]); pu("n",n[i]);
    f128 lo_m=unsafe?1:(1-MG), hi_m=unsafe?1:(1+MG);
    pu("Psi_up_T",Ncount(Lup_T[i])); pu("Psi_lo_T",Ncount(Llo_T[i]));
    u128 pun=Ncount(Lup_n[i]),pln=Ncount(Llo_n[i]),puT=Ncount(Lup_T[i]),plT=Ncount(Llo_T[i]);
    pu("Psi_up_n",pun); pu("Psi_lo_n",pln);
    u128 Aup=pun-plT, Alo=(pln>puT)?pln-puT:0; pu("A_up",Aup); pu("A_lo",Alo);
    f128 Sup=expsum(0,Lup_T[i],rmax_s*Rq)*hi_m, Slo=expsum(0,Llo_T[i],rmin_s*Rq)*lo_m;
    pq("S_up",Sup); pq("S_lo",Slo);
    // tail lower bound, reported by ln-range pieces to show convergence
    f128 tail=0; long j0=Lthr[i]; int NP=8;
    for(int k=1;k<=NP;k++){ long j1=(long)ceilq(Rq*(lnT[i]+(f128)E*k/NP)); if(k==NP&&j1<J)j1=J; if(j1>J)j1=J;
      f128 part=expsum(j0,j1,rmin_s*Rq); tail+=part; char nm[32];sprintf(nm,"tail_piece_%d",k);pq(nm,part); j0=j1+1; }
    f128 tail_lo=tail*lo_m; pq("tail_lo",tail_lo);
    f128 delta_lo=Pi_lo*tail_lo*lo_m; pq("delta_lo",delta_lo);
    f128 ratio=delta_lo*(f128)n[i]/(f128)Aup*lo_m; pq("ratio_lo",ratio);
    int cert = (delta_lo*(f128)n[i]*lo_m > 2*(f128)Aup); printf("certified %s\n",cert?"yes":"no");
    f128 rup_hint = (f128)0; (void)rup_hint;
  }
  printf("total_seconds %.1f\n",omp_get_wtime()-t0);
  return 0; }
