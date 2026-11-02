/* Route B2 (seat C): routeB.c's point-driven canonical algorithm with a DYNAMIC PERIOD.
   The uncovered set U and private sets P_j are periodic mod T = lcm(chosen moduli); we store them
   on Z/T and lift (replicate) only when a chosen modulus enlarges T. Same search tree as routeB.c
   (node counts must agree exactly), much cheaper per node when T << lcm(all moduli).
   usage: routeB2 <dump 0|1> m1 < m2 < ... */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int K; static long long Mod[64]; static long long Lmax;
static u64 *U[70]; static u64 *P[70][70]; static long long Tper[70];
static int used[64]; static int chosenM[70]; static long long chosenR[70];
static unsigned char *forb[64];
static long long nodes=0, total=0, bycount[70];
static int dump;
#define HS (1<<20)
static u64 hkey[HS]; static long long hval[HS]; static int hused[HS];
static void hadd(u64 key){ u64 h=(key*0x9E3779B97F4A7C15ULL)>>44; while(hused[h]&&hkey[h]!=key) h=(h+1)&(HS-1); if(!hused[h]){hused[h]=1;hkey[h]=key;hval[h]=0;} hval[h]++; }
static long long gcdll(long long a,long long b){while(b){long long t=a%b;a=b;b=t;}return a;}
static inline int getbit(const u64*s,long long p){return (s[p>>6]>>(p&63))&1;}
/* len (1..64) bits of src starting at p, p+len <= T (array padded by one word) */
static inline u64 extract(const u64*s,long long p,int len){
  long long w=p>>6; int o=p&63; u64 v = o ? ((s[w]>>o)|(s[w+1]<<(64-o))) : s[w];
  return len==64 ? v : (v & ((1ULL<<len)-1));
}
/* 64 bits of the T-periodic set src starting at absolute position p (0<=p<T) */
static inline u64 get64(const u64*s,long long T,long long p){
  u64 r=0; int filled=0;
  while(filled<64){ long long room=T-p; int len = (64-filled) < room ? (64-filled) : (int)room;
    r |= extract(s,p,len) << filled; filled += len; p += len; if(p==T) p=0; }
  return r;
}
/* dst (period T2) = lift of src (period T) ; T | T2 ; src has no bits at positions >= T */
static long long liftwords=0, opwords=0;
static void lift(u64*dst,long long T2,const u64*src,long long T){
  long long W2=(T2+63)/64, W=(T+63)/64;
  memset(dst,0,(W2+1)*8);
  for(long long off=0; off<T2; off+=T){
    long long base=off>>6; int sh=off&63;
    if(sh==0){ for(long long w=0;w<W;w++) dst[base+w] |= src[w]; }
    else { for(long long w=0;w<W;w++){ dst[base+w] |= src[w]<<sh; dst[base+w+1] |= src[w]>>(64-sh); } }
  }
  liftwords += W2;
  if(T2&63) dst[W2-1] &= (1ULL<<(T2&63))-1;
  dst[W2]=0;
}
static u64 *tmp[70]; static u64 **pre[64];
static void mkclass(u64*C,long long T,long long n,long long a){ long long W=(T+63)/64; memset(C,0,W*8); for(long long z=a%n;z<T;z+=n) C[z>>6]|=1ULL<<(z&63); }

static void dfs(int k, long long T){
  nodes++;
  long long W=(T+63)/64;
  const u64 *Uk=U[k];
  long w=0; while(w<W && Uk[w]==0) w++;
  if(w==W){ total++; bycount[k]++; u64 key=0; for(int j=0;j<k;j++) key|=1ULL<<chosenM[j]; hadd(key);
    if(dump){ printf("SYS"); for(int j=0;j<k;j++) printf(" %lld/%lld",chosenR[j],Mod[chosenM[j]]); printf("\n"); }
    return; }
  long long z=(long long)w*64+__builtin_ctzll(Uk[w]);
  for(int i=0;i<K;i++){
    if(used[i]) continue;
    long long n=Mod[i], r=z%n;
    if(forb[i][r]) continue;
    long long T2 = T/gcdll(T,n)*n; long long W2=(T2+63)/64;
    const u64 *C=pre[i][r];
    int ok=1;
    for(int j=0;j<k&&ok;j++){
      u64 *Pn=P[k+1][j];
      if(T2==T) memcpy(Pn,P[k][j],W2*8); else lift(Pn,T2,P[k][j],T);
      u64 any=0; opwords+=W2; for(long t=0;t<W2;t++){ u64 v=Pn[t]&~C[t]; Pn[t]=v; any|=v; }
      if(!any) ok=0;
    }
    if(!ok) continue;
    { u64*Un=U[k+1]; u64*Pn=P[k+1][k];
      if(T2==T) memcpy(Un,Uk,W2*8); else lift(Un,T2,Uk,T);
      for(long t=0;t<W2;t++){ Pn[t]=Un[t]&C[t]; Un[t]&=~C[t]; } }
    int ch[64]; int nch=0;
    for(int j=0;j<i;j++) if(!used[j]){ long long rr=z%Mod[j]; if(!forb[j][rr]){ forb[j][rr]=1; ch[nch++]=j; } }
    used[i]=1; chosenM[k]=i; chosenR[k]=r;
    dfs(k+1,T2);
    used[i]=0;
    for(int t=0;t<nch;t++) forb[ch[t]][z%Mod[ch[t]]]=0;
  }
}
int main(int argc,char**argv){
  dump=atoi(argv[1]); K=argc-2; Lmax=1;
  for(int i=0;i<K;i++){ Mod[i]=atoll(argv[2+i]); if(i&&Mod[i]<=Mod[i-1]){fprintf(stderr,"increasing please\n");return 1;} Lmax=Lmax/gcdll(Lmax,Mod[i])*Mod[i]; }
  long long Wm=(Lmax+63)/64;
  fprintf(stderr,"K=%d Lmax=%lld Wmax=%lld (%.0f MB per level set)\n",K,Lmax,Wm,(double)Wm*8*(K+2)*(K+2)/1e6);
  for(int i=0;i<K;i++){ forb[i]=calloc(Mod[i],1); pre[i]=malloc(sizeof(u64*)*Mod[i]); for(long long a=0;a<Mod[i];a++){ pre[i][a]=calloc(Wm+1,8); mkclass(pre[i][a],Lmax,Mod[i],a);} }
  for(int d=0;d<=K+1;d++){ U[d]=calloc(Wm+1,8); tmp[d]=calloc(Wm+1,8); for(int j=0;j<=K;j++){ P[d][j]=calloc(Wm+1,8); if(!P[d][j]){fprintf(stderr,"oom\n");return 2;} } }
  U[0][0]=1; /* period 1: the single point, uncovered */
  dfs(0,1);
  printf("MODULI"); for(int i=0;i<K;i++) printf(" %lld",Mod[i]); printf("\nLmax %lld nodes %lld\nTOTAL %lld\n",Lmax,nodes,total); fprintf(stderr,"liftwords %lld opwords %lld\n",liftwords,opwords);
  for(int k=0;k<=K;k++) if(bycount[k]) printf("CLASSES %d count %lld\n",k,bycount[k]);
  for(long h=0;h<HS;h++) if(hused[h]){ printf("SET"); for(int i=0;i<K;i++) if(hkey[h]>>i&1) printf(" %lld",Mod[i]); printf(" : %lld\n",hval[h]); }
  return 0;
}
