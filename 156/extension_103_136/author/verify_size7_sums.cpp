#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <iostream>
#include <mutex>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kMarks = 7;
#ifndef VERIFY_156_K7_MAXIMUM
#define VERIFY_156_K7_MAXIMUM 110
#endif
constexpr int kMaximum = VERIFY_156_K7_MAXIMUM;
constexpr int kWords = (2 * kMaximum) / 64 + 1;
using SumMask = std::array<std::uint64_t, kWords>;

struct Local {
  std::array<int, kMarks> marks{};
  std::uint64_t endpoint_tests = 0;
  std::uint64_t sidon = 0;
  std::uint64_t hull_covered = 0;
};

struct Best {
  int run = 0;
  int lo = 0;
  int hi = -1;
  std::array<int, kMarks> marks{};
};

std::atomic<std::uint64_t> total_endpoint_tests{0};
std::atomic<std::uint64_t> total_sidon{0};
std::atomic<std::uint64_t> total_hull_covered{0};
std::atomic<std::uint64_t> completed_tasks{0};
std::mutex best_mutex;
Best best;

bool contains(const SumMask& sums, int value) {
  if (value < 0 || value > 2 * kMaximum) return false;
  return (sums[static_cast<std::size_t>(value / 64)] &
          (UINT64_C(1) << (value % 64))) != 0;
}

void insert(SumMask& sums, int value) {
  sums[static_cast<std::size_t>(value / 64)] |=
      UINT64_C(1) << (value % 64);
}

bool add_mark(const std::array<int, kMarks>& marks, int used, int value,
              const SumMask& old_sums, SumMask& new_sums) {
  new_sums = old_sums;
  for (int index = 0; index < used; ++index) {
    const int sum = value + marks[index];
    if (contains(old_sums, sum)) return false;
    insert(new_sums, sum);
  }
  if (contains(old_sums, 2 * value)) return false;
  insert(new_sums, 2 * value);
  return true;
}

bool blocked(const std::array<int, kMarks>& marks, const SumMask& sums,
             int candidate) {
  if (std::find(marks.begin(), marks.end(), candidate) != marks.end()) {
    return true;
  }
  if (contains(sums, 2 * candidate)) return true;
  for (int mark : marks) {
    if (contains(sums, candidate + mark)) return true;
  }
  return false;
}

bool better(int run, int lo, const std::array<int, kMarks>& marks,
            const Best& incumbent) {
  if (run != incumbent.run) return run > incumbent.run;
  if (marks != incumbent.marks) return marks < incumbent.marks;
  return lo < incumbent.lo;
}

void evaluate(Local& local, int maximum, const SumMask& sums) {
  ++local.sidon;
  for (int value = 0; value <= maximum; ++value) {
    if (!blocked(local.marks, sums, value)) return;
  }
  ++local.hull_covered;
  int lo = 0;
  int hi = maximum;
  while (blocked(local.marks, sums, lo - 1)) --lo;
  while (blocked(local.marks, sums, hi + 1)) ++hi;
  const int run = hi - lo + 1;

  std::lock_guard<std::mutex> lock(best_mutex);
  if (better(run, lo, local.marks, best)) {
    best = Best{run, lo, hi, local.marks};
  }
}

void choose(Local& local, int maximum, int used, int next,
            const SumMask& sums) {
  if (used == kMarks - 1) {
    ++local.endpoint_tests;
    SumMask final_sums{};
    if (!add_mark(local.marks, used, maximum, sums, final_sums)) return;
    local.marks[used] = maximum;
    evaluate(local, maximum, final_sums);
    return;
  }

  const int interiors_after = (kMarks - 1) - (used + 1);
  const int last = maximum - 1 - interiors_after;
  for (int value = next; value <= last; ++value) {
    SumMask next_sums{};
    if (!add_mark(local.marks, used, value, sums, next_sums)) continue;
    local.marks[used] = value;
    choose(local, maximum, used + 1, value + 1, next_sums);
  }
}

std::string display(const std::array<int, kMarks>& marks) {
  std::string result = "{";
  for (int index = 0; index < kMarks; ++index) {
    if (index != 0) result += ',';
    result += std::to_string(marks[index]);
  }
  return result + '}';
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
    const auto [maximum, first] = tasks[task];
    Local local;
    local.marks[0] = 0;
    local.marks[1] = first;
    SumMask sums{};
    insert(sums, 0);
    SumMask with_first{};
    if (!add_mark(local.marks, 1, first, sums, with_first)) continue;
    choose(local, maximum, 2, first + 1, with_first);
    total_endpoint_tests.fetch_add(local.endpoint_tests,
                                   std::memory_order_relaxed);
    total_sidon.fetch_add(local.sidon, std::memory_order_relaxed);
    total_hull_covered.fetch_add(local.hull_covered,
                                 std::memory_order_relaxed);
    completed_tasks.fetch_add(1, std::memory_order_relaxed);
  }

  std::cout << "tasks=" << completed_tasks.load() << '/' << tasks.size()
            << " endpoint_tests=" << total_endpoint_tests.load()
            << " sidon=" << total_sidon.load()
            << " hull_covered=" << total_hull_covered.load()
            << " best_run=" << best.run
            << " best_marks=" << display(best.marks)
            << " best_interval=[" << best.lo << ',' << best.hi << "]\n";

  bool pass = completed_tasks.load() == tasks.size();
  if constexpr (kMaximum == 110) {
    pass = pass &&
           total_endpoint_tests.load() == UINT64_C(1181593954) &&
           total_sidon.load() == UINT64_C(728238188) &&
           total_hull_covered.load() == UINT64_C(455390) &&
           best.run == 101 && best.lo == -17 && best.hi == 83 &&
           best.marks == std::array<int, kMarks>{0, 24, 27, 35, 39, 41, 75};
  } else if constexpr (kMaximum == 135) {
    pass = pass &&
           total_endpoint_tests.load() == UINT64_C(4664137760) &&
           total_sidon.load() == UINT64_C(3188523904) &&
           total_hull_covered.load() == UINT64_C(455390) &&
           best.run == 101 && best.lo == -17 && best.hi == 83 &&
           best.marks == std::array<int, kMarks>{0, 24, 27, 35, 39, 41, 75};
  }
  std::cout << "PAIR_SUM_ENUMERATION=" << (pass ? "PASS" : "FAIL") << '\n';
  return pass ? 0 : 1;
}
