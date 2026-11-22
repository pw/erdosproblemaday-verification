/* knm_check.c: written 2026-11-19 (Claude Opus 5.5, under the author's direction).
   Written from the definition only; shares no code with the search programs.
   k(n,m) = least k such that every oriented graph on k vertices has n pairwise
   non-adjacent vertices or a transitive tournament on m vertices.
   A witness for k(n,m) >= N+1 is an oriented graph on N vertices with
   independence number <= n-1 and no transitive tournament on m vertices.
   Usage: knm_check N n m arcfile [flip a b]
   arcfile: first line "N A" (vertices, arcs), then lines "a b" meaning a -> b;
   lines starting with # ignored. The header must match N and the arc count.
   (2026-11-20: header reading added for the Zenodo record; nothing else changed.)
   Prints: arcs, degree ranges, exact independence number, exact size of the
   largest transitive subtournament, and PASS/FAIL for (n,m). Exit 0 iff PASS. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 B;
static int N;
static B OUT[128], ADJ[128];
static int bitcount(B x){ unsigned long long lo=(unsigned long long)x, hi=(unsigned long long)(x>>64); return __builtin_popcountll(lo)+__builtin_popcountll(hi);}
static int lowbit(B x){ unsigned long long lo=(unsigned long long)x; if(lo) return __builtin_ctzll(lo); return 64+__builtin_ctzll((unsigned long long)(x>>64)); }
static B ONE(int i){ return ((B)1)<<i; }
/* largest transitive subtournament: choose a source v, then recurse in OUT[v] within candidates */
static int besttt;
static void tt(B cand, int depth){
  if(depth>besttt) besttt=depth;
  if(depth+bitcount(cand)<=besttt) return;
  /* every transitive tournament has a unique source, so each is enumerated once
     when its vertices are taken in order; v is NOT removed from later branches. */
  B rest=cand;
  while(rest){ int v=lowbit(rest); rest&=~ONE(v); tt(cand&OUT[v], depth+1); }
}
/* independence number: max clique in the non-adjacency graph */
static int bestind;
static void ind(B cand, int depth){
  if(depth>bestind) bestind=depth;
  if(depth+bitcount(cand)<=bestind) return;
  while(cand){ int v=lowbit(cand); cand&=~ONE(v); ind(cand&~ADJ[v], depth+1); if(depth+bitcount(cand)<=bestind) return; }
}
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 2;}
  N=atoi(argv[1]); int n=atoi(argv[2]), m=atoi(argv[3]);
  if(N<1||N>128){fprintf(stderr,"N out of range\n");return 2;}
  FILE*f=fopen(argv[4],"r"); if(!f){perror("open");return 2;}
  char line[256]; int arcs=0, bad=0, hN=-1, hA=-1;
  while(fgets(line,sizeof line,f)){
    if(line[0]=='#'||line[0]=='\n') continue;
    if(hN<0){ if(sscanf(line,"%d %d",&hN,&hA)!=2||hN!=N){fprintf(stderr,"header \"N A\" missing or N differs\n");return 2;} continue; }
    int a,b; if(sscanf(line,"%d %d",&a,&b)!=2){fprintf(stderr,"parse: %s",line);return 2;}
    if(a<0||b<0||a>=N||b>=N){fprintf(stderr,"vertex out of range %d %d\n",a,b);return 2;}
    if(a==b){printf("LOOP at %d\n",a);bad=1;continue;}
    if(OUT[a]&ONE(b)){printf("DUPLICATE arc %d->%d\n",a,b);bad=1;continue;}
    OUT[a]|=ONE(b); arcs++;
  }
  fclose(f);
  if(arcs!=hA){fprintf(stderr,"header says %d arcs, file has %d\n",hA,arcs);return 2;}
  if(argc>=8 && strcmp(argv[5],"flip")==0){ /* negative control: reverse or add/remove one pair */
    int a=atoi(argv[6]), b=atoi(argv[7]);
    if(OUT[a]&ONE(b)){OUT[a]&=~ONE(b);OUT[b]|=ONE(a);printf("control: reversed %d->%d\n",a,b);}
    else if(OUT[b]&ONE(a)){OUT[b]&=~ONE(a);printf("control: removed %d->%d\n",b,a);arcs--;}
    else {OUT[a]|=ONE(b);printf("control: added %d->%d\n",a,b);arcs++;}
  }
  for(int a=0;a<N;a++) for(int b=0;b<N;b++) if((OUT[a]&ONE(b))&&(OUT[b]&ONE(a))&&a<b){printf("2-CYCLE %d %d\n",a,b);bad=1;}
  int dmin=1000,dmax=-1,imin=1000,imax=-1;
  for(int a=0;a<N;a++){ ADJ[a]=OUT[a]; }
  for(int a=0;a<N;a++) for(int b=0;b<N;b++) if(OUT[a]&ONE(b)) ADJ[b]|=ONE(a);
  for(int a=0;a<N;a++){ int d=bitcount(OUT[a]); int e=0; for(int b=0;b<N;b++) if(OUT[b]&ONE(a)) e++;
    if(d<dmin)dmin=d; if(d>dmax)dmax=d; if(e<imin)imin=e; if(e>imax)imax=e; }
  /* count transitive triangles directly as a separate check */
  long tt3=0; for(int x=0;x<N;x++) for(int y=0;y<N;y++) if(OUT[x]&ONE(y)) tt3+=bitcount(OUT[x]&OUT[y]);
  B all=0; for(int i=0;i<N;i++) all|=ONE(i);
  besttt=0; tt(all,0);
  bestind=0; ind(all,0);
  printf("N=%d arcs=%d oriented=%s outdeg=[%d,%d] indeg=[%d,%d]\n",N,arcs,bad?"NO":"yes",dmin,dmax,imin,imax);
  printf("transitive_triangles=%ld largest_transitive_subtournament=%d independence_number=%d\n",tt3,besttt,bestind);
  int pass=!bad && besttt<=m-1 && bestind<=n-1;
  printf("witness for k(%d,%d) >= %d: %s\n",n,m,N+1,pass?"PASS":"FAIL");
  return pass?0:1;
}
