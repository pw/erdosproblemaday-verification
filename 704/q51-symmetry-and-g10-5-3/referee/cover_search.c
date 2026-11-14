// exact 3-cover search over kept orbit-masks, with per-orbit index; argv[1]=1 plants a cover (control)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int cmp128(const void*a,const void*b){u128 x=*(u128*)a,y=*(u128*)b;return x<y?-1:x>y;}
int main(int argc,char**argv){ int plant=argc>1&&atoi(argv[1]);
  FILE*f=fopen("kept_ref.bin","rb"); u128*K=malloc(sizeof(u128)*200000); long n=fread(K,sizeof(u128),200000,f); fclose(f);
  u128 FULL=(((u128)1)<<99)-1;
  if(plant){ // find a disjoint pair A(orbit0),B and add complement as a fake member
    for(long i=0;i<n&&plant==1;i++){ if(!(K[i]&1)) continue; for(long j=0;j<n;j++) if(!(K[i]&K[j])){ K[n++]=FULL&~K[i]&~K[j]; plant=2; break; } } }
  qsort(K,n,sizeof(u128),cmp128);
  long *cnt=calloc(99,sizeof(long)); long **lst=malloc(99*sizeof(long*));
  for(int o=0;o<99;o++){ lst[o]=malloc(sizeof(long)*n); }
  for(long i=0;i<n;i++) for(int o=0;o<99;o++) if((K[i]>>o)&1) lst[o][cnt[o]++]=i;
  long pairs=0,covers=0;
  for(long ii=0;ii<cnt[0];ii++){ u128 A=K[lst[0][ii]]; u128 nA=FULL&~A; int low=0; while(!((nA>>low)&1)) low++;
    for(long jj=0;jj<cnt[low];jj++){ u128 B=K[lst[low][jj]]; if(A&B) continue; pairs++; u128 C=FULL&~A&~B;
      if(bsearch(&C,K,n,sizeof(u128),cmp128)) covers++; } }
  printf("n=%ld plant=%d pairs=%ld covers=%ld\n",n,plant,pairs,covers); return 0; }
