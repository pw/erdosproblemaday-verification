#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <mutex>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kMarks = 7;
#ifndef VERIFY_156_K7_MAXIMUM
#define VERIFY_156_K7_MAXIMUM 105
#endif
constexpr int kMaximum = VERIFY_156_K7_MAXIMUM;
constexpr int kOffset = kMaximum + 1;
constexpr int kStampSize = 3 * kMaximum + 3;
using u128 = unsigned __int128;

struct LocalSearch {
  std::array<int, kMarks> marks{};
  std::array<std::uint32_t, kStampSize> stamp{};
  std::uint32_t generation = 0;
  std::uint64_t endpoint_tests = 0;
  std::uint64_t golomb = 0;
  std::uint64_t hull_covered = 0;
};

struct Best {
  int run = 0;
  int lo = 0;
  int hi = -1;
  std::array<int, kMarks> marks{};
};

std::atomic<std::uint64_t> total_endpoint_tests{0};
std::atomic<std::uint64_t> total_golomb{0};
std::atomic<std::uint64_t> total_hull_covered{0};
std::atomic<std::uint64_t> completed_tasks{0};
std::mutex best_mutex;
Best best;
std::array<Best, kMaximum + 1> best_by_maximum{};

bool better_candidate(int run, int lo,
                      const std::array<int, kMarks>& marks,
                      const Best& incumbent) {
  if (run != incumbent.run) return run > incumbent.run;
  if (marks != incumbent.marks) return marks < incumbent.marks;
  return lo < incumbent.lo;
}

bool add_mark(const std::array<int, kMarks>& marks, int used, int value,
              u128 old_mask, u128& new_mask) {
  u128 added = 0;
  for (int index = 0; index < used; ++index) {
    const int difference = value - marks[index];
    const u128 bit = static_cast<u128>(1) << difference;
    if ((old_mask & bit) != 0 || (added & bit) != 0) return false;
    added |= bit;
  }
  new_mask = old_mask | added;
  return true;
}

void evaluate(LocalSearch& search, int maximum, u128 differences) {
  ++search.golomb;
  ++search.generation;
  if (search.generation == 0) {
    search.stamp.fill(0);
    ++search.generation;
  }
  const std::uint32_t generation = search.generation;
  auto block = [&](int value) {
    search.stamp[value + kOffset] = generation;
  };
  auto blocked = [&](int value) {
    return search.stamp[value + kOffset] == generation;
  };

  for (int mark : search.marks) block(mark);
  for (int difference = 1; difference <= maximum; ++difference) {
    if ((differences & (static_cast<u128>(1) << difference)) == 0) continue;
    for (int mark : search.marks) {
      block(mark - difference);
      block(mark + difference);
    }
  }
  for (int left = 0; left < kMarks; ++left) {
    for (int right = left + 1; right < kMarks; ++right) {
      const int sum = search.marks[left] + search.marks[right];
      if ((sum & 1) == 0) block(sum / 2);
    }
  }

  for (int value = 0; value <= maximum; ++value) {
    if (!blocked(value)) return;
  }
  ++search.hull_covered;
  int lo = 0;
  int hi = maximum;
  while (blocked(lo - 1)) --lo;
  while (blocked(hi + 1)) ++hi;
  const int run = hi - lo + 1;

  std::lock_guard<std::mutex> lock(best_mutex);
  if (better_candidate(run, lo, search.marks, best)) {
    best.run = run;
    best.lo = lo;
    best.hi = hi;
    best.marks = search.marks;
  }
  if (better_candidate(run, lo, search.marks,
                       best_by_maximum[maximum])) {
    best_by_maximum[maximum].run = run;
    best_by_maximum[maximum].lo = lo;
    best_by_maximum[maximum].hi = hi;
    best_by_maximum[maximum].marks = search.marks;
  }
}

