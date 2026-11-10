// Independent Lemma test: for every x <= X and EVERY prime q with q^2 <= x+1, (q,x)!=(2,3): q holds e_x(q) alone.
// Also: q^2 = x+2 boundary cases, and in the Theorem's proof the count of (m,q) small factors with e_n(q) == m/q (bound attained)
// and with e_n(q) == Q.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char**argv){ long X=atol(argv[1]);
  int *spf=calloc(X+3,4),*e=calloc(X+3,4),*cnt=calloc(X+3,4); int *pr=malloc(4*(X+3)); int np=0;
  for(long i=2;i<=X+2;i++) if(!spf[i]){ pr[np++]=i; for(long j=i;j<=X+2;j+=i) if(!spf[j]) spf[j]=i; }
  long fail=0, checks=0, b2=0, b2fail=0, att_mq=0, att_Q=0, tight=0;
  for(long x=2;x<=X;x++){
    long n=x-1, m=x;
    // before updating to x: e = exponents in n!. Theorem-proof check for m = x
    { long t=m; long Q=0; long fs[20]; int nf=0; while(t>1){ long p=spf[t]; fs[nf++]=p; while(t%p==0) t/=p; }
      Q=fs[nf-1]; if(Q*Q>m){ long k=m/Q; for(int i=0;i<nf-1;i++){ long q=fs[i]; if(e[q]==m/q) att_mq++; if(e[q]==Q) att_Q++; if(e[q]==k+1) tight++; } } }
    long t=x; while(t>1){ long p=spf[t]; int v=0; while(t%p==0){t/=p;v++;} if(e[p]>0) cnt[e[p]]--; e[p]+=v; cnt[e[p]]++; }
    for(int i=0;i<np;i++){ long q=pr[i]; if(q*q>x+2) break;
      if(q*q<=x+1){ if(q==2&&x==3) continue; checks++; if(cnt[e[q]]!=1){ fail++; if(fail<10) printf("FAIL x=%ld q=%ld\n",x,q);} }
      else { b2++; if(cnt[e[q]]!=1) b2fail++; } }
  }
  printf("X=%ld lemma checks=%ld failures=%ld | boundary q^2=x+2: %ld cases, %ld not alone | proof bound e_n(q)=m/q attained %ld, e_n(q)=Q %ld, e_n(q)=k+1 %ld\n",X,checks,fail,b2,b2fail,att_mq,att_Q,tight);
}
