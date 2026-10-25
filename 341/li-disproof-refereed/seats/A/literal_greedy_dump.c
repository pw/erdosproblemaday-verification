/* Literal greedy, independent of greedy341.c: for each candidate t > a_n test
   "exists j<=k<=n with a_j + a_k == t" by scanning the element list (equal indices allowed).
   Compares against Li's S computed from the Lean definitions, and against greedy under i<j as a contrast.
   usage: literal_greedy N mode   (mode 0: i<=j allowed equal ; mode 1: i<j distinct) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int Y0(long n){ if(n==0) return 1; for(long a=1; 4*a<=n; a*=8) if(4*a<=n && n<8*a) return 1; return 0; }
static int Y1(long n){ if(1<=n&&n<=3) return 1; for(long a=1; 16*a<=n+1; a*=8) if(16*a<=n+1 && n<32*a) return 1; return 0; }
static int Y2(long n){ if(n<=1 || (7<=n&&n<=15)) return 1; for(long a=1; 64*a<=n+1; a*=8) if(64*a<=n+1 && n<128*a) return 1; return 0; }
static int LiS(long n){ long r=n%49,q=n/49;
  if(n==1||n==2||n==5||n==13||n==27||n==36||n==47) return 1;
  if(r==3||r==22||r==32||r==40||r==48) return 1;
  if(r==7) return Y0(q); if(r==14) return Y1(q); if(r==28) return Y2(q); return 0; }
int main(int argc,char**argv){
  long N=atol(argv[1]); int mode=atoi(argv[2]);
  long seed[]={1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,63,71,77,81,89,97}; int k=21;
  char *in=calloc(N+1,1); long *a=malloc(sizeof(long)*(N/2+100)); long n=0;
  for(int i=0;i<k;i++){ a[n++]=seed[i]; in[seed[i]]=1; }
  long mism=0, firstm=-1;
  for(long t=98;t<=N;t++){
    int rep=0;
    for(long j=0;j<n && 2*a[j]<=t;j++){ long v=t-a[j]; if(v<a[j]) break; if(in[v]){ if(mode==1 && v==a[j]) continue; rep=1; break; } }
    if(!rep){ a[n++]=t; in[t]=1; }
  }
  for(long t=0;t<=N;t++){ if((in[t]!=0)!=(LiS(t)!=0)){ mism++; if(firstm<0) firstm=t; } }
  { char fn[64]; snprintf(fn,64,"lit_mode%d_%ld.u32",mode,N); FILE*fo=fopen(fn,"wb"); for(long i=0;i<n;i++){ unsigned x=(unsigned)a[i]; fwrite(&x,4,1,fo);} fclose(fo);} printf("mode=%d N=%ld |greedy|=%ld mismatches_vs_LiS=%ld first=%ld\n",mode,N,n,mism,firstm);
  /* positive control: Li's S must disagree with greedy if we perturb one element */
  return 0;
}
