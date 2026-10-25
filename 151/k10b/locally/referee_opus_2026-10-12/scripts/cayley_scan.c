/* For every group table in tables.txt: enumerate inverse-closed 8-subsets S of G\{e} whose link graph
   (s~t iff s^-1 t in S) is cubic, triangle-free, with independence number 3 (== Wagner graph).
   stdout: "n gid nfound desc"; file argv[2]: "S n gid s1..s8". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, T[64][64], inv[64], ncls, cls[64][2], clsz[64];
static int S[16], ns; static unsigned long long inS;
static long found; static FILE *out; static int gid;
static int adj(int s,int t){ return (inS>>T[inv[s]][t])&1ULL; }
static int ok_partial(void){
  int deg[16]; memset(deg,0,sizeof deg);
  for(int i=0;i<ns;i++) for(int j=i+1;j<ns;j++) if(adj(S[i],S[j])){deg[i]++;deg[j]++; if(deg[i]>3||deg[j]>3) return 0;}
  for(int i=0;i<ns;i++) for(int j=i+1;j<ns;j++) if(adj(S[i],S[j])) for(int k=j+1;k<ns;k++) if(adj(S[i],S[k])&&adj(S[j],S[k])) return 0;
  return 1;
}
static int full_check(void){
  int deg[8]={0};
  for(int i=0;i<8;i++) for(int j=0;j<8;j++) if(i!=j && adj(S[i],S[j])) deg[i]++;
  for(int i=0;i<8;i++) if(deg[i]!=3) return 0;
  for(int a=0;a<8;a++)for(int b=a+1;b<8;b++)for(int c=b+1;c<8;c++)for(int d=c+1;d<8;d++){
    int I[4]={a,b,c,d}, ind=1;
    for(int x=0;x<4&&ind;x++)for(int y=x+1;y<4;y++) if(adj(S[I[x]],S[I[y]])){ind=0;break;}
    if(ind) return 0;
  }
  return 1;
}
static void dfs(int i){
  if(ns==8){ if(full_check()){ found++; fprintf(out,"S %d %d",n,gid); for(int k=0;k<8;k++) fprintf(out," %d",S[k]); fprintf(out,"\n"); } return; }
  if(i==ncls) return;
  if(ns+clsz[i]<=8){
    for(int k=0;k<clsz[i];k++){ S[ns++]=cls[i][k]; inS|=1ULL<<cls[i][k]; }
    if(ok_partial()) dfs(i+1);
    for(int k=0;k<clsz[i];k++){ ns--; inS&=~(1ULL<<cls[i][k]); }
  }
  dfs(i+1);
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); out=fopen(argv[2],"w"); static char line[200000];
  while(fgets(line,sizeof line,f)){
    if(line[0]=='\n') continue;
    char desc[1000]; desc[0]=0;
    sscanf(line,"%d %d %[^\n]",&n,&gid,desc);
    for(int r=0;r<n;r++){ for(int c=0;c<n;c++) if(fscanf(f,"%d",&T[r][c])!=1){fprintf(stderr,"parse\n");return 1;} }
    if(!fgets(line,sizeof line,f)) {}
    for(int a=0;a<n;a++) for(int b=0;b<n;b++) if(T[a][b]==0){inv[a]=b;break;}
    int seen[64]={0}; ncls=0;
    for(int g=1;g<n;g++){ if(seen[g]) continue; seen[g]=1; cls[ncls][0]=g; clsz[ncls]=1; if(inv[g]!=g){seen[inv[g]]=1; cls[ncls][1]=inv[g]; clsz[ncls]=2;} ncls++; }
    found=0; ns=0; inS=0; dfs(0);
    printf("%d %d %ld %s\n",n,gid,found,desc); fflush(stdout);
  }
  return 0;
}
