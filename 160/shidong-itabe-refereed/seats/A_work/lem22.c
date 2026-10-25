/* Exhaustive check of Shi-Dong Lemma 2.2 (digitwise k-AP) on Z/p^L Z for given k,p,L.
   For every (a,d): if tau-symmetric on digits 0..L-2 then digit vectors must form an AP in F_p^L,
   with h != 0 iff d != 0. Also counts how many such APs have a nonzero step in a NON-top digit
   (i.e. the test is not degenerate). Control mode (argv[4]=1): drop the tau check on digit 0 -> must fail. */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv){
  int k=atoi(argv[1]), p=atoi(argv[2]), L=atoi(argv[3]); int ctl = argc>4 ? atoi(argv[4]) : 0;
  long long P=1; for(int j=0;j<L;j++) P*=p;
  int tau[1000]; for(int x=0;x<p;x++) tau[x]=((k-1)*x)/p;
  long long checked=0, viol=0, nontop=0, hzero_bad=0;
  int dig[16][12];
  for(long long a=0;a<P;a++) for(long long d=0;d<P;d++){
    long long n=a;
    int ok=1;
    for(int i=0;i<k;i++){ long long m=n; for(int j=0;j<L;j++){dig[i][j]=m%p; m/=p;} n=(n+d)%P; }
    for(int j=(ctl?1:0);j<=L-2 && ok;j++) for(int i=1;i<=k/2;i++) if(tau[dig[i-1][j]]!=tau[dig[k-i][j]]){ok=0;break;}
    if(!ok) continue;
    checked++;
    int h[12], hnz=0, ntz=0;
    for(int j=0;j<L;j++){ h[j]=((dig[1][j]-dig[0][j])%p+p)%p; if(h[j]) {hnz=1; if(j<L-1) ntz=1;} }
    int ap=1;
    for(int i=2;i<k && ap;i++) for(int j=0;j<L;j++) if( ((dig[0][j]+ (long long)i*h[j])%p) != dig[i][j]) {ap=0;break;}
    if(!ap){ viol++; if(viol<=3) printf("VIOLATION a=%lld d=%lld\n",a,d); }
    if((d!=0) != hnz) hzero_bad++;
    if(ntz) nontop++;
  }
  printf("k=%d p=%d L=%d ctl=%d: tau-symmetric APs=%lld  (with nonzero step below top digit: %lld)  non-AP digit vectors=%lld  h=0<->d=0 failures=%lld\n",
         k,p,L,ctl,checked,nontop,viol,hzero_bad);
  return viol||hzero_bad;
}
