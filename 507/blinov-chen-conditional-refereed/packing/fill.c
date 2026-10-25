#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* Read a base AP-free set (one int per line) and a cap M. Keep base elements <= M, verify AP-free,
   then greedily add x = 0..M (increasing, or in a given order) whenever x creates no 3-AP. Print size and the K-th element. */
static unsigned char *forb, *in;
static int *S; static int ns;
static void add(int x,int M){ for(int i=0;i<ns;i++){int y=S[i]; long z=2L*x-y; if(z>=0&&z<=M) forb[z]=1; z=2L*y-x; if(z>=0&&z<=M) forb[z]=1; if(((x+y)&1)==0) forb[(x+y)/2]=1;} S[ns++]=x; in[x]=1; }
int main(int argc,char**argv){
  int M=atoi(argv[2]); int K=atoi(argv[3]); unsigned seed=argc>4?atoi(argv[4]):0;
  forb=calloc(M+1,1); in=calloc(M+1,1); S=malloc(sizeof(int)*(M+2)); ns=0;
  FILE*f=fopen(argv[1],"r"); int x; int nb=0;
  while(fscanf(f,"%d",&x)==1){ if(x<=M){ if(forb[x]||in[x]){fprintf(stderr,"BASE NOT AP-FREE at %d\n",x); return 2;} add(x,M); nb++; } }
  fclose(f);
  int *ord=malloc(sizeof(int)*(M+1)); for(int i=0;i<=M;i++) ord[i]=i;
  if(seed){ srand(seed); for(int i=M;i>0;i--){int j=rand()%(i+1); int t=ord[i]; ord[i]=ord[j]; ord[j]=t;} }
  int added=0; for(int i=0;i<=M;i++){int y=ord[i]; if(!in[y]&&!forb[y]){add(y,M); added++;}}
  /* sort and report */
  int cnt=0, kth=-1; for(int y=0;y<=M;y++) if(in[y]){ if(cnt==K-1) kth=y; cnt++; }
  printf("base=%d added=%d total=%d Kth=%d\n",nb,added,cnt,kth);
  if(argc>5){FILE*o=fopen(argv[5],"w"); for(int y=0;y<=M;y++) if(in[y]) fprintf(o,"%d\n",y); fclose(o);}
  return 0;
}
