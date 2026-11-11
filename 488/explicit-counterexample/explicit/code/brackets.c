// Rigorous brackets for the smooth-band counterexample to Erdos #488 (route B: integer-weight knapsack).
// Ld(s) = sum e_p * w_p with w_p = floor(R ln p) (weights_RB.txt, certified in weights.py). For every s: Ld(s) <= R ln s,
// and R ln s < Ld(s) + Omega(s) <= Ld(s)(1 + 1/w2), w2 = w_2 = floor(R ln 2) (each prime weight >= w2).
// Cd[k] = #{P-smooth s : Ld(s) = k}, built by unbounded-knapsack DP, adding primes in increasing order.
//   Psi_up(x) = #{Ld <= floor(R ln x)}                 >= Psi(x)
//   Psi_lo(x) = #{Ld * (1 + 1/w2) <= R ln x}           <= Psi(x)
//   tail_lo(T)= sum_{Ld(s) = k > R ln T, k < K} exp(-k(1+1/w2)/R)  <= sum_{s > T} 1/s
//   delta_lo  = prod(1-1/p) * tail_lo * (1 - 1e-9)     <= density of multiples of A = {P-smooth a : T < a <= qT}
//   certified counterexample (n = qT, m = lcm A) iff delta_lo * qT > 2 * (Psi_up(qT) - Psi_lo(T)).
// usage: brackets RB lnXmax weights_file mode ...
//   mode scan  y_lo y_hi  : for each prime y in [y_lo,y_hi], first grid T = round(10^(j/10)), 10 <= j/10, qT < 1.8e19 certified, ratio_lo there
//   mode at    y T1 T2 ...: full numbers for one y at given T
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef unsigned __int128 u128; typedef unsigned long long u64;
static long K; static u128 *C; static long double R;
static int np; static u64 P[1000], Wt[1000];
static void add_prime(u64 w){ for(long base=w; base<K; base+=w){ long len = (base+(long)w<=K)? (long)w : K-base;
  #pragma omp parallel for schedule(static)
  for(long j=0;j<len;j++) C[base+j]+=C[base+j-w]; } }
