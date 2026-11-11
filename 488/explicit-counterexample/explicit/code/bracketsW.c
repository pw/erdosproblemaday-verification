// Certificate with a FINITE m = W*T (Liu, Lemma 12(iii)): for the band A = {P-smooth a : T < a <= L*T}, y <= L <= q,
//   M_A(n) = |A| = Psi(LT) - Psi(T)  (n = LT),     M_A(WT) = sum_{u rough, u < W} (Psi(WT/u) - Psi(T))   (rough = no prime <= y)
// (both re-checked by direct sieving in identity_check.py). We require W < q^2, so rough u < W are 1 and the primes in [q, W).
// Bounds (see brackets.c): Psi_up(x) = #{Ld <= floor(R ln x)},  Psi_lo(x) = #{Ld (1+1/w2) <= R ln x}.
//   |A| <= Psi_up(LT) - Psi_lo(T);   M_A(WT) >= sum_u max(0, Psi_lo(floor(WT/u)) - Psi_up(T)).
// Certified counterexample iff  n * M_lo(m) > 2 * m * |A|_up   (all integers, compared exactly in u128).
// usage: bracketsW RB lnXmax weights y L Wlo Whi Wstep T1 [T2 ...]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef unsigned __int128 u128; typedef unsigned long long u64;
static long K; static u128 *C; static long double R; static u64 w2;
static void add_prime(u64 w){ for(long base=w; base<K; base+=w){ long len=(base+(long)w<=K)?(long)w:K-base;
  #pragma omp parallel for schedule(static)
  for(long j=0;j<len;j++) C[base+j]+=C[base+j-w]; } }
static char* u128s(u128 v, char*b){ char t[64]; int i=0; if(!v){strcpy(b,"0");return b;} while(v){t[i++]='0'+(int)(v%10); v/=10;} for(int j=0;j<i;j++) b[j]=t[i-1-j]; b[i]=0; return b; }
static u128 Pup(long double x){ long k=(long)floorl(R*logl(x)+1e-6L); if(k>=K){fprintf(stderr,"K too small\n");exit(4);} return C[k]; }
static u128 Plo(long double x){ long k=(long)floorl(R*logl(x)*(long double)w2/((long double)w2+1)-1e-6L); if(k<0) return 0; if(k>=K){fprintf(stderr,"K too small\n");exit(4);} return C[k]; }
static int isprime(u64 n){ if(n<2) return 0; for(u64 d=2;d*d<=n;d++) if(n%d==0) return 0; return 1; }
int main(int argc,char**argv){
  int RB=atoi(argv[1]); double lnX=atof(argv[2]); R=ldexpl(1.0L,RB); K=(long)(R*lnX)+1;
  int y=atoi(argv[4]); u64 L=strtoull(argv[5],0,10); u64 Wlo=strtoull(argv[6],0,10), Whi=strtoull(argv[7],0,10), Wst=strtoull(argv[8],0,10);
  FILE*f=fopen(argv[3],"r"); u64 p,w,P[1000],Wt[1000]; int np=0; while(fscanf(f,"%llu %llu",&p,&w)==2){ P[np]=p; Wt[np]=w; np++; } fclose(f);
  C=calloc(K,sizeof(u128)); C[0]=1; w2=Wt[0]; int i=0;
  for(;i<np && P[i]<=(u64)y;i++) add_prime(Wt[i]);
  u64 q=P[i]; if(L<P[i-1]||L>q){fprintf(stderr,"need y<=L<=q\n");return 2;} if(Whi>=q*q){fprintf(stderr,"need W<q^2\n");return 2;}
  for(long k=1;k<K;k++) C[k]+=C[k-1];   // prefix sums in place: C[k] = #{Ld <= k}
  static u64 U[400000]; int nu=0; U[nu++]=1; for(u64 u=q;u<Whi;u++) if(isprime(u)) U[nu++]=u;   // rough u < Whi: 1 and primes >= q
  printf("# RB=%d K=%ld y=%d L=%llu q=%llu rough-u count(<%llu)=%d\n",RB,K,y,L,q,Whi,nu);
  char b1[64],b2[64],b3[64],b4[64];
  for(int a=9;a<argc;a++){ u64 T=strtoull(argv[a],0,10); u128 n=(u128)L*T;
    u128 PTup=Pup((long double)T), PTlo=Plo((long double)T), PNup=Pup((long double)L*(long double)T);
    u128 Aup=PNup-PTlo;
    long double best=0; u64 bestW=0; u128 bestM=0;
    for(u64 W=Wlo; W<=Whi; W+=Wst){ if((u128)W*T<=n) continue; u128 m=(u128)W*T; u128 M=0;
      for(int j=0;j<nu && U[j]<W;j++){ u128 x=m/U[j]; u128 lo=Plo((long double)x); if(lo>PTup) M+=lo-PTup; }
      long double r=(long double)n*(long double)M/((long double)m*(long double)Aup);
      int cert = n*M > 2*m*Aup;
      if(r>best){best=r;bestW=W;bestM=M;}
      if(argc-9<=2) printf("  T=%llu W=%llu m=%s M_lo(m)=%s ratio_lo=%.9Lf certified=%d\n",T,W,u128s(m,b1),u128s(M,b2),r,cert);
    }
    u128 m=(u128)bestW*T; int cert = n*bestM > 2*m*Aup;
    char b5[64],b6[64]; printf("T=%llu n=%s |A|<=%s Psi(T) in [%s,%s] bestW=%llu m=%s M_lo(m)=%s ratio_lo=%.9Lf certified=%d\n",T,u128s(n,b1),u128s(Aup,b2),u128s(PTlo,b3),u128s(PTup,b4),bestW,u128s(m,b5),u128s(bestM,b6),best,cert); fflush(stdout);
    if(cert && getenv("STOP_AFTER_CERT")) return 0;
  }
  return 0;
}
