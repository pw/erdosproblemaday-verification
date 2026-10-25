// check778c.cpp — INDEPENDENT checker for solve778 strategy certificates (Erdős #778, (1:2) clique game on K_n), C++ + nauty.
// Third implementation (after solve778.cpp's own search and check778.py): shares with the solver ONLY the lexicographic
// edge numbering and the rules of the game. Canonical forms come from nauty's densenauty on a two-layer graph
// (layer 0 = Alice's red edges, layer 1 = Bob's blue edges, rung i -- n+i, the two layers as colour classes), and the
// canonical KEY is read off nauty's canonical graph itself (its two layers as edge masks), so no hashing of our own.
// Cliques and both cutoffs are re-derived here from first principles. Exploration is level-synchronous (by Alice's edge
// count), exhaustive over Alice's moves, transposition only through canonical forms.
//   winner=bob certificates only ("R B e f": at Bob-to-move representative (R,B) Bob replies e,f). Exit 0 ACCEPT, 1 REJECT, 2 CANNOT SEE.
//   usage: check778c <cert> [--no-cutoff] [--threads k]   (threads > 1 needs a TLS-built nauty)
#define MAXN 32
#include "nauty.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <omp.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
struct H128 { size_t operator()(const u128& x) const { u64 a=(u64)x, b=(u64)(x>>64); a^=b*0x9E3779B97F4A7C15ULL; a^=a>>29; a*=0xBF58476D1CE4E5B9ULL; a^=a>>32; return a; } };

static int n, m, A; static bool TRI=false, NOCUT=false; static int NT=1;
static int eidx[12][12]; static int ea[66], eb[66];
static u64 FULL;
// vertex-subset tables (n <= 10 -> 1024 subsets): edge mask inside S, and |S|
static std::vector<u64> EM; static std::vector<int> SZ;

static inline int pc(u64 x){ return __builtin_popcountll(x); }
static int omega(u64 mask){ int best=1; for(size_t S=1;S<EM.size();S++) if(SZ[S]>best && (EM[S] & ~mask)==0) best=SZ[S]; return best; }
static int alpha(u64 R){ return omega(FULL & ~R); }
static int omega_budget(u64 R,u64 B,int k){ int best=1; for(size_t S=1;S<EM.size();S++){ if(SZ[S]<=best) continue; u64 es=EM[S]; if(es&B) continue; if(pc(es & ~R)<=k) best=SZ[S]; } return best; }
static bool tri_completable(u64 R,u64 B,int k){ for(size_t S=1;S<EM.size();S++){ if(SZ[S]!=3) continue; u64 es=EM[S]; if(es&B) continue; if(pc(es&~R)<=k) return true; } return false; }
static bool terminal_bob_wins(u64 R,u64 B){ if((R|B)!=FULL || (R&B)) { fprintf(stderr,"internal: terminal called on non-full board\n"); exit(2);} return TRI ? omega(R)<=2 : alpha(R)>omega(R); }
static bool bob_cutoff(u64 R,u64 B){ int kA=A-pc(R); return TRI ? !tri_completable(R,B,kA) : omega(B)>omega_budget(R,B,kA); }
static bool alice_cutoff(u64 R,u64 B){ return TRI ? omega(R)>=3 : omega(R)>=alpha(R); }

