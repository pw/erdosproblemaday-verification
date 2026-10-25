#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <iostream>
#include <mutex>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int kMaxMarks = 6;
constexpr int kMaximum = 135;
constexpr int kWords = (2 * kMaximum) / 64 + 1;
using SumMask = std::array<std::uint64_t, kWords>;

struct Local {
  std::array<int, kMaxMarks> marks{};
  std::uint64_t endpoint_tests = 0;
  std::uint64_t sidon = 0;
  std::uint64_t hull_covered = 0;
};

struct Best {
  int run = 0;
  int lo = 0;
  int hi = -1;
  std::array<int, kMaxMarks> marks{};
};

std::array<std::atomic<std::uint64_t>, kMaxMarks + 1> endpoint_tests{};
std::array<std::atomic<std::uint64_t>, kMaxMarks + 1> sidon{};
std::array<std::atomic<std::uint64_t>, kMaxMarks + 1> hull_covered{};
std::array<Best, kMaxMarks + 1> best{};
std::mutex best_mutex;
std::atomic<std::uint64_t> completed_tasks{0};

bool contains(const SumMask& sums, int value) {
  if (value < 0 || value > 2 * kMaximum) return false;
  return (sums[static_cast<std::size_t>(value / 64)] &
          (UINT64_C(1) << (value % 64))) != 0;
}

void insert(SumMask& sums, int value) {
  sums[static_cast<std::size_t>(value / 64)] |=
      UINT64_C(1) << (value % 64);
}

bool add_mark(const std::array<int, kMaxMarks>& marks, int used, int value,
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

bool blocked(const std::array<int, kMaxMarks>& marks, int count,
             const SumMask& sums, int candidate) {
  for (int index = 0; index < count; ++index) {
    if (marks[index] == candidate) return true;
  }
  if (contains(sums, 2 * candidate)) return true;
  for (int index = 0; index < count; ++index) {
    if (contains(sums, candidate + marks[index])) return true;
  }
  return false;
}

bool better(int count, int run, int lo,
            const std::array<int, kMaxMarks>& marks,
            const Best& incumbent) {
  if (run != incumbent.run) return run > incumbent.run;
  if (std::lexicographical_compare(marks.begin(), marks.begin() + count,
                                   incumbent.marks.begin(),
                                   incumbent.marks.begin() + count)) {
    return true;
  }
  if (std::equal(marks.begin(), marks.begin() + count,
                 incumbent.marks.begin())) {
    return lo < incumbent.lo;
  }
  return false;
}

void evaluate(Local& local, int count, int maximum, const SumMask& sums) {
  ++local.sidon;
  for (int value = 0; value <= maximum; ++value) {
    if (!blocked(local.marks, count, sums, value)) return;
  }
  ++local.hull_covered;
  int lo = 0;
  int hi = maximum;
  while (blocked(local.marks, count, sums, lo - 1)) --lo;
  while (blocked(local.marks, count, sums, hi + 1)) ++hi;
  const int run = hi - lo + 1;

  std::lock_guard<std::mutex> lock(best_mutex);
  if (better(count, run, lo, local.marks, best[count])) {
    best[count] = Best{run, lo, hi, local.marks};
  }
}

void choose(Local& local, int count, int maximum, int used, int next,
            const SumMask& sums) {
  if (used == count - 1) {
    ++local.endpoint_tests;
    SumMask final_sums{};
    if (!add_mark(local.marks, used, maximum, sums, final_sums)) return;
    local.marks[used] = maximum;
    evaluate(local, count, maximum, final_sums);
    return;
  }
  const int interiors_after = (count - 1) - (used + 1);
  const int last = maximum - 1 - interiors_after;
  for (int value = next; value <= last; ++value) {
    SumMask next_sums{};
    if (!add_mark(local.marks, used, value, sums, next_sums)) continue;
    local.marks[used] = value;
    choose(local, count, maximum, used + 1, value + 1, next_sums);
  }
}

std::string display(const std::array<int, kMaxMarks>& marks, int count) {
  std::string result = "{";
  for (int index = 0; index < count; ++index) {
    if (index != 0) result += ',';
    result += std::to_string(marks[index]);
  }
  return result + '}';
}

}  // namespace


int main() {
  Local singleton;
  singleton.marks[0] = 0;
  SumMask zero_sums{};
  insert(zero_sums, 0);
  evaluate(singleton, 1, 0, zero_sums);
  endpoint_tests[1] = 1;
  sidon[1] = singleton.sidon;
  hull_covered[1] = singleton.hull_covered;

  std::vector<std::tuple<int, int, int>> tasks;
  for (int count = 2; count <= kMaxMarks; ++count) {
    for (int maximum = count - 1; maximum <= kMaximum; ++maximum) {
      if (count == 2) {
        tasks.emplace_back(count, maximum, -1);
      } else {
        for (int first = 1; first <= maximum - (count - 2); ++first) {
          tasks.emplace_back(count, maximum, first);
        }
      }
    }
  }

#pragma omp parallel for schedule(dynamic, 1)
  for (std::size_t task = 0; task < tasks.size(); ++task) {
    const auto [count, maximum, first] = tasks[task];
    Local local;
    local.marks[0] = 0;
    if (count == 2) {
      ++local.endpoint_tests;
      SumMask sums{};
      insert(sums, 0);
      SumMask final_sums{};
      if (add_mark(local.marks, 1, maximum, sums, final_sums)) {
        local.marks[1] = maximum;
        evaluate(local, count, maximum, final_sums);
      }
    } else {
      local.marks[1] = first;
      SumMask sums{};
      insert(sums, 0);
      SumMask with_first{};
      if (add_mark(local.marks, 1, first, sums, with_first)) {
        choose(local, count, maximum, 2, first + 1, with_first);
      }
    }
    endpoint_tests[count].fetch_add(local.endpoint_tests,
                                    std::memory_order_relaxed);
    sidon[count].fetch_add(local.sidon, std::memory_order_relaxed);
    hull_covered[count].fetch_add(local.hull_covered,
                                  std::memory_order_relaxed);
    completed_tasks.fetch_add(1, std::memory_order_relaxed);
  }

  constexpr std::array<std::uint64_t, kMaxMarks + 1> expected_sidon = {
      0, 1, 135, 8978, 383262, 11347918, 233716482};
  constexpr std::array<std::uint64_t, kMaxMarks + 1> expected_hull = {
      0, 1, 2, 8, 76, 1102, 20166};
  constexpr std::array<int, kMaxMarks + 1> expected_best = {
      0, 1, 4, 10, 22, 42, 67};
  bool pass = completed_tasks.load() == tasks.size();
  for (int count = 1; count <= kMaxMarks; ++count) {
    std::cout << "k=" << count
              << " endpoint_tests=" << endpoint_tests[count].load()
              << " sidon=" << sidon[count].load()
              << " hull_covered=" << hull_covered[count].load()
              << " best_run=" << best[count].run
              << " best_marks=" << display(best[count].marks, count)
              << " best_interval=[" << best[count].lo << ','
              << best[count].hi << "]\n";
    pass = pass && sidon[count].load() == expected_sidon[count] &&
           hull_covered[count].load() == expected_hull[count] &&
           best[count].run == expected_best[count];
  }
  std::cout << "tasks=" << completed_tasks.load() << '/' << tasks.size()
            << '\n';
  std::cout << "SIZE_LE_6_PAIR_SUM_ENUMERATION="
            << (pass ? "PASS" : "FAIL") << '\n';
  return pass ? 0 : 1;
}