static char* u128s(u128 v, char*b){ char t[64]; int i=0; if(!v){strcpy(b,"0");return b;} while(v){t[i++]='0'+(int)(v%10); v/=10;} for(int j=0;j<i;j++) b[j]=t[i-1-j]; b[i]=0; return b; }
// evaluate at sorted list of (kT_up, kT_lo_for_Psi, kqT_up): need Pfx at arbitrary indices and tails
typedef struct { long double T; u64 Ti; long kTup, kTlo, kNup; u128 PsiTlo, PsiTup, PsiNup, PsiNlo; long double tail; } Ev;
static void evaluate(Ev*ev,int ne,u64 w2){
  // prefix pass
  long need[1024]; int nn=0; for(int i=0;i<ne;i++){ need[nn++]=ev[i].kTup; need[nn++]=ev[i].kTlo; need[nn++]=ev[i].kNup; }
  // simple: compute prefix at each needed index via one sequential pass over sorted needed indices
  long idx[1024]; for(int i=0;i<nn;i++) idx[i]=need[i];
  for(int i=0;i<nn;i++) for(int j=i+1;j<nn;j++) if(idx[j]<idx[i]){long t=idx[i];idx[i]=idx[j];idx[j]=t;}
  u128 val[1024]; u128 run=0; long k=0; for(int i=0;i<nn;i++){ long tgt=idx[i]; if(tgt>=K) tgt=K-1; while(k<=tgt){ run+=C[k]; k++; } val[i]=run; }
  for(int e=0;e<ne;e++){ for(int i=0;i<nn;i++){ if(idx[i]==ev[e].kTup) ev[e].PsiTup=val[i]; if(idx[i]==ev[e].kTlo) ev[e].PsiTlo=val[i]; if(idx[i]==ev[e].kNup) ev[e].PsiNup=val[i]; } }
  // tail pass (descending), weights g^k, g = exp(-(1+1/w2)/R)
  long double beta=(1.0L+1.0L/(long double)w2)/R;
  long kk[200]; for(int e=0;e<ne;e++) kk[e]=ev[e].kTup; // tail over k > kTup (= floor(R ln T))
  long double acc=0; long top=K-1;
  // sort eval indices by kTup descending via simple selection on the fly
  int done[200]={0};
  long double ginv=expl(beta), gk=0;
  int ord[200]; for(int e=0;e<ne;e++) ord[e]=e;            // eval indices sorted by kTup descending
  for(int a=0;a<ne;a++) for(int b2=a+1;b2<ne;b2++) if(kk[ord[b2]]>kk[ord[a]]){int t=ord[a];ord[a]=ord[b2];ord[b2]=t;}
  int ptr=0; while(ptr<ne && kk[ord[ptr]]>top){ ev[ord[ptr]].tail=0; done[ord[ptr]]=1; ptr++; }
  for(long j=top;j>=0;j--){ while(ptr<ne && kk[ord[ptr]]==j){ ev[ord[ptr]].tail=acc; done[ord[ptr]]=1; ptr++; }
    if(ptr>=ne) break;
    if(((top-j)&1023)==0) gk=expl(-beta*(long double)j);     // exact re-anchor every 1024 cells
    if(C[j]) acc+= (long double)C[j]*gk;
    gk*=ginv; }
  for(int e=0;e<ne;e++) if(!done[e]) ev[e].tail=acc;
}
int main(int argc,char**argv){
  int RB=atoi(argv[1]); double lnX=atof(argv[2]); R=ldexpl(1.0L,RB); K=(long)(R*lnX)+1;
  FILE*f=fopen(argv[3],"r"); u64 p,w; while(fscanf(f,"%llu %llu",&p,&w)==2){ P[np]=p; Wt[np]=w; np++; } fclose(f);
  C=calloc(K,sizeof(u128)); if(!C){fprintf(stderr,"oom\n");return 1;} C[0]=1;
  u64 w2=Wt[0];
  const char*mode=argv[4];
  int ylo,yhi; u64 Tlist[64]; int nT=0;
  if(!strcmp(mode,"scan")){ ylo=atoi(argv[5]); yhi=atoi(argv[6]); }
  else { ylo=yhi=atoi(argv[5]); for(int i=6;i<argc;i++) Tlist[nT++]=strtoull(argv[i],0,10); }
  long double c=1; char b1[64],b2[64],b3[64],b4[64];
  printf("# RB=%d K=%ld lnXmax=%.2f w2=%llu\n",RB,K,lnX,w2);
  for(int i=0;i<np && P[i]<=(u64)yhi;i++){
    add_prime(Wt[i]); c*= 1.0L-1.0L/(long double)P[i];
    if((int)P[i]<ylo) continue;
    u64 q=P[i+1]; long double clo=c*(1.0L-1e-12L);
    Ev ev[200]; int ne=0;
    if(!strcmp(mode,"scan")){ for(int j=100;j<=210;j++){ long double T=roundl(powl(10.0L,j/10.0L)); if(T*(long double)q>1.8e19L) break; ev[ne].Ti=(u64)T; ne++; } }
    else for(int j=0;j<nT;j++){ ev[ne].Ti=Tlist[j]; ne++; }
    for(int e=0;e<ne;e++){ long double T=(long double)ev[e].Ti; long double lnT=logl(T), lnN=logl(T*(long double)q);
      // floor(R ln x) with a safety: use floor of (value + 1e-6) for the UP index (only enlarges Psi_up), floor(value*w2/(w2+1) - 1e-6) for LO
      ev[e].kTup=(long)floorl(R*lnT+1e-6L); ev[e].kNup=(long)floorl(R*lnN+1e-6L); ev[e].kTlo=(long)floorl(R*lnT*(long double)w2/((long double)w2+1)-1e-6L); }
    evaluate(ev,ne,w2);
    int first=-1;
    for(int e=0;e<ne;e++){ long double T=(long double)ev[e].Ti; long double n=T*(long double)q;
      if(ev[e].kNup>=K-1){ continue; }
      if(ev[e].PsiNup<=ev[e].PsiTlo){ fprintf(stderr,"FATAL: Psi_up(qT) <= Psi_lo(T) at y=%llu T=%llu\n",P[i],ev[e].Ti); exit(3);} 
      u128 Aup=ev[e].PsiNup-ev[e].PsiTlo; long double dlo=clo*ev[e].tail*(1.0L-1e-9L);
      long double rlo=dlo*n/(long double)Aup; int cert = dlo*n > 2.0L*(long double)Aup*(1.0L+1e-12L);
      if(!strcmp(mode,"scan")){ if(cert && first<0){ first=e; printf("y=%llu q=%llu first certified T=%llu n=qT=%.4Le ratio_lo=%.6Lf |A|<=%s\n",P[i],q,ev[e].Ti,n,rlo,u128s(Aup,b1)); fflush(stdout);} }
      else printf("y=%llu q=%llu T=%llu n=%llu Psi(T) in [%s, %s] Psi(qT)<=%s |A|<=%s tail_lo=%.20Le delta_lo=%.20Le ratio_lo=%.9Lf certified=%d\n",
                  P[i],q,ev[e].Ti,(u64)(ev[e].Ti*q),u128s(ev[e].PsiTlo,b1),u128s(ev[e].PsiTup,b2),u128s(ev[e].PsiNup,b3),u128s(Aup,b4),ev[e].tail,dlo,rlo,cert);
    }
    if(!strcmp(mode,"scan") && first<0){ printf("y=%llu q=%llu none certified on grid\n",P[i],q); fflush(stdout);} }
  return 0;
}
