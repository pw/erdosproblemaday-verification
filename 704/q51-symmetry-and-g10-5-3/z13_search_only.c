/* The exact-3-cover step of z13.c, run on a record file (for the planted control). Same loop, copied verbatim. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
typedef struct { u128 mask; uint8_t role[13]; } kept_t;
static int cmpk(const void*a,const void*b){ u128 x=((const kept_t*)a)->mask,y=((const kept_t*)b)->mask; return x<y?-1:x>y; }
int main(int argc,char**argv){
    FILE*f=fopen(argv[1],"rb"); fseek(f,0,SEEK_END); long nK=ftell(f)/sizeof(kept_t); rewind(f);
    kept_t*K=malloc(nK*sizeof(kept_t)); if(fread(K,sizeof(kept_t),nK,f)!=(size_t)nK) return 1; fclose(f);
    qsort(K,nK,sizeof(kept_t),cmpk);
    u128 full=(((u128)1)<<99)-1; long pairs=0, sols=0;
    for(long i=0;i<nK;i++){
        if(!(K[i].mask&1)) continue;
        for(long j=0;j<nK;j++){
            if(K[i].mask&K[j].mask) continue;
            u128 rest=full^K[i].mask^K[j].mask;
            if(K[j].mask>rest) continue;
            pairs++;
            long lo=0,hi=nK; while(lo<hi){ long mid=(lo+hi)/2; if(K[mid].mask<rest) lo=mid+1; else hi=mid; }
            for(long k=lo;k<nK&&K[k].mask==rest;k++){ sols++; printf("SOLUTION roles[0] of the three: %d %d %d\n",K[i].role[0],K[j].role[0],K[k].role[0]); }
        }
    }
    printf("records %ld, pairs examined %ld, exact 3-covers %ld\n",nK,pairs,sols); return 0;
}
