/* S3: all colourings of J(13,5,3) with 39 maximum independent sets that are invariant under x -> x+1 (mod 13).
   Such a colouring = three Z13-orbits of classes; each orbit has exactly one class whose INF point is 0.
   So: enumerate the 9,979,200 copies of W with INF = 0, keep those whose 33 sets lie in 33 distinct Z13-orbits
   (of the 99 orbits of 5-sets), then find all triples of kept copies whose orbit-masks partition the 99 orbits.
   Output: counts; kept copies to z13_kept.bin; solutions to stdout.  Also (F39): kept copies that are transversals
   of the 33 orbits of F39 = <x+1, 3x>.                                                                          */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static int orb13[8192], orb39[8192];
static int popc(int x){return __builtin_popcount(x);}
static int rot(int m,int c){ int r=0; for(int i=0;i<13;i++) if(m>>i&1) r|=1<<((i+c)%13); return r; }
static int mul3(int m){ int r=0; for(int i=0;i<13;i++) if(m>>i&1) r|=1<<((3*i)%13); return r; }
typedef struct { u128 mask; uint8_t role[13]; } kept_t;   /* role[]: inf,a1,a2,a3,b1,b2,b3,s12,s12',s13,s13',s23,s23' */
static kept_t *K; static long nK=0, capK=0;
static int build(const uint8_t *r, int *sets){
    int inf=r[0], n=0;
    int B[3];
    B[0]=(1<<r[1])|(1<<r[4])|(1<<r[7])|(1<<r[8])|(1<<r[9])|(1<<r[10]);
    B[1]=(1<<r[2])|(1<<r[5])|(1<<r[7])|(1<<r[8])|(1<<r[11])|(1<<r[12]);
    B[2]=(1<<r[3])|(1<<r[6])|(1<<r[9])|(1<<r[10])|(1<<r[11])|(1<<r[12]);
    for(int i=0;i<3;i++) for(int x=0;x<13;x++) if(B[i]>>x&1) sets[n++]=B[i]^(1<<x);
    int c6=(1<<inf)|(1<<r[1])|(1<<r[2])|(1<<r[3]);
    int c9=(1<<inf)|(1<<r[4])|(1<<r[5])|(1<<r[6]);
    for(int j=7;j<13;j++) sets[n++]=c6|(1<<r[j]);
    for(int x=0;x<13;x++) if(!(c9>>x&1)) sets[n++]=c9|(1<<x);
    return n;
}
static int cmpk(const void*a,const void*b){ u128 x=((const kept_t*)a)->mask,y=((const kept_t*)b)->mask; return x<y?-1:x>y; }
int main(int argc,char**argv){
    /* orbit tables */
    int no=0; memset(orb13,-1,sizeof orb13);
    for(int m=0;m<8192;m++) if(popc(m)==5 && orb13[m]<0){ for(int c=0;c<13;c++) orb13[rot(m,c)]=no; no++; }
    int no39=0; memset(orb39,-1,sizeof orb39);
    for(int m=0;m<8192;m++) if(popc(m)==5 && orb39[m]<0){ int x=m; for(int e=0;e<3;e++){ for(int c=0;c<13;c++) orb39[rot(x,c)]=no39; x=mul3(x);} no39++; }
    fprintf(stderr,"Z13 orbits %d, F39 orbits %d\n",no,no39);
    long total=0, f39=0; long hist[34]; memset(hist,0,sizeof hist);
    static const int pairings[15][6]={{0,1,2,3,4,5},{0,1,2,4,3,5},{0,1,2,5,3,4},{0,2,1,3,4,5},{0,2,1,4,3,5},{0,2,1,5,3,4},
        {0,3,1,2,4,5},{0,3,1,4,2,5},{0,3,1,5,2,4},{0,4,1,2,3,5},{0,4,1,3,2,5},{0,4,1,5,2,3},{0,5,1,2,3,4},{0,5,1,3,2,4},{0,5,1,4,2,3}};
    static const int perm3[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    uint8_t r[13]; int sets[33];
    r[0]=0;
    for(int a1=1;a1<=12;a1++) for(int a2=a1+1;a2<=12;a2++) for(int a3=a2+1;a3<=12;a3++){
      int rest9[9],n9=0; for(int x=1;x<=12;x++) if(x!=a1&&x!=a2&&x!=a3) rest9[n9++]=x;
      for(int i=0;i<9;i++) for(int j=i+1;j<9;j++) for(int k=j+1;k<9;k++){
        int bb[3]={rest9[i],rest9[j],rest9[k]}; int sh[6],ns=0; for(int t=0;t<9;t++) if(t!=i&&t!=j&&t!=k) sh[ns++]=rest9[t];
        for(int pb=0;pb<6;pb++) for(int pr=0;pr<15;pr++) for(int pa=0;pa<6;pa++){
          r[1]=a1;r[2]=a2;r[3]=a3; r[4]=bb[perm3[pb][0]]; r[5]=bb[perm3[pb][1]]; r[6]=bb[perm3[pb][2]];
          int P[3][2]; for(int q=0;q<3;q++){P[q][0]=sh[pairings[pr][2*q]];P[q][1]=sh[pairings[pr][2*q+1]];}
          for(int q=0;q<3;q++){ r[7+2*q]=P[perm3[pa][q]][0]; r[8+2*q]=P[perm3[pa][q]][1]; }
          int n=build(r,sets); if(n!=33){fprintf(stderr,"bad n\n");return 1;}
          total++;
          u128 mask=0; int distinct=0; for(int s=0;s<33;s++){ u128 b=(u128)1<<orb13[sets[s]]; if(!(mask&b)){mask|=b;distinct++;} }
          hist[distinct]++;
          if(distinct==33){
            if(nK==capK){capK=capK?2*capK:1<<16; K=realloc(K,capK*sizeof(kept_t));}
            K[nK].mask=mask; memcpy(K[nK].role,r,13); nK++;
            uint64_t m39=0; int d39=0; for(int s=0;s<33;s++){ uint64_t b=1ULL<<orb39[sets[s]]; if(!(m39&b)){m39|=b;d39++;} }
            if(d39==33){ f39++; printf("F39_TRANSVERSAL roles"); for(int t=0;t<13;t++) printf(" %d",r[t]); printf("\n"); }
          }
        }
      }
    }
    fprintf(stderr,"copies with INF=0: %ld (expect 9979200)\n",total);
    fprintf(stderr,"distinct-orbit histogram (#Z13-orbits met by the 33 sets : #copies):\n");
    for(int d=0;d<=33;d++) if(hist[d]) fprintf(stderr,"  %d : %ld\n",d,hist[d]);
    fprintf(stderr,"kept (33 distinct Z13-orbits): %ld ; of these F39-transversals: %ld\n",nK,f39);
    FILE*f=fopen("z13_kept.bin","wb"); fwrite(K,sizeof(kept_t),nK,f); fclose(f);
    /* exact 3-cover of the 99 orbits */
    qsort(K,nK,sizeof(kept_t),cmpk);
    u128 full=(((u128)1)<<99)-1; long pairs=0, sols=0;
    for(long i=0;i<nK;i++){
        if(!(K[i].mask&1)) continue;                  /* W1 contains orbit 0 */
        for(long j=0;j<nK;j++){
            if(K[i].mask&K[j].mask) continue;
            u128 rest=full^K[i].mask^K[j].mask;
            if(K[j].mask>rest) continue;              /* order W2 < W3 by mask */
            pairs++;
            long lo=0,hi=nK; while(lo<hi){ long mid=(lo+hi)/2; if(K[mid].mask<rest) lo=mid+1; else hi=mid; }
            for(long k=lo;k<nK&&K[k].mask==rest;k++){
                sols++;
                printf("SOLUTION");
                for(int t=0;t<13;t++) printf(" %d",K[i].role[t]); printf(" |");
                for(int t=0;t<13;t++) printf(" %d",K[j].role[t]); printf(" |");
                for(int t=0;t<13;t++) printf(" %d",K[k].role[t]); printf("\n");
            }
        }
    }
    fprintf(stderr,"disjoint pairs examined: %ld ; exact 3-covers (role-labelled triples W1,W2,W3): %ld\n",pairs,sols);
    return 0;
}
