#include <stdio.h>
#include <stdlib.h>
static long P,M; static char Fm[100000];
static int Y0(long n){ if(n==0) return 1; for(long a=1; 4*a<=n; a*=8) if(4*a<=n && n<8*a) return 1; return 0; }
static int Y1(long n){ if(1<=n&&n<=3) return 1; for(long a=1; 16*a<=n+1; a*=8) if(16*a<=n+1 && n<32*a) return 1; return 0; }
static int Y2(long n){ if(n<=1 || (7<=n&&n<=15)) return 1; for(long a=1; 64*a<=n+1; a*=8) if(64*a<=n+1 && n<128*a) return 1; return 0; }
static int isB(long r){ return r==M-3||r==M-1||r==6*P+3; }
static int Sp(long n){ long r=n%M,q=n/M; if(n>0 && n<M && !Fm[n]) return 1; if(isB(r)) return 1;
  if(r==P) return Y0(q); if(r==2*P) return Y1(q); if(r==4*P) return Y2(q); return 0; }
int main(int c,char**v){ P=atol(v[1]); long N=atol(v[2]); M=7*P;
  long Q[6]={P,2*P,4*P,M-3,M-1,6*P+3}, Bv[3]={M-3,M-1,6*P+3}, Pv[3]={P,2*P,4*P};
  for(int i=0;i<6;i++){ Fm[Q[i]%M]=1; for(int j=0;j<3;j++){ Fm[((Q[i]-Bv[j])%M+M)%M]=1; Fm[((Q[i]-Pv[j])%M+M)%M]=1; } }
  /* seed A_p = D ∪ B ∪ (M+B) ∪ {p,4p,M+2p,M+4p}, built from the PAPER's definition, not from S_p */
  char *in=calloc(N+1,1); long *a=malloc(sizeof(long)*(N+10)); long n=0, k=0;
  for(long x=1;x<2*M;x++){ int s = (x<M && !Fm[x]) || (x<M && isB(x)) || (x>=M && isB(x-M)) || x==P || x==4*P || x==M+2*P || x==M+4*P;
    if(s){ a[n++]=x; in[x]=1; } }
  k=n;
  for(long t=2*M;t<=N;t++){ int rep=0; for(long j=0;j<n && 2*a[j]<=t;j++){ if(in[t-a[j]]){rep=1;break;} } if(!rep){a[n++]=t;in[t]=1;} }
  long mism=0,first=-1; for(long t=0;t<=N;t++) if((in[t]!=0)!=(Sp(t)!=0)){ mism++; if(first<0) first=t; }
  printf("p=%ld M=%ld |A_p|=%ld (7p-20=%ld) N=%ld |greedy|=%ld mismatches_vs_S_p=%ld first=%ld\n",P,M,k,7*P-20,N,n,mism,first);
  return 0; }
