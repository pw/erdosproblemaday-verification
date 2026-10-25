#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

namespace {

constexpr int MAX_N = 95;
constexpr int MAX_L = MAX_N - 1;
constexpr int MAX_K = 6;
constexpr int SUM_BITS = 2 * MAX_L + 1;
constexpr int MIN_X = -MAX_L - 1;
constexpr int MAX_X = 2 * MAX_L + 1;
constexpr int BLOCK_BITS = MAX_X - MIN_X + 1;

struct Stats {
  std::uint64_t sidon = 0;
  std::uint64_t hull_covered = 0;
  std::uint64_t digest = 1469598103934665603ULL;
  int best_run = 0;
  int best_lo = 0;
  int best_hi = -1;
  std::vector<int> best_marks;
};

std::array<int, MAX_K> marks{};
std::array<Stats, MAX_K + 1> stats{};

void mix(std::uint64_t &h, std::uint64_t value) {
  for (int i = 0; i < 8; ++i) {
    h ^= static_cast<unsigned char>(value & 0xffU);
    h *= 1099511628211ULL;
    value >>= 8;
  }
}

bool add_mark(int used, int x, const std::bitset<SUM_BITS> &old_sums,
              std::bitset<SUM_BITS> &new_sums) {
  new_sums = old_sums;
  for (int i = 0; i < used; ++i) {
    const int sum = x + marks[i];
    if (new_sums.test(sum)) return false;
    new_sums.set(sum);
  }
  if (new_sums.test(2 * x)) return false;
  new_sums.set(2 * x);
  return true;
}

void evaluate(int k, const std::bitset<SUM_BITS> &sums) {
  Stats &s = stats[k];
  ++s.sidon;

  std::array<unsigned char, BLOCK_BITS> blocked{};
  auto block = [&](int x) {
    if (MIN_X <= x && x <= MAX_X) blocked[x - MIN_X] = 1;
  };
  auto is_blocked = [&](int x) {
    return MIN_X <= x && x <= MAX_X && blocked[x - MIN_X] != 0;
  };

  for (int i = 0; i < k; ++i) block(marks[i]);
  for (int sum = 0; sum < SUM_BITS; ++sum) {
    if (!sums.test(sum)) continue;
    for (int i = 0; i < k; ++i) block(sum - marks[i]);
    if ((sum & 1) == 0) block(sum / 2);
  }

  const int L = marks[k - 1];
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
  for (int i = 0; i < k; ++i) mix(s.digest, static_cast<std::uint64_t>(marks[i]));
  mix(s.digest, static_cast<std::uint64_t>(lo - MIN_X));
  mix(s.digest, static_cast<std::uint64_t>(hi - MIN_X));

  if (run > s.best_run) {
    s.best_run = run;
    s.best_lo = lo;
    s.best_hi = hi;
    s.best_marks.assign(marks.begin(), marks.begin() + k);
  }
}

void search(int k, int used, int next, const std::bitset<SUM_BITS> &sums) {
  if (used == k) {
    evaluate(k, sums);
    return;
  }
  const int remaining_after = k - used - 1;
  for (int x = next; x <= MAX_L - remaining_after; ++x) {
    std::bitset<SUM_BITS> next_sums;
    if (!add_mark(used, x, sums, next_sums)) continue;
    marks[used] = x;
    search(k, used + 1, x + 1, next_sums);
  }
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

std::string join(const std::vector<int> &values) {
  std::string out = "{";
  for (std::size_t i = 0; i < values.size(); ++i) {
    if (i != 0) out += ",";
    out += std::to_string(values[i]);
  }
  return out + "}";
}

}  // namespace

int main() {
  marks[0] = 0;
  std::bitset<SUM_BITS> initial_sums;
  initial_sums.set(0);
  for (int k = 1; k <= MAX_K; ++k) search(k, 1, 1, initial_sums);

  std::cout << "Independent pair-sum frontier audit\n";
  std::cout << "all normalized sets with maximum mark <= " << MAX_L << "\n";
  for (int k = 1; k <= MAX_K; ++k) {
    const Stats &s = stats[k];
    std::cout << "k=" << k
              << " raw_total=" << binomial(MAX_L, k - 1)
              << " sidon_by_sums=" << s.sidon
              << " hull_covered=" << s.hull_covered
              << " digest=0x" << std::hex << std::setw(16) << std::setfill('0')
              << s.digest << std::dec << std::setfill(' ')
              << " best_run=" << s.best_run
              << " best_marks=" << join(s.best_marks)
              << " best_interval=[" << s.best_lo << ',' << s.best_hi << "]\n";
  }
  bool ok = true;
  for (int k = 1; k <= MAX_K; ++k) ok = ok && stats[k].best_run < 68;
  std::cout << "CONCLUSION no maximal Sidon set of size <=6 in [1,n] for 68<=n<="
            << MAX_N << ": " << (ok ? "CERTIFIED" : "FAILED") << "\n";
  return ok ? 0 : 1;
}
