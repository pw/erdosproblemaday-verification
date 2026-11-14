#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#define NV 252
typedef struct{uint64_t w[4];} bs;
int vm[NV]; bs nonadj[NV]; long cnt=0; int cur[13]; 
FILE *out;
static int popc(bs a){return __builtin_popcountll(a.w[0])+__builtin_popcountll(a.w[1])+__builtin_popcountll(a.w[2])+__builtin_popcountll(a.w[3]);}
void rec(bs cand,int depth,int need){
  if(need==0){ cnt++; if(out){ for(int i=0;i<depth;i++) fprintf(out,"%d ",vm[cur[i]]); fprintf(out,"\n");} return; }
  if(popc(cand)<need) return;
  for(int b=0;b<4;b++) while(cand.w[b]){
    int i=b*64+__builtin_ctzll(cand.w[b]); cand.w[b]&=cand.w[b]-1;
    bs nc; for(int k=0;k<4;k++) nc.w[k]=cand.w[k]&nonadj[i].w[k];
    if(popc(nc)<need-1) { if(popc(cand)<need-1) return; else continue; }
    cur[depth]=i; rec(nc,depth+1,need-1);
    if(popc(cand)<need) return;
  }
}
int main(int argc,char**argv){
  int n=0; for(int m=0;m<1024;m++) if(__builtin_popcount(m)==5) vm[n++]=m;
  for(int i=0;i<NV;i++){ memset(&nonadj[i],0,sizeof(bs)); for(int j=i+1;j<NV;j++) if(__builtin_popcount(vm[i]&vm[j])!=3) nonadj[i].w[j/64]|=1ULL<<(j%64); }
  int size=atoi(argv[1]); out = argc>2? fopen(argv[2],"w"):NULL;
  bs c; memset(&c,0,sizeof c); for(int j=0;j<NV;j++) c.w[j/64]|=1ULL<<(j%64);
  rec(c,0,size);
  printf("independent sets of size %d: %ld\n",size,cnt);
  if(out) fclose(out);
}
