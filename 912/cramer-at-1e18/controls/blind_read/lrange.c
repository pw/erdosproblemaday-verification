#include <stdio.h>
#include <stdlib.h>
int main(int argc,char**argv){ long X=atol(argv[1]); double c=atof(argv[2]);
  int *spf=calloc(X+3,4),*e=calloc(X+3,4),*cnt=calloc(X+3,4); int *pr=malloc(4*(X+3)); int np=0;
  for(long i=2;i<=X+2;i++) if(!spf[i]){ pr[np++]=i; for(long j=i;j<=X+2;j+=i) if(!spf[j]) spf[j]=i; }
  long fail=0, first=-1;
  for(long x=2;x<=X;x++){ long t=x; while(t>1){ long p=spf[t]; int v=0; while(t%p==0){t/=p;v++;} if(e[p]>0) cnt[e[p]]--; e[p]+=v; cnt[e[p]]++; }
    for(int i=0;i<np;i++){ long q=pr[i]; if((double)q*q> c*x) break; if(x==3) continue; if(cnt[e[q]]!=1){ fail++; if(first<0){first=x; printf("first fail x=%ld q=%ld q^2/x=%.3f\n",x,q,(double)q*q/x);} } } }
  printf("c=%.2f X=%ld failures=%ld\n",c,X,fail); }
