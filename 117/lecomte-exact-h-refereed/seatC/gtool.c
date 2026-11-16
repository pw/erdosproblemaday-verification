/* gtool.c -- clique / colouring workhorse for graphs with <= 1024 vertices.
 *
 * stdin:  n  then n lines, each a 0/1 string of length n (adjacency rows)
 * argv:   mode args...
 *   clique  TLIM_SEC LB         exact max clique (bitset MCQ, colour bound); stops at TLIM.
 *                               prints: CLIQUE size proven(0/1) nodes  v1 v2 ...
 *   heurclique ITERS SEED       randomised greedy + 1-swap local search; prints CLIQUE size 0 0 v...
 *   dsatur                      prints: COL k c0 c1 ... c(n-1)
 *   tabu K ITERS SEED           tabucol with K colours; prints COL K c... or FAIL K conflicts
 * Witnesses are re-checked independently in Python (graphlib.check_*).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 1024
#define W 16
typedef uint64_t bs[W];

static int n;
static bs adj[MAXN];
static char adjm[MAXN][MAXN];

static inline void bs_clear(bs a){memset(a,0,sizeof(bs));}
static inline void bs_set(bs a,int i){a[i>>6]|=1ULL<<(i&63);}
static inline void bs_reset(bs a,int i){a[i>>6]&=~(1ULL<<(i&63));}
static inline int bs_test(const bs a,int i){return (a[i>>6]>>(i&63))&1;}
static inline int bs_empty(const bs a){for(int w=0;w<W;w++) if(a[w]) return 0; return 1;}
static inline int bs_count(const bs a){int c=0;for(int w=0;w<W;w++) c+=__builtin_popcountll(a[w]);return c;}
static inline int bs_first(const bs a){for(int w=0;w<W;w++) if(a[w]) return w*64+__builtin_ctzll(a[w]); return -1;}

static void read_graph(void){
  if(scanf("%d",&n)!=1){fprintf(stderr,"bad input\n");exit(2);}
  if(n>MAXN){fprintf(stderr,"n too big\n");exit(2);}
  static char buf[MAXN+8];
  for(int i=0;i<n;i++){
    if(scanf("%s",buf)!=1 || (int)strlen(buf)!=n){fprintf(stderr,"bad row %d\n",i);exit(2);}
    bs_clear(adj[i]);
    for(int j=0;j<n;j++){adjm[i][j]=(buf[j]=='1'); if(buf[j]=='1') bs_set(adj[i],j);}
  }
  for(int i=0;i<n;i++){ if(adjm[i][i]){fprintf(stderr,"loop\n");exit(2);} for(int j=0;j<n;j++) if(adjm[i][j]!=adjm[j][i]){fprintf(stderr,"asym\n");exit(2);} }
}

/* ---------- exact max clique (BBMC-style) on relabelled graph ---------- */
static int ord[MAXN];         /* new index -> old */
static bs radj[MAXN];
static int best[MAXN], bestsz, cur[MAXN], cursz;
static long long nodes; static double tlim; static clock_t t0; static int timed_out;

static void expand(bs P){
  nodes++;
  if((nodes & 1023)==0 && (double)(clock()-t0)/CLOCKS_PER_SEC > tlim){timed_out=1;}
  if(timed_out) return;
  int verts[MAXN], cols[MAXN], m=0;
  bs Q; memcpy(Q,P,sizeof(bs));
  int c=0;
  while(!bs_empty(Q)){
    c++;
    bs R; memcpy(R,Q,sizeof(bs));
    while(!bs_empty(R)){
      int v=bs_first(R);
      bs_reset(R,v); bs_reset(Q,v);
      for(int w=0;w<W;w++) R[w]&=~radj[v][w];
      verts[m]=v; cols[m]=c; m++;
    }
  }
  bs PP; memcpy(PP,P,sizeof(bs));
  for(int idx=m-1; idx>=0; idx--){
    if(cursz+cols[idx] <= bestsz) return;
    int v=verts[idx];
    bs NP; for(int w=0;w<W;w++) NP[w]=PP[w]&radj[v][w];
    cur[cursz++]=v;
    if(bs_empty(NP)){ if(cursz>bestsz){bestsz=cursz; memcpy(best,cur,sizeof(int)*cursz);} }
    else expand(NP);
    cursz--;
    bs_reset(PP,v);
    if(timed_out) return;
  }
}

