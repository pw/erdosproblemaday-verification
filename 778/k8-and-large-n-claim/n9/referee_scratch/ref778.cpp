// ref778: independent reference solver for the (1:2) clique game on K_n (n<=7). No nauty: memo keyed by brute-force
// canonical form (lex-min over all n! vertex permutations). Own clique routine (recursive branch on adjacency bitmasks).
// No cutoffs: every line is played to the full board. Bob wins iff alpha(R) > omega(R) at the end.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
typedef unsigned __int128 u128; typedef uint64_t u64;
static int n, m, A; static int eidx[12][12]; static int ea[66], eb[66]; static u64 FULL; static bool TRI=false;
static std::vector<u64> EM; static std::vector<int> SZ;   // for the VERBATIM checker cutoffs only
#include "cutoffs_verbatim.inc"
// ---- own clique number
static int adjv[12];
static int mc_rec(int P,int sz){ if(!P) return sz; int best=sz; while(P){ if(sz+__builtin_popcount(P)<=best) break; int v=__builtin_ctz(P); P&=~(1<<v); int b=mc_rec(P&adjv[v],sz+1); if(b>best) best=b; } return best; }
static int myomega(u64 E){ for(int i=0;i<n;i++) adjv[i]=0; for(int k=0;k<m;k++) if(E>>k&1){ adjv[ea[k]]|=1<<eb[k]; adjv[eb[k]]|=1<<ea[k]; } return mc_rec((1<<n)-1,0); }
static bool myterminal(u64 R){ int w=myomega(R), a=myomega(FULL&~R); return a>w; }
// ---- brute canonical form
static std::vector<std::vector<u64>> lo, hi;
static inline u64 mapmask(int p,u64 x){ return lo[p][x&255] | hi[p][(x>>8)&255] | hi[p][256+((x>>16)&255)]; }
static u128 bcanon(u64 R,u64 B){ u128 best=~(u128)0; for(size_t p=0;p<lo.size();p++){ u128 v=((u128)mapmask(p,R)<<64)|mapmask(p,B); if(v<best) best=v; } return best; }
struct H{ size_t operator()(const u128&x)const{ u64 a=(u64)x,b=(u64)(x>>64); return a*0x9E3779B97F4A7C15ULL ^ (b+0x632BE59BD9B4E019ULL)*0xBF58476D1CE4E5B9ULL; } };
static std::unordered_map<u128,char,H> memoA, memoB, allA, allB, noneA, noneB;
static bool valB(u64 R,u64 B);
static bool valA(u64 R,u64 B){ // Alice to move; true iff Bob wins with optimal play
    u64 fr=FULL&~(R|B); if(!fr) return myterminal(R);
    u128 k=bcanon(R,B); auto it=memoA.find(k); if(it!=memoA.end()) return it->second;
    bool res=true; for(int e=0;e<m && res;e++) if(fr>>e&1){ u64 R2=R|(1ULL<<e); if(!(fr&~(1ULL<<e))) res=myterminal(R2); else res=valB(R2,B); }
    memoA[k]=res; return res; }
static bool valB(u64 R,u64 B){ // Bob to move
    u64 fr=FULL&~(R|B); if(!fr) return myterminal(R);
    u128 k=bcanon(R,B); auto it=memoB.find(k); if(it!=memoB.end()) return it->second;
    bool res=false; if(__builtin_popcountll(fr)==1) res=valA(R,B|fr); else
    for(int e=0;e<m && !res;e++) if(fr>>e&1) for(int f=e+1;f<m && !res;f++) if(fr>>f&1) res=valA(R,B|(1ULL<<e)|(1ULL<<f));
    memoB[k]=res; return res; }
// "always": Bob wins under ALL continuations; "none": Bob wins under NO continuation
static bool alwB(u64 R,u64 B); static bool nonB(u64 R,u64 B);
static bool alwA(u64 R,u64 B){ u64 fr=FULL&~(R|B); if(!fr) return myterminal(R); u128 k=bcanon(R,B); auto it=allA.find(k); if(it!=allA.end()) return it->second;
    bool res=true; for(int e=0;e<m&&res;e++) if(fr>>e&1){ u64 R2=R|(1ULL<<e); res = (fr&~(1ULL<<e))? alwB(R2,B) : myterminal(R2); } allA[k]=res; return res; }
static bool alwB(u64 R,u64 B){ u64 fr=FULL&~(R|B); if(!fr) return myterminal(R); u128 k=bcanon(R,B); auto it=allB.find(k); if(it!=allB.end()) return it->second;
    bool res=true; if(__builtin_popcountll(fr)==1) res=alwA(R,B|fr); else for(int e=0;e<m&&res;e++) if(fr>>e&1) for(int f=e+1;f<m&&res;f++) if(fr>>f&1) res=alwA(R,B|(1ULL<<e)|(1ULL<<f)); allB[k]=res; return res; }
