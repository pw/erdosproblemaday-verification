// Exact smooth-band statistics for the explicit Erdos #488 counterexample (route A).
// P = primes <= y, q = next prime > y. For each threshold T (integer):
//   Psi(x)  = #{P-smooth s <= x}               (exact, u64)
//   |A|     = Psi(qT) - Psi(T)                  (A = P-smooth band (T, qT])
//   S(T)    = sum_{P-smooth s <= T} 1/s         (__float128 accumulation)
//   delta   = 1 - prod_{p<=y}(1-1/p) * S(T)     (exact density of multiples of A; see identity_check.py)
//   ratio   = delta * qT / |A|   -> counterexample to #488 (n = qT, m = lcm(A)) iff ratio > 2
// Method: s = u * b with u 5-smooth (sorted table U, prefix sums of 1/u) and b (7..y)-smooth (parallel DFS).
// usage: psi_multi y threads xfile   -> exact Psi(x) for every x in xfile (route A engine, up to 1100 x)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <quadmath.h>
#include <omp.h>
typedef unsigned long long u64; typedef __float128 f128;
static u64 pr[4000]; static int np, q;
static u64 *U; static f128 *W; static long nU;
static int K; static u64 X[1100]; static int isT[1100];   // thresholds sorted ascending; isT: is a T (needs S)
static u64 N;
static int cmpu(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b; return x<y?-1:x>y;}
static inline long upto(u64 t){ long lo=0,hi=nU; while(lo<hi){ long mid=(lo+hi)>>1; if(U[mid]<=t) lo=mid+1; else hi=mid; } return lo; }
typedef struct { u64 cnt[1100]; f128 S[1100]; u64 nodes; char pad[64]; } Acc;
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
  FILE*fx=fopen(argv[3],"r"); u64 xv; while(fscanf(fx,"%llu",&xv)==1){ X[K]=xv; isT[K]=0; K++; } fclose(fx);
  for(int i=0;i<K;i++) for(int j=i+1;j<K;j++) if(X[j]<X[i]){u64 t=X[i];X[i]=X[j];X[j]=t;}
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
  static u64 cnt[1100]; u64 nodes=0;
  for(int t=0;t<th;t++){ nodes+=accs[t].nodes; for(int k=0;k<K;k++) cnt[k]+=accs[t].cnt[k]; }
  printf("# y=%d nodes=%llu wall=%.1fs\n",y,nodes,t1-t0);
  for(int k=0;k<K;k++) printf("%llu %llu\n",X[k],cnt[k]);
  return 0;
}
