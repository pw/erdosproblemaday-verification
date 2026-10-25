#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <tuple>
#include <vector>

using namespace std;

static constexpr int N = 21;

struct Constraint {
  array<int, 4> v{};
  array<int, 6> pairs{};
  int nv = 0;
  int np = 0;
  bool bad = false;
  int weight = 1;
};

struct Search {
  mt19937_64 rng;
  int mat[N][N]{};             // 0 absent, +1 row -> column, -1 reverse
  int pair_id[N][N]{};
  vector<pair<int,int>> endpoints;
  vector<Constraint> constraints;
  vector<vector<int>> affected;
  vector<int> bad_list, bad_pos;
  vector<long long> tabu_until;
  vector<int> best_state;
  int best_cost = 1e9;
  long long step = 0;

  explicit Search(uint64_t seed) : rng(seed) { build_constraints(); }

  void build_constraints() {
    for (int u = 0; u < N; ++u) for (int v = u + 1; v < N; ++v) {
      int id = (int) endpoints.size();
      pair_id[u][v] = pair_id[v][u] = id;
      endpoints.push_back({u,v});
    }
    affected.resize(endpoints.size());
    tabu_until.assign(endpoints.size(), 0);
    for (int a = 0; a < N; ++a) for (int b = a + 1; b < N; ++b)
      for (int c = b + 1; c < N; ++c) {
        Constraint q; q.nv=3; q.np=3; q.v={a,b,c,0};
        q.pairs={pair_id[a][b],pair_id[a][c],pair_id[b][c],0,0,0};
        int id=constraints.size(); constraints.push_back(q);
        for(int k=0;k<3;++k) affected[q.pairs[k]].push_back(id);
      }
    for (int a = 0; a < N; ++a) for (int b = a + 1; b < N; ++b)
      for (int c = b + 1; c < N; ++c) for (int d = c + 1; d < N; ++d) {
        Constraint q; q.nv=4; q.np=6; q.v={a,b,c,d};
        int vs[4]={a,b,c,d}, at=0;
        for(int i=0;i<4;++i) for(int j=i+1;j<4;++j)
          q.pairs[at++]=pair_id[vs[i]][vs[j]];
        int id=constraints.size(); constraints.push_back(q);
        for(int k=0;k<6;++k) affected[q.pairs[k]].push_back(id);
      }
    bad_pos.assign(constraints.size(), -1);
  }

  bool violation(const Constraint &q) const {
    if (q.nv == 3) {
      int a=q.v[0], b=q.v[1], c=q.v[2];
      return mat[a][b]==0 && mat[a][c]==0 && mat[b][c]==0;
    }
    int deg[4]={0,0,0,0};
    for(int i=0;i<4;++i) for(int j=i+1;j<4;++j) {
      int s=mat[q.v[i]][q.v[j]];
      if(!s) return false;
      if(s==1) ++deg[i]; else ++deg[j];
    }
    sort(deg,deg+4);
    return deg[0]==0 && deg[1]==1 && deg[2]==2 && deg[3]==3;
  }

  void add_bad(int cid) {
    if(bad_pos[cid]>=0) return;
    bad_pos[cid]=bad_list.size(); bad_list.push_back(cid);
  }
  void remove_bad(int cid) {
    int p=bad_pos[cid]; if(p<0) return;
    int last=bad_list.back(); bad_list[p]=last; bad_pos[last]=p;
    bad_list.pop_back(); bad_pos[cid]=-1;
  }
  void rebuild_bad() {
    bad_list.clear(); fill(bad_pos.begin(),bad_pos.end(),-1);
    for(int i=0;i<(int)constraints.size();++i) {
      constraints[i].bad=violation(constraints[i]);
      if(constraints[i].bad) add_bad(i);
    }
    if((int)bad_list.size()<best_cost) {
      best_cost=bad_list.size(); best_state.clear();
      for(auto [u,v]:endpoints) best_state.push_back(mat[u][v]);
      cerr << "best=" << best_cost << " step=" << step << "\n";
    }
  }

  void set_pair(int pid, int state) {
    auto [u,v]=endpoints[pid]; mat[u][v]=state; mat[v][u]=-state;
  }

  int affected_bad_count(int pid) const {
    int result=0;
    for(int cid:affected[pid])
      if(violation(constraints[cid])) result += constraints[cid].weight;
    return result;
  }

  int degree_penalty(int v) const {
    int out=0,in=0,non=0;
    for(int u=0;u<N;++u) if(u!=v) {
      if(mat[v][u]==1) ++out;
      else if(mat[v][u]==-1) ++in;
      else ++non;
    }
    return max(0,out-8)+max(0,in-8)+max(0,non-7);
  }

