#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

namespace {

#ifndef SEARCH_156_K
#define SEARCH_156_K 7
#endif
constexpr int K = SEARCH_156_K;

bool maximal_sidon(const std::array<int, K> &a, int n) {
  std::vector<unsigned char> sums(2 * n + 1, 0);
  std::vector<unsigned char> member(n + 1, 0);
  for (int x : a) member[x] = 1;
  for (int i = 0; i < K; ++i) {
    for (int j = i; j < K; ++j) {
      const int s = a[i] + a[j];
      if (sums[s]) return false;
      sums[s] = 1;
    }
  }
  for (int x = 1; x <= n; ++x) {
    if (member[x]) continue;
    bool blocked = sums[2 * x] != 0;
    for (int mark : a) blocked = blocked || sums[x + mark] != 0;
    if (!blocked) return false;
  }
  return true;
}

}  // namespace

int main(int argc, char **argv) {
  const int first_n = argc > 1 ? std::atoi(argv[1]) : 90;
  const int last_n = argc > 2 ? std::atoi(argv[2]) : 100;
  const std::uint64_t limit = argc > 3 ? std::strtoull(argv[3], nullptr, 10) : 500000000ULL;

  for (int n = first_n; n <= last_n; ++n) {
    std::mt19937_64 rng(0x156000000ULL + static_cast<std::uint64_t>(n));
    std::vector<int> pool(n);
    std::iota(pool.begin(), pool.end(), 1);
    bool found = false;
    for (std::uint64_t attempt = 1; attempt <= limit; ++attempt) {
      std::array<int, K> a{};
      for (int i = 0; i < K; ++i) {
        std::uniform_int_distribution<int> pick(i, n - 1);
        const int j = pick(rng);
        std::swap(pool[i], pool[j]);
        a[i] = pool[i];
      }
      std::sort(a.begin(), a.end());
      if (maximal_sidon(a, n)) {
        std::cout << "n=" << n << " attempts=" << attempt << " witness={";
        for (int i = 0; i < K; ++i) {
          if (i != 0) std::cout << ',';
          std::cout << a[i];
        }
        std::cout << "}\n";
        found = true;
        break;
      }
    }
    if (!found) {
      std::cout << "n=" << n << " no_witness_in_attempts=" << limit << "\n";
      return EXIT_FAILURE;
    }
  }
  return EXIT_SUCCESS;
}