static bool nonA(u64 R,u64 B){ u64 fr=FULL&~(R|B); if(!fr) return !myterminal(R); u128 k=bcanon(R,B); auto it=noneA.find(k); if(it!=noneA.end()) return it->second;
    bool res=true; for(int e=0;e<m&&res;e++) if(fr>>e&1){ u64 R2=R|(1ULL<<e); res = (fr&~(1ULL<<e))? nonB(R2,B) : !myterminal(R2); } noneA[k]=res; return res; }
static bool nonB(u64 R,u64 B){ u64 fr=FULL&~(R|B); if(!fr) return !myterminal(R); u128 k=bcanon(R,B); auto it=noneB.find(k); if(it!=noneB.end()) return it->second;
    bool res=true; if(__builtin_popcountll(fr)==1) res=nonA(R,B|fr); else for(int e=0;e<m&&res;e++) if(fr>>e&1) for(int f=e+1;f<m&&res;f++) if(fr>>f&1) res=nonA(R,B|(1ULL<<e)|(1ULL<<f)); noneB[k]=res; return res; }
// ---- strategy emission: rows "R B e f" at Bob-to-move positions, one per class; Bob plays first winning pair, else first pair
static std::unordered_set<u128,H> emittedB, visitedA; static FILE* OUT;
static void emitB(u64 R,u64 B);
static void emitA(u64 R,u64 B){ u64 fr=FULL&~(R|B); if(!fr) return; u128 k=bcanon(R,B); if(!visitedA.insert(k).second) return;
    for(int e=0;e<m;e++) if(fr>>e&1){ u64 R2=R|(1ULL<<e); if(fr&~(1ULL<<e)) emitB(R2,B); } }
static void emitB(u64 R,u64 B){ u64 fr=FULL&~(R|B); u128 k=bcanon(R,B); if(!emittedB.insert(k).second) return;
    if(__builtin_popcountll(fr)==1){ fprintf(stderr,"single free edge for Bob (m=2 mod 3?)\n"); exit(3); }
    int be=-1,bf=-1; for(int e=0;e<m && be<0;e++) if(fr>>e&1) for(int f=e+1;f<m;f++) if(fr>>f&1){ if(valA(R,B|(1ULL<<e)|(1ULL<<f))){ be=e; bf=f; break; } }
    if(be<0){ for(int e=0;e<m && be<0;e++) if(fr>>e&1) for(int f=e+1;f<m;f++) if(fr>>f&1){ be=e; bf=f; break; } }
    fprintf(OUT,"%llu %llu %d %d\n",(unsigned long long)R,(unsigned long long)B,be,bf);
    emitA(R,B|(1ULL<<be)|(1ULL<<bf)); }
static void setup(int nn){ n=nn; m=0; for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ eidx[i][j]=eidx[j][i]=m; ea[m]=i; eb[m]=j; m++; }
    A=(m+2)/3; FULL=(1ULL<<m)-1; EM.assign(1u<<n,0); SZ.assign(1u<<n,0);
    for(unsigned S=1;S<(1u<<n);S++){ SZ[S]=__builtin_popcount(S); u64 es=0; for(int i=0;i<n;i++) if(S>>i&1) for(int j=i+1;j<n;j++) if(S>>j&1) es|=1ULL<<eidx[i][j]; EM[S]=es; }
    std::vector<int> pp(n); for(int i=0;i<n;i++) pp[i]=i;
    do{ std::vector<int> em(m); for(int k=0;k<m;k++) em[k]=eidx[pp[ea[k]]][pp[eb[k]]]; std::vector<u64> L(256,0),Hh(512,0);
        for(int x=0;x<256;x++) for(int b=0;b<8;b++) if(x>>b&1){ if(b<m) L[x]|=1ULL<<em[b]; if(8+b<m) Hh[x]|=1ULL<<em[8+b]; if(16+b<m) Hh[256+x]|=1ULL<<em[16+b]; }
        lo.push_back(L); hi.push_back(Hh); } while(std::next_permutation(pp.begin(),pp.end())); }
