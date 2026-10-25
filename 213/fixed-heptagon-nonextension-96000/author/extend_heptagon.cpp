#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

using u64 = std::uint64_t;
using i64 = std::int64_t;
using i128 = __int128_t;

namespace {

constexpr i64 D = 22270;
constexpr i64 BOUND = 96000;
constexpr i64 K = 2002;
static_assert(static_cast<__uint128_t>(4) * D * D * BOUND * BOUND <=
              std::numeric_limits<u64>::max());
constexpr std::array<std::array<i64, 7>, 7> M{{
    {{0, 22270, 22098, 16637, 9248, 8908, 8636}},
    {{22270, 0, 21488, 11397, 15138, 20698, 13746}},
    {{22098, 21488, 0, 10795, 14450, 13430, 20066}},
    {{16637, 11397, 10795, 0, 7395, 11135, 11049}},
    {{9248, 15138, 14450, 7395, 0, 5780, 5916}},
    {{8908, 20698, 13430, 11135, 5780, 0, 10744}},
    {{8636, 13746, 20066, 11049, 5916, 10744, 0}},
}};

u64 square_root_if_square(u64 n) {
  u64 r = static_cast<u64>(std::sqrt(static_cast<long double>(n)));
  while (static_cast<__uint128_t>(r) * r < n) ++r;
  while (static_cast<__uint128_t>(r) * r > n) --r;
  return static_cast<__uint128_t>(r) * r == n ? r : 0;
}

u64 heron_product(i64 a, i64 b, i64 c) {
  // For a triangle on the fixed base D with other sides at most BOUND,
  // 16*area^2 <= 4*D^2*BOUND^2; the static assertion makes u64 exact.
  return static_cast<u64>(a + b + c) * (a + b - c) *
         (a - b + c) * (-a + b + c);
}

struct PointData {
  i64 x_num;
  i64 y_coeff;
};

std::array<PointData, 7> heptagon_coordinates() {
  std::array<PointData, 7> p{};
  p[0] = {0, 0};
  p[1] = {2 * D * D, 0};
  for (int j = 2; j < 7; ++j) {
    const i64 a = M[0][j];
    const i64 b = M[1][j];
    const u64 h = heron_product(D, a, b);
    if (h % K != 0) throw std::runtime_error("wrong characteristic");
    const u64 s = square_root_if_square(h / K);
    if (!s) throw std::runtime_error("non-square characteristic quotient");
    p[j].x_num = a * a - b * b + D * D;
    p[j].y_coeff = static_cast<i64>(s);
  }

  // Fix vertex 2 above the base. Each later sign is forced by its distance
  // from vertex 2.
  const i128 den = static_cast<i128>(4) * D * D;
  for (int j = 3; j < 7; ++j) {
    int matches = 0;
    i64 selected = 0;
    for (const i64 sign : {-1, 1}) {
      const i128 dx = static_cast<i128>(p[j].x_num) - p[2].x_num;
      const i128 dy = static_cast<i128>(sign) * p[j].y_coeff - p[2].y_coeff;
      const i128 lhs = den * M[2][j] * M[2][j];
      const i128 rhs = dx * dx + static_cast<i128>(K) * dy * dy;
      if (lhs == rhs) {
        ++matches;
        selected = sign * p[j].y_coeff;
      }
    }
    if (matches != 1) throw std::runtime_error("orientation not uniquely forced");
    p[j].y_coeff = selected;
  }
  return p;
}

bool integral_bounded_distance(const PointData& a, const PointData& b,
                               i64* distance = nullptr) {
  const i128 dx = static_cast<i128>(a.x_num) - b.x_num;
  const i128 dy = static_cast<i128>(a.y_coeff) - b.y_coeff;
  const i128 numerator = dx * dx + static_cast<i128>(K) * dy * dy;
  const i128 denominator = static_cast<i128>(4) * D * D;
  if (numerator == 0 || numerator % denominator != 0) return false;
  const i128 squared = numerator / denominator;
  if (squared > static_cast<i128>(BOUND) * BOUND) return false;
  const u64 root = square_root_if_square(static_cast<u64>(squared));
  if (!root) return false;
  if (distance) *distance = static_cast<i64>(root);
  return true;
}

bool matches_all_vertices(const std::array<PointData, 7>& h, i64 a, i64 b,
                          i64 s, int side) {
  const PointData candidate{a * a - b * b + D * D, side * s};
  for (const PointData& vertex : h) {
    if (!integral_bounded_distance(candidate, vertex)) return false;
  }
  return true;
}

}  // namespace

