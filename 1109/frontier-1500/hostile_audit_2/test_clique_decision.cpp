#define main erdos1109_frozen_program_main
#include "/home/exedev/erdos_scratch/erdos1109_exact_frontier_2026-08-11/verify_1109_frontier.cpp"
#undef main

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <vector>

namespace {

std::uint64_t tests = 0;

bool BruteExists(const std::array<Bits, kMaxVertices>& adjacency,
                 int vertex_count, std::uint64_t candidates, int target) {
  if (target == 0) return true;
  for (std::uint64_t subset = candidates;; subset = (subset - 1) & candidates) {
    if (std::popcount(subset) == target) {
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
      if (clique) return true;
    }
    if (subset == 0) break;
  }
  return false;
}

void CheckDecision(const std::array<Bits, kMaxVertices>& adjacency,
                   int vertex_count, Bits candidates, int target,
                   bool expected) {
  CliqueDecision decision(adjacency, vertex_count, target);
  const bool actual = decision.Run(candidates);
  assert(actual == expected);
  if (actual) {
    const auto& witness = decision.witness();
    assert(static_cast<int>(witness.size()) == target);
    std::vector<int> sorted = witness;
    std::sort(sorted.begin(), sorted.end());
    assert(std::adjacent_find(sorted.begin(), sorted.end()) == sorted.end());
    for (int vertex : witness) assert(candidates.test(vertex));
    for (std::size_t i = 0; i < witness.size(); ++i) {
      for (std::size_t j = i + 1; j < witness.size(); ++j) {
        assert(adjacency[witness[i]].test(witness[j]));
      }
    }
  }
  ++tests;
}

void SetEdge(std::array<Bits, kMaxVertices>& adjacency, int left, int right) {
  adjacency[left].set(right);
  adjacency[right].set(left);
}

void ExhaustSmallGraphs() {
  auto adjacency = std::make_unique<std::array<Bits, kMaxVertices>>();
  for (int n = 0; n <= 6; ++n) {
    const int edge_count = n * (n - 1) / 2;
    const std::uint64_t graph_count = std::uint64_t{1} << edge_count;
    for (std::uint64_t graph = 0; graph < graph_count; ++graph) {
      *adjacency = {};
      int edge_index = 0;
      for (int left = 0; left < n; ++left) {
        for (int right = left + 1; right < n; ++right, ++edge_index) {
          if (graph & (std::uint64_t{1} << edge_index)) {
            SetEdge(*adjacency, left, right);
          }
        }
      }

      const std::uint64_t all = n == 0 ? 0 : (std::uint64_t{1} << n) - 1;
      const std::uint64_t pool_count = n <= 5 ? (std::uint64_t{1} << n) : 1;
      for (std::uint64_t pool_number = 0; pool_number < pool_count; ++pool_number) {
        const std::uint64_t pool = n <= 5 ? pool_number : all;
        Bits candidates;
        for (int vertex = 0; vertex < n; ++vertex) {
          if (pool & (std::uint64_t{1} << vertex)) candidates.set(vertex);
        }
        for (int target = 0; target <= n + 1; ++target) {
          CheckDecision(*adjacency, n, candidates, target,
                        BruteExists(*adjacency, n, pool, target));
        }
      }
    }
  }
}

void CheckKnownFamilies() {
  auto adjacency = std::make_unique<std::array<Bits, kMaxVertices>>();
  const std::array<int, 8> sizes = {63, 64, 65, 127, 128, 129, 610, 2048};
  for (int n : sizes) {
    Bits all;
    for (int vertex = 0; vertex < n; ++vertex) all.set(vertex);

    *adjacency = {};
    CheckDecision(*adjacency, n, all, 0, true);
    CheckDecision(*adjacency, n, all, 1, true);
    CheckDecision(*adjacency, n, all, 2, false);

    *adjacency = {};
    for (int left = 0; left < n; ++left) {
      for (int right = left + 1; right < n; ++right) {
        SetEdge(*adjacency, left, right);
      }
    }
    const int complete_target = std::min(n, 44);
    CheckDecision(*adjacency, n, all, complete_target, true);
    if (n <= 129) CheckDecision(*adjacency, n, all, n + 1, false);

    *adjacency = {};
    constexpr int block_size = 7;
    for (int left = 0; left < n; ++left) {
      for (int right = left + 1; right < n; ++right) {
        if (left / block_size == right / block_size) {
          SetEdge(*adjacency, left, right);
        }
      }
    }
    CheckDecision(*adjacency, n, all, std::min(n, block_size), true);
    if (n > block_size) CheckDecision(*adjacency, n, all, block_size + 1, false);

    *adjacency = {};
    constexpr int parts = 11;
    for (int left = 0; left < n; ++left) {
      for (int right = left + 1; right < n; ++right) {
        if (left % parts != right % parts) SetEdge(*adjacency, left, right);
      }
    }
    CheckDecision(*adjacency, n, all, std::min(n, parts), true);
    if (n > parts) CheckDecision(*adjacency, n, all, parts + 1, false);
  }
}

void CheckRandomGraphs() {
  auto adjacency = std::make_unique<std::array<Bits, kMaxVertices>>();
  std::mt19937_64 generator(0x1109A392165ULL);
  for (int trial = 0; trial < 300; ++trial) {
    const int n = 1 + generator() % 14;
    *adjacency = {};
    for (int left = 0; left < n; ++left) {
      for (int right = left + 1; right < n; ++right) {
        if ((generator() & 255) < (generator() & 255)) {
          SetEdge(*adjacency, left, right);
        }
      }
    }
    std::uint64_t pool = generator() & ((std::uint64_t{1} << n) - 1);
    Bits candidates;
    for (int vertex = 0; vertex < n; ++vertex) {
      if (pool & (std::uint64_t{1} << vertex)) candidates.set(vertex);
    }
    for (int target = 0; target <= n + 1; ++target) {
      CheckDecision(*adjacency, n, candidates, target,
                    BruteExists(*adjacency, n, pool, target));
    }
  }
}

}  // namespace

int main() {
  ExhaustSmallGraphs();
  CheckKnownFamilies();
  CheckRandomGraphs();
  std::cout << "PASS exact_frozen_CliqueDecision tests=" << tests
            << " exhaustive_graph_order=6 word_boundaries=63,64,65,127,128,129,610,2048"
            << '\n';
}
