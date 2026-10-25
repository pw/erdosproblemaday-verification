#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

constexpr int n = 7;
constexpr int universe = 1 << n;

bool union_closed(const std::vector<int>& family) {
  std::array<bool, universe> present{};
  for (int a : family) present[a] = true;
  for (int a : family)
    for (int b : family)
      if (!present[a | b]) return false;
  return true;
}

void audit_cnf(const std::string& path) {
  std::ifstream in(path);
  if (!in) throw std::runtime_error("cannot open CNF");

  bool saw_header = false;
  int declared_vars = -1, declared_clauses = -1, clauses = 0;
  int red = 0, blue = 0;
  std::unordered_set<std::string> canonical;
  std::string line;
  while (std::getline(in, line)) {
    if (line.empty() || line[0] == 'c') continue;
    if (!saw_header) {
      std::istringstream hs(line);
      std::string p, cnf, trailing;
      if (!(hs >> p >> cnf >> declared_vars >> declared_clauses) ||
          p != "p" || cnf != "cnf" || (hs >> trailing))
        throw std::runtime_error("bad DIMACS header");
      saw_header = true;
      continue;
    }

    std::istringstream ls(line);
    std::vector<int> lits;
    int lit;
    bool ended = false;
    while (ls >> lit) {
      if (ended) throw std::runtime_error("tokens after clause terminator");
      if (lit == 0) ended = true;
      else lits.push_back(lit);
    }
    if (!ended) throw std::runtime_error("unterminated clause");
    ++clauses;
    if (clauses == 1) {
      if (lits != std::vector<int>{-1})
        throw std::runtime_error("symmetry unit is not -1");
      continue;
    }
    if (lits.size() != 7) throw std::runtime_error("non-seven family clause");
    const bool negative = lits.front() < 0;
    std::vector<int> family;
    for (int x : lits) {
      if ((x < 0) != negative || x == 0 || std::abs(x) > universe)
        throw std::runtime_error("bad literal or mixed signs");
      family.push_back(std::abs(x) - 1);
    }
    std::sort(family.begin(), family.end());
    if (std::adjacent_find(family.begin(), family.end()) != family.end())
      throw std::runtime_error("repeated mask in family");
    if (!union_closed(family))
      throw std::runtime_error("family clause is not union-closed");

    std::string key(1, negative ? 'R' : 'B');
    for (int a : family) key.push_back(static_cast<char>(a));
    if (!canonical.insert(key).second)
      throw std::runtime_error("duplicate signed family clause");
    (negative ? red : blue)++;
  }
  if (!saw_header || declared_vars != universe || declared_clauses != clauses ||
      clauses != 42035 || red != 22232 || blue != 19802 ||
      canonical.size() != 42034)
    throw std::runtime_error("CNF counts mismatch");

  std::cout << "CNF semantics: " << clauses << " clauses, " << red
            << " red forbidders, " << blue << " blue forbidders PASS\n";
}

struct Search {
  std::array<bool, universe> colour{};
  bool meets = false;
  int best = 0;
  std::vector<int> witness;

  // state: -2 is the other colour, -1 excluded, 0 undecided, 1 selected.
  bool saturate(std::array<int8_t, universe>& state) const {
    bool changed = true;
    while (changed) {
      changed = false;
      std::vector<int> chosen;
      for (int a = 0; a < universe; ++a)
        if (state[a] == 1) chosen.push_back(a);
      for (std::size_t i = 0; i < chosen.size(); ++i) {
        for (std::size_t j = i; j < chosen.size(); ++j) {
          const int results[2] = {chosen[i] | chosen[j], chosen[i] & chosen[j]};
          const int count = meets ? 2 : 1;
          for (int k = 0; k < count; ++k) {
            const int q = results[k];
            if (!colour[q] || state[q] < 0) return false;
            if (state[q] == 0) {
              state[q] = 1;
              changed = true;
            }
          }
        }
      }
    }
    return true;
  }

  void dfs(std::array<int8_t, universe> state) {
    if (!saturate(state)) return;
    int selected = 0, undecided = 0;
    std::vector<int> now;
    for (int a = 0; a < universe; ++a) {
      selected += state[a] == 1;
      undecided += state[a] == 0;
      if (state[a] == 1) now.push_back(a);
    }
    if (selected > best) {
      best = selected;
      witness = std::move(now);
    }
    if (selected + undecided <= best) return;

    int branch = -1, branch_score = -1;
    for (int x = 0; x < universe; ++x) if (state[x] == 0) {
      std::array<bool, universe> new_result{};
      int score = 0;
      for (int y = 0; y < universe; ++y) if (state[y] == 1) {
        const int results[2] = {x | y, x & y};
        const int count = meets ? 2 : 1;
        for (int k = 0; k < count; ++k) {
          const int q = results[k];
          if (!colour[q] || state[q] == -1) score += 100;
          else if (state[q] == 0 && !new_result[q]) {
            new_result[q] = true;
            ++score;
          }
        }
      }
      if (score > branch_score) {
        branch_score = score;
        branch = x;
      }
    }
    if (branch < 0) return;
    auto include = state;
    include[branch] = 1;
    dfs(include);
    state[branch] = -1;
    dfs(state);
  }

