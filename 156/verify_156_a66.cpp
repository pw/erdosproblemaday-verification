#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

namespace {

#ifndef VERIFY_156_N
#define VERIFY_156_N 66
#endif

constexpr int N = VERIFY_156_N;
constexpr int MAX_K = 6;
constexpr int MAX_L = N - 1;

using u128 = unsigned __int128;

struct Stats {
  std::uint64_t endpoint_tests = 0;
  std::uint64_t golomb_normalized = 0;
  std::uint64_t hull_covered = 0;
  std::uint64_t placements_66 = 0;
  std::uint64_t digest = 1469598103934665603ULL;
  int best_run = 0;
  int best_lo = 0;
  int best_hi = -1;
  std::vector<int> best_marks;
  std::vector<int> first_witness;
  std::vector<std::vector<int>> all_witnesses;
};

std::array<Stats, MAX_K + 1> stats;
std::array<int, MAX_K> marks{};

void mix(std::uint64_t &h, std::uint64_t value) {
  for (int i = 0; i < 8; ++i) {
    h ^= static_cast<unsigned char>(value & 0xffU);
    h *= 1099511628211ULL;
    value >>= 8;
  }
}

bool add_mark(int used, int x, u128 old_mask, u128 &new_mask) {
  u128 added = 0;
  for (int i = 0; i < used; ++i) {
    const int d = x - marks[i];
    const u128 bit = static_cast<u128>(1) << d;
    if ((old_mask & bit) != 0 || (added & bit) != 0) return false;
    added |= bit;
  }
  new_mask = old_mask | added;
  return true;
}

void evaluate(int k, int L, u128 difference_mask) {
  Stats &s = stats[k];
  ++s.golomb_normalized;

  constexpr int MIN_X = -MAX_L - 1;
  constexpr int MAX_X = 2 * MAX_L + 1;
  constexpr int WIDTH = MAX_X - MIN_X + 1;
  std::array<unsigned char, WIDTH> blocked{};
  auto block = [&](int x) {
    if (MIN_X <= x && x <= MAX_X) blocked[x - MIN_X] = 1;
  };
  auto is_blocked = [&](int x) {
    return MIN_X <= x && x <= MAX_X && blocked[x - MIN_X] != 0;
  };

  for (int i = 0; i < k; ++i) block(marks[i]);
  for (int d = 1; d <= L; ++d) {
    if ((difference_mask & (static_cast<u128>(1) << d)) == 0) continue;
    for (int i = 0; i < k; ++i) {
      block(marks[i] - d);
      block(marks[i] + d);
    }
  }
  for (int i = 0; i < k; ++i) {
    for (int j = i + 1; j < k; ++j) {
      const int sum = marks[i] + marks[j];
      if ((sum & 1) == 0) block(sum / 2);
    }
  }

  bool covered = true;
  for (int x = 0; x <= L; ++x) covered = covered && is_blocked(x);
  int lo = 0;
  int hi = L;
  int run = 0;
  if (covered) {
    ++s.hull_covered;
    while (is_blocked(lo - 1)) --lo;
    while (is_blocked(hi + 1)) ++hi;
    run = hi - lo + 1;
  }

  mix(s.digest, static_cast<std::uint64_t>(k));
  mix(s.digest, static_cast<std::uint64_t>(L));
  for (int i = 0; i < k; ++i) mix(s.digest, static_cast<std::uint64_t>(marks[i]));
  mix(s.digest, static_cast<std::uint64_t>(lo + MAX_L + 1));
  mix(s.digest, static_cast<std::uint64_t>(hi + MAX_L + 1));

  if (run > s.best_run) {
    s.best_run = run;
    s.best_lo = lo;
    s.best_hi = hi;
    s.best_marks.assign(marks.begin(), marks.begin() + k);
  }

  if (!covered) return;
  for (int shift = 0; shift <= N - 1 - L; ++shift) {
    bool maximal = true;
    for (int x = -shift; x <= N - 1 - shift; ++x) {
      if (!is_blocked(x)) {
        maximal = false;
        break;
      }
    }
    if (!maximal) continue;
    ++s.placements_66;
    std::vector<int> witness;
    for (int i = 0; i < k; ++i) witness.push_back(marks[i] + shift + 1);
    if (s.first_witness.empty()) s.first_witness = witness;
    s.all_witnesses.push_back(witness);
  }
}

void choose_interiors(int k, int L, int used, int next, u128 mask) {
  if (used == k - 1) {
    ++stats[k].endpoint_tests;
    u128 final_mask = 0;
    if (!add_mark(used, L, mask, final_mask)) return;
    marks[used] = L;
    evaluate(k, L, final_mask);
    return;
  }

  const int interiors_left_after_choice = (k - 1) - (used + 1);
  const int largest_choice = L - 1 - interiors_left_after_choice;
  for (int x = next; x <= largest_choice; ++x) {
    u128 next_mask = 0;
    if (!add_mark(used, x, mask, next_mask)) continue;
    marks[used] = x;
    choose_interiors(k, L, used + 1, x + 1, next_mask);
  }
}

std::string join(const std::vector<int> &values) {
  std::string out = "{";
  for (std::size_t i = 0; i < values.size(); ++i) {
    if (i != 0) out += ",";
    out += std::to_string(values[i]);
  }
  out += "}";
  return out;
}

std::uint64_t binomial(int n, int r) {
  if (r < 0 || r > n) return 0;
  r = std::min(r, n - r);
  std::uint64_t answer = 1;
  for (int i = 1; i <= r; ++i) {
    answer = answer * static_cast<std::uint64_t>(n - r + i) /
             static_cast<std::uint64_t>(i);
  }
  return answer;
}

}  // namespace

