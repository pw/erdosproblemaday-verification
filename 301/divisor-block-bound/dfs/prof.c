/* Exact divisor-block profile for Erdos #301 by depth-first search (independent of the CP-SAT code).
   D = divisors of M up to TMAX, increasing. F(t) = max size of a subset of D∩[1,t] with no
   1/a = sum_{b in B} 1/b (B nonempty, elements distinct; all b > a). Scaled by M: a subset is free iff
   for each chosen a, M/a is not a subset sum of {M/b : b chosen, b > a}. We decide elements in
   DECREASING order, so when a is decided, every larger chosen element is known: keep R = bitset of
   subset sums of the chosen elements (bit 0 set), a may be added iff bit M/a of R is 0, then R |= R<<(M/a).
   At each new divisor d: search for a free set of size F+1 containing d (d is the largest element).
   Pruning: chosen + #(remaining e with bit M/e of R still 0) >= F+1 (R only grows, so a blocked element
   stays blocked).  Output per divisor: d, grow/jump, F, h, nodes.  Usage: prof M TMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
typedef uint64_t u64;
static long M; static int W; static long *val; static int n; static long nodes; static int need;
static u64 *R; /* R[level*W ...] */
static int chosen[512]; static int Fk[2000]; static int curi;
static int getbit(const u64 *r, long i){ return (r[i>>6]>>(i&63))&1; }
static void shor(const u64 *src, u64 *dst, long s){ /* dst = src | (src << s), bits beyond M dropped */
  long ws=s>>6, bs=s&63; for(int i=0;i<W;i++) dst[i]=src[i];
  for(int i=W-1;i>=ws;i--){ u64 v=src[i-ws]<<bs; if(bs && i-ws-1>=0) v|=src[i-ws-1]>>(64-bs); dst[i]|=v; }
  long top=M+1; if(top%64){ dst[W-1]&=(((u64)1)<<(top%64))-1; } }
/* elements indexed 0..k-1 decreasing (idx 0 = d). level = number decided. cnt = chosen count */
static long *el; static int k; static int found;
static void dfs(int pos, int cnt, int lvl){
  nodes++;
  if(cnt>=need){ found=1; return; }
  if(pos>=k) return;
  u64 *r=R+(long)lvl*W;
  /* remaining = el[pos..k-1] = val[curi-pos .. 0]. For each split j: (#unblocked in el[pos..j-1]) + F(prefix val[0..curi-j]) */
  int cu=0, best=1<<30;
  for(int j=pos;j<k;j++){ int b=cu+Fk[curi-j]; if(b<best) best=b; if(cnt+best<need) return; if(!getbit(r,M/el[j])) cu++; }
  if(cu<best) best=cu;
  if(cnt+best<need) return;
  long t=M/el[pos];
  if(!getbit(r,t)){ chosen[cnt]=pos; shor(r,R+(long)(lvl+1)*W,t); dfs(pos+1,cnt+1,lvl+1); if(found) return; }
  dfs(pos+1,cnt,lvl);
}
int main(int argc,char**argv){
  M=atol(argv[1]); long TMAX=argc>2?atol(argv[2]):M; if(TMAX<=0) TMAX=M;
  W=(int)((M+1+63)/64);
  val=malloc(sizeof(long)*2000); n=0; for(long d=1; d<=M && d<=TMAX; d++) if(M%d==0) val[n++]=d;
  R=calloc((size_t)(n+2)*W,sizeof(u64)); el=malloc(sizeof(long)*n);
  int F=0; double Wsum=0; clock_t c0=clock();
  printf("M=%ld n=%d\n",M,n);
  for(int i=0;i<n;i++){
    k=i+1; for(int j=0;j<k;j++) el[j]=val[i-j]; /* decreasing, el[0]=d */
    need=F+1; found=0; nodes=0; curi=i;
    memset(R,0,sizeof(u64)*W); R[0]=1; /* empty sum */
    /* d must be chosen: R empty-sum only, so d is always allowed */
    chosen[0]=0; shor(R,R+W,M/el[0]); dfs(1,1,1);
    if(found){ F++; Fk[i]=F; printf("d=%ld grow F=%d h=%d nodes=%ld wit=",val[i],F,i+1-F,nodes); for(int c=0;c<F;c++) printf("%ld%s",el[chosen[c]],c+1<F?",":""); printf("\n"); }
    else { Fk[i]=F; Wsum+=1.0/val[i]; printf("d=%ld jump F=%d h=%d nodes=%ld W=%.9f\n",val[i],F,i+1-F,nodes,Wsum); }
    fflush(stdout);
  }
  printf("done cpu=%.1fs\n",(double)(clock()-c0)/CLOCKS_PER_SEC);
}
