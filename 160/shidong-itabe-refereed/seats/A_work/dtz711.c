/* DTZ Lemma 7.11 colouring psi = (Psi, chi) on Z/M^m Z for a = (1,2,3,4) (the only case Shi-Dong Lemma 5.2 needs):
   Psi = sum of squared base-M digits, chi = digits mod a! = 24.  Claim: no 4-AP b,b+d,b+2d,b+3d (d!=0 mod N)
   with c(b)=c(b+2d) and c(b+d)=c(b+3d) (ABAB, incl. AAAA).  mode 1: drop chi; mode 2: drop Psi (controls). */
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char**argv){ int M=atoi(argv[1]), m=atoi(argv[2]), mode=argc>3?atoi(argv[3]):0;
  long N=1; for(int j=0;j<m;j++) N*=M;
  long long *col=malloc(sizeof(long long)*N);
  for(long n=0;n<N;n++){ long t=n; long long ps=0, ch=0, mul=1; for(int j=0;j<m;j++){ int x=t%M; t/=M; ps+=x*x; ch+= (x%24)*mul; mul*=24; }
    col[n]= mode==1 ? ps : mode==2 ? ch : ps*1000000000LL + ch; }
  long long bad=0; long fb=-1, fd=-1;
  for(long d=1; d<N; d++) for(long b=0;b<N;b++){
    if(col[b]==col[(b+2*d)%N] && col[(b+d)%N]==col[(b+3*d)%N]){ bad++; if(fb<0){fb=b;fd=d;} } }
  printf("M=%d m=%d N=%ld mode=%d: ABAB-type 4-APs in Z/NZ = %lld (first b=%ld d=%ld)\n",M,m,N,mode,bad,fb,fd);
  return bad?1:0; }
