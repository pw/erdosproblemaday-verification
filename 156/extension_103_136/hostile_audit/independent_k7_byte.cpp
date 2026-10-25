#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <tuple>
#include <vector>

namespace {

constexpr int kMarks = 7;
constexpr int kMaximum = 135;
constexpr int kSumMaximum = 2 * kMaximum;

struct State {
  std::array<int, kMarks> marks{};
  std::array<unsigned char, kMaximum + 1> differences{};
  std::array<unsigned char, kSumMaximum + 1> sums{};
};

struct Best {
  int run = 0;
  int lo = 0;
  int hi = -1;
  std::array<int, kMarks> marks{};
};

struct Totals {
  std::uint64_t endpoint_attempts = 0;
  std::uint64_t canonical_sidon = 0;
  std::uint64_t canonical_hull = 0;
  std::array<std::uint64_t, kMaximum + 1> endpoints_by_length{};
  std::array<std::uint64_t, kMaximum + 1> sidon_by_length{};
  std::array<std::uint64_t, kMaximum + 1> hull_by_length{};
  Best best;
};

bool push(State& state, int used, int value) {
  std::array<int, kMarks> inserted{};
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

  // Difference uniqueness implies these new unordered sums are all fresh.
  // Assert that equivalence at every accepted transition, then maintain the
  // sum table solely for the independent blocking calculation below.
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

bool blocked(const State& state, int candidate) {
  for (int mark : state.marks) {
    if (mark == candidate) return true;
  }
  const int diagonal = 2 * candidate;
  if (0 <= diagonal && diagonal <= kSumMaximum &&
      state.sums[static_cast<std::size_t>(diagonal)] != 0) {
    return true;
  }
  for (int mark : state.marks) {
    const int sum = candidate + mark;
    if (0 <= sum && sum <= kSumMaximum &&
        state.sums[static_cast<std::size_t>(sum)] != 0) {
      return true;
    }
  }
  return false;
}

bool better(const Best& candidate, const Best& incumbent) {
  if (candidate.run != incumbent.run) return candidate.run > incumbent.run;
  if (candidate.marks != incumbent.marks) {
    return candidate.marks < incumbent.marks;
  }
  return candidate.lo < incumbent.lo;
}

void consider(Totals& totals, const Best& candidate) {
  if (better(candidate, totals.best)) totals.best = candidate;
}

void evaluate_canonical(State& state, int maximum, Totals& totals) {
  ++totals.canonical_sidon;
  ++totals.sidon_by_length[static_cast<std::size_t>(maximum)];
  for (int candidate = 0; candidate <= maximum; ++candidate) {
    if (!blocked(state, candidate)) return;
  }

  ++totals.canonical_hull;
  ++totals.hull_by_length[static_cast<std::size_t>(maximum)];
  int lo = 0;
  int hi = maximum;
  while (blocked(state, lo - 1)) --lo;
  while (blocked(state, hi + 1)) ++hi;
  const int run = hi - lo + 1;
  consider(totals, Best{run, lo, hi, state.marks});

  std::array<int, kMarks> reflected{};
  for (int index = 0; index < kMarks; ++index) {
    reflected[static_cast<std::size_t>(index)] =
        maximum - state.marks[static_cast<std::size_t>(kMarks - 1 - index)];
  }
  consider(totals,
           Best{run, maximum - hi, maximum - lo, reflected});
}

void choose(State& state, int maximum, int used, int next, Totals& totals) {
  if (used == kMarks - 1) {
    ++totals.endpoint_attempts;
    ++totals.endpoints_by_length[static_cast<std::size_t>(maximum)];

    // Every successful ruler and its reflection have opposite first/last-gap
    // ordering. Equal gaps already repeat a difference. Test only the unique
    // canonical orientation, while counting all valid-prefix endpoint tries.
    const int last_gap = maximum - state.marks[kMarks - 2];
    if (state.marks[1] >= last_gap) return;
    if (!push(state, used, maximum)) return;
    evaluate_canonical(state, maximum, totals);
    pop(state, used, maximum);
    return;
  }

  const int interiors_after = (kMarks - 1) - (used + 1);
  const int last = maximum - 1 - interiors_after;
  for (int value = next; value <= last; ++value) {
    if (!push(state, used, value)) continue;
    choose(state, maximum, used + 1, value + 1, totals);
    pop(state, used, value);
  }
}

void merge(Totals& destination, const Totals& source) {
  destination.endpoint_attempts += source.endpoint_attempts;
  destination.canonical_sidon += source.canonical_sidon;
  destination.canonical_hull += source.canonical_hull;
  for (int length = 0; length <= kMaximum; ++length) {
    destination.endpoints_by_length[static_cast<std::size_t>(length)] +=
        source.endpoints_by_length[static_cast<std::size_t>(length)];
    destination.sidon_by_length[static_cast<std::size_t>(length)] +=
        source.sidon_by_length[static_cast<std::size_t>(length)];
    destination.hull_by_length[static_cast<std::size_t>(length)] +=
        source.hull_by_length[static_cast<std::size_t>(length)];
  }
  if (better(source.best, destination.best)) destination.best = source.best;
}

std::string display(const std::array<int, kMarks>& marks) {
  std::string result = "{";
  for (int index = 0; index < kMarks; ++index) {
    if (index != 0) result += ',';
    result += std::to_string(marks[static_cast<std::size_t>(index)]);
  }
  return result + '}';
}

}  // namespace

int main() {
  std::vector<std::tuple<int, int, int>> tasks;
  for (int maximum = kMarks - 1; maximum <= kMaximum; ++maximum) {
    for (int first = 1; first <= maximum - 5; ++first) {
      for (int second = first + 1; second <= maximum - 4; ++second) {
        if (second != 2 * first) tasks.emplace_back(maximum, first, second);
      }
    }
  }

  Totals total;
#pragma omp parallel
  {
    Totals thread_total;
#pragma omp for schedule(dynamic, 4)
    for (std::size_t task_index = 0; task_index < tasks.size(); ++task_index) {
      const auto [maximum, first, second] = tasks[task_index];
      State state;
      state.marks[0] = 0;
      state.sums[0] = 1;
      const bool first_ok = push(state, 1, first);
      const bool second_ok = first_ok && push(state, 2, second);
      assert(first_ok && second_ok);
      choose(state, maximum, 3, second + 1, thread_total);
    }
#pragma omp critical
    merge(total, thread_total);
  }

  std::uint64_t new_hull = 0;
  for (int length = 102; length <= kMaximum; ++length) {
    new_hull += 2 * total.hull_by_length[static_cast<std::size_t>(length)];
  }
  const std::uint64_t full_sidon = 2 * total.canonical_sidon;
  const std::uint64_t full_hull = 2 * total.canonical_hull;
  std::cout << "prefix3_tasks=" << tasks.size()
            << " endpoint_attempts=" << total.endpoint_attempts
            << " canonical_sidon=" << total.canonical_sidon
            << " full_sidon=" << full_sidon
            << " canonical_hull=" << total.canonical_hull
            << " full_hull=" << full_hull
            << " hull_with_length_102_135=" << new_hull << '\n';
  std::cout << "best_run=" << total.best.run
            << " best_marks=" << display(total.best.marks)
            << " best_interval=[" << total.best.lo << ',' << total.best.hi
            << "]\n";

  const bool pass = total.endpoint_attempts == UINT64_C(4664137760) &&
                    full_sidon == UINT64_C(3188523904) &&
                    full_hull == UINT64_C(455390) && new_hull == 0 &&
                    total.best.run == 101 && total.best.lo == -17 &&
                    total.best.hi == 83 &&
                    total.best.marks ==
                        std::array<int, kMarks>{0, 24, 27, 35, 39, 41, 75};
  std::cout << "INDEPENDENT_BYTE_SYMMETRY_K7=" << (pass ? "PASS" : "FAIL")
            << '\n';
  return pass ? EXIT_SUCCESS : EXIT_FAILURE;
}
