/* Referee checker B (independent, written from scratch).
   Enumerates k-sets of DISTINCT positive integers x1 > x2 > ... > xk (DESCENDING order),
   requires every nonempty subset sum to be <= N and all of them to share one colour.
   Colour of integer i = byte i-1 of the first line of the file ('0'/'1').
   Usage: chkB FILE K [maxprint] [flip_pos ...]
          chkB --zero N K [maxprint]      (all-zero colouring of [N])
   Prints count of monochromatic k-sets (and per-colour), and up to maxprint examples. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int N, K, maxprint;
static unsigned char col[1<<16];
static long long cnt[2];
static int setv[16];
static int sums[16][1<<12]; /* sums[j] = all subset sums (incl 0) of first j chosen */
static void rec(int j, int prev, int c){
  int ns = 1<<j; int total = sums[j][ns-1]; /* total = sum of all chosen (last entry by construction) */
  if (j==K){ cnt[c]++; if (cnt[0]+cnt[1] <= maxprint){ printf("MONO colour %d:", c); for(int t=0;t<K;t++) printf(" %d", setv[t]); printf("\n"); } return; }
  int hi = prev-1; if (hi > N-total) hi = N-total;
  for (int x = hi; x >= 1; x--){
    /* need K-j-1 more distinct elements below x: x-1 >= K-j-1 */
    if (x-1 < K-j-1) break;
    int ok = 1;
    for (int t=0;t<ns;t++){ int s = sums[j][t]+x; if (s > N || col[s]!=c){ ok=0; break; } }
    if (!ok) continue;
    for (int t=0;t<ns;t++){ sums[j+1][t]=sums[j][t]; sums[j+1][t+ns]=sums[j][t]+x; }
    setv[j]=x; rec(j+1, x, c);
  }
}
int main(int argc, char**argv){
  int argi=1;
  if (argc>1 && !strcmp(argv[1],"--zero")){ N=atoi(argv[2]); K=atoi(argv[3]); maxprint = argc>4?atoi(argv[4]):0; for(int i=1;i<=N;i++) col[i]=0; argi=argc; }
  else {
    FILE*f=fopen(argv[1],"rb"); if(!f){perror("open");return 2;}
    static char buf[1<<17]; size_t n=fread(buf,1,sizeof buf,f); fclose(f);
    size_t L=0; while (L<n && buf[L]!='\n' && buf[L]!='\r') L++;
    for (size_t i=0;i<L;i++){ if(buf[i]!='0'&&buf[i]!='1'){ fprintf(stderr,"BAD CHAR at %zu: %d\n",i,buf[i]); return 2;} col[i+1]=buf[i]-'0'; }
    N=(int)L; K=atoi(argv[2]); maxprint = argc>3?atoi(argv[3]):0;
    for (int a=4;a<argc;a++){ int p=atoi(argv[a]); if(p<1||p>N){fprintf(stderr,"bad flip\n");return 2;} col[p]^=1; }
  }
  sums[0][0]=0;
  /* first element: choose colour from x itself */
  for (int x=N; x>=K; x--){ int c=col[x]; sums[1][0]=0; sums[1][1]=x; setv[0]=x; rec(1,x,c); }
  if (K==1){ /* rec handles j==K at depth 1 */ }
  printf("N=%d K=%d mono_total=%lld (colour0=%lld colour1=%lld)\n", N, K, cnt[0]+cnt[1], cnt[0], cnt[1]);
  return (cnt[0]+cnt[1])?1:0;
}