  void commit(int pid, int state) {
    vector<char> old; old.reserve(affected[pid].size());
    for(int cid:affected[pid]) old.push_back(constraints[cid].bad);
    set_pair(pid,state);
    for(int k=0;k<(int)affected[pid].size();++k) {
      int cid=affected[pid][k]; bool now=violation(constraints[cid]);
      if(now!=old[k]) { if(now) add_bad(cid); else remove_bad(cid); }
      constraints[cid].bad=now;
    }
  }

  bool underlying_edge(int u,int v) const { return mat[u][v]!=0; }

  vector<int> find_clique(int wanted) {
    vector<int> chosen;
    for(int mask=0;mask<(1<<20);++mask) {
      if(__builtin_popcount((unsigned)mask)!=wanted) continue;
      bool ok=true;
      for(int i=0;i<20&&ok;++i) if(mask&(1<<i))
        for(int j=i+1;j<20;++j) if((mask&(1<<j))&&!underlying_edge(i+1,j+1)) {ok=false;break;}
      if(ok) { for(int i=0;i<20;++i) if(mask&(1<<i)) chosen.push_back(i+1); return chosen; }
    }
    return {};
  }

  void initialize(int out_size,int in_size,int non_size,int restart) {
    memset(mat,0,sizeof(mat));
    if(restart%2==1) {
      // Diverse start: greedily build a triangle-free nonedge graph of
      // maximum degree seven, then orient every complementary edge randomly.
      for(int v=1;v<N;++v) set_pair(pair_id[0][v], v<=out_size ? 1 : (v<=out_size+in_size ? -1 : 0));
      vector<int> internal;
      for(int id=0;id<(int)endpoints.size();++id) if(endpoints[id].first!=0) {
        internal.push_back(id); set_pair(id,(rng()&1)?1:-1);
      }
      vector<int> nondeg(N,0);
      for(int v=1;v<N;++v) if(mat[0][v]==0) ++nondeg[0],++nondeg[v];
      for(int round=0;round<5;++round) {
        shuffle(internal.begin(),internal.end(),rng);
        for(int id:internal) {
          auto [u,v]=endpoints[id];
          if(mat[u][v]==0 || nondeg[u]>=7 || nondeg[v]>=7) continue;
          bool triangle=false;
          for(int w=0;w<N;++w) if(w!=u&&w!=v&&mat[u][w]==0&&mat[v][w]==0) {triangle=true;break;}
          if(!triangle && (rng()%100)<75) set_pair(id,0),++nondeg[u],++nondeg[v];
        }
      }
      fill(tabu_until.begin(),tabu_until.end(),0);
      for(auto &q:constraints) q.weight=1;
      rebuild_bad();
      return;
    }
    static const vector<vector<int>> sets={
      {1,2,4,14,15,17},{1,2,6,12,13,15},
      {2,3,5,6,11,12},{2,4,5,7,11,14}
    };
    auto C=sets[restart%sets.size()];
    // Put a randomly relabelled cyclic order-20 witness on vertices 1..20.
    vector<int> label(20); iota(label.begin(),label.end(),1); shuffle(label.begin(),label.end(),rng);
    for(int i=0;i<20;++i) for(int j=i+1;j<20;++j) {
      int d=(j-i)%20, s=0;
      if(find(C.begin(),C.end(),d)!=C.end()) s=1;
      else if(find(C.begin(),C.end(),(20-d)%20)!=C.end()) s=-1;
      int u=label[i],v=label[j];
      if(u<v) set_pair(pair_id[u][v],s); else set_pair(pair_id[u][v],-s);
    }
    vector<int> non=find_clique(non_size);
    if(non.empty()) { cerr<<"no clique initialization\n"; exit(2); }
    vector<int> remaining;
    for(int v=1;v<N;++v) if(find(non.begin(),non.end(),v)==non.end()) remaining.push_back(v);
    shuffle(remaining.begin(),remaining.end(),rng);
    for(int v:non) set_pair(pair_id[0][v],0);
    for(int k=0;k<out_size;++k) set_pair(pair_id[0][remaining[k]],1);
    for(int k=out_size;k<out_size+in_size;++k) set_pair(pair_id[0][remaining[k]],-1);
    fill(tabu_until.begin(),tabu_until.end(),0);
    for(auto &q:constraints) q.weight=1;
    rebuild_bad();
  }

