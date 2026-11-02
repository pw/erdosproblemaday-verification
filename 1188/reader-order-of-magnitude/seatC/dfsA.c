/* Route A (seat C): modulus-driven exact DFS counting minimal distinct covering systems
   whose moduli are drawn from a given list (processed in the given order).
   Works in Z/L, L = lcm(list), with bitsets. No number-theoretic lemma is used:
   pruning is only (1) a new class must meet the currently uncovered set (else it has no
   private point, now or later), (2) every chosen class keeps a nonempty private set
   (points covered by it alone; private sets only shrink as classes are added),
   (3) density: |U| <= sum over remaining moduli m of L/m, (4) once U is empty, every
   further class would have no private point, so exactly one completion (skip all).
   Optional translation normalisation: residue of the first chosen class fixed to 0,
   weight = its modulus (translation z->z+b is a bijection between {a_first = c} and
   {a_first = 0}).  Usage: dfsA <norm 0|1> <dump 0|1> m1 m2 ... */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned long long u64;
static int K; static long long Mod[64]; static long long L; static long W;
static u64 **cls[64];           /* cls[i][a] bitset of a mod Mod[i] in Z/L */
static double remcap[65];      /* sum_{j>=i} L/Mod[j] */
static int norm, dump;
static u64 *U[66]; static u64 *P[66][66]; static long long ucount[66];
static int chosenIdx[66], chosenRes[66];
static __int128 total = 0;
static __int128 bycount[66];
/* histogram by moduli-set mask (K <= 62) : simple hash */
#define HS (1<<20)
static u64 hkey[HS]; static __int128 hval[HS]; static int hused[HS];
static void hadd(u64 key, __int128 v){ u64 h = (key * 0x9E3779B97F4A7C15ULL) >> 44; while(hused[h] && hkey[h]!=key) h=(h+1)&(HS-1); if(!hused[h]){hused[h]=1;hkey[h]=key;hval[h]=0;} hval[h]+=v; }
static long long nodes = 0;

static long long gcdll(long long a,long long b){while(b){long long t=a%b;a=b;b=t;}return a;}
static int popc(const u64*x){ long long c=0; for(long w=0;w<W;w++) c+=__builtin_popcountll(x[w]); return (int)c; }
static void print128(__int128 v){ char buf[64]; int i=63; buf[i]=0; if(v==0){printf("0");return;} while(v>0){buf[--i]='0'+(int)(v%10); v/=10;} printf("%s",buf+i); }

static void record(int k, __int128 weight){
  total += weight; bycount[k] += weight;
  u64 key=0; for(int j=0;j<k;j++) key |= 1ULL<<chosenIdx[j];
  hadd(key, weight);
  if(dump){ printf("SYS w="); print128(weight); printf(" :"); for(int j=0;j<k;j++) printf(" %d/%lld", chosenRes[j], Mod[chosenIdx[j]]); printf("\n"); }
}

/* depth i = index of next modulus to decide; k = number of chosen classes so far */
static void dfs(int i, int k, __int128 weight){
  nodes++;
  if(ucount[k]==0){ record(k, weight); return; }
  if(i==K) return;
  if((double)ucount[k] > remcap[i] + 0.5) return;   /* density prune */
  /* option: skip modulus i */
  dfs(i+1, k, weight);
  /* option: choose a residue */
  long long n = Mod[i];
  long long amax = (norm && k==0) ? 1 : n;
  __int128 w2 = (norm && k==0) ? weight * n : weight;
  u64 *Un = U[k+1];
  for(long long a=0;a<amax;a++){
    u64 *C = cls[i][a];
    /* intersection with U */
    long long inter=0; const u64 *Uk=U[k];
    for(long w=0;w<W;w++) inter += __builtin_popcountll(Uk[w] & C[w]);
    if(inter==0) continue;
    int ok=1;
    for(int j=0;j<k && ok;j++){
      const u64 *Pj=P[k][j]; u64 *Pn=P[k+1][j]; u64 any=0;
      for(long w=0;w<W;w++){ u64 t=Pj[w] & ~C[w]; Pn[w]=t; any|=t; }
      if(!any) ok=0;
    }
    if(!ok) continue;
    { u64 *Pn=P[k+1][k]; for(long w=0;w<W;w++){ Pn[w]=Uk[w] & C[w]; Un[w]=Uk[w] & ~C[w]; } }
    ucount[k+1] = ucount[k]-inter;
    chosenIdx[k]=i; chosenRes[k]=(int)a;
    dfs(i+1, k+1, w2);
  }
}

int main(int argc, char**argv){
  if(argc<4){fprintf(stderr,"usage\n");return 1;}
  norm=atoi(argv[1]); dump=atoi(argv[2]); K=argc-3;
  L=1; for(int i=0;i<K;i++){ Mod[i]=atoll(argv[3+i]); L = L/gcdll(L,Mod[i])*Mod[i]; }
  W=(L+63)/64;
  fprintf(stderr,"K=%d L=%lld W=%ld\n",K,L,W);
  for(int i=0;i<K;i++){
    long long n=Mod[i]; cls[i]=malloc(sizeof(u64*)*n);
    for(long long a=0;a<n;a++){ cls[i][a]=calloc(W,8); for(long long z=a; z<L; z+=n) cls[i][a][z>>6] |= 1ULL<<(z&63); }
  }
  remcap[K]=0; for(int i=K-1;i>=0;i--) remcap[i]=remcap[i+1]+(double)L/(double)Mod[i];
  for(int d=0; d<=K+1; d++){ U[d]=calloc(W,8); for(int j=0;j<=K;j++) P[d][j]=calloc(W,8); }
  for(long long z=0; z<L; z++) U[0][z>>6] |= 1ULL<<(z&63);
  ucount[0]=L;
  dfs(0,0,1);
  printf("MODULI"); for(int i=0;i<K;i++) printf(" %lld",Mod[i]); printf("\nL %lld nodes %lld\nTOTAL ",L,nodes); print128(total); printf("\n");
  for(int k=0;k<=K;k++) if(bycount[k]){ printf("CLASSES %d count ",k); print128(bycount[k]); printf("\n"); }
  for(long h=0;h<HS;h++) if(hused[h]){ printf("SET"); for(int i=0;i<K;i++) if(hkey[h]>>i&1) printf(" %lld",Mod[i]); printf(" : "); print128(hval[h]); printf("\n"); }
  return 0;
}
