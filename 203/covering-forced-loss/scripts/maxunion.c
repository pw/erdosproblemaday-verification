// maxunion.c — EXACT maximum, over every choice of cosets, of the number of points of the torus (Z/T)^2 covered by
// the union of the cosets C_i = {(k,l): u_i k + v_i l ≡ c_i (mod e_i)}, T = lcm(e_i).  First coset fixed to 0
// (translation invariance: chi_1 is onto Z/e_1).  Usage: maxunion <file with lines "e u v">  → prints T, Σ1/e·T²,
// max covered, #optimal choices, one witness choice.  Brute force; no solver, no heuristics.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static long gcdl(long a,long b){while(b){long t=a%b;a=b;b=t;}return a;}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); long e[32],u[32],v[32]; int n=0;
  while(fscanf(f,"%ld %ld %ld",&e[n],&u[n],&v[n])==3) n++;
  long T=1; for(int i=0;i<n;i++) T=T/gcdl(T,e[i])*e[i];
  long W=(T*T+63)/64; 
  // bitsets: for prime i, coset c: index offset
  long tot=0; for(int i=0;i<n;i++) tot+=e[i];
  uint64_t *bs=calloc((size_t)tot*W,8); long off[33]; off[0]=0; for(int i=0;i<n;i++) off[i+1]=off[i]+e[i];
  for(long k=0;k<T;k++) for(long l=0;l<T;l++){ long x=k*T+l;
    for(int i=0;i<n;i++){ long c=((u[i]*k+v[i]*l)%e[i]+e[i])%e[i]; bs[(off[i]+c)*W + x/64] |= (1ULL<<(x%64)); } }
  // control: each coset bitset has exactly T*T/e_i points
  for(int i=0;i<n;i++) for(long c=0;c<e[i];c++){ long cnt=0; for(long w=0;w<W;w++) cnt+=__builtin_popcountll(bs[(off[i]+c)*W+w]);
    if(cnt!=T*T/e[i]){ printf("CONTROL FAIL prime %d coset %ld count %ld != %ld\n",i,c,cnt,T*T/e[i]); return 2;} }
  long choice[32]; for(int i=0;i<n;i++) choice[i]=0;
  long best=-1, nbest=0; long bestc[32]; double configs=1; for(int i=1;i<n;i++) configs*=e[i];
  uint64_t *acc=malloc(W*8);
  // enumerate choices c_1..c_{n-1} (c_0=0) odometer
  while(1){
    memcpy(acc,bs+off[0]*W,W*8);
    for(int i=1;i<n;i++){ const uint64_t*b=bs+(off[i]+choice[i])*W; for(long w=0;w<W;w++) acc[w]|=b[w]; }
    long cnt=0; for(long w=0;w<W;w++) cnt+=__builtin_popcountll(acc[w]);
    if(cnt>best){best=cnt;nbest=1;memcpy(bestc,choice,sizeof(choice));} else if(cnt==best) nbest++;
    int i=1; while(i<n){ choice[i]++; if(choice[i]<e[i]) break; choice[i]=0; i++; } if(i>=n) break;
  }
  double sum=0; for(int i=0;i<n;i++) sum+=1.0/e[i];
  printf("n=%d T=%ld points=%ld configs=%.0f sum1/e=%.6f (=%.1f pts)\n",n,T,T*T,configs,sum,sum*T*T);
  printf("MAX covered=%ld density=%.6f  forced loss=%.6f  (#optimal choices %ld)\n",best,(double)best/(T*T),sum-(double)best/(T*T),nbest);
  printf("witness cosets:"); for(int i=0;i<n;i++) printf(" %ld",bestc[i]); printf("\n");
  return 0;
}
