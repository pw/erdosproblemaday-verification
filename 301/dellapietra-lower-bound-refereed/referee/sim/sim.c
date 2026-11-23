// Simulate the rough-third construction: simple (full top) vs regular-top variant.
// usage: sim N L At Kt [Ah Kh]   (Kh<0 => no head regularity)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
static int *spf;
static double At,Kt,Ah,Kh; static int L;
static int regular(long n, double A, double K){
  // Omega_L(n,x) <= A log(log x/log L)+K for all x>=L ; check at each prime factor >= L
  int cnt=0; double lL=log((double)L);
  // collect prime factors ascending
  int ps[64], np=0;
  long m=n; while(m>1){int p=spf[m]; ps[np++]=p; m/=p;}
  // spf gives ascending order already
  for(int i=0;i<np;i++){ if(ps[i]<L) continue; cnt++; double rhs=A*log(log((double)ps[i])/lL)+K; if(cnt>rhs+1e-12) return 0; }
  return 1;
}
int main(int argc,char**argv){
  long N=atol(argv[1]); L=atoi(argv[2]); At=atof(argv[3]); Kt=atof(argv[4]);
  Ah=argc>5?atof(argv[5]):1; Kh=argc>6?atof(argv[6]):-1;
  spf=malloc(sizeof(int)*(N+1));
  for(long i=0;i<=N;i++) spf[i]=0;
  for(long i=2;i<=N;i++) if(!spf[i]){ for(long j=i;j<=N;j+=i) if(!spf[j]) spf[j]=(int)i; }
  long top_start=(N+1)/2;
  char *T=calloc(N+1,1); long topsize=0;
  for(long n=top_start;n<=N;n++){ T[n]=regular(n,At,Kt); topsize+=T[n]; }
  long low=0, lowreg=0, del_simple=0, del_reg=0, rel_simple=0, rel_reg=0;
  for(long a=N/3+1; 2*a<N; a++){
    if(a<2) continue; if(spf[a]<L) continue; // L-rough (a>1)
    low++;
    if(Kh>=0 && !regular(a,Ah,Kh)) continue;
    lowreg++;
    // factor a, enumerate divisors of a^2
    int ps[64],es[64],np=0; long m=a;
    while(m>1){int p=spf[m]; int e=0; while(m%p==0){m/=p;e++;} ps[np]=p; es[np]=2*e; np++;}
    long divs[200000]; int nd=1; divs[0]=1;
    for(int i=0;i<np;i++){ int cur=nd; long pk=1; for(int e=1;e<=es[i];e++){ pk*=ps[i]; for(int j=0;j<cur;j++) divs[nd++]=divs[j]*pk; } }
    int bs=0, br=0; __int128 a2=(__int128)a*a;
    for(int j=0;j<nd;j++){ long d=divs[j]; if(d>=a) continue; long b=a+d; long c=a+(long)(a2/d);
      if(b>=top_start && c<=N && b<c){ rel_simple++; bs=1; if(T[b]&&T[c]){rel_reg++; br=1;} } }
    del_simple+=bs; del_reg+=br;
  }
  long full_top=N-top_start+1;
  long size_simple=full_top+low-del_simple;
  long size_reg=topsize+lowreg-del_reg;
  printf("N=%ld L=%d At=%.5f Kt=%.2f Kh=%.1f | low=%ld lowreg=%ld | simple: del=%ld rel=%ld size=%ld dens=%.6f excess=%.6f | regtop: topremoved=%ld del=%ld rel=%ld size=%ld dens=%.6f excess=%.6f\n",
    N,L,At,Kt,Kh,low,lowreg,del_simple,rel_simple,size_simple,(double)size_simple/N,(double)size_simple/N-0.5,
    full_top-topsize,del_reg,rel_reg,size_reg,(double)size_reg/N,(double)size_reg/N-0.5);
  return 0;
}