  int run() {
    std::array<int8_t, universe> state{};
    for (int a = 0; a < universe; ++a) state[a] = colour[a] ? 0 : -2;
    dfs(state);
    return best;
  }
};

std::array<bool, universe> rank_colour(std::initializer_list<int> ranks) {
  std::array<bool, universe> result{};
  for (int a = 0; a < universe; ++a)
    result[a] = std::find(ranks.begin(), ranks.end(), __builtin_popcount(a)) != ranks.end();
  return result;
}

bool closure_stays(const std::array<bool, universe>& colour,
                   const std::array<int, 5>& seeds) {
  std::array<bool, universe> in{};
  std::vector<int> work(seeds.begin(), seeds.end());
  for (int a : work) in[a] = true;
  for (std::size_t cursor = 0; cursor < work.size(); ++cursor) {
    const int a = work[cursor];
    for (std::size_t j = 0; j < work.size(); ++j) {
      const int results[2] = {a | work[j], a & work[j]};
      for (int q : results) {
        if (!colour[q]) return false;
        if (!in[q]) {
          in[q] = true;
          work.push_back(q);
        }
      }
    }
  }
  return true;
}

void choose_five(const std::vector<int>& members, int at, int used,
                 std::array<int, 5>& seeds,
                 const std::array<bool, universe>& colour,
                 std::uint64_t& total, std::uint64_t& survivors) {
  if (used == 5) {
    ++total;
    survivors += closure_stays(colour, seeds);
    return;
  }
  const int need = 5 - used;
  for (int i = at; i <= static_cast<int>(members.size()) - need; ++i) {
    seeds[used] = members[i];
    choose_five(members, i + 1, used + 1, seeds, colour, total, survivors);
  }
}

void audit_five_seeds(const std::array<bool, universe>& red) {
  for (int want = 0; want <= 1; ++want) {
    std::vector<int> members;
    for (int a = 0; a < universe; ++a)
      if (red[a] == static_cast<bool>(want)) members.push_back(a);
    std::array<int, 5> seeds{};
    std::uint64_t total = 0, survivors = 0;
    auto colour = red;
    if (!want) for (int a = 0; a < universe; ++a) colour[a] = !colour[a];
    choose_five(members, 0, 0, seeds, colour, total, survivors);
    const std::uint64_t expected = want ? 21111090ULL : 2118760ULL;
    if (total != expected || survivors != 0)
      throw std::runtime_error("five-seed audit mismatch");
    std::cout << (want ? "red" : "blue") << " lattice five-seeds: "
              << total << ", monochromatic closures " << survivors << "\n";
  }
}

void assert_closed_witness(const std::array<bool, universe>& colour,
                           const std::vector<int>& family, bool meets) {
  std::array<bool, universe> present{};
  for (int a : family) {
    if (!colour[a]) throw std::runtime_error("wrong-colour witness member");
    present[a] = true;
  }
  for (int a : family) for (int b : family) {
    if (!present[a | b] || (meets && !present[a & b]))
      throw std::runtime_error("unclosed witness");
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: hostile_audit lower_core.cnf\n";
    return 2;
  }
  audit_cnf(argv[1]);

  const auto union_red = rank_colour({3, 4, 6});
  auto union_blue = union_red;
  for (bool& x : union_blue) x = !x;
  Search ur{union_red, false, 0, {}}, ub{union_blue, false, 0, {}};
  const int ur_max = ur.run(), ub_max = ub.run();
  if (ur_max != 6 || ub_max != 7)
    throw std::runtime_error("union exact maxima mismatch");
  assert_closed_witness(union_red, {7, 11, 13, 14, 15, 63}, false);
  assert_closed_witness(union_blue, {0, 1, 2, 3, 31, 103, 127}, false);
  std::cout << "independent union DFS maxima: red " << ur_max << ", blue "
            << ub_max << " PASS\n";

  const auto lattice_red = rank_colour({0, 2, 3, 5});
  auto lattice_blue = lattice_red;
  for (bool& x : lattice_blue) x = !x;
  Search lr{lattice_red, true, 0, {}}, lb{lattice_blue, true, 0, {}};
  const int lr_max = lr.run(), lb_max = lb.run();
  if (lr_max != 4 || lb_max != 4)
    throw std::runtime_error("lattice exact maxima mismatch");
  assert_closed_witness(lattice_red, {0, 3, 7, 31}, true);
  assert_closed_witness(lattice_blue, {1, 15, 63, 127}, true);
  std::cout << "independent lattice DFS maxima: red " << lr_max << ", blue "
            << lb_max << " PASS\n";

  audit_five_seeds(lattice_red);
  std::cout << "HOSTILE AUDIT PASS\n";
}
