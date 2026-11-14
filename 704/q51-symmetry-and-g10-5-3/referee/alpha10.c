// Referee: alpha(J(10,5,3)) and count of maximum independent sets, by bitset branch and bound (vertex-transitive: count sets containing v0, scale).
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#define NV 252
typedef struct { uint64_t w[4]; } BS;
static BS nonadj[NV]; static int vm[NV]; static int best=0; static long cnt[64];
static int pc(BS*b){return __builtin_popcountll(b->w[0])+__builtin_popcountll(b->w[1])+__builtin_popcountll(b->w[2])+__builtin_popcountll(b->w[3]);}
static int target;
// enumerate all independent sets in increasing vertex order, count by size >= target, track max
static void rec(int sz, BS cand){
  if(sz>best) best=sz;
  if(sz>=target) cnt[sz]++;
  if(sz+pc(&cand)<target) return;
  for(int k=0;k<4;k++) while(cand.w[k]){ int b=__builtin_ctzll(cand.w[k]); cand.w[k]&=cand.w[k]-1; int v=k*64+b;
    BS c2; for(int t=0;t<4;t++) c2.w[t]=cand.w[t]&nonadj[v].w[t];
    if(sz+1+pc(&c2)>=target || sz+1>best) rec(sz+1,c2); }
}
int main(int argc,char**argv){ int n=0; for(int m=0;m<1024;m++) if(__builtin_popcount(m)==5) vm[n++]=m;
  for(int i=0;i<NV;i++){ memset(&nonadj[i],0,sizeof(BS)); for(int j=0;j<NV;j++) if(j>i && __builtin_popcount(vm[i]&vm[j])!=3) nonadj[i].w[j/64]|=1ULL<<(j%64); }
  // sets containing vertex 0 (={0,1,2,3,4}), as smallest element ordering = all sets with 0 as min index
  target=12; best=0; memset(cnt,0,sizeof cnt);
  BS c=nonadj[0]; rec(1,c);
  printf("max independent set containing v0: %d ; # with v0 of size 12: %ld, size 13: %ld\n",best,cnt[12],cnt[13]);
  // global count of size-12 (all start vertices)
  long tot12=0,tot13=0; int gbest=0;
  for(int v=0;v<NV;v++){ best=0; memset(cnt,0,sizeof cnt); rec(1,nonadj[v]); tot12+=cnt[12]; tot13+=cnt[13]; if(best>gbest) gbest=best; }
  printf("alpha = %d ; total independent 12-sets = %ld ; 13-sets = %ld\n",gbest,tot12,tot13);
}
