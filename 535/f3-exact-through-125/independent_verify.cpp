#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <tuple>
#include <vector>

namespace {

constexpr int MAX_N = 125;
constexpr int WORDS = 2;
using Bits = std::array<std::uint64_t, WORDS>;

struct Solver {
  int n;
  int target;
  std::vector<int> order;
  std::vector<std::vector<Bits>> conflicts;
  std::uint64_t nodes = 0;

  explicit Solver(int n_value, int target_value) : n(n_value), target(target_value) {
    std::vector<std::tuple<int, int, int>> edges;
    std::vector<int> degree(n, 0);
    for (int a = 0; a < n; ++a) {
      for (int b = a + 1; b < n; ++b) {
        for (int c = b + 1; c < n; ++c) {
          const int x = std::gcd(a + 1, b + 1);
          if (x == std::gcd(a + 1, c + 1) && x == std::gcd(b + 1, c + 1)) {
            edges.emplace_back(a, b, c);
            ++degree[a];
            ++degree[b];
            ++degree[c];
          }
        }
      }
    }
    edge_count = edges.size();

    order.resize(n);
    std::iota(order.begin(), order.end(), 0);
    // A separate, arithmetic order: increasing integer value.  The Python
    // verifier instead uses decreasing hypergraph degree.
    (void)degree;
    std::vector<int> position(n);
    for (int i = 0; i < n; ++i) position[order[i]] = i;

    conflicts.assign(n, std::vector<Bits>(n, Bits{}));
    auto mark = [&](int i, int j, int k) {
      conflicts[i][j][k / 64] |= std::uint64_t{1} << (k % 64);
    };
    for (const auto& [a, b, c] : edges) {
      const int i = position[a], j = position[b], k = position[c];
      mark(i, j, k); mark(j, i, k);
      mark(i, k, j); mark(k, i, j);
      mark(j, k, i); mark(k, j, i);
    }
  }

  std::size_t edge_count = 0;

  static int count(const Bits& bits) {
    return std::popcount(bits[0]) + std::popcount(bits[1]);
  }

  static bool empty(const Bits& bits) { return bits[0] == 0 && bits[1] == 0; }

  static int first(const Bits& bits) {
    if (bits[0]) return std::countr_zero(bits[0]);
    return 64 + std::countr_zero(bits[1]);
  }

  static void erase(Bits& bits, int vertex) {
    bits[vertex / 64] &= ~(std::uint64_t{1} << (vertex % 64));
  }

  bool search(std::vector<int>& chosen, Bits candidates) {
    ++nodes;
    if (static_cast<int>(chosen.size()) == target) return true;
    if (static_cast<int>(chosen.size()) + count(candidates) < target) return false;
    if (empty(candidates)) return false;

    // This binary include/exclude recursion is deliberately shaped differently
    // from the Python loop recursion, though both enumerate the same subsets.
    const int vertex = first(candidates);
    erase(candidates, vertex);

    Bits included_candidates = candidates;
    for (int old : chosen) {
      for (int word = 0; word < WORDS; ++word) {
        included_candidates[word] &= ~conflicts[old][vertex][word];
      }
    }
    chosen.push_back(vertex);
    if (search(chosen, included_candidates)) return true;
    chosen.pop_back();
    return search(chosen, candidates);
  }

  bool exists() {
    Bits candidates{};
    for (int i = 0; i < n; ++i) candidates[i / 64] |= std::uint64_t{1} << (i % 64);
    std::vector<int> chosen;
    return search(chosen, candidates);
  }
};

bool bad_triple(int a, int b, int c) {
  const int d = std::gcd(a, b);
  return d == std::gcd(a, c) && d == std::gcd(b, c);
}

template <std::size_t K>
void check_witness(const std::array<int, K>& witness, int first_n) {
  assert(std::is_sorted(witness.begin(), witness.end()));
  assert(witness.front() >= 1 && witness.back() <= first_n);
  for (std::size_t i = 0; i < K; ++i)
    for (std::size_t j = i + 1; j < K; ++j)
      for (std::size_t k = j + 1; k < K; ++k)
        assert(!bad_triple(witness[i], witness[j], witness[k]));
}

}  // namespace

int main() {
  check_witness(std::array{10, 12, 13, 15, 18, 20, 24, 40, 48, 54, 75, 80, 91, 96}, 101);
  check_witness(std::array{11, 14, 20, 24, 30, 33, 36, 40, 48, 80, 90, 96, 98, 99, 108}, 108);
  check_witness(std::array{14, 20, 21, 24, 25, 30, 36, 40, 48, 63, 80, 90, 96, 98, 108, 125}, 125);

  for (const auto& [n, target, expected_edges] : {
           std::tuple{107, 15, std::size_t{71799}},
           std::tuple{124, 16, std::size_t{109838}},
           std::tuple{125, 17, std::size_t{113132}},
       }) {
    Solver solver(n, target);
    assert(solver.edge_count == expected_edges);
    const bool exists = solver.exists();
    std::cout << "n=" << n << " target=" << target
              << " edges=" << solver.edge_count << " binary_nodes=" << solver.nodes
              << " result=" << (exists ? "SAT" : "UNSAT") << '\n';
    if (exists) return 1;
  }
  std::cout << "INDEPENDENT PASS: exact f_3(N) for 101 <= N <= 125\n";
}
