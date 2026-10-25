#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <tuple>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

namespace {

constexpr u64 D = 22270;
constexpr u64 B = 96000;
constexpr u64 K = 2002;

static_assert(static_cast<u128>(4) * D * D * B * B <=
              std::numeric_limits<u64>::max());

u64 exact_square_root_or_zero(u64 n) {
  if (n == 0) return 0;
  u64 r = static_cast<u64>(std::sqrt(static_cast<double>(n)));
  while (static_cast<u128>(r) * r < n) ++r;
  while (static_cast<u128>(r) * r > n) --r;
  return static_cast<u128>(r) * r == n ? r : 0;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: audit_sum_difference OUTPUT.tsv\n";
    return 2;
  }

  std::vector<std::tuple<u64, u64, u64>> candidates;
  u64 triangle_pairs = 0;

  // Let sum=a+b and delta=b-a for a<=b. Strict nondegeneracy is
  // sum>D and delta<D. Integrality requires sum and delta to have the
  // same parity. Positivity and b<=B give delta<=sum-2 and delta<=2B-sum.
  for (u64 sum = D + 1; sum <= 2 * B; ++sum) {
    const u64 cap = std::min({D - 1, sum - 2, 2 * B - sum});
    u64 delta = sum & 1U;
    for (; delta <= cap; delta += 2) {
      ++triangle_pairs;
      const u64 a = (sum - delta) / 2;
      const u64 b = (sum + delta) / 2;
      const u64 heron = (sum + D) * (sum - D) * (D + delta) * (D - delta);
      if (heron % K != 0) continue;
      const u64 root = exact_square_root_or_zero(heron / K);
      if (root != 0) candidates.emplace_back(a, b, root);
    }
  }

  std::sort(candidates.begin(), candidates.end());
  std::ofstream out(argv[1]);
  if (!out) {
    std::cerr << "cannot open output\n";
    return 2;
  }
  out << "a\tb\ts\n";
  for (const auto& [a, b, s] : candidates) {
    out << a << '\t' << b << '\t' << s << '\n';
  }

  std::cout << "triangle_pairs=" << triangle_pairs << '\n';
  std::cout << "characteristic_2002=" << candidates.size() << '\n';
  return 0;
}
