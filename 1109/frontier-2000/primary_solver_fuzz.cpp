#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main erdos1109_frontier_program_main
#include "verify_1109_frontier.cpp"
#undef main
#pragma GCC diagnostic pop

#include <cassert>
#include <cstdint>
#include <iostream>
#include <random>

namespace {

int BruteMaximumClique(const std::array<Bits, kMaxVertices>& adjacency,
                       int vertex_count, std::uint64_t pool) {
  int best = 0;
  for (std::uint64_t subset = pool;; subset = (subset - 1) & pool) {
    const int size = std::popcount(subset);
    if (size > best) {
      bool clique = true;
      for (int left = 0; left < vertex_count && clique; ++left) {
        if (!(subset & (std::uint64_t{1} << left))) continue;
        for (int right = left + 1; right < vertex_count; ++right) {
          if ((subset & (std::uint64_t{1} << right)) &&
              !adjacency[left].test(right)) {
            clique = false;
            break;
          }
        }
      }
      if (clique) best = size;
    }
    if (subset == 0) break;
  }
  return best;
}

void CheckWitnessIndices(const std::array<Bits, kMaxVertices>& adjacency,
                         const std::vector<int>& witness, int target) {
  assert(static_cast<int>(witness.size()) == target);
  for (int left_index = 0; left_index < target; ++left_index) {
    assert(0 <= witness[left_index] && witness[left_index] < kMaxVertices);
    for (int right_index = left_index + 1; right_index < target; ++right_index) {
      assert(adjacency[witness[left_index]].test(witness[right_index]));
    }
  }
}

}  // namespace

int main() {
  constexpr int kCases = 4000;
  std::mt19937_64 generator(1109);
  std::uint64_t decisions = 0;

  for (int case_index = 0; case_index < kCases; ++case_index) {
    const int vertex_count = 1 + static_cast<int>(generator() % 12);
    std::array<Bits, kMaxVertices> adjacency{};
    const int edge_threshold = static_cast<int>(generator() % 101);
    for (int left = 0; left < vertex_count; ++left) {
      for (int right = left + 1; right < vertex_count; ++right) {
        if (static_cast<int>(generator() % 101) <= edge_threshold) {
          adjacency[left].set(right);
          adjacency[right].set(left);
        }
      }
    }

    const std::uint64_t all = (std::uint64_t{1} << vertex_count) - 1;
    std::uint64_t pool_mask = generator() & all;
    if (case_index % 4 == 0) pool_mask = all;
    Bits pool;
    for (int vertex = 0; vertex < vertex_count; ++vertex) {
      if (pool_mask & (std::uint64_t{1} << vertex)) pool.set(vertex);
    }
    const int exact_maximum = BruteMaximumClique(adjacency, vertex_count, pool_mask);

    for (int target = 0; target <= vertex_count + 1; ++target) {
      CliqueDecision solver(adjacency, vertex_count, target);
      const bool found = solver.Run(pool);
      assert(found == (target <= exact_maximum));
      assert(solver.nodes() > 0);
      if (found) CheckWitnessIndices(adjacency, solver.witness(), target);
      ++decisions;
    }
  }

  std::cout << "cases=" << kCases << " decisions=" << decisions
            << " seed=1109 max_vertices=12\n";
  std::cout << "CONCLUSION exact primary clique solver agrees with brute force\n";
}
