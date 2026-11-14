/* TabuCol on J(13,5,3) (1287 vertices, 5-sets adjacent iff they meet in exactly 3). Usage: tabucol k seed maxiters(1e6) out */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define NV 1287
static int nb[NV][280], deg[NV], col[NV], *gam, *tabu, K;
static uint64_t s[2];
static inline uint64_t rnd(void){ uint64_t a=s[0],b=s[1]; s[0]=b; a^=a<<23; s[1]=a^b^(a>>17)^(b>>26); return s[1]+b; }
int main(int argc,char**argv){
    K=atoi(argv[1]); uint64_t seed=strtoull(argv[2],0,10); double maxit=atof(argv[3])*1e6; const char*out=argv[4];
    s[0]=seed*0x9E3779B97F4A7C15ULL+7; s[1]=seed^0xD1B54A32D192ED03ULL; for(int i=0;i<20;i++) rnd();
    int masks[NV],n=0; for(int m=0;m<8192;m++) if(__builtin_popcount(m)==5) masks[n++]=m;
    for(int i=0;i<NV;i++) for(int j=0;j<NV;j++) if(i!=j && __builtin_popcount(masks[i]&masks[j])==3) nb[i][deg[i]++]=j;
    gam=calloc(NV*K,sizeof(int)); tabu=calloc(NV*K,sizeof(int));
    for(int v=0;v<NV;v++) col[v]=rnd()%K;
    for(int v=0;v<NV;v++) for(int e=0;e<deg[v];e++) gam[v*K+col[nb[v][e]]]++;
    long conf=0; for(int v=0;v<NV;v++) conf+=gam[v*K+col[v]]; conf/=2;
    long best=conf;
    for(double it=1; it<=maxit && conf>0; it+=1){
        int bv=-1,bc=-1,bd=1<<30,cnt=0; long iti=(long)it;
        for(int v=0;v<NV;v++){ int g0=gam[v*K+col[v]]; if(!g0) continue;
            for(int c=0;c<K;c++){ if(c==col[v]) continue; int d=gam[v*K+c]-g0;
                if(tabu[v*K+c]>iti && !(conf+d<best)) continue;
                if(d<bd){bd=d;bv=v;bc=c;cnt=1;} else if(d==bd){ cnt++; if(rnd()%cnt==0){bv=v;bc=c;} } } }
        if(bv<0) continue;
        int old=col[bv]; col[bv]=bc; conf+=bd;
        for(int e=0;e<deg[bv];e++){ int u=nb[bv][e]; gam[u*K+old]--; gam[u*K+bc]++; }
        tabu[bv*K+old]=iti+(int)(0.6*conf)+rnd()%10;
        if(conf<best){ best=conf; }
    }
    printf("k=%d seed=%llu best_conflicts=%ld final=%ld\n",K,(unsigned long long)seed,best,conf);
    if(conf==0){ FILE*f=fopen(out,"w"); for(int v=0;v<NV;v++) fprintf(f,"%d %d\n",masks[v],col[v]); fclose(f); printf("PROPER %d-colouring written to %s\n",K,out); }
    return 0;
}
