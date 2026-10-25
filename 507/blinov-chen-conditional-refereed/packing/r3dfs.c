#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
/* exact r_3(n), n=1..NMAX, lexicographically first optimal set containing 0. bitset forbids. */
#define MAXN 256
int best[MAXN+1]; int bestset[MAXN+1][MAXN];
int cur[MAXN]; int clen; int n, target, found;
typedef struct { unsigned long long w[4]; } bs;
static inline int tst(bs*b,int i){return (b->w[i>>6]>>(i&63))&1;}
static inline void st(bs*b,int i){b->w[i>>6]|=1ULL<<(i&63);}
long long nodes;
void dfs(bs forb,int nxt){
  if(found) return;
  if(clen==target){found=1;return;}
  int rem=target-clen;
  for(int x=nxt;x<n;x++){
    if(best[n-x]<rem) return;
    if(tst(&forb,x)) continue;
    nodes++;
    bs nf=forb;
    for(int i=0;i<clen;i++){int z=2*x-cur[i]; if(z<n) st(&nf,z);}
    cur[clen++]=x;
    dfs(nf,x+1);
    if(found) return;
    clen--;
  }
}
int main(int argc,char**argv){
  int NMAX=atoi(argv[1]); double tl=atof(argv[2]);
  best[0]=0; best[1]=1; bestset[1][0]=0;
  for(n=2;n<=NMAX;n++){
    target=best[n-1]+1; found=0; clen=1; cur[0]=0; nodes=0;
    bs f; memset(&f,0,sizeof f);
    clock_t t0=clock();
    dfs(f,1);
    double sec=(double)(clock()-t0)/CLOCKS_PER_SEC;
    if(found){best[n]=target; memcpy(bestset[n],cur,sizeof(int)*target);}
    else {best[n]=best[n-1]; memcpy(bestset[n],bestset[n-1],sizeof(int)*best[n]);}
    printf("%d %d %.1fs :",n,best[n],sec); for(int i=0;i<best[n];i++) printf(" %d",bestset[n][i]); printf("\n"); fflush(stdout);
    if(sec>tl) {fprintf(stderr,"time limit at n=%d\n",n); break;}
  }
}
