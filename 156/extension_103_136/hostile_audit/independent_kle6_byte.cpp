#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <utility>
#include <vector>

namespace {

constexpr int kMaxMarks = 6;
constexpr int kMaximum = 135;
constexpr int kSumMaximum = 2 * kMaximum;

struct State {
  std::array<int, kMaxMarks> marks{};
  std::array<unsigned char, kMaximum + 1> differences{};
  std::array<unsigned char, kSumMaximum + 1> sums{};
};

struct Best {
  int run = 0;
  int lo = 0;
  int hi = -1;
  std::array<int, kMaxMarks> marks{};
};

struct Totals {
  std::array<std::uint64_t, kMaxMarks + 1> endpoint_attempts{};
  std::array<std::uint64_t, kMaxMarks + 1> canonical_sidon{};
  std::array<std::uint64_t, kMaxMarks + 1> canonical_hull{};
  std::array<Best, kMaxMarks + 1> best{};
};

bool push(State& state, int used, int value) {
  std::array<int, kMaxMarks> inserted{};
  int inserted_count = 0;
  for (int index = 0; index < used; ++index) {
    const int difference = value - state.marks[index];
    assert(1 <= difference && difference <= kMaximum);
    if (state.differences[static_cast<std::size_t>(difference)] != 0) {
      for (int undo = 0; undo < inserted_count; ++undo) {
        state.differences[static_cast<std::size_t>(inserted[undo])] = 0;
      }
      return false;
    }
    state.differences[static_cast<std::size_t>(difference)] = 1;
    inserted[inserted_count++] = difference;
  }
  for (int index = 0; index < used; ++index) {
    const int sum = value + state.marks[index];
    assert(state.sums[static_cast<std::size_t>(sum)] == 0);
    state.sums[static_cast<std::size_t>(sum)] = 1;
  }
  assert(state.sums[static_cast<std::size_t>(2 * value)] == 0);
  state.sums[static_cast<std::size_t>(2 * value)] = 1;
  state.marks[static_cast<std::size_t>(used)] = value;
  return true;
}

void pop(State& state, int used, int value) {
  for (int index = 0; index < used; ++index) {
    const int difference = value - state.marks[index];
    assert(state.differences[static_cast<std::size_t>(difference)] != 0);
    state.differences[static_cast<std::size_t>(difference)] = 0;
    const int sum = value + state.marks[index];
    assert(state.sums[static_cast<std::size_t>(sum)] != 0);
    state.sums[static_cast<std::size_t>(sum)] = 0;
  }
  assert(state.sums[static_cast<std::size_t>(2 * value)] != 0);
  state.sums[static_cast<std::size_t>(2 * value)] = 0;
}

bool blocked(const State& state, int count, int candidate) {
  for (int index = 0; index < count; ++index) {
    if (state.marks[static_cast<std::size_t>(index)] == candidate) return true;
  }
  const int diagonal = 2 * candidate;
  if (0 <= diagonal && diagonal <= kSumMaximum &&
      state.sums[static_cast<std::size_t>(diagonal)] != 0) {
    return true;
  }
  for (int index = 0; index < count; ++index) {
    const int sum = candidate + state.marks[static_cast<std::size_t>(index)];
    if (0 <= sum && sum <= kSumMaximum &&
        state.sums[static_cast<std::size_t>(sum)] != 0) {
      return true;
    }
  }
  return false;
}

bool better(const Best& candidate, const Best& incumbent, int count) {
  if (candidate.run != incumbent.run) return candidate.run > incumbent.run;
  if (!std::equal(candidate.marks.begin(), candidate.marks.begin() + count,
                  incumbent.marks.begin())) {
    return std::lexicographical_compare(
        candidate.marks.begin(), candidate.marks.begin() + count,
        incumbent.marks.begin(), incumbent.marks.begin() + count);
  }
  return candidate.lo < incumbent.lo;
}

void consider(Totals& totals, int count, const Best& candidate) {
  if (better(candidate, totals.best[static_cast<std::size_t>(count)], count)) {
    totals.best[static_cast<std::size_t>(count)] = candidate;
  }
}

void evaluate(State& state, int count, Totals& totals, bool include_reflection) {
  const int maximum = state.marks[static_cast<std::size_t>(count - 1)];
  ++totals.canonical_sidon[static_cast<std::size_t>(count)];
  for (int candidate = 0; candidate <= maximum; ++candidate) {
    if (!blocked(state, count, candidate)) return;
  }
  ++totals.canonical_hull[static_cast<std::size_t>(count)];
  int lo = 0;
  int hi = maximum;
  while (blocked(state, count, lo - 1)) --lo;
  while (blocked(state, count, hi + 1)) ++hi;
  const int run = hi - lo + 1;
  consider(totals, count, Best{run, lo, hi, state.marks});
  if (!include_reflection) return;

  std::array<int, kMaxMarks> reflected{};
  for (int index = 0; index < count; ++index) {
    reflected[static_cast<std::size_t>(index)] =
        maximum - state.marks[static_cast<std::size_t>(count - 1 - index)];
  }
  consider(totals, count,
           Best{run, maximum - hi, maximum - lo, reflected});
}

void visit(State& state, int used, int next, Totals& totals) {
  assert(3 <= used && used <= kMaxMarks);
  const int maximum = state.marks[static_cast<std::size_t>(used - 1)];
  const int first_gap = state.marks[1];
  const int last_gap = maximum - state.marks[static_cast<std::size_t>(used - 2)];
  assert(first_gap != last_gap);
  if (first_gap < last_gap) evaluate(state, used, totals, true);
  if (used == kMaxMarks) return;

  for (int value = next; value <= kMaximum; ++value) {
    ++totals.endpoint_attempts[static_cast<std::size_t>(used + 1)];
    if (!push(state, used, value)) continue;
    visit(state, used + 1, value + 1, totals);
    pop(state, used, value);
  }
}

void merge(Totals& destination, const Totals& source) {
  for (int count = 1; count <= kMaxMarks; ++count) {
    destination.endpoint_attempts[static_cast<std::size_t>(count)] +=
        source.endpoint_attempts[static_cast<std::size_t>(count)];
    destination.canonical_sidon[static_cast<std::size_t>(count)] +=
        source.canonical_sidon[static_cast<std::size_t>(count)];
    destination.canonical_hull[static_cast<std::size_t>(count)] +=
        source.canonical_hull[static_cast<std::size_t>(count)];
    if (better(source.best[static_cast<std::size_t>(count)],
               destination.best[static_cast<std::size_t>(count)], count)) {
      destination.best[static_cast<std::size_t>(count)] =
          source.best[static_cast<std::size_t>(count)];
    }
  }
}

std::string display(const std::array<int, kMaxMarks>& marks, int count) {
  std::string result = "{";
  for (int index = 0; index < count; ++index) {
    if (index != 0) result += ',';
    result += std::to_string(marks[static_cast<std::size_t>(index)]);
  }
  return result + '}';
}

}  // namespace