// canonical form: fills key (canonical layers), lab (lab[p] = vertex at canonical position p)
static void canon(u64 R,u64 B,u128& key,int* lab){
    const int nv=2*n, mm=SETWORDSNEEDED(nv);
    graph g[MAXN*MAXM], cg[MAXN*MAXM]; int ptn[MAXN], orbits[MAXN]; statsblk stats; DEFAULTOPTIONS_GRAPH(opt);
    opt.getcanon=TRUE; opt.defaultptn=FALSE;
    EMPTYGRAPH(g,mm,nv);
    for(int k=0;k<m;k++){ if(R>>k&1) ADDONEEDGE(g,ea[k],eb[k],mm); if(B>>k&1) ADDONEEDGE(g,n+ea[k],n+eb[k],mm); }
    for(int i=0;i<n;i++) ADDONEEDGE(g,i,n+i,mm);
    for(int i=0;i<nv;i++){ lab[i]=i; ptn[i]=1; } ptn[n-1]=0; ptn[nv-1]=0;
    densenauty(g,lab,ptn,orbits,&opt,&stats,mm,nv,cg);
    for(int p=0;p<n;p++) if(lab[p]>=n){ fprintf(stderr,"internal: nauty did not preserve the layer order\n"); exit(2); }
    // key = the canonical graph folded back into one coloured K_n: layer-0 positions carry the red edges; layer-1 positions
    // are mapped to layer-0 positions through the rungs (tau), and the blue edges are read in those coordinates. This is a
    // complete invariant (the folded graph IS the position); reading the two layers alone would drop the rung matching.
    u64 Rc=0,Bc=0; int tau[MAXN];
    for(int p=0;p<n;p++){ set* row=GRAPHROW(cg,p,mm); int cnt=0; for(int q=n;q<nv;q++) if(ISELEMENT(row,q)){ tau[q-n]=p; cnt++; } if(cnt!=1){ fprintf(stderr,"internal: rung count %d at position %d\n",cnt,p); exit(2);} }
    for(int p=0;p<n;p++){ set* row=GRAPHROW(cg,p,mm); for(int q=p+1;q<n;q++) if(ISELEMENT(row,q)) Rc|=1ULL<<eidx[p][q]; }
    for(int q1=0;q1<n;q1++){ set* row2=GRAPHROW(cg,n+q1,mm); for(int q2=q1+1;q2<n;q2++) if(ISELEMENT(row2,n+q2)) Bc|=1ULL<<eidx[tau[q1]][tau[q2]]; }
    key=((u128)Rc<<64)|Bc;
}

