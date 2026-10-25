#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = std::uint64_t;

struct Occurrence {
  std::uint8_t word;
  std::uint8_t offset;
};

class SubsequenceCounter {
 public:
  explicit SubsequenceCounter(int n) : n_(n), by_symbol_(n) {
    for (int step = 1; 3 * step < n_; ++step) {
      for (int start = 0; start + 3 * step < n_; ++start) {
        const std::array<int, 4> forward{
            start, start + step, start + 2 * step, start + 3 * step};
        AddWord(forward);
        AddWord({forward[3], forward[2], forward[1], forward[0]});
      }
    }
    progress_.assign(words_.size(), 0);
  }

  u64 CountAll() {
    if (n_ < 3) return Search(0, 0);

    struct Prefix {
      int a;
      int b;
      int c;
    };
    std::vector<Prefix> prefixes;
    for (int a = 0; a < n_; ++a) {
      for (int b = 0; b < n_; ++b) {
        if (b == a) continue;
        for (int c = 0; c < n_; ++c) {
          if (c == a || c == b) continue;
          prefixes.push_back({a, b, c});
        }
      }
    }

    u64 total = 0;
#pragma omp parallel for schedule(dynamic, 1) reduction(+ : total)
    for (std::size_t i = 0; i < prefixes.size(); ++i) {
      SubsequenceCounter local(n_);
      const Prefix p = prefixes[i];
      if (!local.Push(p.a) || !local.Push(p.b) || !local.Push(p.c)) {
        throw std::logic_error("a three-symbol prefix completed a four-symbol word");
      }
      const std::uint32_t used = (1u << p.a) | (1u << p.b) | (1u << p.c);
      total += local.Search(3, used);
    }
    return total;
  }

  int WordCount() const { return static_cast<int>(words_.size()); }

 private:
  void AddWord(const std::array<int, 4>& values) {
    if (words_.size() >= 256) throw std::logic_error("word id does not fit in one byte");
    const std::uint8_t id = static_cast<std::uint8_t>(words_.size());
    words_.push_back(values);
    for (std::uint8_t offset = 0; offset < 4; ++offset) {
      by_symbol_[values[offset]].push_back({id, offset});
    }
  }

  bool Push(int symbol) {
    for (const Occurrence occurrence : by_symbol_[symbol]) {
      if (progress_[occurrence.word] == occurrence.offset && occurrence.offset == 3) {
        return false;
      }
    }
    for (const Occurrence occurrence : by_symbol_[symbol]) {
      if (progress_[occurrence.word] == occurrence.offset) {
        ++progress_[occurrence.word];
      }
    }
    return true;
  }

  void Pop(int symbol) {
    for (const Occurrence occurrence : by_symbol_[symbol]) {
      if (progress_[occurrence.word] == occurrence.offset + 1) {
        --progress_[occurrence.word];
      }
    }
  }

  u64 Search(int depth, std::uint32_t used) {
    if (depth == n_) return 1;
    u64 result = 0;
    for (int symbol = 0; symbol < n_; ++symbol) {
      const std::uint32_t bit = 1u << symbol;
      if ((used & bit) != 0 || !Push(symbol)) continue;
      result += Search(depth + 1, used | bit);
      Pop(symbol);
    }
    return result;
  }

  int n_;
  std::vector<std::array<int, 4>> words_;
  std::vector<std::vector<Occurrence>> by_symbol_;
  std::vector<std::uint8_t> progress_;
};

static u64 Factorial(int n) {
  u64 result = 1;
  for (int i = 2; i <= n; ++i) result *= static_cast<u64>(i);
  return result;
}

int main(int argc, char** argv) {
  int max_n = 14;
  if (argc > 1) max_n = std::atoi(argv[1]);
  if (max_n < 1 || max_n > 14) return 2;

#ifdef _OPENMP
  std::cout << "threads=" << omp_get_max_threads() << '\n';
#else
  std::cout << "threads=1\n";
#endif
  for (int n = 1; n <= max_n; ++n) {
    SubsequenceCounter counter(n);
    const auto start = std::chrono::steady_clock::now();
    const u64 count = counter.CountAll();
    const auto stop = std::chrono::steady_clock::now();
    if (count > Factorial(n)) throw std::overflow_error("count exceeded n!");
    const double seconds =
        std::chrono::duration_cast<std::chrono::duration<double>>(stop - start).count();
    std::cout << "n=" << n << " oriented_words=" << counter.WordCount()
              << " theta4=" << count << " seconds=" << seconds << '\n';
  }
}