int main(int argc, char** argv) {
  std::ofstream candidate_file;
  if (argc == 3 && std::string(argv[1]) == "--emit-candidates") {
    candidate_file.open(argv[2]);
    if (!candidate_file) {
      std::cerr << "cannot open candidate output\n";
      return 2;
    }
    candidate_file << "a\tb\ts\n";
  } else if (argc != 1) {
    std::cerr << "usage: extend_heptagon [--emit-candidates PATH]\n";
    return 2;
  }

  const auto h = heptagon_coordinates();

  // Definition-level self-check of all 21 published distances.
  for (int i = 0; i < 7; ++i) {
    for (int j = i + 1; j < 7; ++j) {
      i64 got = 0;
      if (!integral_bounded_distance(h[i], h[j], &got) || got != M[i][j]) {
        std::cerr << "heptagon reconstruction failed at " << i << ',' << j
                  << '\n';
        return 2;
      }
    }
  }

  u64 triangle_pairs = 0;
  u64 characteristic_2002 = 0;
  u64 oriented_candidates = 0;
  u64 degenerate_candidates = 0;
  u64 extensions = 0;

  const auto test_degenerate = [&](i64 x_num) {
    ++degenerate_candidates;
    const PointData candidate{x_num, 0};
    for (const PointData& vertex : h) {
      if (!integral_bounded_distance(candidate, vertex)) return;
    }
    ++extensions;
    std::cout << "degenerate extension x_num=" << x_num << '\n';
  };

  // Collinear candidates have no triangle characteristic and are handled
  // separately. Here t is the positive distance from the nearer anchor.
  for (i64 t = 1; t < D; ++t) test_degenerate(2 * D * t);
  for (i64 t = 1; t <= BOUND - D; ++t) {
    test_degenerate(-2 * D * t);
    test_degenerate(2 * D * (D + t));
  }

  // The base has length D and candidate distances a,b are at most BOUND.
  // Swapping a,b is handled explicitly below, so only a<=b is enumerated.
  for (i64 a = 1; a <= BOUND; ++a) {
    const i64 first_b = std::max(a, D - a + 1);
    const i64 last_b = std::min(BOUND, D + a - 1);
    for (i64 b = first_b; b <= last_b; ++b) {
      ++triangle_pairs;
      const u64 hp = heron_product(D, a, b);
      if (hp % K != 0) continue;
      const u64 s = square_root_if_square(hp / K);
      if (!s) continue;
      ++characteristic_2002;
      if (candidate_file) candidate_file << a << '\t' << b << '\t' << s << '\n';

      for (int swap = 0; swap <= (a != b); ++swap) {
        const i64 aa = swap ? b : a;
        const i64 bb = swap ? a : b;
        for (const int side : {-1, 1}) {
          ++oriented_candidates;
          if (matches_all_vertices(h, aa, bb, static_cast<i64>(s), side)) {
            ++extensions;
            std::cout << "extension a=" << aa << " b=" << bb
                      << " s=" << s << " side=" << side << '\n';
          }
        }
      }
    }
  }

  std::cout << "triangle_pairs=" << triangle_pairs << '\n';
  std::cout << "distance_bound=" << BOUND << '\n';
  std::cout << "characteristic_2002=" << characteristic_2002 << '\n';
  std::cout << "oriented_candidates=" << oriented_candidates << '\n';
  std::cout << "degenerate_candidates=" << degenerate_candidates << '\n';
  std::cout << "extensions=" << extensions << '\n';
  return extensions == 0 ? 0 : 1;
}