static int degcmp_deg[MAXN];
static int cmpdeg(const void*a,const void*b){int x=*(const int*)a,y=*(const int*)b; return degcmp_deg[y]-degcmp_deg[x];}

static void do_clique(double tl, int lb){
  for(int i=0;i<n;i++){ord[i]=i; degcmp_deg[i]=bs_count(adj[i]);}
  qsort(ord,n,sizeof(int),cmpdeg);
  int pos[MAXN]; for(int i=0;i<n;i++) pos[ord[i]]=i;
  for(int i=0;i<n;i++){ bs_clear(radj[i]); for(int j=0;j<n;j++) if(adjm[ord[i]][ord[j]]) bs_set(radj[i],j); }
  bestsz = lb>0 ? lb-1 : 0;   /* search only for cliques of size >= lb */
  int found=0;
  cursz=0; nodes=0; tlim=tl; t0=clock(); timed_out=0;
  bs P; bs_clear(P); for(int i=0;i<n;i++) bs_set(P,i);
  int base=bestsz;
  expand(P);
  found = bestsz>base;
  printf("CLIQUE %d %d %lld", found?bestsz:0, timed_out?0:1, nodes);
  if(found) for(int i=0;i<bestsz;i++) printf(" %d",ord[best[i]]);
  printf("\n");
  /* semantics: if found, the clique printed is maximum among cliques of size>=lb (proven if flag 1).
     if not found and proven, no clique of size >= lb exists. */
}

/* ---------- heuristic clique ---------- */
static unsigned long long rng_s=88172645463325252ULL;
static inline unsigned long long rnd(void){rng_s^=rng_s<<13; rng_s^=rng_s>>7; rng_s^=rng_s<<17; return rng_s;}

static void do_heurclique(int iters, unsigned long long seed){
  rng_s = seed*2654435761ULL+12345;
  int bestc[MAXN], bsz=0;
  int C[MAXN], csz;
  for(int it=0; it<iters; it++){
    bs P; bs_clear(P); for(int i=0;i<n;i++) bs_set(P,i);
    csz=0;
    while(!bs_empty(P)){
      /* pick a random vertex among those with max degree inside P (with prob 1/2) else random */
      int cand[MAXN], nc=0; for(int v=0;v<n;v++) if(bs_test(P,v)) cand[nc++]=v;
      int v;
      if(rnd()&1){ int bd=-1; int ties=0; v=cand[0];
        for(int k=0;k<nc;k++){ int u=cand[k]; int d=0; for(int w=0;w<W;w++) d+=__builtin_popcountll(P[w]&adj[u][w]);
          if(d>bd){bd=d; v=u; ties=1;} else if(d==bd){ ties++; if(rnd()%ties==0) v=u; } }
      } else v=cand[rnd()%nc];
      C[csz++]=v;
      for(int w=0;w<W;w++) P[w]&=adj[v][w];
    }
    /* 1-swap plateau moves: try remove one vertex and add two */
    int improved=1, rounds=0;
    while(improved && rounds<50){
      improved=0; rounds++;
      for(int r=0;r<csz && !improved;r++){
        bs P2; for(int w=0;w<W;w++) P2[w]=~0ULL;
        for(int i=0;i<csz;i++) if(i!=r) for(int w=0;w<W;w++) P2[w]&=adj[C[i]][w];
        for(int i=0;i<csz;i++) bs_reset(P2,C[i]);
        for(int u=n; u<W*64; u++) bs_reset(P2,u);
        /* find two adjacent vertices in P2 */
        for(int u=0;u<n && !improved;u++) if(bs_test(P2,u)){
          for(int w=0;w<W;w++) if(P2[w]&adj[u][w]){ int x=w*64+__builtin_ctzll(P2[w]&adj[u][w]);
            C[r]=u; C[csz++]=x; improved=1; break; }
        }
      }
    }
    if(csz>bsz){bsz=csz; memcpy(bestc,C,sizeof(int)*csz);}
  }
  printf("CLIQUE %d 0 0",bsz); for(int i=0;i<bsz;i++) printf(" %d",bestc[i]); printf("\n");
}

