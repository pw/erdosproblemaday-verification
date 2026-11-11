// Exact smooth-band statistics for the explicit Erdos #488 counterexample (route A).
// P = primes <= y, q = next prime > y. For each threshold T (integer):
//   Psi(x)  = #{P-smooth s <= x}               (exact, u64)
//   |A|     = Psi(qT) - Psi(T)                  (A = P-smooth band (T, qT])
//   S(T)    = sum_{P-smooth s <= T} 1/s         (__float128 accumulation)
//   delta   = 1 - prod_{p<=y}(1-1/p) * S(T)     (exact density of multiples of A; see identity_check.py)
//   ratio   = delta * qT / |A|   -> counterexample to #488 (n = qT, m = lcm(A)) iff ratio > 2
// Method: s = u * b with u 5-smooth (sorted table U, prefix sums of 1/u) and b (7..y)-smooth (parallel DFS).
// usage: psi488 y threads T1 [T2 ...]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <quadmath.h>
#include <omp.h>
typedef unsigned long long u64; typedef __float128 f128;
static u64 pr[4000]; static int np, q;
static u64 *U; static f128 *W; static long nU;
static int K; static u64 X[64]; static int isT[64];   // thresholds sorted ascending; isT: is a T (needs S)
static u64 N;
static int cmpu(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b; return x<y?-1:x>y;}
static inline long upto(u64 t){ long lo=0,hi=nU; while(lo<hi){ long mid=(lo+hi)>>1; if(U[mid]<=t) lo=mid+1; else hi=mid; } return lo; }
typedef struct { u64 cnt[64]; f128 S[64]; u64 nodes; char pad[64]; } Acc;
static inline void process(u64 s, Acc *a){
  a->nodes++;
  f128 inv = 1.0Q/(f128)s;
  for(int k=K-1;k>=0;k--){ if(X[k]<s) break; long c=upto(X[k]/s); a->cnt[k]+=c; if(isT[k] && c>0) a->S[k]+=inv*W[c-1]; }
}
static void dfs(u64 s,int imax,Acc*a){ process(s,a); for(int i=imax-1;i>=3;i--){ u64 t=s; while(t<=N/pr[i]){ t*=pr[i]; dfs(t,i,a);} } }
typedef struct { u64 s; int imax; int procself; } Task;
int main(int argc,char**argv){
  int y=atoi(argv[1]); int th=atoi(argv[2]);
  for(int k=2;;k++){ int p=1; for(int d=2;(long)d*d<=k;d++) if(k%d==0){p=0;break;} if(p){ if(k<=y) pr[np++]=k; else {q=k;break;} } }
  if(y<5){fprintf(stderr,"need y>=5\n");return 1;}
  int nT=argc-3; u64 T[32];
  for(int j=0;j<nT;j++){ T[j]=strtoull(argv[3+j],0,10); X[K]=T[j]; isT[K]=1; K++; X[K]=T[j]*(u64)q; isT[K]=0; K++; if(T[j] > 18446744073709551615ULL/q){fprintf(stderr,"overflow\n");return 1;} }
  // sort thresholds with flags
  for(int i=0;i<K;i++) for(int j=i+1;j<K;j++) if(X[j]<X[i]){u64 t=X[i];X[i]=X[j];X[j]=t;int f=isT[i];isT[i]=isT[j];isT[j]=f;}
  N=X[K-1];
  // 5-smooth table <= N
  long cap=1<<20; U=malloc(cap*8); nU=0;
  for(u64 a=1;;a*=2){ for(u64 b=a;;b*=3){ for(u64 c=b;;c*=5){ U[nU++]=c; if(c>N/5) break; } if(b>N/3) break; } if(a>N/2) break; }
  qsort(U,nU,8,cmpu); W=malloc(nU*sizeof(f128)); f128 acc=0; for(long i=0;i<nU;i++){ acc+=1.0Q/(f128)U[i]; W[i]=acc; }
  // tasks: depth-2 split of the (7..y)-smooth DFS
  long ntask=0, tcap=1<<22; Task*tk=malloc(tcap*sizeof(Task));
  tk[ntask++]=(Task){1,3,1}; // s=1 alone (imax=3 => no recursion)
  for(int i=np-1;i>=3;i--){ u64 t=1; while(t<=N/pr[i]){ t*=pr[i];
      tk[ntask++]=(Task){t,3,1};   // process t itself only
      for(int j=i-1;j>=3;j--){ u64 v=t; while(v<=N/pr[j]){ v*=pr[j]; tk[ntask++]=(Task){v,j,1}; } } } }
  Acc *accs=calloc(th,sizeof(Acc));
  double t0=omp_get_wtime();
  #pragma omp parallel for schedule(dynamic,1) num_threads(th)
  for(long i=0;i<ntask;i++){ Acc*a=&accs[omp_get_thread_num()]; if(tk[i].imax==3) process(tk[i].s,a); else dfs(tk[i].s,tk[i].imax,a); }
  double t1=omp_get_wtime();
  u64 cnt[64]={0}, nodes=0; f128 S[64]={0};
  for(int t=0;t<th;t++){ nodes+=accs[t].nodes; for(int k=0;k<K;k++){ cnt[k]+=accs[t].cnt[k]; S[k]+=accs[t].S[k]; } }
  f128 c=1; for(int i=0;i<np;i++) c*= (f128)(pr[i]-1)/(f128)pr[i];
  char buf[128]; quadmath_snprintf(buf,sizeof buf,"%.36Qe",c);
  printf("# y=%d q=%d primes=%d |U|=%ld tasks=%ld nodes=%llu wall=%.1fs prod(1-1/p)=%s\n",y,q,np,nU,ntask,nodes,t1-t0,buf);
  printf("# T Psi(T) Psi(qT) |A| S(T) delta ratio margin=delta*qT-2|A|\n");
  for(int j=0;j<nT;j++){ int kt=-1,kn=-1; for(int k=0;k<K;k++){ if(X[k]==T[j]&&isT[k]) kt=k; if(X[k]==T[j]*(u64)q&&!isT[k]) kn=k; }
    u64 A=cnt[kn]-cnt[kt]; f128 delta=1-c*S[kt]; f128 n=(f128)T[j]*(f128)q; f128 ratio=delta*n/(f128)A; f128 margin=delta*n-2*(f128)A;
    char sS[64],sd[64],sr[64],sm[64]; quadmath_snprintf(sS,64,"%.30Qe",S[kt]); quadmath_snprintf(sd,64,"%.25Qe",delta); quadmath_snprintf(sr,64,"%.12Qf",ratio); quadmath_snprintf(sm,64,"%.6Qe",margin);
    printf("%llu %llu %llu %llu %s %s %s %s\n",T[j],cnt[kt],cnt[kn],A,sS,sd,sr,sm); }
  return 0;
}
