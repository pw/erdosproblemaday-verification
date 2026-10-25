// omega.c — for every totient a <= AMAX, find l(a) = least n with phi(n)=a by scanning n in
// increasing order (first hit = least preimage), and record the decomposition
//   R(n) = n/phi(n) = T(n) * W(n)
// T(n) = 2 if 4|n; otherwise prod over Fermat primes F (3,5,17,257,65537) dividing n EXACTLY once of F/(F-1)
// W(n) = product of p/(p-1) over every other odd prime p | n (non-Fermat, or Fermat with exponent >= 2)
// (If 4|n we also multiply W by F/(F-1) for Fermat primes dividing n exactly once — for a least
//  preimage that set is empty by the swap 2^e*F -> 2^(e+2^s); we COUNT violations as a check.)
// Usage: omega AMAX NMAX  (scan n <= NMAX; complete for a <= AMAX iff l(a) <= NMAX for all such a)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define SEG (1<<22)
static int isfermat(uint64_t p){return p==3||p==5||p==17||p==257||p==65537;}
int main(int argc,char**argv){
  uint64_t AMAX=strtoull(argv[1],0,10), NMAX=strtoull(argv[2],0,10);
  uint64_t PL=(uint64_t)sqrt((double)NMAX)+2;
  // small primes
  char*comp=calloc(PL+1,1); uint32_t*pr=malloc(sizeof(uint32_t)*(PL)); int np=0;
  for(uint64_t i=2;i<=PL;i++){ if(!comp[i]){pr[np++]=i; for(uint64_t j=i*i;j<=PL;j+=i)comp[j]=1;} }
  uint8_t*seen=calloc(AMAX/8+1,1); uint32_t*ELL=calloc(AMAX+1,4);
  uint64_t*phi=malloc(8*SEG),*rem=malloc(8*SEG); double*W=malloc(8*SEG); double*T=malloc(8*SEG);
  uint8_t*bad=malloc(SEG);
  uint64_t ntot=0, viol=0; double bestR=0,bestW=0; uint64_t bestRa=0,bestWa=0;
  // histogram of W for least preimages
  uint64_t hist[64]; memset(hist,0,sizeof hist);
  FILE*rec=fopen("records.tsv","w");
  fprintf(rec,"kind\ta\tl\tR\tT\tW\n");
  double recR=0, recW=0;
  for(uint64_t lo=1; lo<=NMAX; lo+=SEG){
    uint64_t hi=lo+SEG-1; if(hi>NMAX)hi=NMAX; uint64_t len=hi-lo+1;
    for(uint64_t i=0;i<len;i++){phi[i]=lo+i; rem[i]=lo+i; W[i]=1.0; T[i]=1.0; bad[i]=0;}
    // track fermat-simple product separately in T; 4|n handled after
    for(int k=0;k<np;k++){
      uint64_t p=pr[k]; if(p*p>hi && p>hi) break;
      uint64_t start=((lo+p-1)/p)*p;
      for(uint64_t m=start;m<=hi;m+=p){
        uint64_t i=m-lo; int e=0;
        while(rem[i]%p==0){rem[i]/=p;e++;}
        phi[i]=phi[i]/p*(p-1);
        if(p==2){ if(e>=2) T[i]*=2.0; /* e==1: n=2 mod 4, never least */ }
        else if(isfermat(p) && e==1) T[i]*=(double)p/(p-1);
        else W[i]*=(double)p/(p-1);
      }
    }
    for(uint64_t ii=0;ii<len;ii++){ uint64_t i=len-1-ii;
      if(rem[i]>1){ uint64_t q=rem[i]; phi[i]=phi[i]/q*(q-1);
        if(isfermat(q)) T[i]*=(double)q/(q-1); else W[i]*=(double)q/(q-1); }
      uint64_t n=lo+i, a=phi[i];
      if(a>AMAX) continue;
      if(seen[a>>3]&(1<<(a&7))) continue;
      seen[a>>3]|=1<<(a&7); ntot++; ELL[a]=(uint32_t)n;
      double Tn=T[i], Wn=W[i];
      if(n%4==0){ // fold any fermat-simple factor out of T (T was 2*fermat-simple)
        double f=Tn/2.0; if(f>1.0+1e-12){viol++; Wn*=f; Tn=2.0;} }
      double R=(double)n/(double)a;
      if(R>bestR){bestR=R;bestRa=a;}
      if(Wn>bestW){bestW=Wn;bestWa=a;}
      int b=(int)((Wn-1.0)*32.0); if(b>63)b=63; hist[b]++;
      if(R>recR+1e-15){recR=R; fprintf(rec,"R\t%llu\t%llu\t%.9f\t%.9f\t%.9f\n",(unsigned long long)a,(unsigned long long)n,R,Tn,Wn);}
      if(Wn>recW+1e-15){recW=Wn; fprintf(rec,"W\t%llu\t%llu\t%.9f\t%.9f\t%.9f\n",(unsigned long long)a,(unsigned long long)n,R,Tn,Wn);}
    }
  }
  fclose(rec); { FILE*bf=fopen("omega_ell.bin","wb"); fwrite(ELL,4,AMAX+1,bf); fclose(bf);}
  printf("AMAX=%llu NMAX=%llu distinct totients <= AMAX found: %llu\n",(unsigned long long)AMAX,(unsigned long long)NMAX,(unsigned long long)ntot);
  printf("max R=%.9f at a=%llu ; max W=%.9f at a=%llu ; 4|l with fermat-simple factor (should be 0): %llu\n",bestR,(unsigned long long)bestRa,bestW,(unsigned long long)bestWa,(unsigned long long)viol);
  printf("W histogram (bin width 1/32 from 1.0):\n");
  for(int b=0;b<64;b++) if(hist[b]) printf("  W in [%.4f,%.4f): %llu\n",1+b/32.0,1+(b+1)/32.0,(unsigned long long)hist[b]);
  return 0;
}