int main(int argc,char** argv){
    if(argc<2){ fprintf(stderr,"usage\n"); return 2; }
    std::string path=argv[1];
    for(int i=2;i<argc;i++){ std::string a=argv[i]; if(a=="--no-cutoff") NOCUT=true; else if(a=="--threads") NT=atoi(argv[++i]); }
    FILE* f=fopen(path.c_str(),"r"); if(!f){ printf("CANNOT SEE :: cannot open %s\n",path.c_str()); return 2; }
    char line[256]; if(!fgets(line,sizeof line,f) || line[0]!='#'){ printf("CANNOT SEE :: no header\n"); return 2; }
    std::string winner, mode; { char* t=strtok(line," \n"); while(t){ if(!strncmp(t,"n=",2)) n=atoi(t+2); else if(!strncmp(t,"mode=",5)) mode=t+5; else if(!strncmp(t,"winner=",7)) winner=t+7; else if(!strncmp(t,"aliceEdges=",11)) A=atoi(t+11); t=strtok(NULL," \n"); } }
    if(n<3||n>10||(mode!="clique"&&mode!="triangle")){ printf("CANNOT SEE :: bad header n=%d mode=%s\n",n,mode.c_str()); return 2; }
    if(winner!="bob"){ printf("CANNOT SEE :: this checker handles winner=bob certificates only (got %s)\n",winner.c_str()); return 2; }
    TRI=(mode=="triangle"); m=0; for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ eidx[i][j]=eidx[j][i]=m; ea[m]=i; eb[m]=j; m++; }
    if(A!=(m+2)/3){ printf("CANNOT SEE :: aliceEdges=%d but ceil(m/3)=%d\n",A,(m+2)/3); return 2; }
    FULL=(m==64)?~0ULL:((1ULL<<m)-1);
    EM.assign(1u<<n,0); SZ.assign(1u<<n,0);
    for(unsigned S=1;S<(1u<<n);S++){ SZ[S]=__builtin_popcount(S); u64 es=0; for(int i=0;i<n;i++) if(S>>i&1) for(int j=i+1;j<n;j++) if(S>>j&1) es|=1ULL<<eidx[i][j]; EM[S]=es; }
    omp_set_num_threads(NT);
    auto T0=std::chrono::steady_clock::now(); auto el=[&]{ return std::chrono::duration<double>(std::chrono::steady_clock::now()-T0).count(); };
    // ---- load certificate: canonical key -> Bob's reply in canonical coordinates
    std::unordered_map<u128,uint16_t,H128> table; table.reserve(1<<24);
    long long rows=0, dups=0, inconsistent=0; std::string err; 
    std::vector<u64> bufR,bufB; std::vector<int> bufe,buff; bufR.reserve(1<<20);
    auto flush=[&](){
        size_t N=bufR.size(); std::vector<u128> keys(N); std::vector<uint16_t> rep(N); std::vector<char> bad(N,0);
        #pragma omp parallel for schedule(dynamic,1024)
        for(size_t i=0;i<N;i++){ u64 R=bufR[i],B=bufB[i]; int e=bufe[i],fe=buff[i];
            if(e==fe||e<0||fe<0||e>=m||fe>=m||(R>>e&1)||(B>>e&1)||(R>>fe&1)||(B>>fe&1)||(R&B)||(R|B)&~FULL){ bad[i]=1; continue; }
            int lab[MAXN]; u128 key; canon(R,B,key,lab); int pos[MAXN]; for(int p=0;p<2*n;p++) pos[lab[p]]=p;
            int ec=eidx[pos[ea[e]]][pos[eb[e]]], fc=eidx[pos[ea[fe]]][pos[eb[fe]]]; if(ec>fc) std::swap(ec,fc);
            keys[i]=key; rep[i]=(uint16_t)(ec*64+fc); }
        for(size_t i=0;i<N;i++){ if(bad[i]){ if(err.empty()){ char b[160]; snprintf(b,sizeof b,"reply not free / malformed row at R=%llu B=%llu",(unsigned long long)bufR[i],(unsigned long long)bufB[i]); err=b; } continue; }
            auto it=table.find(keys[i]); if(it==table.end()) table.emplace(keys[i],rep[i]); else { dups++; if(it->second!=rep[i]) inconsistent++; } }
        bufR.clear(); bufB.clear(); bufe.clear(); buff.clear(); };
    while(fgets(line,sizeof line,f)){ if(line[0]=='#'||line[0]=='\n') continue; unsigned long long R,B; int e,fe; if(sscanf(line,"%llu %llu %d %d",&R,&B,&e,&fe)!=4){ printf("CANNOT SEE :: bad row: %s",line); return 2; }
        rows++; bufR.push_back(R); bufB.push_back(B); bufe.push_back(e); buff.push_back(fe); if(bufR.size()>=(1u<<10)) flush(); }
    flush(); fclose(f);
    if(!err.empty()){ printf("REJECT :: %s\n",err.c_str()); return 1; }
    fprintf(stderr,"[%.0fs] loaded %lld rows -> %zu canonical classes (%lld duplicate rows, %lld with a different reply; duplicates keep the first)\n",el(),rows,table.size(),dups,inconsistent);
    // ---- level-synchronous walk over Alice-to-move positions
    std::unordered_set<u128,H128> seen; seen.reserve(1<<24);
    std::vector<std::pair<u64,u64>> cur{{0,0}}; long long nodes=0,leaves=0,cutoffs=0; int level=0;
    while(!cur.empty()){
        size_t N=cur.size(); nodes+=N; 
        std::vector<std::pair<u64,u64>> nxt; size_t gen=0; long long lv=0,cf=0; std::string lerr; const size_t CH=7;
        for(size_t c0=0;c0<N && lerr.empty();c0+=CH){ size_t c1=std::min(N,c0+CH);
        std::vector<std::vector<std::pair<u128,std::pair<u64,u64>>>> loc(NT);
        #pragma omp parallel reduction(+:lv,cf)
        { int t=omp_get_thread_num(); auto& out=loc[t]; int lab[MAXN]; u128 key;
          #pragma omp for schedule(dynamic,256)
          for(size_t i=c0;i<c1;i++){ u64 R=cur[i].first,B=cur[i].second; u64 freeM=FULL&~(R|B);
            if(!freeM){ if(!terminal_bob_wins(R,B)){ 
                #pragma omp critical
                { if(lerr.empty()){ char b[160]; snprintf(b,sizeof b,"terminal lost at R=%llu B=%llu",(unsigned long long)R,(unsigned long long)B); lerr=b; } } }
                else lv++; continue; }
            if(!NOCUT){ if(alice_cutoff(R,B)){ 
                #pragma omp critical
                { if(lerr.empty()){ char b[160]; snprintf(b,sizeof b,"alice cutoff holds inside Bob's tree at R=%llu B=%llu",(unsigned long long)R,(unsigned long long)B); lerr=b; } } continue; }
                if(bob_cutoff(R,B)){ cf++; continue; } }
            for(int e=0;e<m;e++){ if(!(freeM>>e&1)) continue; u64 R2=R|(1ULL<<e); u64 free2=freeM&~(1ULL<<e);
                if(!free2){ if(!terminal_bob_wins(R2,B)){ 
                    #pragma omp critical
                    { if(lerr.empty()){ char b[160]; snprintf(b,sizeof b,"terminal lost at R=%llu B=%llu",(unsigned long long)R2,(unsigned long long)B); lerr=b; } } }
                    else lv++; continue; }
                if(!NOCUT && bob_cutoff(R2,B)){ cf++; continue; }
                canon(R2,B,key,lab); auto it=table.find(key);
                if(it==table.end()){ 
                    #pragma omp critical
                    { if(lerr.empty()){ char b[160]; snprintf(b,sizeof b,"no Bob reply recorded for R=%llu B=%llu",(unsigned long long)R2,(unsigned long long)B); lerr=b; } } continue; }
                int ec=it->second/64, fc=it->second%64;  // canonical edge indices -> current vertices via lab
                int a=eidx[lab[ea[ec]]][lab[eb[ec]]], b2=eidx[lab[ea[fc]]][lab[eb[fc]]];
                if(a==b2 || ((R2|B)>>a&1) || ((R2|B)>>b2&1)){ 
                    #pragma omp critical
                    { if(lerr.empty()){ char b[160]; snprintf(b,sizeof b,"transported reply not free at R=%llu B=%llu",(unsigned long long)R2,(unsigned long long)B); lerr=b; } } continue; }
                u64 B2 = (pc(free2)==1) ? (B|(1ULL<<a)) : (B|(1ULL<<a)|(1ULL<<b2));
                u128 key2; int lab2[MAXN]; canon(R2,B2,key2,lab2);
                out.push_back({key2,{R2,B2}}); } } }
        for(auto& v:loc){ gen+=v.size(); for(auto& x:v) if(seen.insert(x.first).second) nxt.push_back(x.second); std::vector<std::pair<u128,std::pair<u64,u64>>>().swap(v); }
        }
        leaves+=lv; cutoffs+=cf;
        if(!lerr.empty()){ printf("REJECT :: %s\n",lerr.c_str()); return 1; }
        std::vector<std::pair<u64,u64>>().swap(cur);
        fprintf(stderr,"[%.0fs] level %d (|R|=%d): %zu positions explored, %zu children generated, %zu new at level %d; leaves so far %lld, cutoffs %lld, seen %zu\n",el(),level,level,N,gen,nxt.size(),level+1,leaves,cutoffs,seen.size());
        cur.swap(nxt); level++; }
    printf("ACCEPT :: ACCEPT winner=bob n=%d mode=%s: %lld Alice-to-move positions explored, %lld terminal leaves, %lld cutoff leaves, %zu certificate entries (%lld rows, %lld duplicate rows) [check778c, nauty %s, threads %d, %.0f s]\n",n,mode.c_str(),nodes,leaves,cutoffs,table.size(),rows,dups,NAUTYVERSION,NT,el());
    return 0;
}