void choose(LocalSearch& search, int maximum, int used, int next,
            u128 differences) {
  if (used == kMarks - 1) {
    ++search.endpoint_tests;
    u128 final_differences = 0;
    if (!add_mark(search.marks, used, maximum, differences,
                  final_differences)) {
      return;
    }
    search.marks[used] = maximum;
    evaluate(search, maximum, final_differences);
    return;
  }

  const int interiors_after_choice = (kMarks - 1) - (used + 1);
  const int last_choice = maximum - 1 - interiors_after_choice;
  for (int value = next; value <= last_choice; ++value) {
    u128 next_differences = 0;
    if (!add_mark(search.marks, used, value, differences,
                  next_differences)) {
      continue;
    }
    search.marks[used] = value;
    choose(search, maximum, used + 1, value + 1, next_differences);
  }
}

std::string display(const std::array<int, kMarks>& marks) {
  std::string result = "{";
  for (int index = 0; index < kMarks; ++index) {
    if (index != 0) result += ',';
    result += std::to_string(marks[index]);
  }
  result += '}';
  return result;
}

}  // namespace

int main() {
  std::vector<std::pair<int, int>> tasks;
  for (int maximum = kMarks - 1; maximum <= kMaximum; ++maximum) {
    for (int first = 1; first <= maximum - (kMarks - 2); ++first) {
      tasks.emplace_back(maximum, first);
    }
  }

#pragma omp parallel for schedule(dynamic, 1)
  for (std::size_t task = 0; task < tasks.size(); ++task) {
    LocalSearch search;
    search.marks[0] = 0;
    search.marks[1] = tasks[task].second;
    const u128 initial = static_cast<u128>(1) << search.marks[1];
    choose(search, tasks[task].first, 2, search.marks[1] + 1, initial);
    total_endpoint_tests.fetch_add(search.endpoint_tests,
                                   std::memory_order_relaxed);
    total_golomb.fetch_add(search.golomb, std::memory_order_relaxed);
    total_hull_covered.fetch_add(search.hull_covered,
                                 std::memory_order_relaxed);
    completed_tasks.fetch_add(1, std::memory_order_relaxed);
  }

  std::cout << "tasks=" << completed_tasks.load() << '/' << tasks.size()
            << " endpoint_tests=" << total_endpoint_tests.load()
            << " golomb=" << total_golomb.load()
            << " hull_covered=" << total_hull_covered.load()
            << " best_run=" << best.run
            << " best_marks=" << display(best.marks)
            << " best_interval=[" << best.lo << ',' << best.hi << "]\n";
  int covered_through = 67;
  for (int n = 68; n <= best.run; ++n) {
    bool covered = false;
    for (int maximum = kMarks - 1;
         maximum <= std::min(kMaximum, n - 1); ++maximum) {
      if (best_by_maximum[maximum].run >= n) {
        covered = true;
        break;
      }
    }
    if (!covered) break;
    covered_through = n;
  }
  std::cout << "seven_mark_upper_bound_contiguous_through=" << covered_through
            << "\n";
  int prefix_best = 0;
  for (int maximum = kMarks - 1; maximum <= kMaximum; ++maximum) {
    if (best_by_maximum[maximum].run > prefix_best) {
      prefix_best = best_by_maximum[maximum].run;
      std::cout << "record maximum=" << maximum
                << " run=" << prefix_best
                << " marks=" << display(best_by_maximum[maximum].marks)
                << " interval=[" << best_by_maximum[maximum].lo << ','
                << best_by_maximum[maximum].hi << "]\n";
    }
  }
  std::cout << "SEVEN_MARK_ENUMERATION_COMPLETE\n";
  bool passed = completed_tasks.load() == tasks.size();
  if constexpr (kMaximum == 101) {
    constexpr std::array<int, kMarks> expected_marks =
        {0, 24, 27, 35, 39, 41, 75};
    passed = passed && total_endpoint_tests.load() == 659485834ULL &&
             total_golomb.load() == 386623922ULL &&
             total_hull_covered.load() == 455390ULL &&
             best.run == 101 && best.lo == -17 && best.hi == 83 &&
             best.marks == expected_marks && covered_through == 101;
  }
  std::cout << "CERTIFIED=" << (passed ? "PASS" : "FAIL") << '\n';
  return passed ? EXIT_SUCCESS : EXIT_FAILURE;
}
