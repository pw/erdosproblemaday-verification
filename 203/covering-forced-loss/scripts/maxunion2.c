// maxunion2.c — like maxunion.c but (a) each prime has an explicit ALLOWED coset list (file: one line per prime,
// space-separated cosets), (b) an optional FIXED set given as a raw bitset file (W uint64 words, T*T bits, row-major
// x = k*T + l) OR'd into every union.  All combinations of allowed cosets are enumerated (no translation trick).
// Usage: maxunion2 block.txt allowed.txt fixed.bin|-
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static long gcdl(long a,long b){while(b){long t=a%b;a=b;b=t;}return a;}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); long e[32],u[32],v[32]; int n=0;
  while(fscanf(f,"%ld %ld %ld",&e[n],&u[n],&v[n])==3) n++; fclose(f);
  long T=1; for(int i=0;i<n;i++) T=T/gcdl(T,e[i])*e[i]; long W=(T*T+63)/64;
  // allowed lists
  long *allow[32]; int na[32]; f=fopen(argv[2],"r"); char line[65536];
  for(int i=0;i<n;i++){ if(!fgets(line,sizeof line,f)){printf("allowed file short\n");return 2;} allow[i]=malloc(sizeof(long)*e[i]); na[i]=0;
    char*s=line; long c; int k; while(sscanf(s,"%ld%n",&c,&k)==1){ if(c<0||c>=e[i]){printf("bad coset\n");return 2;} allow[i][na[i]++]=c; s+=k; } if(na[i]==0){printf("prime %d has NO allowed coset -> it covers nothing\n",i);} }
  fclose(f);
  long tot=0; for(int i=0;i<n;i++) tot+=e[i]; long off[33]; off[0]=0; for(int i=0;i<n;i++) off[i+1]=off[i]+e[i];
  uint64_t *bs=calloc((size_t)tot*W,8);
  for(long k=0;k<T;k++) for(long l=0;l<T;l++){ long x=k*T+l; for(int i=0;i<n;i++){ long c=((u[i]*k+v[i]*l)%e[i]+e[i])%e[i]; bs[(off[i]+c)*W+x/64]|=(1ULL<<(x%64)); } }
  for(int i=0;i<n;i++) for(long c=0;c<e[i];c++){ long cnt=0; for(long w=0;w<W;w++) cnt+=__builtin_popcountll(bs[(off[i]+c)*W+w]); if(cnt!=T*T/e[i]){printf("CONTROL FAIL\n");return 2;} }
  uint64_t *fixed=calloc(W,8); long fixedcnt=0;
  if(strcmp(argv[3],"-")){ f=fopen(argv[3],"rb"); if(fread(fixed,8,W,f)!=(size_t)W){printf("fixed file size mismatch (want %ld words)\n",W);return 2;} fclose(f); for(long w=0;w<W;w++) fixedcnt+=__builtin_popcountll(fixed[w]); }
  int idx[32]; for(int i=0;i<n;i++) idx[i]=0; double configs=1; for(int i=0;i<n;i++) configs*= (na[i]?na[i]:1);
  long best=-1,nbest=0; long bestc[32]; uint64_t*acc=malloc(W*8);
  while(1){
    memcpy(acc,fixed,W*8);
    for(int i=0;i<n;i++){ if(!na[i]) continue; const uint64_t*b=bs+(off[i]+allow[i][idx[i]])*W; for(long w=0;w<W;w++) acc[w]|=b[w]; }
    long cnt=0; for(long w=0;w<W;w++) cnt+=__builtin_popcountll(acc[w]);
    if(cnt>best){best=cnt;nbest=1;for(int i=0;i<n;i++) bestc[i]= na[i]?allow[i][idx[i]]:-1;} else if(cnt==best) nbest++;
    int i=0; while(i<n){ if(!na[i]){i++;continue;} idx[i]++; if(idx[i]<na[i]) break; idx[i]=0; i++; } if(i>=n) break;
  }
  double sum=0; for(int i=0;i<n;i++) if(na[i]) sum+=1.0/e[i];
  printf("n=%d T=%ld points=%ld configs=%.0f fixed=%ld (%.6f) sum1/e(active)=%.6f\n",n,T,T*T,configs,fixedcnt,(double)fixedcnt/(T*T),sum);
  printf("MAX covered=%ld density=%.6f (#optimal %ld)\nwitness:",best,(double)best/(T*T),nbest); for(int i=0;i<n;i++) printf(" %ld",bestc[i]); printf("\n");
  return 0;
}
