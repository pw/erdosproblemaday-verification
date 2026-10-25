#include <array>
#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

namespace {

constexpr int kMaximumMark = 101;
constexpr int kMaximumSize = 6;
constexpr int kDifferenceBits = 3 * kMaximumMark + 2;

struct Stats {
  std::uint64_t raw = 0;
  std::uint64_t sidon = 0;
  std::uint64_t hull_covered = 0;
  int best_run = 0;
  int best_lo = 0;
  int best_hi = -1;
  std::vector<int> best_marks;
};

std::array<int, kMaximumSize> marks{};
std::array<Stats, kMaximumSize + 1> stats{};

bool leaf_is_sidon(int size, std::bitset<kDifferenceBits>& differences) {
  differences.reset();
  for (int right = 1; right < size; ++right) {
    for (int left = 0; left < right; ++left) {
      const int difference = marks[right] - marks[left];
      if (differences.test(difference)) return false;
      differences.set(difference);
    }
  }
  return true;
}

// This deliberately tests insertion from first principles. It does not construct
// the algebraic blocked set used by either frozen enumerator.
bool insertion_breaks_sidon(int size, int x,
                            const std::bitset<kDifferenceBits>& old_differences) {
  std::bitset<kDifferenceBits> differences = old_differences;
  for (int i = 0; i < size; ++i) {
    int difference = x - marks[i];
    if (difference == 0) return true;
    if (difference < 0) difference = -difference;
    if (differences.test(difference)) return true;
    differences.set(difference);
  }
  return false;
}

void evaluate(int size) {
  Stats& current = stats[size];
  ++current.raw;

  std::bitset<kDifferenceBits> old_differences;
  if (!leaf_is_sidon(size, old_differences)) return;
  ++current.sidon;

  const int maximum = marks[size - 1];
  for (int x = 0; x <= maximum; ++x) {
    if (!insertion_breaks_sidon(size, x, old_differences)) return;
  }
  ++current.hull_covered;

  int lo = 0;
  while (insertion_breaks_sidon(size, lo - 1, old_differences)) --lo;
  int hi = maximum;
  while (insertion_breaks_sidon(size, hi + 1, old_differences)) ++hi;
  const int run = hi - lo + 1;
  if (run > current.best_run) {
    current.best_run = run;
    current.best_lo = lo;
    current.best_hi = hi;
    current.best_marks.assign(marks.begin(), marks.begin() + size);
  }
}

// Enumerate every tail combination. No partial Sidon test or prefix pruning is
// performed, unlike both frozen C++ searches.
void combinations(int size, int used, int next) {
  if (used == size) {
    evaluate(size);
    return;
  }
  const int positions_after = size - used - 1;
  for (int x = next; x <= kMaximumMark - positions_after; ++x) {
    marks[used] = x;
    combinations(size, used + 1, x + 1);
  }
}

void print_marks(const std::vector<int>& values) {
  std::cout << '{';
  for (std::size_t i = 0; i < values.size(); ++i) {
    if (i != 0) std::cout << ',';
    std::cout << values[i];
  }
  std::cout << '}';
}

}  // namespace

int main() {
  marks[0] = 0;
  for (int size = 1; size <= kMaximumSize; ++size) {
    combinations(size, 1, 1);
  }

  constexpr std::array<std::uint64_t, kMaximumSize + 1> expected_raw = {
      0, 1, 101, 5050, 166650, 4082925, 79208745};
  constexpr std::array<std::uint64_t, kMaximumSize + 1> expected_sidon = {
      0, 1, 101, 5000, 156816, 3316012, 46198688};
  constexpr std::array<std::uint64_t, kMaximumSize + 1> expected_covered = {
      0, 1, 2, 8, 76, 1102, 20166};
  constexpr std::array<int, kMaximumSize + 1> expected_best = {
      0, 1, 4, 10, 22, 42, 67};

  bool passed = true;
  for (int size = 1; size <= kMaximumSize; ++size) {
    const Stats& current = stats[size];
    std::cout << "k=" << size << " raw=" << current.raw
              << " sidon=" << current.sidon
              << " hull_covered=" << current.hull_covered
              << " best_run=" << current.best_run << " best_marks=";
    print_marks(current.best_marks);
    std::cout << " best_interval=[" << current.best_lo << ','
              << current.best_hi << "]\n";
    passed = passed && current.raw == expected_raw[size] &&
             current.sidon == expected_sidon[size] &&
             current.hull_covered == expected_covered[size] &&
             current.best_run == expected_best[size];
  }
  std::cout << "THIRD_ENUMERATION=" << (passed ? "PASS" : "FAIL") << '\n';
  return passed ? EXIT_SUCCESS : EXIT_FAILURE;
}
