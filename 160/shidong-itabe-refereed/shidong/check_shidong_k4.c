// Second, decorrelated implementation of the Shi–Dong Corollary 1.2 check (k=4) in C.
// Differences from the Python checker: the norm is computed as det of the 3x3 multiplication-by-z matrix
// over F_p (not as z^(1+p+p^2)); the irreducible cubic is searched from the TOP of the coefficient range;
// the symmetric-4-AP enumeration runs over (a, d) with d in 1..M-1 using unsigned arithmetic.
// usage: ./check_shidong_k4 p  -> prints palette, violation count, and three control counts (each must be > 0).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int P;
static int c0,c1,c2; // f = T^3 + c2 T^2 + c1 T + c0
static int md(long long x){ x%=P; if(x<0) x+=P; return (int)x; }
static int has_root(int a0,int a1,int a2){ for(int t=0;t<P;t++){ long long v=((long long)t*t%P*t + (long long)a2*t%P*t + (long long)a1*t + a0)%P; if(v==0) return 1;} return 0; }
// multiply (x0 + x1 T + x2 T^2) by T modulo f : T^3 = -c2 T^2 - c1 T - c0
static void mulT(int *x){ int x2=x[2]; x[2]=md(x[1] - (long long)x2*c2); x[1]=md(x[0] - (long long)x2*c1); x[0]=md(-(long long)x2*c0); }
// norm = det of the matrix whose columns are z, zT, zT^2 in the basis 1,T,T^2
static int norm_det(int z0,int z1,int z2){
  int a[3]={z0,z1,z2}, b[3], c[3];
  memcpy(b,a,sizeof a); mulT(b); memcpy(c,b,sizeof b); mulT(c);
  // det [a b c] (columns)
  long long d = (long long)a[0]*(((long long)b[1]*c[2]-(long long)b[2]*c[1])%P)
              - (long long)a[1]*(((long long)b[0]*c[2]-(long long)b[2]*c[0])%P)
              + (long long)a[2]*(((long long)b[0]*c[1]-(long long)b[1]*c[0])%P);
  return md(d);
}
static uint32_t *col;
static long long count_sym(uint32_t *cl, uint32_t M, int stop){
  long long bad=0;
  for(uint32_t a=0;a<M;a++){ uint32_t ca=cl[a];
    for(uint32_t d=1; d<M; d++){
      uint32_t a3=(a+3ull*d)%M; if(cl[a3]!=ca) continue;
      uint32_t a1=(a+d)%M, a2=(a+2ull*d)%M; if(cl[a1]==cl[a2]){ bad++; if(stop) return bad; }
    }
  }
  return bad;
}
int main(int argc,char**argv){
  if(argc<2){fprintf(stderr,"usage: p\n");return 2;} P=atoi(argv[1]);
  // irreducible cubic: search from the top
  int found=0; for(c2=P-1;c2>=0&&!found;c2--) for(c1=P-1;c1>=0&&!found;c1--) for(c0=P-1;c0>=0;c0--) if(!has_root(c0,c1,c2)){found=1;break;}
  if(!found){fprintf(stderr,"no irreducible cubic\n");return 2;}
  // c2,c1 were post-decremented by the for loops when found via break? handle: recompute exactly
  // (simplest: redo search storing values)
  int f0=-1,f1=-1,f2=-1;
  for(int a2=P-1;a2>=0&&f0<0;a2--) for(int a1=P-1;a1>=0&&f0<0;a1--) for(int a0=P-1;a0>=0;a0--) if(!has_root(a0,a1,a2)){f0=a0;f1=a1;f2=a2;break;}
  c0=f0;c1=f1;c2=f2;
  // norm table + anisotropy check
  int *nt = malloc(sizeof(int)*P*P*P); long long zeros=0;
  for(int z0=0;z0<P;z0++)for(int z1=0;z1<P;z1++)for(int z2=0;z2<P;z2++){ int n=norm_det(z0,z1,z2); nt[(z0*P+z1)*P+z2]=n; if(n==0 && (z0|z1|z2)) zeros++; }
  if(zeros){ printf("p=%d: norm has %lld nontrivial zeros -> CANNOT SEE (bad field construction)\n",P,zeros); return 2; }
  uint32_t M=(uint32_t)P*P*P*P;
  col=malloc(sizeof(uint32_t)*M); uint32_t *cNoQ=malloc(sizeof(uint32_t)*M), *cIso=malloc(sizeof(uint32_t)*M), *cTau=malloc(sizeof(uint32_t)*M);
  // colour encoding: tau0 + 3 tau1 + 9 tau2 + 27 q  (q in 0..P-1) -> unique integer; palette counted via a bitmap
  unsigned char *seen=calloc(27*P+1,1); long long palette=0;
  for(uint32_t n=0;n<M;n++){ uint32_t m=n; int x[4]; for(int j=0;j<4;j++){x[j]=m%P;m/=P;}
    int t0=3*x[0]/P,t1=3*x[1]/P,t2=3*x[2]/P;
    int q=md(x[0]+nt[(x[1]*P+x[2])*P+x[3]]);
    uint32_t cc=t0+3*t1+9*t2+27*q; col[n]=cc; if(!seen[cc]){seen[cc]=1;palette++;}
    cNoQ[n]=t0+3*t1+9*t2;
    int qi=md((long long)x[1]*x[1]%P*x[1]); cIso[n]=t0+3*t1+9*t2+27*qi;           // isotropic 'norm' x1^3
    cTau[n]=t0+9*t2+27*q;                                                          // tau on digit 1 dropped
  }
  long long bad=count_sym(col,M,0);
  long long b1=count_sym(cNoQ,M,1), b2=count_sym(cIso,M,1), b3=count_sym(cTau,M,1);
  printf("p=%d: f=T^3+%dT^2+%dT+%d  M=%u  palette=%lld (<=27p=%d: %s)  symmetric 4-APs=%lld\n",P,c2,c1,c0,M,palette,27*P,palette<=27*P?"yes":"NO",bad);
  printf("   controls: no-Q -> %lld   isotropic form -> %lld   drop tau(x1) -> %lld   (each must be >0)\n",b1,b2,b3);
  if(bad) return 1; if(!(b1&&b2&&b3)) return 2; return 0;
}
