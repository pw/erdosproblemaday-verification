// Referee: own enumeration of copies of W with INF=0, Z13-orbit histogram, exact 3-cover search.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int orb[1<<13]; static int nidx=0; static int idx5[1<<13];
static int rot(int m){ return ((m<<1)|(m>>12)) & 0x1fff; }
typedef struct { uint64_t h; } H;
static uint64_t *hashes; static long nh=0;
static u128 *kept; static long nk=0;
static uint64_t mix(uint64_t x){x^=x>>33;x*=0xff51afd7ed558ccdULL;x^=x>>33;x*=0xc4ceb9fe1a85ec53ULL;x^=x>>33;return x;}
static int cmpu(const void*a,const void*b){uint64_t x=*(uint64_t*)a,y=*(uint64_t*)b;return x<y?-1:x>y;}
static int cmp128(const void*a,const void*b){u128 x=*(u128*)a,y=*(u128*)b;return x<y?-1:x>y;}
long hist[100];
int main(){
  int norb=0; memset(orb,-1,sizeof orb);
  for(int m=0;m<(1<<13);m++){ if(__builtin_popcount(m)!=5) continue; idx5[m]=nidx++;
    if(orb[m]<0){ int x=m; for(int i=0;i<13;i++){ orb[x]=norb; x=rot(x);} norb++; } }
  printf("5-sets %d, Z13 orbits %d\n", nidx, norb);
  hashes=malloc(sizeof(uint64_t)*10000000); kept=malloc(sizeof(u128)*1000000);
  int pts[12]; for(int i=0;i<12;i++) pts[i]=i+1;
  // a1<a2<a3 from 1..12
  for(int i1=0;i1<12;i1++)for(int i2=i1+1;i2<12;i2++)for(int i3=i2+1;i3<12;i3++){
    int a[3]={pts[i1],pts[i2],pts[i3]}; int rest[9],nr=0;
    for(int t=0;t<12;t++) if(t!=i1&&t!=i2&&t!=i3) rest[nr++]=pts[t];
    for(int j1=0;j1<9;j1++)for(int j2=0;j2<9;j2++)for(int j3=0;j3<9;j3++){
      if(j1==j2||j1==j3||j2==j3) continue;
      int b[3]={rest[j1],rest[j2],rest[j3]}; int r6[6],n6=0;
      for(int t=0;t<9;t++) if(t!=j1&&t!=j2&&t!=j3) r6[n6++]=rest[t];
      // labelled unordered pairs S12,S13,S23 from r6: choose S12 (15), S13 from remaining 4 (6), S23 rest
      for(int p=0;p<6;p++)for(int q=p+1;q<6;q++){
        int r4[4],n4=0; for(int t=0;t<6;t++) if(t!=p&&t!=q) r4[n4++]=r6[t];
        for(int u=0;u<4;u++)for(int v=u+1;v<4;v++){
          int r2[2],n2=0; for(int t=0;t<4;t++) if(t!=u&&t!=v) r2[n2++]=r4[t];
          int S12=(1<<r6[p])|(1<<r6[q]), S13=(1<<r4[u])|(1<<r4[v]), S23=(1<<r2[0])|(1<<r2[1]);
          int B[3]={(1<<a[0])|(1<<b[0])|S12|S13,(1<<a[1])|(1<<b[1])|S12|S23,(1<<a[2])|(1<<b[2])|S13|S23};
          int sets[33],ns=0;
          for(int k=0;k<3;k++) for(int x=0;x<13;x++) if(B[k]>>x&1) sets[ns++]=B[k]&~(1<<x);
          int c6=1|(1<<a[0])|(1<<a[1])|(1<<a[2]), c9=1|(1<<b[0])|(1<<b[1])|(1<<b[2]);
          int sh=S12|S13|S23;
          for(int x=0;x<13;x++) if(sh>>x&1) sets[ns++]=c6|(1<<x);
          for(int x=0;x<13;x++) if(!(c9>>x&1)) sets[ns++]=c9|(1<<x);
          if(ns!=33){printf("bad ns\n");return 1;}
          // independence check (sampled cheaply: every 1000th) and distinctness
          uint64_t h=0; u128 om=0; int distinct=0;
          for(int s=0;s<33;s++){ if(__builtin_popcount(sets[s])!=5){printf("bad size\n");return 1;}
            h+=mix(idx5[sets[s]]+1); u128 bit=((u128)1)<<orb[sets[s]]; if(!(om&bit)){distinct++; om|=bit;} }
          if(nh%997==0){ for(int s=0;s<33;s++)for(int t=s+1;t<33;t++){ int c=__builtin_popcount(sets[s]&sets[t]); if(c==3||c==5){printf("not indep\n");return 1;} } }
          hashes[nh++]=h; hist[distinct]++;
          if(distinct==33) kept[nk++]=om;
        }}
    }}
  qsort(hashes,nh,8,cmpu); long nd=nh>0; for(long i=1;i<nh;i++) if(hashes[i]!=hashes[i-1]) nd++;
  printf("generated %ld copies with INF=0, distinct (by set-hash) %ld\n", nh, nd);
  for(int d=0;d<=33;d++) if(hist[d]) printf("  %d : %ld\n", d, hist[d]);
  printf("kept %ld\n", nk);
  // distinct kept orbit-masks
  qsort(kept,nk,sizeof(u128),cmp128); long nkd=nk>0; for(long i=1;i<nk;i++) if(kept[i]!=kept[i-1]) nkd++;
  printf("distinct orbit-sets among kept: %ld\n", nkd);
  // 3-cover: A contains orbit 0; B contains lowest orbit not in A, disjoint; C = complement must be in kept (binary search)
  u128 FULL=(((u128)1)<<99)-1; long pairs=0, covers=0;
  for(long i=0;i<nk;i++){ u128 A=kept[i]; if(!(A&1)) continue;
    u128 notA=FULL&~A; int low=0; while(!((notA>>low)&1)) low++;
    for(long j=0;j<nk;j++){ u128 B=kept[j]; if(!((B>>low)&1)) continue; if(A&B) continue; pairs++;
      u128 C=FULL&~A&~B; if(bsearch(&C,kept,nk,sizeof(u128),cmp128)) covers++; } }
  printf("disjoint (A with orbit0, B with lowest missing) pairs: %ld ; exact 3-covers: %ld\n", pairs, covers);
  // planted control: check search finds a cover if we add the complement of some disjoint pair
  return 0;
}