  bool run_profile(int out_size,int in_size,int non_size,int restarts,int steps_per_restart) {
    uniform_real_distribution<double> real01(0.0,1.0);
    for(int restart=0;restart<restarts;++restart) {
      initialize(out_size,in_size,non_size,restart);
      for(int local=0;local<steps_per_restart;++local,++step) {
        if(bad_list.empty()) return true;
        int cid=bad_list[rng()%bad_list.size()];
        const auto &q=constraints[cid];
        auto make_moves = [&]() {
          vector<tuple<int,int,int>> result;
          for(int k=0;k<q.np;++k) {
            int pid=q.pairs[k]; auto [u,v]=endpoints[pid];
            if(u==0) continue; // root profile remains canonical
            int old=mat[u][v];
            int old_count=affected_bad_count(pid)+8*(degree_penalty(u)+degree_penalty(v));
            for(int state=-1;state<=1;++state) if(state!=old) {
              set_pair(pid,state);
              int delta=affected_bad_count(pid)+8*(degree_penalty(u)+degree_penalty(v))-old_count;
              set_pair(pid,old);
              result.push_back({delta,pid,state});
            }
          }
          return result;
        };
        auto moves=make_moves();
        if(moves.empty()) { cerr<<"fixed-only violated constraint\n"; return false; }
        int chosen=-1;
        if(real01(rng)<0.025) chosen=rng()%moves.size();
        else {
          int best=1e9;
          vector<int> ties;
          for(int i=0;i<(int)moves.size();++i) {
            auto [delta,pid,state]=moves[i];
            bool tabu=tabu_until[pid]>step;
            if(tabu && (int)bad_list.size()+delta>0) continue;
            if(delta<best) {best=delta;ties={i};}
            else if(delta==best) ties.push_back(i);
          }
          if(best>=0) {
            // Breakout: persistent violated constraints gain weight, allowing
            // temporary increases in their unweighted count to escape a
            // one-obstruction local minimum.
            for(int bad:bad_list) ++constraints[bad].weight;
            moves=make_moves(); best=1e9; ties.clear();
            for(int i=0;i<(int)moves.size();++i) {
              auto [delta,pid,state]=moves[i];
              bool tabu=tabu_until[pid]>step;
              if(tabu && (int)bad_list.size()+delta>0) continue;
              if(delta<best) {best=delta;ties={i};}
              else if(delta==best) ties.push_back(i);
            }
          }
          if(ties.empty()) chosen=rng()%moves.size(); else chosen=ties[rng()%ties.size()];
        }
        auto [delta,pid,state]=moves[chosen];
        commit(pid,state); tabu_until[pid]=step+5+(rng()%7);
        if((int)bad_list.size()<best_cost) {
          best_cost=bad_list.size(); best_state.clear();
          for(auto [u,v]:endpoints) best_state.push_back(mat[u][v]);
          cerr << "best=" << best_cost << " profile="<<out_size<<","<<in_size<<","<<non_size
               << " restart="<<restart<<" step="<<step<<"\n";
        }
      }
    }
    return false;
  }

  void print_graph() const {
    cout << "STATES ";
    for(auto [u,v]:endpoints) cout << (mat[u][v]==0?'0':(mat[u][v]==1?'+':'-'));
    cout << "\n";
    cout << "ARCS";
    for(int id=0;id<(int)endpoints.size();++id) {
      auto [u,v]=endpoints[id]; int s=mat[u][v];
      if(s==1) cout<<" "<<u<<">"<<v;
      else if(s==-1) cout<<" "<<v<<">"<<u;
    }
    cout<<"\nNONEDGES";
    for(auto [u,v]:endpoints) if(mat[u][v]==0) cout<<" "<<u<<"~"<<v;
    cout<<"\n";
  }

  void restore_best() {
    if(best_state.size()!=endpoints.size()) return;
    for(int id=0;id<(int)endpoints.size();++id) set_pair(id,best_state[id]);
    rebuild_bad();
  }
};

int main(int argc,char **argv) {
  if(argc<5) { cerr<<"usage: local out in non seed [restarts] [steps]\n"; return 2; }
  int o=stoi(argv[1]),i=stoi(argv[2]),z=stoi(argv[3]); uint64_t seed=stoull(argv[4]);
  int restarts=argc>5?stoi(argv[5]):100, steps=argc>6?stoi(argv[6]):200000;
  Search search(seed);
  bool sat=search.run_profile(o,i,z,restarts,steps);
  cerr<<"DONE status="<<(sat?"SAT":"UNKNOWN")<<" best="<<search.best_cost<<" steps="<<search.step<<"\n";
  if(!sat) search.restore_best();
  search.print_graph();
  return sat?0:1;
}
