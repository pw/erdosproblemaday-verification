// Referee: enumerate all copies of W, count those disjoint from W, find a representative copy for each of the 101 LP columns.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define D 309
static int o5[8192],o4[8192],o6[8192],opt[13]; static int inW[8192];
static uint8_t T[101][D]; static int found[101]; static int roles[101][13];
int main(){ memset(o5,-1,sizeof o5);
  FILE*f=fopen("reftables.txt","r"); int k,m,o; while(fscanf(f,"%d %d %d",&k,&m,&o)==3){ if(k==5)o5[m]=o; else if(k==4)o4[m]=o; else if(k==6)o6[m]=o; else opt[m]=o;} fclose(f);
  for(int m=0;m<8192;m++) inW[m]=(__builtin_popcount(m)==5 && o5[m]<0);
  int nW=0; for(int m=0;m<8192;m++) nW+=inW[m]; printf("W sets: %d\n",nW);
  f=fopen("targets.bin","rb"); if(fread(T,D,101,f)!=101) return 1; fclose(f);
  long total=0,disj=0; int nfound=0; uint8_t F[D];
  for(int inf=0;inf<13;inf++){ int pts[12],np=0; for(int x=0;x<13;x++) if(x!=inf) pts[np++]=x;
   for(int i1=0;i1<12;i1++)for(int i2=i1+1;i2<12;i2++)for(int i3=i2+1;i3<12;i3++){
    int a[3]={pts[i1],pts[i2],pts[i3]}; int rest[9],nr=0; for(int t=0;t<12;t++) if(t!=i1&&t!=i2&&t!=i3) rest[nr++]=pts[t];
    for(int j1=0;j1<9;j1++)for(int j2=0;j2<9;j2++)for(int j3=0;j3<9;j3++){ if(j1==j2||j1==j3||j2==j3) continue;
     int b[3]={rest[j1],rest[j2],rest[j3]}; int r6[6],n6=0; for(int t=0;t<9;t++) if(t!=j1&&t!=j2&&t!=j3) r6[n6++]=rest[t];
     for(int p=0;p<6;p++)for(int q=p+1;q<6;q++){ int r4[4],n4=0; for(int t=0;t<6;t++) if(t!=p&&t!=q) r4[n4++]=r6[t];
      for(int u=0;u<4;u++)for(int v=u+1;v<4;v++){ int r2[2],n2=0; for(int t=0;t<4;t++) if(t!=u&&t!=v) r2[n2++]=r4[t];
       int S12=(1<<r6[p])|(1<<r6[q]),S13=(1<<r4[u])|(1<<r4[v]),S23=(1<<r2[0])|(1<<r2[1]);
       int B[3]={(1<<a[0])|(1<<b[0])|S12|S13,(1<<a[1])|(1<<b[1])|S12|S23,(1<<a[2])|(1<<b[2])|S13|S23};
       int c6=(1<<inf)|(1<<a[0])|(1<<a[1])|(1<<a[2]), c9=(1<<inf)|(1<<b[0])|(1<<b[1])|(1<<b[2]), sh=S12|S13|S23;
       int sets[33],ns=0;
       for(int kk=0;kk<3;kk++) for(int x=0;x<13;x++) if(B[kk]>>x&1) sets[ns++]=B[kk]^(1<<x);
       for(int x=0;x<13;x++) if(sh>>x&1) sets[ns++]=c6|(1<<x);
       for(int x=0;x<13;x++) if(!(c9>>x&1)) sets[ns++]=c9|(1<<x);
       total++; int ok=1; for(int s=0;s<33;s++) if(inW[sets[s]]){ok=0;break;} if(!ok) continue; disj++;
       if(nfound==101) continue;
       memset(F,0,D); for(int s=0;s<33;s++) F[o5[sets[s]]]++;
       int cand=-1; for(int t=0;t<101;t++) if(!found[t] && !memcmp(F,T[t],101)){cand=t;break;}
       if(cand<0) continue;
       uint8_t *g=F+101,*h=F+101+69,*pt=F+101+69+135;
       for(int kk=0;kk<3;kk++){ h[o6[B[kk]]]+=3; for(int x=0;x<13;x++)for(int y=x+1;y<13;y++) if((B[kk]>>x&1)&&(B[kk]>>y&1)) g[o4[B[kk]^(1<<x)^(1<<y)]]++; }
       g[o4[c9]]+=4; g[o4[c6]]+=3;
       for(int x=0;x<13;x++)for(int y=x+1;y<13;y++){ if((sh>>x&1)&&(sh>>y&1)) h[o6[c6|(1<<x)|(1<<y)]]++; if(!(c9>>x&1)&&!(c9>>y&1)) h[o6[c9|(1<<x)|(1<<y)]]++; }
       pt[opt[inf]]=1;
       for(int t=0;t<101;t++) if(!found[t] && !memcmp(F,T[t],D)){ found[t]=1; nfound++;
         int R[13]={inf,a[0],a[1],a[2],b[0],b[1],b[2],r6[p],r6[q],r4[u],r4[v],r2[0],r2[1]}; memcpy(roles[t],R,sizeof R); break; }
      }}}}}
  printf("copies %ld, disjoint from W %ld, columns matched %d/101\n",total,disj,nfound);
  FILE*o2=fopen("lp_reps.txt","w"); for(int t=0;t<101;t++){ fprintf(o2,"%d",found[t]); for(int i=0;i<13;i++) fprintf(o2," %d",roles[t][i]); fprintf(o2,"\n"); } fclose(o2);
}
