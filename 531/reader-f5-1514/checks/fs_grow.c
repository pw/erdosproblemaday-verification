/* fs_grow.c -- Erdos #531 checker (ours, written 2026-10-29 for submission 8a7svk; independent of the submitter's code).
   Counts monochromatic j-sets, j = 1..K, of a 2-colouring of {1..N}: a set A = {a1<...<aj} is monochromatic iff every
   nonempty subset sum lies in one colour class C (so in particular sum(A) <= N).  Grows sets: given A with subset-sum
   set FS(A) inside C, the admissible next elements x > max(A) are exactly
       C  AND  (C >> s) for every s in FS(A)        [bit x of (C>>s) is bit x+s of C],
   because FS(A+{x}) = FS(A) | {x} | (FS(A)+x), and x+s <= N is forced by membership in C.  Exhaustive by construction.
   Usage: fs_grow FILE K [N]     (FILE: '0'/'1' characters; anything else other than newlines is an error)
   Exit 0 iff no monochromatic K-set. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define MAXN 8192
#define W (MAXN/64+2)
static int N, K, NW;
static uint64_t cls[2][W];
static long long cnt[2][8];
static int ex[2][8][8], have[2][8];
static int A[8];
static void shr(const uint64_t *src, int s, uint64_t *dst){ /* dst bit i = src bit i+s */
  int q=s>>6, r=s&63;
  for(int i=0;i<NW;i++){
    uint64_t lo = (i+q<NW)? src[i+q]:0, hi=(i+q+1<NW)? src[i+q+1]:0;
    dst[i] = r? (lo>>r)|(hi<<(64-r)) : lo;
  }
}
static void grow(int c, int j, int *fs, int nfs){
  /* A[0..j-1] is monochromatic in colour c with subset sums fs[0..nfs-1] */
  cnt[c][j]++;
  if(!have[c][j]){ have[c][j]=1; for(int t=0;t<j;t++) ex[c][j][t]=A[t]; }
  if(j==K) return;
  uint64_t cand[W], tmp[W];
  memcpy(cand, cls[c], sizeof(uint64_t)*NW);
  for(int t=0;t<nfs;t++){ shr(cls[c], fs[t], tmp); for(int i=0;i<NW;i++) cand[i]&=tmp[i]; }
  int last=A[j-1];
  for(int i=0;i<NW;i++){
    uint64_t w=cand[i];
    while(w){
      int b=__builtin_ctzll(w); w&=w-1;
      int x=i*64+b;
      if(x<=last || x>N) continue;
      A[j]=x;
      int nfs2=nfs; int fs2[64];
      memcpy(fs2,fs,sizeof(int)*nfs); fs2[nfs2++]=x;
      for(int t=0;t<nfs;t++) fs2[nfs2++]=fs[t]+x;
      grow(c,j+1,fs2,nfs2);
    }
  }
}
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage: fs_grow FILE K [N]\n");return 2;}
  FILE*f=fopen(argv[1],"rb"); if(!f){perror("open");return 2;}
  static char col[MAXN+2]; int n=0,ch;
  while((ch=fgetc(f))!=EOF){
    if(ch=='0'||ch=='1'){ if(n>=MAXN){fprintf(stderr,"too long\n");return 2;} col[++n]=(char)(ch-'0'); }
    else if(ch=='\n'||ch=='\r') continue;
    else { fprintf(stderr,"bad char %d\n",ch); return 2; }
  }
  K=atoi(argv[2]); if(K<1||K>6){fprintf(stderr,"K in 1..6\n");return 2;}
  N = argc>3? atoi(argv[3]) : n; if(N<1||N>n){fprintf(stderr,"N out of range (file has %d)\n",n);return 2;}
  NW = N/64+2;
  memset(cls,0,sizeof cls);
  for(int x=1;x<=N;x++) cls[(int)col[x]][x>>6] |= 1ULL<<(x&63);
  for(int c=0;c<2;c++) for(int x=1;x<=N;x++) if(col[x]==c){ A[0]=x; int fs[1]={x}; grow(c,1,fs,1); }
  printf("N=%d K=%d\n",N,K);
  for(int j=1;j<=K;j++){
    printf("  j=%d: mono colour0=%lld colour1=%lld",j,cnt[0][j],cnt[1][j]);
    int c = have[0][j]?0:(have[1][j]?1:-1);
    if(c>=0){ printf("  e.g. colour%d {",c); for(int t=0;t<j;t++) printf("%s%d",t?",":"",ex[c][j][t]); printf("}"); }
    printf("\n");
  }
  long long m=cnt[0][K]+cnt[1][K];
  if(m==0) printf("RESULT PROPER (no monochromatic %d-set)\n",K); else printf("RESULT NOT PROPER: %lld monochromatic %d-sets\n",m,K);
  return m?1:0;
}