/* ---------- DSATUR ---------- */
static void do_dsatur(void){
  static int col[MAXN]; static bs satc[MAXN]; /* colours seen, up to 1024 colours */
  int deg[MAXN]; for(int i=0;i<n;i++){col[i]=-1; bs_clear(satc[i]); deg[i]=bs_count(adj[i]);}
  int k=0;
  for(int step=0;step<n;step++){
    int v=-1, bsat=-1, bdeg=-1;
    for(int u=0;u<n;u++) if(col[u]<0){ int s=bs_count(satc[u]); if(s>bsat || (s==bsat && deg[u]>bdeg)){v=u;bsat=s;bdeg=deg[u];} }
    int c=0; while(bs_test(satc[v],c)) c++;
    col[v]=c; if(c+1>k) k=c+1;
    for(int u=0;u<n;u++) if(adjm[v][u]) bs_set(satc[u],c);
  }
  printf("COL %d",k); for(int i=0;i<n;i++) printf(" %d",col[i]); printf("\n");
}

/* ---------- Tabucol ---------- */
static void do_tabu(int K, long long iters, unsigned long long seed){
  rng_s = seed*2654435761ULL+777;
  int *col=malloc(sizeof(int)*n);
  int *gam=calloc((size_t)n*K,sizeof(int));
  long long *tabu=calloc((size_t)n*K,sizeof(long long));
  for(int i=0;i<n;i++) col[i]=rnd()%K;
  for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(adjm[i][j]) gam[i*K+col[j]]++;
  long long conf=0; for(int i=0;i<n;i++) conf+=gam[i*K+col[i]]; conf/=2;
  long long bestconf=conf;
  for(long long it=0; it<iters && conf>0; it++){
    int bv=-1,bc=-1; int bdelta=1<<30; int ties=0;
    for(int v=0;v<n;v++){ int gv=gam[v*K+col[v]]; if(gv==0) continue;
      for(int c=0;c<K;c++){ if(c==col[v]) continue; int d=gam[v*K+c]-gv;
        int istabu = tabu[(size_t)v*K+c]>it;
        if(istabu && !(conf+d<bestconf)) continue;
        if(d<bdelta){bdelta=d;bv=v;bc=c;ties=1;} else if(d==bdelta){ties++; if(rnd()%ties==0){bv=v;bc=c;}} } }
    if(bv<0) continue;
    int old=col[bv]; col[bv]=bc; conf+=bdelta;
    for(int u=0;u<n;u++) if(adjm[bv][u]){gam[u*K+old]--; gam[u*K+bc]++;}
    tabu[(size_t)bv*K+old]=it+ (long long)(0.6*conf) + (rnd()%10);
    if(conf<bestconf) bestconf=conf;
  }
  if(conf==0){printf("COL %d",K); for(int i=0;i<n;i++) printf(" %d",col[i]); printf("\n");}
  else printf("FAIL %d %lld\n",K,bestconf);
}

int main(int argc,char**argv){
  if(argc<2){fprintf(stderr,"usage\n");return 2;}
  read_graph();
  if(!strcmp(argv[1],"clique")) do_clique(atof(argv[2]), argc>3?atoi(argv[3]):0);
  else if(!strcmp(argv[1],"heurclique")) do_heurclique(atoi(argv[2]), strtoull(argv[3],0,10));
  else if(!strcmp(argv[1],"dsatur")) do_dsatur();
  else if(!strcmp(argv[1],"tabu")) do_tabu(atoi(argv[2]), atoll(argv[3]), strtoull(argv[4],0,10));
  else {fprintf(stderr,"bad mode\n"); return 2;}
  return 0;
}
