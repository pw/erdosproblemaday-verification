/* Route B in C (seat C): same point-driven canonical algorithm as routeB.py (see its docstring),
   ported for speed. Least uncovered point z; branch on the modulus m covering z (class z mod m);
   forbid residue z mod m' for every unused m' < m. Leaf: U empty -> count (private sets are kept
   nonempty on insertion). No normalisation, no lemma.  usage: routeB <dump 0|1> m1 m2 ... (sorted asc) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int K; static long long Mod[64]; static long long L; static long W;
static u64 *U[70]; static u64 *P[70][70];
static int used[64]; static int chosenM[70]; static long long chosenR[70];
/* forbidden residues: stack of (modulus index, residue) */
static unsigned char *forb[64];
static long long nodes=0; static long long total=0; static long long bycount[70];
static int dump;
#define HS (1<<20)
static u64 hkey[HS]; static long long hval[HS]; static int hused[HS];
static void hadd(u64 key){ u64 h=(key*0x9E3779B97F4A7C15ULL)>>44; while(hused[h]&&hkey[h]!=key) h=(h+1)&(HS-1); if(!hused[h]){hused[h]=1;hkey[h]=key;hval[h]=0;} hval[h]++; }
static long long gcdll(long long a,long long b){while(b){long long t=a%b;a=b;b=t;}return a;}
static inline int isset(const u64*C,long long z){return (C[z>>6]>>(z&63))&1;}
/* class bitset generated into buffer */
static u64 *cbuf[70];
static void mkclass(u64*C,long long n,long long a){ memset(C,0,W*8); for(long long z=a;z<L;z+=n) C[z>>6]|=1ULL<<(z&63); }
static u64 **pre[64]; static int usepre;

static void dfs(int k, long startw){
  nodes++;
  const u64 *Uk=U[k];
  long w=startw; while(w<W && Uk[w]==0) w++;
  if(w==W){ total++; bycount[k]++; u64 key=0; for(int j=0;j<k;j++) key|=1ULL<<chosenM[j]; hadd(key);
    if(dump){ printf("SYS"); for(int j=0;j<k;j++) printf(" %lld/%lld",chosenR[j],Mod[chosenM[j]]); printf("\n"); }
    return; }
  long long z = (long long)w*64 + __builtin_ctzll(Uk[w]);
  for(int i=0;i<K;i++){
    if(used[i]) continue;
    long long n=Mod[i], r=z%n;
    if(forb[i][r]) continue;
    const u64 *C;
    if(usepre) C=pre[i][r]; else { mkclass(cbuf[k],n,r); C=cbuf[k]; }
    int ok=1;
    for(int j=0;j<k&&ok;j++){ const u64*Pj=P[k][j]; u64*Pn=P[k+1][j]; u64 any=0; for(long t=0;t<W;t++){u64 v=Pj[t]&~C[t]; Pn[t]=v; any|=v;} if(!any) ok=0; }
    if(!ok) continue;
    { u64*Pn=P[k+1][k]; u64*Un=U[k+1]; for(long t=0;t<W;t++){ Pn[t]=Uk[t]&C[t]; Un[t]=Uk[t]&~C[t]; } }
    /* forbid z mod m' for unused m' < m */
    int ch[64]; int nch=0;
    for(int j=0;j<i;j++) if(!used[j]){ long long rr=z%Mod[j]; if(!forb[j][rr]){ forb[j][rr]=1; ch[nch++]=j; } }
    used[i]=1; chosenM[k]=i; chosenR[k]=r;
    dfs(k+1, w);
    used[i]=0;
    for(int t=0;t<nch;t++) forb[ch[t]][z%Mod[ch[t]]]=0;
  }
}
int main(int argc,char**argv){
  dump=atoi(argv[1]); K=argc-2; L=1;
  for(int i=0;i<K;i++){ Mod[i]=atoll(argv[2+i]); if(i&&Mod[i]<=Mod[i-1]){fprintf(stderr,"moduli must be strictly increasing\n");return 1;} L=L/gcdll(L,Mod[i])*Mod[i]; }
  W=(L+63)/64;
  double premem=0; for(int i=0;i<K;i++) premem += (double)Mod[i]*W*8;
  usepre = premem < 3e9;
  fprintf(stderr,"K=%d L=%lld W=%ld precompute=%d (%.0f MB)\n",K,L,W,usepre,premem/1e6);
  for(int i=0;i<K;i++){ forb[i]=calloc(Mod[i],1); if(usepre){ pre[i]=malloc(sizeof(u64*)*Mod[i]); for(long long a=0;a<Mod[i];a++){ pre[i][a]=malloc(W*8); mkclass(pre[i][a],Mod[i],a);} } }
  for(int d=0;d<=K+1;d++){ U[d]=calloc(W,8); cbuf[d]=calloc(W,8); for(int j=0;j<=K;j++) P[d][j]=calloc(W,8); }
  for(long long z=0;z<L;z++) U[0][z>>6]|=1ULL<<(z&63);
  dfs(0,0);
  printf("MODULI"); for(int i=0;i<K;i++) printf(" %lld",Mod[i]); printf("\nL %lld nodes %lld\nTOTAL %lld\n",L,nodes,total);
  for(int k=0;k<=K;k++) if(bycount[k]) printf("CLASSES %d count %lld\n",k,bycount[k]);
  for(long h=0;h<HS;h++) if(hused[h]){ printf("SET"); for(int i=0;i<K;i++) if(hkey[h]>>i&1) printf(" %lld",Mod[i]); printf(" : %lld\n",hval[h]); }
  return 0;
}