int main() {
  Totals total;
  total.endpoint_attempts[1] = 1;
  total.canonical_sidon[1] = 1;
  total.canonical_hull[1] = 1;
  total.best[1] = Best{1, 0, 0, {}};
  total.endpoint_attempts[2] = kMaximum;
  for (int maximum = 1; maximum <= kMaximum; ++maximum) {
    State pair_state;
    pair_state.marks[0] = 0;
    pair_state.sums[0] = 1;
    const bool ok = push(pair_state, 1, maximum);
    assert(ok);
    evaluate(pair_state, 2, total, false);
  }

  std::vector<std::pair<int, int>> pair_tasks;
  for (int first = 1; first < kMaximum; ++first) {
    for (int second = first + 1; second <= kMaximum; ++second) {
      pair_tasks.emplace_back(first, second);
    }
  }
#pragma omp parallel
  {
    Totals thread_total;
#pragma omp for schedule(dynamic, 1)
    for (std::size_t task_index = 0; task_index < pair_tasks.size();
         ++task_index) {
      const auto [first, second] = pair_tasks[task_index];
      State state;
      state.marks[0] = 0;
      state.sums[0] = 1;
      const bool first_ok = push(state, 1, first);
      assert(first_ok);
      ++thread_total.endpoint_attempts[3];
      if (!push(state, 2, second)) continue;
      visit(state, 3, second + 1, thread_total);
    }
#pragma omp critical
    merge(total, thread_total);
  }

  constexpr std::array<std::uint64_t, kMaxMarks + 1> expected_attempts = {
      0, 1, 135, 9045, 396506, 12452396, 285696286};
  constexpr std::array<std::uint64_t, kMaxMarks + 1> expected_sidon = {
      0, 1, 135, 8978, 383262, 11347918, 233716482};
  constexpr std::array<std::uint64_t, kMaxMarks + 1> expected_hull = {
      0, 1, 2, 8, 76, 1102, 20166};
  constexpr std::array<int, kMaxMarks + 1> expected_best = {
      0, 1, 4, 10, 22, 42, 67};
  bool pass = true;
  for (int count = 1; count <= kMaxMarks; ++count) {
    const std::uint64_t sidon = count <= 2
                                    ? total.canonical_sidon[count]
                                    : 2 * total.canonical_sidon[count];
    const std::uint64_t hull = count <= 2
                                   ? total.canonical_hull[count]
                                   : 2 * total.canonical_hull[count];
    const Best& best = total.best[static_cast<std::size_t>(count)];
    std::cout << "k=" << count
              << " endpoint_attempts=" << total.endpoint_attempts[count]
              << " sidon=" << sidon << " hull_covered=" << hull
              << " best_run=" << best.run
              << " best_marks=" << display(best.marks, count)
              << " best_interval=[" << best.lo << ',' << best.hi << "]\n";
    pass = pass && total.endpoint_attempts[count] == expected_attempts[count] &&
           sidon == expected_sidon[count] && hull == expected_hull[count] &&
           best.run == expected_best[count];
  }
  std::cout << "INDEPENDENT_BYTE_SYMMETRY_KLE6="
            << (pass ? "PASS" : "FAIL") << '\n';
  return pass ? EXIT_SUCCESS : EXIT_FAILURE;
}
