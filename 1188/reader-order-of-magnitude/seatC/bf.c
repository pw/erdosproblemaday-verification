/* Route C (seat C): plain brute force. For the given moduli (lcm L <= 256), enumerate EVERY
   assignment (each modulus: unused, or one of its n residues) with an odometer, form the union
   from scratch, and if it covers Z/L test minimality by private points (each class has a point
   covered by no other class). No pruning, no normalisation.  usage: bf m1 m2 ... */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
#define MAXW 4
static int K; static int Mod[32]; static int L; static int W;
static u64 cl[32][256][MAXW];
static int gcdi(int a,int b){while(b){int t=a%b;a=b;b=t;}return a;}
int main(int argc,char**argv){
  K=argc-1; L=1; for(int i=0;i<K;i++){Mod[i]=atoi(argv[1+i]); L=L/gcdi(L,Mod[i])*Mod[i];}
  if(L>256){fprintf(stderr,"L too big\n");return 1;}
  W=(L+63)/64;
  u64 full[MAXW]={0}; for(int z=0;z<L;z++) full[z>>6]|=1ULL<<(z&63);
  for(int i=0;i<K;i++) for(int a=0;a<Mod[i];a++){ memset(cl[i][a],0,sizeof(cl[i][a])); for(int z=a;z<L;z+=Mod[i]) cl[i][a][z>>6]|=1ULL<<(z&63); }
  int st[32]; for(int i=0;i<K;i++) st[i]=-1; /* -1 = unused */
  long long assignments=0, coverings=0, minimal=0; long long bycount[33]={0};
  /* per moduli-set histogram */
  static long long byset[1<<20]; if(K>20){fprintf(stderr,"K too big\n");return 1;}
  memset(byset,0,sizeof(byset));
  FILE *dumpf = getenv("BF_DUMP") ? fopen(getenv("BF_DUMP"),"w") : NULL;
  while(1){
    assignments++;
    u64 u[MAXW]={0}; int cnt=0;
    for(int i=0;i<K;i++) if(st[i]>=0){ cnt++; for(int w=0;w<W;w++) u[w]|=cl[i][st[i]][w]; }
    int cov = cnt>0; for(int w=0;w<W;w++) if(u[w]!=full[w]) cov=0;
    if(cov){
      coverings++;
      int ok=1;
      for(int i=0;i<K && ok;i++) if(st[i]>=0){
        u64 o[MAXW]={0};
        for(int j=0;j<K;j++) if(j!=i && st[j]>=0) for(int w=0;w<W;w++) o[w]|=cl[j][st[j]][w];
        u64 any=0; for(int w=0;w<W;w++) any |= cl[i][st[i]][w] & ~o[w];
        if(!any) ok=0;
      }
      if(ok){ minimal++; bycount[cnt]++; int key=0; for(int i=0;i<K;i++) if(st[i]>=0) key|=1<<i; byset[key]++;
        if(dumpf){ fprintf(dumpf,"SYS"); for(int i=0;i<K;i++) if(st[i]>=0) fprintf(dumpf," %d/%d",st[i],Mod[i]); fprintf(dumpf,"\n"); } }
    }
    /* odometer */
    int i=K-1; while(i>=0){ st[i]++; if(st[i]<Mod[i]) break; st[i]=-1; i--; }
    if(i<0) break;
  }
  printf("MODULI"); for(int i=0;i<K;i++) printf(" %d",Mod[i]); printf("\nL %d assignments %lld coverings %lld\nTOTAL %lld\n",L,assignments,coverings,minimal);
  for(int k=0;k<=K;k++) if(bycount[k]) printf("CLASSES %d count %lld\n",k,bycount[k]);
  for(int key=0;key<(1<<K);key++) if(byset[key]){ printf("SET"); for(int i=0;i<K;i++) if(key>>i&1) printf(" %d",Mod[i]); printf(" : %lld\n",byset[key]); }
  if(dumpf) fclose(dumpf);
  return 0;
}
