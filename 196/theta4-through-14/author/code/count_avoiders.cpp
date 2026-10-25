#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <utility>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using u128 = unsigned __int128;

static std::string decimal(u128 x) {
  if (x == 0) return "0";
  std::string out;
  while (x != 0) {
    out.push_back(static_cast<char>('0' + x % 10));
    x /= 10;
  }
  std::reverse(out.begin(), out.end());
  return out;
}

struct OrderedTriple {
  int first;
  int second;
  int third;
};

class EndpointCounter {
 public:
  explicit EndpointCounter(int n)
      : n_(n), used_(n, false), position_(n, -1), forbidden_endings_(n) {
    for (int x = 0; x < n_; ++x) {
      for (int d = 1; x - 3 * d >= 0; ++d) {
        forbidden_endings_[x].push_back({x - 3 * d, x - 2 * d, x - d});
      }
      for (int d = 1; x + 3 * d < n_; ++d) {
        forbidden_endings_[x].push_back({x + 3 * d, x + 2 * d, x + d});
      }
    }
  }

  u128 CountWithFirst(int first) {
    used_[first] = true;
    position_[first] = 0;
    const u128 result = Search(1);
    position_[first] = -1;
    used_[first] = false;
    return result;
  }

  u128 CountWithPrefix(int first, int second) {
    used_[first] = true;
    position_[first] = 0;
    used_[second] = true;
    position_[second] = 1;
    const u128 result = Search(2);
    position_[second] = -1;
    used_[second] = false;
    position_[first] = -1;
    used_[first] = false;
    return result;
  }

 private:
  bool CanAppend(int x) const {
    for (const OrderedTriple& t : forbidden_endings_[x]) {
      const int p0 = position_[t.first];
      const int p1 = position_[t.second];
      const int p2 = position_[t.third];
      if (p0 >= 0 && p0 < p1 && p1 < p2) return false;
    }
    return true;
  }

  u128 Search(int depth) {
    if (depth == n_) return 1;
    u128 count = 0;
    for (int x = 0; x < n_; ++x) {
      if (used_[x] || !CanAppend(x)) continue;
      used_[x] = true;
      position_[x] = depth;
      count += Search(depth + 1);
      position_[x] = -1;
      used_[x] = false;
    }
    return count;
  }

  int n_;
  std::vector<bool> used_;
  std::vector<int> position_;
  std::vector<std::vector<OrderedTriple>> forbidden_endings_;
};

static bool DirectlyAvoids(const std::vector<int>& permutation) {
  const int n = static_cast<int>(permutation.size());
  std::vector<int> position(n);
  for (int i = 0; i < n; ++i) position[permutation[i]] = i;
  for (int d = 1; 3 * d < n; ++d) {
    for (int a = 0; a + 3 * d < n; ++a) {
      const int p0 = position[a];
      const int p1 = position[a + d];
      const int p2 = position[a + 2 * d];
      const int p3 = position[a + 3 * d];
      if ((p0 < p1 && p1 < p2 && p2 < p3) ||
          (p0 > p1 && p1 > p2 && p2 > p3)) {
        return false;
      }
    }
  }
  return true;
}

static u128 DirectCount(int n) {
  std::vector<int> permutation(n);
  std::iota(permutation.begin(), permutation.end(), 0);
  u128 count = 0;
  do {
    count += DirectlyAvoids(permutation);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return count;
}

static u128 FastCount(int n) {
  if (n == 1) return 1;
  std::vector<std::pair<int, int>> prefixes;
  for (int first = 0; first < n; ++first) {
    for (int second = 0; second < n; ++second) {
      if (first == second) continue;
      const std::pair<int, int> prefix{first, second};
      const std::pair<int, int> complement{n - 1 - first, n - 1 - second};
      if (prefix < complement) prefixes.push_back(prefix);
    }
  }
  std::vector<u128> prefix_counts(prefixes.size());
#pragma omp parallel for schedule(dynamic, 1)
  for (std::size_t i = 0; i < prefixes.size(); ++i) {
    EndpointCounter counter(n);
    prefix_counts[i] = counter.CountWithPrefix(prefixes[i].first, prefixes[i].second);
  }
  u128 total = 0;
  // No two-distinct-value prefix is fixed by value complementation. Each
  // canonical task therefore represents an orbit of exactly two prefixes.
  for (u128 count : prefix_counts) total += 2 * count;
  return total;
}

int main(int argc, char** argv) {
  int max_n = 12;
  int crosscheck_n = 10;
  if (argc >= 2) max_n = std::atoi(argv[1]);
  if (argc >= 3) crosscheck_n = std::atoi(argv[2]);
  if (max_n < 1 || crosscheck_n < 0) return 2;

#ifdef _OPENMP
  std::cout << "threads=" << omp_get_max_threads() << "\n";
#else
  std::cout << "threads=1\n";
#endif
  for (int n = 1; n <= max_n; ++n) {
    const auto start = std::chrono::steady_clock::now();
    const u128 fast = FastCount(n);
    const auto stop = std::chrono::steady_clock::now();
    const double seconds =
        std::chrono::duration_cast<std::chrono::duration<double>>(stop - start).count();
    std::cout << "theta4(" << n << ")=" << decimal(fast)
              << " fast_seconds=" << seconds;
    if (n <= crosscheck_n) {
      const u128 direct = DirectCount(n);
      std::cout << " direct=" << decimal(direct);
      if (direct != fast) {
        std::cout << " MISMATCH\n";
        return 1;
      }
    }
    std::cout << "\n";
  }
  std::cout << "crosscheck_mismatches=0\n";
  return 0;
}
