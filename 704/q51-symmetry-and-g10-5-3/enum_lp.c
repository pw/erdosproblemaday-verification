/* Enumerate all 129,729,600 copies of W; keep those disjoint from W itself (class 1); emit the distinct
   Aut(W)-orbit feature vectors: [5-set orbit counts | 4-set cut features | 6-set cut features | INF point orbit].
   Features (per copy C'):
     f5[o]  = #sets of C' in orbit o of 5-sets outside W
     g4[o]  = sum over 4-sets U in orbit o of ( [U inside a block of C'] + 4[U = 9-core of C'] + 3[U = 6-core of C'] )
     h6[o]  = sum over 6-sets H in orbit o of ( 3[H block of C'] + #sunflower pairs of C' with union H )
     pt[o]  = [INF of C' in point-orbit o]
   Usage: enum_lp out.bin  (also prints the feature vector of W itself with role args via -w)                    */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int o5[8192], o4[8192], o6[8192], opt[13]; static int n5,n4,n6,npt, D;
static int build(const uint8_t *r, int *sets, int *B, int *c6, int *c9){
    int inf=r[0], n=0;
    B[0]=(1<<r[1])|(1<<r[4])|(1<<r[7])|(1<<r[8])|(1<<r[9])|(1<<r[10]);
    B[1]=(1<<r[2])|(1<<r[5])|(1<<r[7])|(1<<r[8])|(1<<r[11])|(1<<r[12]);
    B[2]=(1<<r[3])|(1<<r[6])|(1<<r[9])|(1<<r[10])|(1<<r[11])|(1<<r[12]);
    for(int i=0;i<3;i++) for(int x=0;x<13;x++) if(B[i]>>x&1) sets[n++]=B[i]^(1<<x);
    *c6=(1<<inf)|(1<<r[1])|(1<<r[2])|(1<<r[3]);
    *c9=(1<<inf)|(1<<r[4])|(1<<r[5])|(1<<r[6]);
    for(int j=7;j<13;j++) sets[n++]=*c6|(1<<r[j]);
    for(int x=0;x<13;x++) if(!(*c9>>x&1)) sets[n++]=*c9|(1<<x);
    return n;
}
static void features(const uint8_t *r, const int *sets, const int *B, int c6, int c9, uint8_t *f, int inW_ok){
    memset(f,0,D);
    for(int s=0;s<33;s++){ int o=o5[sets[s]]; if(o>=0) f[o]++; else if(!inW_ok){fprintf(stderr,"feature on W set\n");exit(1);} }
    uint8_t *g=f+n5, *h=f+n5+n4, *p=f+n5+n4+n6;
    for(int i=0;i<3;i++){
        h[o6[B[i]]]+=3;
        for(int x=0;x<13;x++) if(B[i]>>x&1) for(int y=x+1;y<13;y++) if(B[i]>>y&1) g[o4[B[i]^(1<<x)^(1<<y)]]++;
    }
    g[o4[c9]]+=4; g[o4[c6]]+=3;
    for(int j=7;j<13;j++) for(int k=j+1;k<13;k++) h[o6[c6|(1<<r[j])|(1<<r[k])]]++;
    for(int x=0;x<13;x++) if(!(c9>>x&1)) for(int y=x+1;y<13;y++) if(!(c9>>y&1)) h[o6[c9|(1<<x)|(1<<y)]]++;
    p[opt[r[0]]]=1;
}
static uint64_t hashv(const uint8_t*f){ uint64_t h=1469598103934665603ULL; for(int i=0;i<D;i++){h^=f[i];h*=1099511628211ULL;} return h; }
int main(int argc,char**argv){
    FILE*t=fopen("tables.txt","r"); if(fscanf(t,"%d %d %d %d",&n5,&n4,&n6,&npt)!=4) return 1;
    int k,m,o; memset(o5,-1,sizeof o5);
    while(fscanf(t,"%d %d %d",&k,&m,&o)==3){ if(k==5)o5[m]=o; else if(k==4)o4[m]=o; else if(k==6)o6[m]=o; else opt[m]=o; }
    fclose(t); D=n5+n4+n6+npt;
    uint8_t r[13]; int sets[33],B[3],c6,c9; uint8_t f[512];
    if(argc>2 && !strcmp(argv[1],"-w")){            /* feature vector of a given copy (roles on the command line) */
        for(int i=0;i<13;i++) r[i]=atoi(argv[2+i]);
        build(r,sets,B,&c6,&c9); features(r,sets,B,c6,c9,f,1);
        for(int i=0;i<D;i++) printf("%d ",f[i]); printf("\n"); return 0;
    }
    long cap=1L<<22, used=0; long *slot=malloc(cap*sizeof(long)); memset(slot,-1,cap*sizeof(long));
    long vcap=1L<<21; uint8_t *vec=malloc(vcap*(long)D); uint32_t *mult=malloc(vcap*sizeof(uint32_t));
    long total=0, kept=0;
    static const int pairings[15][6]={{0,1,2,3,4,5},{0,1,2,4,3,5},{0,1,2,5,3,4},{0,2,1,3,4,5},{0,2,1,4,3,5},{0,2,1,5,3,4},
        {0,3,1,2,4,5},{0,3,1,4,2,5},{0,3,1,5,2,4},{0,4,1,2,3,5},{0,4,1,3,2,5},{0,4,1,5,2,3},{0,5,1,2,3,4},{0,5,1,3,2,4},{0,5,1,4,2,3}};
    static const int perm3[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    for(int inf=0;inf<13;inf++){
      int pts[12],np=0; for(int x=0;x<13;x++) if(x!=inf) pts[np++]=x;
      for(int i1=0;i1<12;i1++) for(int i2=i1+1;i2<12;i2++) for(int i3=i2+1;i3<12;i3++){
        int rest9[9],n9=0; for(int x=0;x<12;x++) if(x!=i1&&x!=i2&&x!=i3) rest9[n9++]=pts[x];
        for(int i=0;i<9;i++) for(int j=i+1;j<9;j++) for(int kk=j+1;kk<9;kk++){
          int bb[3]={rest9[i],rest9[j],rest9[kk]}; int sh[6],ns=0; for(int q=0;q<9;q++) if(q!=i&&q!=j&&q!=kk) sh[ns++]=rest9[q];
          for(int pb=0;pb<6;pb++) for(int pr=0;pr<15;pr++) for(int pa=0;pa<6;pa++){
            r[0]=inf; r[1]=pts[i1];r[2]=pts[i2];r[3]=pts[i3]; r[4]=bb[perm3[pb][0]]; r[5]=bb[perm3[pb][1]]; r[6]=bb[perm3[pb][2]];
            int P[3][2]; for(int q=0;q<3;q++){P[q][0]=sh[pairings[pr][2*q]];P[q][1]=sh[pairings[pr][2*q+1]];}
            for(int q=0;q<3;q++){ r[7+2*q]=P[perm3[pa][q]][0]; r[8+2*q]=P[perm3[pa][q]][1]; }
            build(r,sets,B,&c6,&c9); total++;
            int ok=1; for(int s=0;s<33;s++) if(o5[sets[s]]<0){ok=0;break;}
            if(!ok) continue;
            kept++; features(r,sets,B,c6,c9,f,0);
            uint64_t hh=hashv(f); long pos=hh&(cap-1);
            for(;;){ long v=slot[pos]; if(v<0){ if(used==vcap){fprintf(stderr,"vec overflow\n");return 1;}
                        memcpy(vec+used*(long)D,f,D); mult[used]=1; slot[pos]=used++; break; }
                     if(!memcmp(vec+v*(long)D,f,D)){ mult[v]++; break; }
                     pos=(pos+1)&(cap-1); }
          }
        }
      }
      fprintf(stderr,"inf=%d total=%ld kept=%ld distinct=%ld\n",inf,total,kept,used);
    }
    fprintf(stderr,"copies %ld (expect 129729600); disjoint from W: %ld; distinct feature vectors: %ld; D=%d\n",total,kept,used,D);
    FILE*out=fopen(argv[1],"wb"); fwrite(&used,sizeof(long),1,out); fwrite(&D,sizeof(int),1,out);
    fwrite(vec,D,used,out); fwrite(mult,sizeof(uint32_t),used,out); fclose(out);
    return 0;
}
