// Convention test for check778c's canon/transport: random positions, random relabellings, assert (1) key invariance,
// (2) cg == g relabelled by pos (pos[lab[p]]=p), (3) transported reply is free and leads to an isomorphic position.
#define MAXN 32
#include "nauty.h"
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <algorithm>
#include <random>
typedef unsigned __int128 u128; typedef uint64_t u64;
static int n,m; static int eidx[12][12]; static int ea[66],eb[66]; static u128 g_draft;
static void canon(u64 R,u64 B,u128& key,int* lab, graph* cgout){
    const int nv=2*n, mm=SETWORDSNEEDED(nv);
    graph g[MAXN*MAXM], cg[MAXN*MAXM]; int ptn[MAXN], orbits[MAXN]; statsblk stats; DEFAULTOPTIONS_GRAPH(opt);
    opt.getcanon=TRUE; opt.defaultptn=FALSE; EMPTYGRAPH(g,mm,nv);
    for(int k=0;k<m;k++){ if(R>>k&1) ADDONEEDGE(g,ea[k],eb[k],mm); if(B>>k&1) ADDONEEDGE(g,n+ea[k],n+eb[k],mm); }
    for(int i=0;i<n;i++) ADDONEEDGE(g,i,n+i,mm);
    for(int i=0;i<nv;i++){ lab[i]=i; ptn[i]=1; } ptn[n-1]=0; ptn[nv-1]=0;
    densenauty(g,lab,ptn,orbits,&opt,&stats,mm,nv,cg);
    u64 Rc=0,Bc=0; int tau[MAXN];
    for(int p=0;p<n;p++){ set* row=GRAPHROW(cg,p,mm); int cnt=0; for(int q=n;q<nv;q++) if(ISELEMENT(row,q)){ tau[q-n]=p; cnt++; } if(cnt!=1){ printf("rung count %d\n",cnt); exit(1);} }
    for(int p=0;p<n;p++){ set* row=GRAPHROW(cg,p,mm); for(int q=p+1;q<n;q++) if(ISELEMENT(row,q)) Rc|=1ULL<<eidx[p][q]; }
    for(int q1=0;q1<n;q1++){ set* row2=GRAPHROW(cg,n+q1,mm); for(int q2=q1+1;q2<n;q2++) if(ISELEMENT(row2,n+q2)) Bc|=1ULL<<eidx[tau[q1]][tau[q2]]; }
    key=((u128)Rc<<64)|Bc; if(cgout) for(int i=0;i<mm*nv;i++) cgout[i]=cg[i];
    { u64 Bd=0; for(int q1=0;q1<n;q1++){ set* row2=GRAPHROW(cg,n+q1,mm); for(int q2=q1+1;q2<n;q2++) if(ISELEMENT(row2,n+q2)) Bd|=1ULL<<eidx[q1][q2]; } g_draft=((u128)Rc<<64)|Bd; } // the first draft's key: layer 1 read in its own positions, rung matching dropped
    // (2): relabel g by pos and compare with cg
    int pos[MAXN]; for(int p=0;p<nv;p++) pos[lab[p]]=p; graph h[MAXN*MAXM]; EMPTYGRAPH(h,mm,nv);
    for(int k=0;k<m;k++){ if(R>>k&1) ADDONEEDGE(h,pos[ea[k]],pos[eb[k]],mm); if(B>>k&1) ADDONEEDGE(h,pos[n+ea[k]],pos[n+eb[k]],mm); }
    for(int i=0;i<n;i++) ADDONEEDGE(h,pos[i],pos[n+i],mm);
    for(int i=0;i<mm*nv;i++) if(h[i]!=cg[i]){ printf("CONVENTION: relabelling by pos[lab[p]]=p does NOT give cg\n"); exit(1);} 
}
int main(){ n=7; m=0; for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ eidx[i][j]=eidx[j][i]=m; ea[m]=i; eb[m]=j; m++; }
    std::mt19937_64 rng(1); int ok=0;
    for(int t=0;t<2000;t++){ u64 R=0,B=0; for(int k=0;k<m;k++){ int r=rng()%3; if(r==0) R|=1ULL<<k; else if(r==1&&(rng()%2)) B|=1ULL<<k; }
        int perm[12]; for(int i=0;i<n;i++) perm[i]=i; std::shuffle(perm,perm+n,rng);
        u64 R2=0,B2=0; for(int k=0;k<m;k++){ int kk=eidx[perm[ea[k]]][perm[eb[k]]]; if(R>>k&1) R2|=1ULL<<kk; if(B>>k&1) B2|=1ULL<<kk; }
        u128 k1,k2; int l1[MAXN],l2[MAXN]; canon(R,B,k1,l1,nullptr); canon(R2,B2,k2,l2,nullptr);
        if(k1!=k2){ printf("KEY NOT INVARIANT at t=%d\n",t); return 1; }
        // transport a free edge e of P to Q
        int e=-1; for(int k=0;k<m;k++) if(!((R|B)>>k&1)){ e=k; break; } if(e<0) continue;
        int pos1[MAXN]; for(int p=0;p<2*n;p++) pos1[l1[p]]=p; int ec=eidx[pos1[ea[e]]][pos1[eb[e]]];
        int a=eidx[l2[ea[ec]]][l2[eb[ec]]];
        if((R2|B2)>>a&1){ printf("TRANSPORT lands on an occupied edge at t=%d\n",t); return 1; }
        u128 k3,k4; int l3[MAXN],l4[MAXN]; canon(R|(1ULL<<e),B,k3,l3,nullptr); canon(R2|(1ULL<<a),B2,k4,l4,nullptr);
        if(k3!=k4){ printf("TRANSPORTED MOVE NOT ISOMORPHIC at t=%d\n",t); return 1; } ok++; }
    printf("all good: %d transports verified\n",ok);
    // ORACLE: brute force over all n! vertex permutations; key-equal must coincide with isomorphic on random pairs
    auto iso=[&](u64 R1,u64 B1,u64 R2,u64 B2){ int perm[12]; for(int i=0;i<n;i++) perm[i]=i; do{ u64 r=0,b=0; for(int k=0;k<m;k++){ int kk=eidx[perm[ea[k]]][perm[eb[k]]]; if(R1>>k&1) r|=1ULL<<kk; if(B1>>k&1) b|=1ULL<<kk; } if(r==R2&&b==B2) return true; } while(std::next_permutation(perm,perm+n)); return false; };
    int agree=0, keyeq=0, isoc=0;
    for(int t=0;t<400;t++){ u64 R1=0,B1=0; for(int k=0;k<m;k++){ int r=rng()%4; if(r==0) R1|=1ULL<<k; else if(r==1) B1|=1ULL<<k; }
        u64 R2,B2; if(t%2){ int perm[12]; for(int i=0;i<n;i++) perm[i]=i; std::shuffle(perm,perm+n,rng); R2=B2=0; for(int k=0;k<m;k++){ int kk=eidx[perm[ea[k]]][perm[eb[k]]]; if(R1>>k&1) R2|=1ULL<<kk; if(B1>>k&1) B2|=1ULL<<kk; }
            if(t%4==1){ // relabelled copy with ONE blue edge moved to the first free edge (same red graph, same blue edge count; the blue graph itself may change)
                int fr=-1; for(int k=0;k<m;k++) if(!((R2|B2)>>k&1)){ fr=k; break; } int bl=-1; for(int k=0;k<m;k++) if(B2>>k&1){ bl=k; break; } if(fr>=0&&bl>=0){ B2&=~(1ULL<<bl); B2|=1ULL<<fr; } } }
        else { R2=0; B2=0; for(int k=0;k<m;k++){ int r=rng()%4; if(r==0) R2|=1ULL<<k; else if(r==1) B2|=1ULL<<k; } }
        u128 k1,k2; int l1[MAXN],l2[MAXN]; canon(R1,B1,k1,l1,nullptr); canon(R2,B2,k2,l2,nullptr);
        bool ke=(k1==k2), io=iso(R1,B1,R2,B2); keyeq+=ke; isoc+=io; if(ke==io) agree++; else { printf("KEY/ORACLE DISAGREE at t=%d (key-equal %d, isomorphic %d)\n",t,ke,io); return 1; } }
    printf("oracle: %d/400 pairs agree (key-equal %d, isomorphic %d)\n",agree,keyeq,isoc);
    // deliberate arm: same red graph, blue graph relabelled ALONE by a random vertex permutation -> both colour classes' graphs agree by
    // construction, the position usually does not; the correct key must agree with the oracle, and we count how often the draft key does not
    int agree2=0,keyeq2=0,isoc2=0,draftwrong=0,draftwrong_all=0;
    for(int t=0;t<200;t++){ u64 R1=0,B1=0; for(int k=0;k<m;k++){ int r=rng()%4; if(r==0) R1|=1ULL<<k; else if(r==1) B1|=1ULL<<k; }
        u64 B2=0; bool okp=false; for(int tries=0;tries<60 && !okp;tries++){ int perm[12]; for(int i=0;i<n;i++) perm[i]=i; std::shuffle(perm,perm+n,rng); B2=0; for(int k=0;k<m;k++) if(B1>>k&1) B2|=1ULL<<eidx[perm[ea[k]]][perm[eb[k]]]; okp=((B2&R1)==0); }
        if(!okp) continue; u64 R2=R1; // red graph identical, blue graph relabelled alone (and edge-disjoint from red)
        u128 k1,k2; int l1[MAXN],l2[MAXN]; canon(R1,B1,k1,l1,nullptr); u128 d1=g_draft; canon(R2,B2,k2,l2,nullptr); u128 d2=g_draft;
        bool ke=(k1==k2), io=iso(R1,B1,R2,B2); keyeq2+=ke; isoc2+=io; if(ke==io) agree2++; else { printf("DELIBERATE ARM: KEY/ORACLE DISAGREE at t=%d\n",t); return 1; }
        if((d1==d2)!=io) draftwrong++; }
    // and the draft key over the first 400 random pairs, same RNG stream re-seeded
    { std::mt19937_64 rng2(1); for(int t=0;t<2000;t++){ u64 R=0,B=0; for(int k=0;k<m;k++){ int r=rng2()%3; if(r==0) R|=1ULL<<k; else if(r==1&&(rng2()%2)) B|=1ULL<<k; } int perm[12]; for(int i=0;i<n;i++) perm[i]=i; std::shuffle(perm,perm+n,rng2); }
      for(int t=0;t<400;t++){ u64 R1=0,B1=0; for(int k=0;k<m;k++){ int r=rng2()%4; if(r==0) R1|=1ULL<<k; else if(r==1) B1|=1ULL<<k; }
        u64 R2,B2; if(t%2){ int perm[12]; for(int i=0;i<n;i++) perm[i]=i; std::shuffle(perm,perm+n,rng2); R2=B2=0; for(int k=0;k<m;k++){ int kk=eidx[perm[ea[k]]][perm[eb[k]]]; if(R1>>k&1) R2|=1ULL<<kk; if(B1>>k&1) B2|=1ULL<<kk; }
            if(t%4==1){ int fr=-1; for(int k=0;k<m;k++) if(!((R2|B2)>>k&1)){ fr=k; break; } int bl=-1; for(int k=0;k<m;k++) if(B2>>k&1){ bl=k; break; } if(fr>=0&&bl>=0){ B2&=~(1ULL<<bl); B2|=1ULL<<fr; } } }
        else { R2=0; B2=0; for(int k=0;k<m;k++){ int r=rng2()%4; if(r==0) R2|=1ULL<<k; else if(r==1) B2|=1ULL<<k; } }
        u128 k1,k2; int l1[MAXN],l2[MAXN]; canon(R1,B1,k1,l1,nullptr); u128 d1=g_draft; canon(R2,B2,k2,l2,nullptr); u128 d2=g_draft; bool io=iso(R1,B1,R2,B2); if((d1==d2)!=io) draftwrong_all++; } }
    printf("deliberate arm (blue layer permuted alone): %d pairs, key/oracle agree %d/%d (isomorphic %d); FIRST-DRAFT key (rung matching dropped) wrong on %d of them, and on %d of the 400 random pairs\n",agree2,agree2,agree2,isoc2,draftwrong,draftwrong_all); return 0; }
