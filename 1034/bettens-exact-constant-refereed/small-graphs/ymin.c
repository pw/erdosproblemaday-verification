/* For graphs (graph6 on stdin) with 4e > n^2: compute M(G) = max over triangles T of |Y+(T)|
   (vertices adjacent to >= 2 vertices of T, T's own vertices included). Print the histogram of M(G),
   the number of graphs, triangle-free count (must be 0 by Mantel), and one graph attaining the minimum. */
#include <stdio.h>
#include <string.h>
int main(void){
  char line[256], best[256]=""; long long cnt=0, hist[32]={0}, tf=0; int minM=99;
  while(fgets(line,sizeof line,stdin)){
    int n=line[0]-63; unsigned adj[32]={0}; int k=0, e=0; const char*p=line+1;
    for(int j=1;j<n;j++) for(int i=0;i<j;i++){ int byte=k/6, bit=5-k%6; if(((p[byte]-63)>>bit)&1){adj[i]|=1u<<j;adj[j]|=1u<<i;e++;} k++; }
    if(4*e<=n*n) continue;
    cnt++; int M=-1;
    for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) if(adj[a]>>b&1) for(int c=b+1;c<n;c++) if((adj[a]>>c&1)&&(adj[b]>>c&1)){
      unsigned y=(adj[a]&adj[b])|(adj[a]&adj[c])|(adj[b]&adj[c]); int s=__builtin_popcount(y); if(s>M)M=s; }
    if(M<0){tf++; continue;}
    hist[M]++; if(M<minM){minM=M; strcpy(best,line);}
  }
  printf("graphs=%lld trianglefree=%lld minM=%d\n",cnt,tf,minM);
  for(int i=0;i<32;i++) if(hist[i]) printf("M=%d: %lld\n",i,hist[i]);
  printf("witness %s",best); return 0;
}
