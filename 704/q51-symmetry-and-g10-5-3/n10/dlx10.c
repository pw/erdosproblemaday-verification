/* Second instrument for chi(G(10,5,3)) = 21 ?  Own enumeration of all maximum independent sets (size 12) of J(10,5,3) by
   backtracking, then exact cover of the 252 vertices by 21 of them (Algorithm X on bitsets, min-candidates column rule).
   Symmetry: the class containing vertex 0 = {0,1,2,3,4} is taken only from representatives of the orbits of
   Stab(v0) = Sym{0..4} x Sym{5..9} on the sets containing v0 (first-seen representative).
   Usage: dlx10 [maxsol]   prints #sets, #orbit reps, per-rep node counts, solutions found.                      */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define NV 252
typedef struct { uint64_t w[4]; } bs;
static int masks[NV], idx[1024]; static bs adj[NV];
static inline int bget(const bs*b,int i){ return b->w[i>>6]>>(i&63)&1; }
static inline void bset(bs*b,int i){ b->w[i>>6]|=1ULL<<(i&63); }
static inline int bcount(const bs*b){ return __builtin_popcountll(b->w[0])+__builtin_popcountll(b->w[1])+__builtin_popcountll(b->w[2])+__builtin_popcountll(b->w[3]); }
static uint8_t (*sets)[12]; static bs *setb; static long nsets=0, capsets=0;
static int cur[12];
static void enumr(int depth, bs cand){
    if(depth==12){ if(nsets==capsets){capsets=capsets?2*capsets:1<<16; sets=realloc(sets,capsets*12); setb=realloc(setb,capsets*sizeof(bs));}
        memset(&setb[nsets],0,sizeof(bs)); for(int i=0;i<12;i++){sets[nsets][i]=cur[i]; bset(&setb[nsets],cur[i]);} nsets++; return; }
    if(depth+bcount(&cand)<12) return;
    for(int wd=0;wd<4;wd++) while(cand.w[wd]){
        int v=wd*64+__builtin_ctzll(cand.w[wd]); cand.w[wd]&=cand.w[wd]-1;   /* remove v: later choices have larger index */
        bs nc; for(int k=0;k<4;k++) nc.w[k]=cand.w[k]&~adj[v].w[k];
        cur[depth]=v; enumr(depth+1,nc);
    }
}
/* per-vertex list of sets containing it */
static int **vs; static int *vsn;
static long nodes, sols, maxsol; static int chosen[21];
static void search(int depth, bs covered){
    nodes++;
    if(depth==21){ sols++; if(sols<=maxsol){ printf("SOLUTION"); for(int i=0;i<21;i++) printf(" %d",chosen[i]); printf("\n"); fflush(stdout);} return; }
    /* choose uncovered vertex with fewest compatible sets (scan a few candidates fully) */
    int bestv=-1,bestc=1<<30;
    for(int v=0;v<NV;v++){ if(bget(&covered,v)) continue; int c=0;
        for(int t=0;t<vsn[v];t++){ const bs*s=&setb[vs[v][t]]; if(!((s->w[0]&covered.w[0])|(s->w[1]&covered.w[1])|(s->w[2]&covered.w[2])|(s->w[3]&covered.w[3]))) { c++; if(c>=bestc) break; } }
        if(c<bestc){bestc=c;bestv=v; if(c==0) return;} }
    for(int t=0;t<vsn[bestv];t++){ int si=vs[bestv][t]; const bs*s=&setb[si];
        if((s->w[0]&covered.w[0])|(s->w[1]&covered.w[1])|(s->w[2]&covered.w[2])|(s->w[3]&covered.w[3])) continue;
        bs nc; for(int k=0;k<4;k++) nc.w[k]=covered.w[k]|s->w[k]; chosen[depth]=si; search(depth+1,nc);
        if(sols>=maxsol && maxsol>0) return; }
}
int main(int argc,char**argv){
    maxsol=argc>1?atol(argv[1]):1;
    int n=0; for(int m=0;m<1024;m++) idx[m]=(__builtin_popcount(m)==5)?n:-1, n+=(__builtin_popcount(m)==5), masks[n-1>=0?n-1:0]= (__builtin_popcount(m)==5)?m:masks[n-1>=0?n-1:0];
    n=0; for(int m=0;m<1024;m++) if(__builtin_popcount(m)==5) masks[n++]=m;
    for(int i=0;i<NV;i++) for(int j=0;j<NV;j++) if(i!=j&&__builtin_popcount(masks[i]&masks[j])==3) bset(&adj[i],j);
    /* enumerate all independent 12-sets, smallest vertex first */
    for(int v0=0;v0<NV;v0++){ bs cand; memset(&cand,0,sizeof cand); for(int u=v0+1;u<NV;u++) if(!bget(&adj[v0],u)) bset(&cand,u); cur[0]=v0; enumr(1,cand); }
    fprintf(stderr,"maximum independent sets (own enumeration): %ld\n",nsets);
    vs=malloc(NV*sizeof(int*)); vsn=calloc(NV,sizeof(int)); for(long s=0;s<nsets;s++) for(int i=0;i<12;i++) vsn[sets[s][i]]++;
    for(int v=0;v<NV;v++){ vs[v]=malloc(vsn[v]*sizeof(int)); vsn[v]=0; } for(long s=0;s<nsets;s++) for(int i=0;i<12;i++){ int v=sets[s][i]; vs[v][vsn[v]++]=s; }
    fprintf(stderr,"sets containing vertex 0: %d\n",vsn[0]);
    /* orbits of Stab(v0)=S5xS5 on the sets containing v0: canonical form = min over the 14400 group elements of the sorted mask list hash */
    int v0=idx[0x1f]; if(v0!=0){fprintf(stderr,"v0 index %d\n",v0);} 
    int nrep=0; int *rep=malloc(vsn[v0]*sizeof(int)); long *orbsz=malloc(vsn[v0]*sizeof(long));
    { /* build permutation list */
      int perms5[120][5],np=0; int a[5]={0,1,2,3,4};
      for(int i0=0;i0<5;i0++)for(int i1=0;i1<5;i1++)for(int i2=0;i2<5;i2++)for(int i3=0;i3<5;i3++)for(int i4=0;i4<5;i4++){ int p[5]={i0,i1,i2,i3,i4},ok=1; for(int x=0;x<5;x++)for(int y=x+1;y<5;y++) if(p[x]==p[y]) ok=0; if(ok){memcpy(perms5[np++],p,sizeof p);} }
      (void)a;
      char *done=calloc(nsets,1);
      /* map from bitset to set index via sorting: use a hash of the 4 words -> index (linear probing) */
      long cap=1; while(cap<4*nsets) cap<<=1; long *ht=malloc(cap*sizeof(long)); memset(ht,-1,cap*sizeof(long));
      #define H(b) (((b).w[0]*0x9E3779B97F4A7C15ULL)^((b).w[1]*0xC2B2AE3D27D4EB4FULL)^((b).w[2]*0x165667B19E3779F9ULL)^((b).w[3]*0xD6E8FEB86659FD93ULL))
      for(long s=0;s<nsets;s++){ long pos=H(setb[s])&(cap-1); while(ht[pos]>=0) pos=(pos+1)&(cap-1); ht[pos]=s; }
      for(int t=0;t<vsn[v0];t++){ int s=vs[v0][t]; if(done[s]) continue; rep[nrep]=s; long sz=0;
          for(int p=0;p<120;p++) for(int q=0;q<120;q++){
              int pm[10]; for(int x=0;x<5;x++){pm[x]=perms5[p][x]; pm[5+x]=5+perms5[q][x];}
              bs img; memset(&img,0,sizeof img);
              for(int i=0;i<12;i++){ int m=masks[sets[s][i]],r=0; for(int x=0;x<10;x++) if(m>>x&1) r|=1<<pm[x]; bset(&img,idx[r]); }
              long pos=H(img)&(cap-1); long f=-1; while(ht[pos]>=0){ if(!memcmp(&setb[ht[pos]],&img,sizeof(bs))){f=ht[pos];break;} pos=(pos+1)&(cap-1); }
              if(f<0){fprintf(stderr,"image not a known set!\n");return 1;} if(!done[f]){done[f]=1;sz++;} }
          orbsz[nrep++]=sz; }
    }
    long tot=0; for(int r=0;r<nrep;r++) tot+=orbsz[r];
    fprintf(stderr,"orbit representatives under Stab(v0): %d (orbit sizes sum %ld)\n",nrep,tot);
    long totnodes=0;
    for(int r=0;r<nrep;r++){ nodes=0; long s0=sols; chosen[0]=rep[r]; search(1,setb[rep[r]]); totnodes+=nodes;
        fprintf(stderr,"rep %d/%d (orbit %ld): nodes %ld, solutions %ld\n",r+1,nrep,orbsz[r],nodes,sols-s0); fflush(stderr);
        if(sols>=maxsol && maxsol>0) break; }
    fprintf(stderr,"TOTAL nodes %ld ; solutions found %ld (search %s)\n",totnodes,sols,(sols>=maxsol&&maxsol>0)?"stopped at maxsol":"exhaustive over orbit reps");
    return 0;
}
