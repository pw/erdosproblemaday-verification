/* Independent census of the periodic-plus-sparse model (my own formulation).
   Period M. D = full classes (density |D|/M), E = sparse infinite classes (lacunary: usable as fixers, never
   enough on their own), T = D u E must generate Z/M (hypothesis (H)).
   For r in Z/M: need >= 1 dense summand (residue d in D) plus j summands with residues in T summing to r - d.
   dist_T(x) = least number of elements of T (repetition allowed) summing to x (Cayley-graph BFS from 0).
   order = max_r min_{d in D} 1 + dist_T(r-d).
   Compare with floor bound  floor(2M/|D|)-1 and ceil bound ceil(2M/|D|)-1, for |D| <= M/2.
   Enumerate T first (one BFS per T), then all D subset of T. */
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char**argv){
  int MMAX=argc>1?atoi(argv[1]):15;
  for(int M=2;M<=MMAX;M++){
    unsigned full=(1u<<M)-1;
    long long pairs=0,vf=0,vc=0,tightf=0,ctrl=0; double rc=0,rf=0; unsigned wT=0,wD=0; int wo=0;
    for(unsigned T=1;T<=full;T++){
      /* BFS distances from 0 using generators in T */
      int dist[32]; for(int i=0;i<M;i++) dist[i]=-1; dist[0]=0;
      int q[32],qh=0,qt=0; q[qt++]=0;
      while(qh<qt){int u=q[qh++]; for(int k=0;k<M;k++) if(T>>k&1){int v=(u+k)%M; if(dist[v]<0){dist[v]=dist[u]+1;q[qt++]=v;}}}
      int gen=1; for(int i=0;i<M;i++) if(dist[i]<0) gen=0;
      if(!gen) continue;
      /* all nonempty D subset of T with 2|D| <= M */
      for(unsigned D=T;D;D=(D-1)&T){
        int d=__builtin_popcount(D); if(2*d>M) continue;
        int order=0;
        for(int r=0;r<M;r++){
          int best=1<<30;
          for(int k=0;k<M;k++) if(D>>k&1){ int c=1+dist[((r-k)%M+M)%M]; if(c<best) best=c; }
          if(best>order) order=best;
        }
        int fb=(2*M)/d-1, cb=(2*M+d-1)/d-1;
        pairs++;
        if(order>fb) vf++;
        if(order>cb) vc++;
        if(order==fb) tightf++;
        if(order>fb-1) ctrl++;
        double a=(double)order/cb, b=(double)order/fb;
        if(a>rc){rc=a;} if(b>rf||(b==rf&&order>wo)){rf=b;wT=T;wD=D;wo=order;}
      }
    }
    printf("M=%2d pairs=%lld  >floor=%lld  >ceil=%lld  ==floor=%lld  ctrl(>floor-1)=%lld  max order/ceilb=%.4f  max order/floorb=%.4f [T=0x%x D=0x%x order=%d]\n",
           M,pairs,vf,vc,tightf,ctrl,rc,rf,wT,wD,wo);
    fflush(stdout);
  }
  return 0;
}
