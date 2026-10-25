#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <mutex>
#include <vector>

#include <omp.h>

namespace {

constexpr int kSize = 7;
constexpr int kMaximumMark = 101;
constexpr int kDifferenceBits = 3 * kMaximumMark + 2;

struct Best {
  int run = 0;
  int lo = 0;
  int hi = -1;
  std::array<int, kSize> marks{};
};

struct Search {
  std::array<int, kSize> marks{};
  std::uint64_t raw = 0;
  std::uint64_t sidon = 0;
  std::uint64_t hull_covered = 0;
  Best best;
  std::array<Best, kMaximumMark + 1> best_by_maximum{};
};

std::uint64_t total_raw = 0;
std::uint64_t total_sidon = 0;
std::uint64_t total_hull_covered = 0;
Best global_best;
std::array<Best, kMaximumMark + 1> global_best_by_maximum{};
std::mutex merge_mutex;

bool better(const Best& candidate, const Best& incumbent) {
  if (candidate.run != incumbent.run) return candidate.run > incumbent.run;
  if (candidate.marks != incumbent.marks) {
    return candidate.marks < incumbent.marks;
  }
  return candidate.lo < incumbent.lo;
}

bool leaf_is_sidon(
    const std::array<int, kSize>& marks,
    std::bitset<kDifferenceBits>& old_differences) {
  old_differences.reset();
  for (int right = 1; right < kSize; ++right) {
    for (int left = 0; left < right; ++left) {
      const int difference = marks[right] - marks[left];
      if (old_differences.test(static_cast<std::size_t>(difference))) {
        return false;
      }
      old_differences.set(static_cast<std::size_t>(difference));
    }
  }
  return true;
}

// Test the defining positive-difference condition after inserting x.  This
// deliberately does not use the algebraic blocked-set formula.
bool insertion_breaks_sidon(
    const std::array<int, kSize>& marks, int x,
    const std::bitset<kDifferenceBits>& old_differences) {
  std::bitset<kDifferenceBits> differences = old_differences;
  for (int mark : marks) {
    int difference = x - mark;
    if (difference == 0) return true;
    if (difference < 0) difference = -difference;
    const std::size_t index = static_cast<std::size_t>(difference);
    if (differences.test(index)) return true;
    differences.set(index);
  }
  return false;
}

void evaluate(Search& search) {
  ++search.raw;
  std::bitset<kDifferenceBits> old_differences;
  if (!leaf_is_sidon(search.marks, old_differences)) return;
  ++search.sidon;

  const int maximum = search.marks.back();
  for (int x = 0; x <= maximum; ++x) {
    if (!insertion_breaks_sidon(search.marks, x, old_differences)) return;
  }
  ++search.hull_covered;

  int lo = 0;
  while (insertion_breaks_sidon(search.marks, lo - 1, old_differences)) --lo;
  int hi = maximum;
  while (insertion_breaks_sidon(search.marks, hi + 1, old_differences)) ++hi;

  Best candidate;
  candidate.run = hi - lo + 1;
  candidate.lo = lo;
  candidate.hi = hi;
  candidate.marks = search.marks;
  if (better(candidate, search.best)) search.best = candidate;
  if (better(candidate, search.best_by_maximum[maximum])) {
    search.best_by_maximum[maximum] = candidate;
  }
}

// Visit full combinations only.  There is intentionally no partial Sidon
// check and no fixed-maximum normalization used by the production search.
void combinations(Search& search, int used, int next) {
  if (used == kSize) {
    evaluate(search);
    return;
  }
  const int positions_after = kSize - used - 1;
  for (int x = next; x <= kMaximumMark - positions_after; ++x) {
    search.marks[used] = x;
    combinations(search, used + 1, x + 1);
  }
}

void merge(const Search& search) {
  std::lock_guard<std::mutex> lock(merge_mutex);
  total_raw += search.raw;
  total_sidon += search.sidon;
  total_hull_covered += search.hull_covered;
  if (better(search.best, global_best)) global_best = search.best;
  for (int maximum = 0; maximum <= kMaximumMark; ++maximum) {
    if (better(search.best_by_maximum[maximum],
               global_best_by_maximum[maximum])) {
      global_best_by_maximum[maximum] = search.best_by_maximum[maximum];
    }
  }
}

void print_marks(const std::array<int, kSize>& marks) {
  std::cout << '{';
  for (int index = 0; index < kSize; ++index) {
    if (index != 0) std::cout << ',';
    std::cout << marks[index];
  }
  std::cout << '}';
}

}  // namespace

int main() {
#pragma omp parallel for schedule(dynamic, 1)
  for (int first = 1; first <= kMaximumMark - (kSize - 2); ++first) {
    Search search;
    search.marks[0] = 0;
    search.marks[1] = first;
    combinations(search, 2, first + 1);
    merge(search);
  }

  std::cout << "raw=" << total_raw << " sidon=" << total_sidon
            << " hull_covered=" << total_hull_covered
            << " best_run=" << global_best.run << " best_marks=";
  print_marks(global_best.marks);
  std::cout << " best_interval=[" << global_best.lo << ',' << global_best.hi
            << "]\n";

  int covered_through = 67;
  for (int n = 68; n <= 101; ++n) {
    bool covered = false;
    for (int maximum = kSize - 1; maximum <= n - 1; ++maximum) {
      if (global_best_by_maximum[maximum].run >= n) {
        covered = true;
        break;
      }
    }
    if (!covered) break;
    covered_through = n;
  }
  std::cout << "seven_mark_upper_bound_contiguous_through="
            << covered_through << '\n';

  constexpr std::array<int, kSize> expected_marks =
      {0, 24, 27, 35, 39, 41, 75};
  const bool passed =
      total_raw == 1267339920ULL && total_sidon == 386623922ULL &&
      total_hull_covered == 455390ULL && global_best.run == 101 &&
      global_best.lo == -17 && global_best.hi == 83 &&
      global_best.marks == expected_marks && covered_through == 101;
  std::cout << "HOSTILE_DIRECT_ENUMERATION="
            << (passed ? "PASS" : "FAIL") << '\n';
  return passed ? EXIT_SUCCESS : EXIT_FAILURE;
}
