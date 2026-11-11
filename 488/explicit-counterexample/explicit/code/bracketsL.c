// Same certificate as brackets.c, generalised to the band A = {P-smooth a : T < a <= L*T} with y <= L <= q (P = primes <= y,
// q = next prime). For such L the identity still holds (strip primes p <= y <= L from a smooth s > T; cofactors below L
// are P-smooth because L <= q), so multiples of A = {z : P-part(z) > T}, M_A(LT) = |A|, density = prod(1-1/p) sum_{s>T} 1/s.
// T = 2^e (exact powers of two; Gessel's family is L = 256, T = 256^k, y = 251).
// usage: bracketsL RB lnXmax weights y L e1 e2 ...      (prints the certificate for each T = 2^e)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef unsigned __int128 u128; typedef unsigned long long u64;
static long K; static u128 *C; static long double R;
static void add_prime(u64 w){ for(long base=w; base<K; base+=w){ long len=(base+(long)w<=K)?(long)w:K-base;
  #pragma omp parallel for schedule(static)
  for(long j=0;j<len;j++) C[base+j]+=C[base+j-w]; } }
static u128 pfx(long k){ u128 r=0; if(k>=K) k=K-1; for(long j=0;j<=k;j++) r+=C[j]; return r; }
static char* u128s(u128 v, char*b){ char t[64]; int i=0; if(!v){strcpy(b,"0");return b;} while(v){t[i++]='0'+(int)(v%10); v/=10;} for(int j=0;j<i;j++) b[j]=t[i-1-j]; b[i]=0; return b; }
int main(int argc,char**argv){
  int RB=atoi(argv[1]); double lnX=atof(argv[2]); R=ldexpl(1.0L,RB); K=(long)(R*lnX)+1;
  int y=atoi(argv[4]); u64 L=strtoull(argv[5],0,10);
  FILE*f=fopen(argv[3],"r"); u64 p,w,P[1000],Wt[1000]; int np=0; while(fscanf(f,"%llu %llu",&p,&w)==2){ P[np]=p; Wt[np]=w; np++; } fclose(f);
  C=calloc(K,sizeof(u128)); C[0]=1; u64 w2=Wt[0]; long double c=1; int i=0;
  for(;i<np && P[i]<=(u64)y;i++){ add_prime(Wt[i]); c*=1.0L-1.0L/(long double)P[i]; }
  u64 q=P[i]; if(L<(u64)P[i-1] || L>q){ fprintf(stderr,"need y <= L <= q\n"); return 2; }
  long double clo=c*(1.0L-1e-12L), beta=(1.0L+1.0L/(long double)w2)/R;
  printf("# RB=%d K=%ld y=%d L=%llu q=%llu primes=%d\n",RB,K,y,L,q,i);
  char b1[64],b2[64],b3[64];
  for(int a=6;a<argc;a++){ int e=atoi(argv[a]); long double lnT=e*logl(2.0L), lnN=lnT+logl((long double)L);
    long kTup=(long)floorl(R*lnT+1e-6L), kNup=(long)floorl(R*lnN+1e-6L), kTlo=(long)floorl(R*lnT*(long double)w2/((long double)w2+1)-1e-6L);
    if(kNup>=K-1){ printf("e=%d: K too small\n",e); continue; }
    u128 PTlo=pfx(kTlo), PNup=pfx(kNup); u128 Aup=PNup-PTlo;
    long double acc=0, ginv=expl(beta), gk=0; long top=K-1;
    for(long j=top;j>kTup;j--){ if(((top-j)&1023)==0) gk=expl(-beta*(long double)j); if(C[j]) acc+=(long double)C[j]*gk; gk*=ginv; }
    long double dlo=clo*acc*(1.0L-1e-9L); long double n=ldexpl((long double)L,e);
    long double rlo=dlo*n/(long double)Aup; int cert= dlo*n > 2.0L*(long double)Aup*(1.0L+1e-12L);
    printf("T=2^%d n=%llu*2^%d Psi_lo(T)=%s Psi_up(LT)=%s |A|<=%s tail_lo=%.18Le delta_lo=%.18Le ratio_lo=%.9Lf certified=%d\n",
           e,L,e,u128s(PTlo,b1),u128s(PNup,b2),u128s(Aup,b3),acc,dlo,rlo,cert); fflush(stdout); }
  return 0;
}
