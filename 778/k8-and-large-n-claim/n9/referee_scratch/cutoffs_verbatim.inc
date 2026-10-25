static inline int pc(u64 x){ return __builtin_popcountll(x); }
static int omega(u64 mask){ int best=1; for(size_t S=1;S<EM.size();S++) if(SZ[S]>best && (EM[S] & ~mask)==0) best=SZ[S]; return best; }
static int alpha(u64 R){ return omega(FULL & ~R); }
static int omega_budget(u64 R,u64 B,int k){ int best=1; for(size_t S=1;S<EM.size();S++){ if(SZ[S]<=best) continue; u64 es=EM[S]; if(es&B) continue; if(pc(es & ~R)<=k) best=SZ[S]; } return best; }
static bool tri_completable(u64 R,u64 B,int k){ for(size_t S=1;S<EM.size();S++){ if(SZ[S]!=3) continue; u64 es=EM[S]; if(es&B) continue; if(pc(es&~R)<=k) return true; } return false; }
static bool terminal_bob_wins(u64 R,u64 B){ if((R|B)!=FULL || (R&B)) { fprintf(stderr,"internal: terminal called on non-full board\n"); exit(2);} return TRI ? omega(R)<=2 : alpha(R)>omega(R); }
static bool bob_cutoff(u64 R,u64 B){ int kA=A-pc(R); return TRI ? !tri_completable(R,B,kA) : omega(B)>omega_budget(R,B,kA); }
static bool alice_cutoff(u64 R,u64 B){ return TRI ? omega(R)>=3 : omega(R)>=alpha(R); }