int main() {
  marks[0] = 0;
  stats[1].endpoint_tests = 1;
  evaluate(1, 0, 0);

  for (int k = 2; k <= MAX_K; ++k) {
    for (int L = k - 1; L <= MAX_L; ++L) {
      choose_interiors(k, L, 1, 1, 0);
    }
  }

  std::cout << "Problem 156 exact finite frontier verifier\n";
  std::cout << "N=" << N << ", normalized diameter range 0.." << MAX_L << "\n";
  for (int k = 1; k <= MAX_K; ++k) {
    const Stats &s = stats[k];
    const std::uint64_t raw_total = binomial(MAX_L, k - 1);
    std::cout << "k=" << k
              << " raw_total=" << raw_total
              << " pruned_before_endpoint=" << raw_total - s.endpoint_tests
              << " endpoint_tests=" << s.endpoint_tests
              << " endpoint_rejects=" << s.endpoint_tests - s.golomb_normalized
              << " golomb=" << s.golomb_normalized
              << " hull_covered=" << s.hull_covered
              << " placements_N=" << s.placements_66
              << " digest=0x" << std::hex << std::setw(16) << std::setfill('0')
              << s.digest << std::dec << std::setfill(' ')
              << " best_run=" << s.best_run;
    if (!s.best_marks.empty()) {
      std::cout << " best_marks=" << join(s.best_marks)
                << " best_interval=[" << s.best_lo << "," << s.best_hi << "]";
    }
    if (!s.first_witness.empty()) {
      std::cout << " first_witness_in_[1,N]=" << join(s.first_witness);
    }
    std::cout << "\n";
    for (std::size_t i = 0; i < s.all_witnesses.size(); ++i) {
      std::cout << "  witness_" << (i + 1) << "=" << join(s.all_witnesses[i]) << "\n";
    }
  }

  if (N <= 67) {
    bool exact_ok = true;
    for (int k = 1; k <= 5; ++k) exact_ok = exact_ok && stats[k].placements_66 == 0;
    exact_ok = exact_ok && stats[6].placements_66 > 0;
    std::cout << "CONCLUSION a(" << N << ")="
              << (exact_ok ? "6" : "NOT CERTIFIED") << "\n";
    return exact_ok ? EXIT_SUCCESS : EXIT_FAILURE;
  }

  bool lower_ok = true;
  for (int k = 1; k <= 6; ++k) lower_ok = lower_ok && stats[k].best_run < 68;
  std::cout << "CONCLUSION no maximal Sidon set of size <=6 in [1,n] for 68<=n<="
            << N << ": " << (lower_ok ? "CERTIFIED" : "FAILED") << "\n";
  return lower_ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
