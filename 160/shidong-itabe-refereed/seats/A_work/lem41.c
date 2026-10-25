/* EXHAUSTIVE check of Shi-Dong Lemma 4.1 for k=6, p=7 over ALL (y0,h) in F_7^9 x F_7^9 (7^18 pairs),
   via per-layer histograms:  the three symmetric conditions Q(y_{i-1})=Q(y_{6-i}) are additive over
   layers, so #y0 solving them for a given h = (v1,v3,v5) is a convolution of per-layer histograms of
     D(u) = (G(0)-G(5), G(1)-G(4), G(2)-G(3)) in F_7^3,  G(i) = P(u + i v).
   argv[1] = table file for the TOP layer, argv[2] = its dimension D (5 = the paper; 4 = even-degree control;
   argv[3] optional "iso" -> replace top form by w0 * P4(w1..w4) (isotropic degree-5 control, needs D=5 and P4 file argv[4]). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define p 7
static unsigned char P3[343], PT[16807], P4t[2401];
static int pw[8];
static void hist(int D, const unsigned char *tab, int v, uint32_t *H){ /* H[343] for step index v */
  int N=pw[D]; memset(H,0,343*sizeof(uint32_t));
  int vd[8], ud[8], w[8];
  for(int j=0,t=v;j<D;j++){vd[j]=t%p;t/=p;}
  for(int u=0;u<N;u++){
    for(int j=0,t=u;j<D;j++){ud[j]=t%p;t/=p;}
    int G[6];
    for(int i=0;i<6;i++){ int idx=0; for(int j=D-1;j>=0;j--){ w[j]=(ud[j]+i*vd[j])%p; idx=idx*p+w[j]; } G[i]= (D==1)? w[0] : tab[idx]; }
    int x=((G[0]-G[5]+p)%p) + p*((G[1]-G[4]+p)%p) + p*p*((G[2]-G[3]+p)%p);
    H[x]++;
  }
}
static int negidx(int x){ int a=x%p,b=(x/p)%p,c=x/(p*p); return ((p-a)%p)+p*((p-b)%p)+p*p*((p-c)%p); }
static int addidx(int x,int y){ int r=0,m=1; for(int j=0;j<3;j++){ r+=m*(((x%p)+(y%p))%p); x/=p;y/=p;m*=p;} return r; }
int main(int argc,char**argv){
  pw[0]=1; for(int i=1;i<8;i++) pw[i]=pw[i-1]*p;
  FILE*f=fopen("norm_p7_t3.bin","rb"); fread(P3,1,343,f); fclose(f);
  int D=atoi(argv[2]); f=fopen(argv[1],"rb"); fread(PT,1,pw[D],f); fclose(f);
  if(argc>3 && !strcmp(argv[3],"iso")){ f=fopen(argv[4],"rb"); fread(P4t,1,2401,f); fclose(f);
    for(int w=0;w<pw[5];w++){ int w0=w%p; PT[w]=(unsigned char)((w0*P4t[w/p])%p); } }
  unsigned char ID[7]; for(int i=0;i<7;i++) ID[i]=i;
  static uint32_t H1[7][343], H3[343][343]; uint32_t *HT=malloc(sizeof(uint32_t)*343*pw[D]);
  for(int v=0;v<7;v++) hist(1,ID,v,H1[v]);
  for(int v=0;v<343;v++) hist(3,P3,v,H3[v]);
  for(int v=0;v<pw[D];v++) hist(D,PT,v,HT+343*(size_t)v);
  int addt[343][343]; for(int x=0;x<343;x++) for(int y=0;y<343;y++) addt[x][y]=addidx(x,y);
  uint64_t (*C13)[343]=calloc(2401,sizeof(*C13));
  for(int v1=0;v1<7;v1++) for(int v3=0;v3<343;v3++){ uint64_t*C=C13[v1*343+v3];
    for(int x=0;x<343;x++) if(H1[v1][x]) for(int y=0;y<343;y++) if(H3[v3][y]) C[addt[x][y]]+=(uint64_t)H1[v1][x]*H3[v3][y]; }
  int neg[343]; for(int x=0;x<343;x++) neg[x]=negidx(x);
  uint64_t bad_h=0, total_sol_nonzero_h=0, zero_h_count=0; long long firstbad=-1;
  for(int vT=0;vT<pw[D];vT++){ uint32_t*Hv=HT+343*(size_t)vT; uint32_t Hn[343]; for(int x=0;x<343;x++) Hn[x]=Hv[neg[x]];
    for(int c=0;c<2401;c++){ uint64_t s=0; const uint64_t*C=C13[c]; for(int x=0;x<343;x++) s+=C[x]*Hn[x];
      if(vT==0 && c==0) zero_h_count=s; else if(s){ bad_h++; total_sol_nonzero_h+=s; if(firstbad<0) firstbad=(long long)vT*2401+c; } } }
  printf("top layer dim %d%s: h=0 -> %llu solutions (expect 7^%d=%llu); nonzero h with a symmetric k-AP: %llu (total (y0,h) pairs %llu); first bad code %lld\n",
     D, (argc>3?" [iso control]":""), (unsigned long long)zero_h_count, 4+D, (unsigned long long)(7ULL*343*pw[D]), (unsigned long long)bad_h, (unsigned long long)total_sol_nonzero_h, firstbad);
  return bad_h?1:0;
}
