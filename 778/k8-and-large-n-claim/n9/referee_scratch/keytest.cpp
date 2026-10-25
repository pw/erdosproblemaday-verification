// Exhaustive key-completeness test: check778c's canon() (included VERBATIM) vs a brute-force canonical form
// (lexicographic min over all n! vertex permutations; no nauty). Also an "old" key = canonical layers read WITHOUT
// the rung fold, to show the test has teeth against the earlier bug.
#define MAXN 32
#include "nauty.h"
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <map>
typedef unsigned __int128 u128; typedef uint64_t u64;
static int MAXR=99; static int n, m; static int eidx[12][12]; static int ea[66], eb[66];
#include "canon_verbatim.inc"
// old key: same nauty call, but Bc read as layer-1 edges in layer-1 positions (no tau)
static void canon_old(u64 R,u64 B,u128& key){
    const int nv=2*n, mm=SETWORDSNEEDED(nv);
    graph g[MAXN*MAXM], cg[MAXN*MAXM]; int lab[MAXN],ptn[MAXN], orbits[MAXN]; statsblk stats; DEFAULTOPTIONS_GRAPH(opt);
    opt.getcanon=TRUE; opt.defaultptn=FALSE; EMPTYGRAPH(g,mm,nv);
    for(int k=0;k<m;k++){ if(R>>k&1) ADDONEEDGE(g,ea[k],eb[k],mm); if(B>>k&1) ADDONEEDGE(g,n+ea[k],n+eb[k],mm); }
    for(int i=0;i<n;i++) ADDONEEDGE(g,i,n+i,mm);
    for(int i=0;i<nv;i++){ lab[i]=i; ptn[i]=1; } ptn[n-1]=0; ptn[nv-1]=0;
    densenauty(g,lab,ptn,orbits,&opt,&stats,mm,nv,cg);
    u64 Rc=0,Bc=0;
    for(int p=0;p<n;p++){ set* row=GRAPHROW(cg,p,mm); for(int q=p+1;q<n;q++) if(ISELEMENT(row,q)) Rc|=1ULL<<eidx[p][q]; }
    for(int q1=0;q1<n;q1++){ set* row2=GRAPHROW(cg,n+q1,mm); for(int q2=q1+1;q2<n;q2++) if(ISELEMENT(row2,n+q2)) Bc|=1ULL<<eidx[q1][q2]; }
    key=((u128)Rc<<64)|Bc;
}
static std::vector<std::vector<int>> perms; static std::vector<std::vector<u64>> lo, hi; // byte tables
static u64 mapmask(int p,u64 x){ return lo[p][x&255] | hi[p][(x>>8)&255] | (m>16? hi[p][256+((x>>16)&255)] : 0); }
static u128 brute(u64 R,u64 B){ u128 best=~(u128)0; for(size_t p=0;p<perms.size();p++){ u128 v=((u128)mapmask(p,R)<<64)|mapmask(p,B); if(v<best) best=v; } return best; }
struct H{ size_t operator()(const u128&x)const{ u64 a=(u64)x,b=(u64)(x>>64); return a*0x9E3779B97F4A7C15ULL ^ (b+0x632BE59BD9B4E019ULL)*0xBF58476D1CE4E5B9ULL; } };
int main(int argc,char**argv){
    n=atoi(argv[1]); int mode=atoi(argv[2]); MAXR=(argc>3)?atoi(argv[3]):99; // mode 0: all 3^m colourings; 1: game-shaped (|B|=2|R| or 2|R|-2, |R|<=ceil(m/3))
    m=0; for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ eidx[i][j]=eidx[j][i]=m; ea[m]=i; eb[m]=j; m++; }
    if(m>24){ printf("m too big\n"); return 2; }
    std::vector<int> pp(n); for(int i=0;i<n;i++) pp[i]=i;
    do{ perms.push_back(pp); } while(std::next_permutation(pp.begin(),pp.end()));
    for(auto& P:perms){ std::vector<int> em(m); for(int k=0;k<m;k++) em[k]=eidx[P[ea[k]]][P[eb[k]]];
        std::vector<u64> L(256,0), Hh(512,0);
        for(int x=0;x<256;x++){ for(int b=0;b<8;b++) if(x>>b&1){ if(b<m) L[x]|=1ULL<<em[b]; if(8+b<m) Hh[x]|=1ULL<<em[8+b]; if(16+b<m) Hh[256+x]|=1ULL<<em[16+b]; } }
        lo.push_back(L); hi.push_back(Hh); }
    int A=(m+2)/3; long long cnt=0;
    std::unordered_map<u128,u128,H> k2b, b2k, old2b; long long bad_sound=0,bad_canon=0,old_collide=0;
    auto visit=[&](u64 R,u64 B){ cnt++; u128 k; int lab[MAXN]; canon(R,B,k,lab); u128 c=brute(R,B); u128 ko; canon_old(R,B,ko);
        auto a=k2b.emplace(k,c); if(!a.second && a.first->second!=c) bad_sound++;
        auto b=b2k.emplace(c,k); if(!b.second && b.first->second!=k) bad_canon++;
        auto o=old2b.emplace(ko,c); if(!o.second && o.first->second!=c) old_collide++; };
    if(mode==0){ long long tot=1; for(int k=0;k<m;k++) tot*=3; for(long long x=0;x<tot;x++){ long long y=x; u64 R=0,B=0; for(int k=0;k<m;k++){ int d=y%3; y/=3; if(d==1) R|=1ULL<<k; else if(d==2) B|=1ULL<<k; } visit(R,B);} }
    else { // enumerate R with |R|=r, B subset of complement with |B| in {2r,2r-2}
        for(u64 R=0;R<(1ULL<<m);R++){ if(__builtin_popcountll(R)>MAXR) continue; int r=__builtin_popcountll(R); if(r>A || r>MAXR) continue; u64 comp=((1ULL<<m)-1)&~R;
            // enumerate subsets of comp of size 2r and 2r-2 via Gosper over compressed index
            std::vector<int> idx; for(int k=0;k<m;k++) if(comp>>k&1) idx.push_back(k); int f=idx.size();
            for(int s: {2*r,2*r-2}){ if(s<0||s>f) continue; if(r==0&&s!=0) continue; if(s==0){ visit(R,0); continue; }
                u64 c=(1ULL<<s)-1; while(c < (1ULL<<f)){ u64 B=0; for(int t=0;t<f;t++) if(c>>t&1) B|=1ULL<<idx[t]; visit(R,B);
                    u64 lo1=c&-c, r1=c+lo1; c=(((r1^c)>>2)/lo1)|r1; } } } }
    printf("n=%d mode=%d positions=%lld nautyKeys=%zu bruteClasses=%zu  key-equal&non-iso=%lld  iso&key-differ=%lld  | OLD(no rung fold): keys=%zu collisions(key-equal&non-iso)=%lld\n",
        n,mode,cnt,k2b.size(),b2k.size(),bad_sound,bad_canon,old2b.size(),old_collide);
    return (bad_sound||bad_canon)?1:0;
}
