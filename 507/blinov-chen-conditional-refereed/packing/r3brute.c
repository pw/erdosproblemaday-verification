#include <stdio.h>
#include <stdlib.h>
/* exhaustive r_3(n) for n<=24 over all subsets: max popcount of AP-free masks */
int main(int argc,char**argv){int n=atoi(argv[1]);unsigned long N=1UL<<n;int best=0;unsigned long bm=0;
 for(unsigned long m=0;m<N;m++){int pc=__builtin_popcountl(m); if(pc<=best)continue; int ok=1;
  for(int a=0;a<n&&ok;a++) if(m>>a&1) for(int d=1;a+2*d<n;d++) if((m>>(a+d)&1)&&(m>>(a+2*d)&1)){ok=0;break;}
  if(ok){best=pc;bm=m;}}
 printf("%d %d :",n,best); for(int i=0;i<n;i++) if(bm>>i&1) printf(" %d",i); printf("\n"); return 0;}
