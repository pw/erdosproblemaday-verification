// Enumerate all copies of W via role form; count: total, special point 0,
// those with 33 sets in distinct Z13-orbits (special 0), disjoint from W (the 0-based Appendix A family),
// and search for 3 orbit-transversal copies covering all 99 orbits.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int orbit_of[8192];
static int rot(int m){ return ((m<<1)|(m>>12)) & 8191; }
static int Wmask[33];
static unsigned char inW[8192];
typedef struct { uint64_t lo, hi; } m128;
static m128 *T; static long nT=0, capT=0;
static int build(int inf,const int*a,const int*b,const int*S12,const int*S13,const int*S23,int*out){
  int n=0; int B[3];
  int s12=(1<<S12[0])|(1<<S12[1]), s13=(1<<S13[0])|(1<<S13[1]), s23=(1<<S23[0])|(1<<S23[1]);
  B[0]=(1<<a[0])|(1<<b[0])|s12|s13; B[1]=(1<<a[1])|(1<<b[1])|s12|s23; B[2]=(1<<a[2])|(1<<b[2])|s13|s23;
  for(int i=0;i<3;i++) for(int x=0;x<13;x++) if(B[i]>>x&1) out[n++]=B[i]&~(1<<x);
  int c6=(1<<inf)|(1<<a[0])|(1<<a[1])|(1<<a[2]); int c9=(1<<inf)|(1<<b[0])|(1<<b[1])|(1<<b[2]);
  int sh=s12|s13|s23;
  for(int x=0;x<13;x++) if(sh>>x&1) out[n++]=c6|(1<<x);
  for(int y=0;y<13;y++) if(!(c9>>y&1)) out[n++]=c9|(1<<y);
  return n;
}
int main(){
  // orbits
  memset(orbit_of,-1,sizeof orbit_of); int no=0;
  for(int m=0;m<8192;m++) if(__builtin_popcount(m)==5 && orbit_of[m]<0){ int x=m; for(int k=0;k<13;k++){orbit_of[x]=no; x=rot(x);} no++; }
  fprintf(stderr,"orbits %d\n",no);
  // W 0-based from wstruct role form: inf=10,a=(0,11,6),b=(1,12,7),S12=(2,5),S13=(3,4),S23=(8,9)
  { int a[3]={0,11,6},b[3]={1,12,7},S12[2]={2,5},S13[2]={3,4},S23[2]={8,9}; int n=build(10,a,b,S12,S13,S23,Wmask); if(n!=33) return 1; for(int i=0;i<33;i++) inW[Wmask[i]]=1; }
  long total=0, sp0=0, transv=0, disjW=0;
  capT=200000; T=malloc(capT*sizeof(m128));
  for(int inf=0;inf<13;inf++){
    int rest[12],nr=0; for(int x=0;x<13;x++) if(x!=inf) rest[nr++]=x;
    for(int i=0;i<12;i++)for(int j=i+1;j<12;j++)for(int k=j+1;k<12;k++){
      int a[3]={rest[i],rest[j],rest[k]}; int used=(1<<inf)|(1<<a[0])|(1<<a[1])|(1<<a[2]);
      int r2[9],n2=0; for(int x=0;x<13;x++) if(!(used>>x&1)) r2[n2++]=x;
      for(int p=0;p<9;p++)for(int q=0;q<9;q++)if(q!=p)for(int r=0;r<9;r++)if(r!=p&&r!=q){
        int b[3]={r2[p],r2[q],r2[r]}; int u2=used|(1<<b[0])|(1<<b[1])|(1<<b[2]);
        int s[6],ns=0; for(int x=0;x<13;x++) if(!(u2>>x&1)) s[ns++]=x;
        // partition s into 3 labelled unordered pairs: s[0] paired with t, etc.
        for(int t1=1;t1<6;t1++){
          int r3[4],n3=0; for(int x=1;x<6;x++) if(x!=t1) r3[n3++]=s[x];
          for(int t2=1;t2<4;t2++){
            int r4[2],n4=0; for(int x=1;x<4;x++) if(x!=t2) r4[n4++]=r3[x];
            int P[3][2]={{s[0],s[t1]},{r3[0],r3[t2]},{r4[0],r4[1]}};
            // assign pairs to slots S12,S13,S23 in all 6 orders
            int perm[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
            for(int pi=0;pi<6;pi++){
              int out[33]; build(inf,a,b,P[perm[pi][0]],P[perm[pi][1]],P[perm[pi][2]],out);
              total++;
              int dj=1; for(int z=0;z<33;z++) if(inW[out[z]]){dj=0;break;}
              disjW+=dj;
              if(inf==0){ sp0++;
                m128 m={0,0}; int ok=1;
                for(int z=0;z<33;z++){ int o=orbit_of[out[z]]; if(o<64){ if(m.lo>>o&1){ok=0;break;} m.lo|=1ULL<<o;} else { if(m.hi>>(o-64)&1){ok=0;break;} m.hi|=1ULL<<(o-64);} }
                if(ok){ if(nT==capT){capT*=2;T=realloc(T,capT*sizeof(m128));} T[nT++]=m; transv++; }
              }
            }
          }
        }
      }
    }
  }
  printf("total copies %ld  special-point-0 %ld  transversal(sp0) %ld  disjoint-from-W %ld\n",total,sp0,transv,disjW);
  // distinct transversal masks?  search triples covering all 99 orbits
  m128 full={~0ULL, (1ULL<<35)-1};
  if(getenv("PLANT")){ long i0=0; while(!(T[i0].lo&1)) i0++; m128 R={full.lo&~T[i0].lo, full.hi&~T[i0].hi};
    m128 B={0,0}; int c=0; for(int o=0;o<99&&c<33;o++){ int in= o<64?(R.lo>>o&1):(R.hi>>(o-64)&1); if(in){ if(o<64)B.lo|=1ULL<<o; else B.hi|=1ULL<<(o-64); c++; } }
    m128 C={R.lo&~B.lo,R.hi&~B.hi}; T[nT++]=B; T[nT++]=C; fprintf(stderr,"planted\n"); }
  long found=0;
  for(long i=0;i<nT;i++){ if(!(T[i].lo&1)) continue;
    m128 A=T[i]; m128 R={full.lo&~A.lo, full.hi&~A.hi};
    int lowbit = R.lo? __builtin_ctzll(R.lo) : 64+__builtin_ctzll(R.hi);
    for(long j=0;j<nT;j++){
      m128 B=T[j];
      if((B.lo&A.lo)||(B.hi&A.hi)) continue;
      int has = lowbit<64 ? (B.lo>>lowbit&1) : (B.hi>>(lowbit-64)&1); if(!has) continue;
      m128 C={R.lo&~B.lo, R.hi&~B.hi};
      for(long k=0;k<nT;k++) if(T[k].lo==C.lo && T[k].hi==C.hi){ found++; break; }
    }
  }
  printf("covering triples (with orbit 0 in first): %ld\n",found);
  return 0;
}
