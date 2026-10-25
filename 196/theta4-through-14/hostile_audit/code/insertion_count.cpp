#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = std::uint64_t;

static bool NewMaximumIsSafe(const std::vector<std::uint8_t>& word, int slot) {
  const int maximum = static_cast<int>(word.size());
  std::uint8_t position[15]{};
  for (int i = 0; i < maximum; ++i) position[word[i]] = static_cast<std::uint8_t>(i);

  auto after_insertion = [slot, &position](int value) {
    const int old_position = position[value];
    return old_position + (old_position >= slot);
  };

  for (int step = 1; maximum - 3 * step >= 0; ++step) {
    const int p0 = after_insertion(maximum - 3 * step);
    const int p1 = after_insertion(maximum - 2 * step);
    const int p2 = after_insertion(maximum - step);
    if ((p0 < p1 && p1 < p2 && p2 < slot) ||
        (slot < p2 && p2 < p1 && p1 < p0)) {
      return false;
    }
  }
  return true;
}

static void Grow(std::vector<std::uint8_t>& word, int target, u64& leaves) {
  if (static_cast<int>(word.size()) == target) {
    ++leaves;
    return;
  }
  const std::uint8_t maximum = static_cast<std::uint8_t>(word.size());
  for (int slot = 0; slot <= maximum; ++slot) {
    if (!NewMaximumIsSafe(word, slot)) continue;
    word.insert(word.begin() + slot, maximum);
    Grow(word, target, leaves);
    word.erase(word.begin() + slot);
  }
}

static std::vector<std::vector<std::uint8_t>> AvoidersAt(int target) {
  std::vector<std::vector<std::uint8_t>> current{{0}};
  for (int size = 2; size <= target; ++size) {
    std::vector<std::vector<std::uint8_t>> next;
    for (const auto& word : current) {
      for (int slot = 0; slot < size; ++slot) {
        if (!NewMaximumIsSafe(word, slot)) continue;
        auto child = word;
        child.insert(child.begin() + slot, static_cast<std::uint8_t>(size - 1));
        next.push_back(std::move(child));
      }
    }
    current = std::move(next);
  }
  return current;
}

static u64 CountByInsertion(int target) {
  if (target == 1) return 1;
  const int split_size = std::min(target, 8);
  const auto roots = AvoidersAt(split_size);
  u64 total = 0;
#pragma omp parallel for schedule(dynamic, 1) reduction(+ : total)
  for (std::size_t i = 0; i < roots.size(); ++i) {
    auto word = roots[i];
    u64 leaves = 0;
    Grow(word, target, leaves);
    total += leaves;
  }
  return total;
}

int main(int argc, char** argv) {
  int max_n = 12;
  if (argc > 1) max_n = std::atoi(argv[1]);
  if (max_n < 1 || max_n > 14) return 2;

#ifdef _OPENMP
  std::cout << "threads=" << omp_get_max_threads() << '\n';
#else
  std::cout << "threads=1\n";
#endif
  for (int n = 1; n <= max_n; ++n) {
    const auto start = std::chrono::steady_clock::now();
    const u64 count = CountByInsertion(n);
    const auto stop = std::chrono::steady_clock::now();
    const double seconds =
        std::chrono::duration_cast<std::chrono::duration<double>>(stop - start).count();
    std::cout << "n=" << n << " theta4=" << count << " seconds=" << seconds << '\n';
  }
}
