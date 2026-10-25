// Sampling sanity check (NOT a proof) of Shi–Dong Theorem 1.1 at k = 6, p = 7: a 5^8 * 7-colouring of Z/7^9 Z claimed to have no
// nontrivial symmetrically coloured 6-AP.  Colour(n) = (tau(x_0..x_7), Q(x)) with tau(x) = floor(5x/7) and
// Q(x) = x_0 + N_{F_{7^3}/F_7}(x_1,x_2,x_3) + N_{F_{7^5}/F_7}(x_4,...,x_8).  Norms via det of the multiplication matrix.
// Samples S random (a,d) pairs, d != 0; reports violations for the real colouring and for the control with Q dropped
// (control must find violations).  Also samples lines through random a with ALL d for a few a (exhaustive in d).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define P 7
static int md(long long x){x%=P; if(x<0)x+=P; return (int)x;}
// generic: multiply polynomial by T mod monic f of degree t (coeffs f[0..t-1], f[t]=1)
static void mulT(int *x,int t,const int *f){ int top=x[t-1]; for(int i=t-1;i>0;i--) x[i]=md(x[i-1]-(long long)top*f[i]); x[0]=md(-(long long)top*f[0]); }
static int det_mod(int n,int m[8][8]){ // Gaussian elimination mod P
  long long det=1; for(int c=0;c<n;c++){ int piv=-1; for(int r=c;r<n;r++) if(m[r][c]){piv=r;break;} if(piv<0) return 0;
    if(piv!=c){ for(int k=0;k<n;k++){int t=m[c][k];m[c][k]=m[piv][k];m[piv][k]=t;} det=md(-det); }
    int inv=1; for(int e=0;e<P-2;e++) inv=md(inv*m[c][c]); det=md(det*m[c][c]);
    for(int r=c+1;r<n;r++){ if(!m[r][c]) continue; int fac=md((long long)m[r][c]*inv); for(int k=c;k<n;k++) m[r][k]=md(m[r][k]-(long long)fac*m[c][k]); } }
  return (int)det; }
static int norm_t(const int *z,int t,const int *f){ int cur[8]; memcpy(cur,z,sizeof(int)*t); int m[8][8]; for(int j=0;j<t;j++){ for(int i=0;i<t;i++) m[i][j]=cur[i]; mulT(cur,t,f);} return det_mod(t,m); }
static int has_root(const int *f,int t){ for(int x=0;x<P;x++){ long long v=0,pw=1; for(int i=0;i<t;i++){ v=(v+f[i]*pw)%P; pw=pw*x%P;} v=(v+pw)%P; if(v==0) return 1;} return 0; }
static int irreducible(const int *f,int t){ // degree 3: no root; degree 5: no root and no quadratic factor -> check no root of f and gcd with x^(p^2)-x trivial: simpler brute force over all monic quadratics
  if(has_root(f,t)) return 0; if(t==3) return 1;
  for(int b=0;b<P;b++)for(int c=0;c<P;c++){ // divide f by x^2+bx+c
    int r[8]; memcpy(r,f,sizeof(int)*t); r[t]=1; // coefficients, degree t
    for(int d=t;d>=2;d--){ int q=r[d]; if(!q) continue; r[d]=0; r[d-1]=md(r[d-1]-(long long)q*b); r[d-2]=md(r[d-2]-(long long)q*c); }
    if(r[0]==0&&r[1]==0) return 0; }
  return 1; }
static uint64_t rng=0x9E3779B97F4A7C15ull; static uint64_t nxt(){ rng^=rng<<13; rng^=rng>>7; rng^=rng<<17; return rng; }
int main(int argc,char**argv){
  long long S = argc>1? atoll(argv[1]) : 100000000LL;
  int f3[4]={0}, f5[6]={0}; int ok=0;
  for(int a=0;a<P&&!ok;a++)for(int b=0;b<P&&!ok;b++)for(int c=1;c<P&&!ok;c++){ int f[4]={c,b,a,1}; if(irreducible(f,3)){memcpy(f3,f,sizeof f);ok=1;} }
  ok=0; for(int a=0;a<P&&!ok;a++)for(int b=0;b<P&&!ok;b++)for(int c=0;c<P&&!ok;c++)for(int d=0;d<P&&!ok;d++)for(int e=1;e<P&&!ok;e++){ int f[6]={e,d,c,b,a,1}; if(irreducible(f,5)){memcpy(f5,f,sizeof f);ok=1;} }
  printf("f3 = T^3+%dT^2+%dT+%d ; f5 = T^5+%dT^4+%dT^3+%dT^2+%dT+%d\n",f3[2],f3[1],f3[0],f5[4],f5[3],f5[2],f5[1],f5[0]);
  static int n3[343]; static int n5[16807]; long long z3=0,z5=0;
  for(int i=0;i<343;i++){ int z[3]={i%7,(i/7)%7,i/49}; n3[i]=norm_t(z,3,f3); if(n3[i]==0&&i) z3++; }
  for(int i=0;i<16807;i++){ int z[5]={i%7,(i/7)%7,(i/49)%7,(i/343)%7,i/2401}; n5[i]=norm_t(z,5,f5); if(n5[i]==0&&i) z5++; }
  printf("nontrivial zeros: N3 %lld  N5 %lld  (both must be 0)\n",z3,z5); if(z3||z5) return 2;
  uint32_t M=40353607u; // 7^9
  uint32_t *col=malloc(sizeof(uint32_t)*M), *ctl=malloc(sizeof(uint32_t)*M);
  for(uint32_t n=0;n<M;n++){ uint32_t m=n; int x[9]; for(int j=0;j<9;j++){x[j]=m%7;m/=7;}
    uint32_t tau=0; for(int j=0;j<8;j++) tau=tau*5+(5*x[j])/7;
    int q=md(x[0]+n3[x[1]+7*x[2]+49*x[3]]+n5[x[4]+7*x[5]+49*x[6]+343*x[7]+2401*x[8]]);
    col[n]=tau*7+q; ctl[n]=tau; }
  long long bad=0,badctl=0;
  for(long long s=0;s<S;s++){ uint32_t a=nxt()%M, d=1+nxt()%(M-1); uint32_t t[6]; for(int i=0;i<6;i++) t[i]=(uint32_t)(((uint64_t)a+(uint64_t)i*d)%M);
    if(col[t[0]]==col[t[5]]&&col[t[1]]==col[t[4]]&&col[t[2]]==col[t[3]]) bad++;
    if(ctl[t[0]]==ctl[t[5]]&&ctl[t[1]]==ctl[t[4]]&&ctl[t[2]]==ctl[t[3]]) badctl++; }
  // exhaustive in d for a few random a
  long long bad2=0, lines=0; for(int r=0;r<3;r++){ uint32_t a=nxt()%M; for(uint32_t d=1;d<M;d++){ uint32_t t[6]; for(int i=0;i<6;i++) t[i]=(uint32_t)(((uint64_t)a+(uint64_t)i*d)%M); lines++;
      if(col[t[0]]==col[t[5]]&&col[t[1]]==col[t[4]]&&col[t[2]]==col[t[3]]) bad2++; } }
  printf("k=6 p=7: %lld random 6-APs: symmetric in real colouring %lld, in no-Q control %lld (control must be >0)\n",S,bad,badctl);
  printf("          exhaustive-in-d from 3 random starts (%lld 6-APs): symmetric %lld\n",lines,bad2);
  return (bad||bad2)?1:(badctl?0:2);
}
