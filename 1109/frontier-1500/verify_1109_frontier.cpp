#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

namespace {

constexpr int kMaxVertices = 2048;
constexpr int kWords = kMaxVertices / 64;

struct Bits {
  std::array<std::uint64_t, kWords> word{};

  void set(int index) { word[index / 64] |= std::uint64_t{1} << (index % 64); }
  void reset(int index) { word[index / 64] &= ~(std::uint64_t{1} << (index % 64)); }
  bool test(int index) const { return word[index / 64] & (std::uint64_t{1} << (index % 64)); }

  bool any(int words_used) const {
    for (int i = 0; i < words_used; ++i) {
      if (word[i]) return true;
    }
    return false;
  }

  int count(int words_used) const {
    int result = 0;
    for (int i = 0; i < words_used; ++i) result += std::popcount(word[i]);
    return result;
  }

  int first(int words_used) const {
    for (int i = 0; i < words_used; ++i) {
      if (word[i]) return 64 * i + std::countr_zero(word[i]);
    }
    return -1;
  }

  void intersect(const Bits& other, int words_used) {
    for (int i = 0; i < words_used; ++i) word[i] &= other.word[i];
  }

  void remove_neighbors(const Bits& adjacency, int words_used) {
    for (int i = 0; i < words_used; ++i) word[i] &= ~adjacency.word[i];
  }
};

const std::array<int, 39> kPublishedTransitions = {
    1, 5, 19, 23, 37, 41, 59, 87, 101, 105, 113, 131, 151,
    159, 167, 195, 203, 239, 259, 303, 307, 403, 451, 499,
    517, 553, 573, 609, 645, 701, 719, 787, 807, 827, 889,
    1003, 1055, 1067, 1103,
};

class CliqueDecision {
 public:
  CliqueDecision(const std::array<Bits, kMaxVertices>& adjacency,
                 int vertex_count, int target)
      : adjacency_(adjacency),
        words_used_((vertex_count + 63) / 64),
        target_(target) {}

  bool Run(Bits candidates) {
    chosen_.clear();
    witness_.clear();
    nodes_ = 0;
    return Search(candidates);
  }

  std::uint64_t nodes() const { return nodes_; }
  const std::vector<int>& witness() const { return witness_; }

 private:
  bool Search(Bits pool) {
    ++nodes_;
    const int chosen_size = static_cast<int>(chosen_.size());
    if (chosen_size == target_) {
      witness_ = chosen_;
      return true;
    }
    if (chosen_size + pool.count(words_used_) < target_) return false;

    // Partition the pool greedily into independent color classes. A clique
    // uses at most one vertex from each class, so each prefix color is an
    // exact upper bound for the reverse branch scan below.
    Bits remaining = pool;
    std::array<int, kMaxVertices> order{};
    std::array<int, kMaxVertices> color_bound{};
    int order_size = 0;
    int color = 0;
    while (remaining.any(words_used_)) {
      ++color;
      Bits available = remaining;
      while (available.any(words_used_)) {
        const int vertex = available.first(words_used_);
        assert(vertex >= 0 && vertex < kMaxVertices);
        order[order_size] = vertex;
        color_bound[order_size] = color;
        ++order_size;
        remaining.reset(vertex);
        available.reset(vertex);
        available.remove_neighbors(adjacency_[vertex], words_used_);
      }
    }

    for (int position = order_size - 1; position >= 0; --position) {
      if (chosen_size + color_bound[position] < target_) return false;
      const int vertex = order[position];
      if (!pool.test(vertex)) continue;

      Bits next = pool;
      next.intersect(adjacency_[vertex], words_used_);
      chosen_.push_back(vertex);
      if (Search(next)) return true;
      chosen_.pop_back();
      pool.reset(vertex);
    }
    return false;
  }

  const std::array<Bits, kMaxVertices>& adjacency_;
  int words_used_;
  int target_;
  std::uint64_t nodes_ = 0;
  std::vector<int> chosen_;
  std::vector<int> witness_;
};

std::vector<bool> SquarefreeTable(int limit) {
  std::vector<bool> squarefree(limit + 1, true);
  squarefree[0] = false;
  for (int divisor = 2; divisor * divisor <= limit; ++divisor) {
    const int square = divisor * divisor;
    for (int multiple = square; multiple <= limit; multiple += square) {
      squarefree[multiple] = false;
    }
  }
  return squarefree;
}

void CheckWitness(const std::vector<int>& witness,
                  const std::vector<bool>& squarefree) {
  for (std::size_t i = 0; i < witness.size(); ++i) {
    for (std::size_t j = i; j < witness.size(); ++j) {
      assert(squarefree[witness[i] + witness[j]]);
    }
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: " << argv[0] << " MAX_N\n";
    return 2;
  }
  const int max_n = std::stoi(argv[1]);
  assert(max_n >= kPublishedTransitions.back());
  const std::vector<bool> squarefree = SquarefreeTable(2 * max_n);

  std::vector<int> values;
  std::array<Bits, kMaxVertices> adjacency{};
  int optimum = 0;
  std::uint64_t total_nodes = 0;
  std::vector<int> transitions;
  std::vector<std::vector<int>> witnesses;

  for (int n = 1; n <= max_n; ++n) {
    if (!squarefree[2 * n]) continue;
    const int new_index = static_cast<int>(values.size());
    assert(new_index < kMaxVertices);
    Bits old_neighbors;
    for (int old_index = 0; old_index < new_index; ++old_index) {
      if (squarefree[n + values[old_index]]) {
        old_neighbors.set(old_index);
        adjacency[old_index].set(new_index);
      }
    }
    adjacency[new_index] = old_neighbors;
    values.push_back(n);

    if (optimum == 0) {
      optimum = 1;
      transitions.push_back(n);
      witnesses.push_back({n});
      continue;
    }

    CliqueDecision decision(adjacency, new_index + 1, optimum);
    const bool exists = decision.Run(old_neighbors);
    total_nodes += decision.nodes();
    if (n >= kPublishedTransitions.back()) {
      std::cerr << "decision n=" << n << " target=" << optimum
                << " exists=" << exists << " nodes=" << decision.nodes()
                << '\n';
    }
    if (!exists) continue;

    ++optimum;
    std::vector<int> witness;
    for (int index : decision.witness()) witness.push_back(values[index]);
    witness.push_back(n);
    std::sort(witness.begin(), witness.end());
    CheckWitness(witness, squarefree);
    transitions.push_back(n);
    witnesses.push_back(std::move(witness));
  }

  assert(transitions.size() >= kPublishedTransitions.size());
  for (std::size_t i = 0; i < kPublishedTransitions.size(); ++i) {
    assert(transitions[i] == kPublishedTransitions[i]);
  }

  std::cout << "Erdos Problem 1109 C++ exact frontier verifier\n";
  std::cout << "MAX_N=" << max_n << " eligible_vertices=" << values.size()
            << " final_f=" << optimum << " decision_nodes=" << total_nodes
            << '\n';
  for (std::size_t i = 0; i < transitions.size(); ++i) {
    std::cout << "f=" << i + 1 << " first_N=" << transitions[i]
              << " witness={";
    for (std::size_t j = 0; j < witnesses[i].size(); ++j) {
      if (j) std::cout << ',';
      std::cout << witnesses[i][j];
    }
    std::cout << "}\n";
  }
  std::cout << "CONCLUSION exact f(N) certified for 1<=N<=" << max_n << '\n';
}
