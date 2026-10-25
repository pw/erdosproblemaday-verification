// j(P_k) for the primorial P_k, k <= 9, by sieving one full period [0, P_k) (gaps are periodic mod P_k).
// j(n) = max gap between consecutive integers coprime to n (= least m such that every m consecutive integers contain one coprime to n).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){
  int K=atoi(argv[1]); int pr[]={2,3,5,7,11,13,17,19,23,29,31};
  long long P=1; for(int i=0;i<K;i++) P*=pr[i];
  unsigned char *c=malloc(P+1); memset(c,1,P+1);
  for(int i=0;i<K;i++) for(long long x=0;x<=P;x+=pr[i]) c[x]=0;
  long long last=-1,best=0; // 1 is coprime; scan [1, P+1] (P+1 is coprime, closes the wrap gap)
  for(long long x=1;x<=P;x++) if(c[x]){ if(last>=0 && x-last>best) best=x-last; last=x; }
  long long wrap=(P+1)-last; if(wrap>best) best=wrap;
  printf("k=%d P=%lld j=%lld\n",K,P,best); return 0; }
