/* For every copy of W with INF = 0: d39 = number of distinct F39-orbits (F39 = <x+1, 3x> on Z13; 33 orbits of 39 five-sets)
   met by its 33 sets.  Histogram of d39; for d39 >= 31 print the missing orbits and the roles.                      */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int orb39[8192];
static int popc(int x){return __builtin_popcount(x);}
static int rot(int m,int c){ int r=0; for(int i=0;i<13;i++) if(m>>i&1) r|=1<<((i+c)%13); return r; }
static int mul3(int m){ int r=0; for(int i=0;i<13;i++) if(m>>i&1) r|=1<<((3*i)%13); return r; }
static int build(const uint8_t *r, int *sets){
    int inf=r[0], n=0, B[3];
    B[0]=(1<<r[1])|(1<<r[4])|(1<<r[7])|(1<<r[8])|(1<<r[9])|(1<<r[10]);
    B[1]=(1<<r[2])|(1<<r[5])|(1<<r[7])|(1<<r[8])|(1<<r[11])|(1<<r[12]);
    B[2]=(1<<r[3])|(1<<r[6])|(1<<r[9])|(1<<r[10])|(1<<r[11])|(1<<r[12]);
    for(int i=0;i<3;i++) for(int x=0;x<13;x++) if(B[i]>>x&1) sets[n++]=B[i]^(1<<x);
    int c6=(1<<inf)|(1<<r[1])|(1<<r[2])|(1<<r[3]), c9=(1<<inf)|(1<<r[4])|(1<<r[5])|(1<<r[6]);
    for(int j=7;j<13;j++) sets[n++]=c6|(1<<r[j]);
    for(int x=0;x<13;x++) if(!(c9>>x&1)) sets[n++]=c9|(1<<x);
    return n;
}
int main(void){
    int no39=0; memset(orb39,-1,sizeof orb39);
    for(int m=0;m<8192;m++) if(popc(m)==5 && orb39[m]<0){ int x=m; for(int e=0;e<3;e++){ for(int c=0;c<13;c++) orb39[rot(x,c)]=no39; x=mul3(x);} printf("ORBIT %d rep %d\n",no39,m); no39++; }
    long hist[34]; memset(hist,0,sizeof hist); long missing1[33]; memset(missing1,0,sizeof missing1);
    static const int pairings[15][6]={{0,1,2,3,4,5},{0,1,2,4,3,5},{0,1,2,5,3,4},{0,2,1,3,4,5},{0,2,1,4,3,5},{0,2,1,5,3,4},
        {0,3,1,2,4,5},{0,3,1,4,2,5},{0,3,1,5,2,4},{0,4,1,2,3,5},{0,4,1,3,2,5},{0,4,1,5,2,3},{0,5,1,2,3,4},{0,5,1,3,2,4},{0,5,1,4,2,3}};
    static const int perm3[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    uint8_t r[13]; int sets[33]; r[0]=0; long printed[33]; memset(printed,0,sizeof printed);
    for(int a1=1;a1<=12;a1++) for(int a2=a1+1;a2<=12;a2++) for(int a3=a2+1;a3<=12;a3++){
      int rest9[9],n9=0; for(int x=1;x<=12;x++) if(x!=a1&&x!=a2&&x!=a3) rest9[n9++]=x;
      for(int i=0;i<9;i++) for(int j=i+1;j<9;j++) for(int k=j+1;k<9;k++){
        int bb[3]={rest9[i],rest9[j],rest9[k]}; int sh[6],ns=0; for(int t=0;t<9;t++) if(t!=i&&t!=j&&t!=k) sh[ns++]=rest9[t];
        for(int pb=0;pb<6;pb++) for(int pr=0;pr<15;pr++) for(int pa=0;pa<6;pa++){
          r[1]=a1;r[2]=a2;r[3]=a3; r[4]=bb[perm3[pb][0]]; r[5]=bb[perm3[pb][1]]; r[6]=bb[perm3[pb][2]];
          int P[3][2]; for(int q=0;q<3;q++){P[q][0]=sh[pairings[pr][2*q]];P[q][1]=sh[pairings[pr][2*q+1]];}
          for(int q=0;q<3;q++){ r[7+2*q]=P[perm3[pa][q]][0]; r[8+2*q]=P[perm3[pa][q]][1]; }
          build(r,sets);
          uint64_t m39=0; int d=0; for(int s=0;s<33;s++){ uint64_t b=1ULL<<orb39[sets[s]]; if(!(m39&b)){m39|=b;d++;} }
          hist[d]++;
          if(d==32){ int miss=__builtin_ctzll(~m39); missing1[miss]++; if(printed[miss]<3){ printed[miss]++; printf("D32 missing %d roles",miss); for(int t=0;t<13;t++) printf(" %d",r[t]); printf("\n"); } }
        }
      }
    }
    for(int d=0;d<=33;d++) if(hist[d]) printf("HIST %d %ld\n",d,hist[d]);
    for(int o=0;o<33;o++) printf("MISSING1 orbit %d count %ld\n",o,missing1[o]);
    return 0;
}