int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: ref778 n solve|cutcheck|cert <out>|lose <R> <B> <e> <f> <out>|val <R> <B> A|B\n"); return 2; }
    setup(atoi(argv[1])); std::string cmd=argv[2];
    if(cmd=="solve"){ bool v=valA(0,0); printf("n=%d m=%d A=%d: %s wins (classes A=%zu B=%zu)\n",n,m,A,v?"BOB":"ALICE",memoA.size(),memoB.size()); return 0; }
    if(cmd=="val"){ u64 R=strtoull(argv[3],0,10),B=strtoull(argv[4],0,10); bool v= argv[5][0]=='A'? valA(R,B):valB(R,B); printf("%d\n",v); return 0; }
    if(cmd=="cert"){ OUT=fopen(argv[3],"w"); fprintf(OUT,"# erdos778 certificate n=%d mode=clique winner=bob aliceEdges=%d edges=%d edgeorder=lex(i<j) [ref778, no cutoffs]\n",n,A,m);
        if(!valA(0,0)){ fprintf(stderr,"Bob does not win; emitting a (losing) complete strategy anyway\n"); }
        emitA(0,0); fclose(OUT); fprintf(stderr,"rows=%zu\n",emittedB.size()); return 0; }
    if(cmd=="lose"){ // emit losing row for Bob-to-move (R,B) with reply e,f, then a COMPLETE strategy for the subtree
        u64 R=strtoull(argv[3],0,10),B=strtoull(argv[4],0,10); int e=atoi(argv[5]),f=atoi(argv[6]); OUT=fopen(argv[7],"w");
        u64 B2=B|(1ULL<<e)|(1ULL<<f); fprintf(stderr,"valB(pos)=%d  valA(after losing reply)=%d  nonA(after)=%d\n",valB(R,B),valA(R,B2),nonA(R,B2));
        fprintf(OUT,"%llu %llu %d %d\n",(unsigned long long)R,(unsigned long long)B,e,f); emittedB.insert(bcanon(R,B)); emitA(R,B2); fclose(OUT);
        fprintf(stderr,"subtree rows=%zu\n",emittedB.size()); return 0; }
    if(cmd=="findlose"){ // for each row of a cert at |R|>=minR, list replies that LOSE (exact), with cutoff status after the reply
        FILE* f=fopen(argv[3],"r"); int minR=atoi(argv[4]); char line[256]; int shown=0;
        while(fgets(line,sizeof line,f)){ if(line[0]=='#') continue; unsigned long long R,B; int e,ff; if(sscanf(line,"%llu %llu %d %d",&R,&B,&e,&ff)!=4) continue;
            if(__builtin_popcountll(R)!=minR) continue; u64 fr=FULL&~(R|B);
            for(int x=0;x<m;x++) if(fr>>x&1) for(int y=x+1;y<m;y++) if(fr>>y&1){ u64 B2=B|(1ULL<<x)|(1ULL<<y); if(!(FULL&~(R|B2))) continue;
                if(!valA(R,B2)){ printf("%llu %llu %d %d  |R|=%d recorded=(%d,%d) alicecut_after=%d bobcut_after=%d never=%d\n",R,B,x,y,__builtin_popcountll(R),e,ff,(int)alice_cutoff(R,B2),(int)bob_cutoff(R,B2),(int)nonA(R,B2)); if(++shown>=(argc>5?atoi(argv[5]):40)) return 0; } } }
        return 0; }
    if(cmd=="cutcheck"){ // all game-shaped positions: checker's cutoffs vs exact values
        long long nA=0,nB=0, bcA=0,bcB=0, acA=0,acB=0, badBC=0,badBCall=0, badAC=0,badACall=0;
        for(u64 R=0;R<=FULL;R++){ int r=__builtin_popcountll(R); if(r>A) continue; u64 comp=FULL&~R; std::vector<int> idx; for(int k=0;k<m;k++) if(comp>>k&1) idx.push_back(k); int fsz=idx.size();
            for(int which=0;which<2;which++){ int s = which==0? 2*r : 2*r-2; if(s<0||s>fsz) continue; if(which==1 && r==0) continue;
                // which==0: Alice to move (|B|=2|R|), which==1: Bob to move (|B|=2|R|-2)
                u64 c=(s==0)?0:((1ULL<<s)-1);
                while(true){ u64 B=0; for(int t=0;t<fsz;t++) if(c>>t&1) B|=1ULL<<idx[t];
                    u64 fr=FULL&~(R|B);
                    if(fr){ bool v = which==0? valA(R,B):valB(R,B); bool al = which==0? alwA(R,B):alwB(R,B); bool no = which==0? nonA(R,B):nonB(R,B);
                        (which==0?nA:nB)++;
                        if(bob_cutoff(R,B)){ (which==0?bcA:bcB)++; if(!v) badBC++; if(!al) badBCall++; }
                        if(alice_cutoff(R,B)){ (which==0?acA:acB)++; if(v) badAC++; if(!no) badACall++; } }
                    if(s==0) break; u64 lo1=c&-c, r1=c+lo1; c=(((r1^c)>>2)/lo1)|r1; if(c>=(1ULL<<fsz)) break; } } }
        printf("n=%d: Alice-to-move %lld (bobcut %lld, alicecut %lld), Bob-to-move %lld (bobcut %lld, alicecut %lld)\n",n,nA,bcA,acA,nB,bcB,acB);
        printf("  bob_cutoff but Bob does NOT win (optimal): %lld | bob_cutoff but NOT always-Bob: %lld\n",badBC,badBCall);
        printf("  alice_cutoff but Bob wins (optimal):       %lld | alice_cutoff but NOT never-Bob: %lld\n",badAC,badACall);
        return (badBC||badBCall||badAC||badACall)?1:0; }
    return 2; }
