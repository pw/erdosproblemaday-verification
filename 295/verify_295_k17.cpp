// Independent exhaustive verifier for the finite frontier in Erdos problem 295.
//
// It decides whether 1 is a sum of exactly TERMS distinct unit fractions with
// every denominator at least MINIMUM.  Every branch deletion is certified with
// exact GMP rational arithmetic.  Floating point is used only to avoid an exact
// comparison when we keep (rather than delete) a branch, so rounding cannot
// create a false nonexistence result.
#include <gmpxx.h>

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <mutex>
#include <numeric>
#include <string>
#include <thread>
#include <unordered_map>
#include <utility>
#include <vector>

using std::size_t;
using std::uint64_t;

struct Counters {
  uint64_t states = 0;
  uint64_t two_states = 0;
  uint64_t scan_candidates = 0;
  uint64_t factored_states = 0;
  uint64_t divisor_states = 0;
  uint64_t divisor_candidates = 0;

  void add(const Counters& other) {
    states += other.states;
    two_states += other.two_states;
    scan_candidates += other.scan_candidates;
    factored_states += other.factored_states;
    divisor_states += other.divisor_states;
    divisor_candidates += other.divisor_candidates;
  }
};

struct TailKey {
  unsigned long lower;
  int terms;

  bool operator==(const TailKey& other) const {
    return lower == other.lower && terms == other.terms;
  }
};

struct TailHash {
  size_t operator()(const TailKey& key) const {
    return std::hash<unsigned long>{}(key.lower) ^
           (std::hash<int>{}(key.terms) << 1);
  }
};

static thread_local std::unordered_map<TailKey, mpq_class, TailHash> tail_cache;

static const mpq_class& exact_tail(unsigned long lower, int terms) {
  const TailKey key{lower, terms};
  const auto found = tail_cache.find(key);
  if (found != tail_cache.end()) return found->second;

  mpq_class sum(0);
  for (int i = 0; i < terms; ++i) sum += mpq_class(1, lower + i);
  return tail_cache.emplace(key, std::move(sum)).first->second;
}

static double approximate_tail(unsigned long lower, int terms) {
  double sum = 0.0;
  for (int i = terms - 1; i >= 0; --i)
    sum += 1.0 / static_cast<double>(lower + i);
  return sum;
}

// Sound one-sided filter: a branch is pruned only after an exact comparison.
static bool tail_is_too_small(unsigned long lower, int terms,
                              const mpq_class& remainder) {
  if (!(approximate_tail(lower, terms) < remainder.get_d())) return false;
  return exact_tail(lower, terms) < remainder;
}

static std::vector<unsigned long> small_primes;

static void make_small_primes(unsigned long limit) {
  std::vector<bool> composite(limit + 1, false);
  for (unsigned long p = 2; p <= limit; ++p) {
    if (composite[p]) continue;
    small_primes.push_back(p);
    if (p <= limit / p)
      for (unsigned long q = p * p; q <= limit; q += p) composite[q] = true;
  }
}

static mpz_class rho_step(const mpz_class& x, const mpz_class& c,
                          const mpz_class& modulus) {
  return (x * x + c) % modulus;
}

// Deterministic-restart Pollard rho.  The output is checked before it is used.
static mpz_class pollard_rho(const mpz_class& n) {
  if (n % 2 == 0) return 2;
  for (unsigned long seed = 1;; ++seed) {
    mpz_class x = 2 + seed;
    mpz_class y = x;
    const mpz_class c = 1 + 2 * seed;
    mpz_class divisor = 1;
    for (uint64_t iteration = 0; divisor == 1 && iteration < 5000000;
         ++iteration) {
      x = rho_step(x, c, n);
      y = rho_step(rho_step(y, c, n), c, n);
      mpz_class difference = x - y;
      if (difference < 0) difference = -difference;
      mpz_gcd(divisor.get_mpz_t(), difference.get_mpz_t(), n.get_mpz_t());
    }
    if (divisor > 1 && divisor < n && n % divisor == 0) return divisor;
  }
}

static void factor_recursive(const mpz_class& n, std::vector<mpz_class>& raw) {
  if (n == 1) return;
  if (mpz_probab_prime_p(n.get_mpz_t(), 64) != 0) {
    raw.push_back(n);
    return;
  }
  const mpz_class divisor = pollard_rho(n);
  factor_recursive(divisor, raw);
  factor_recursive(n / divisor, raw);
}

static std::vector<std::pair<mpz_class, int>> factor(mpz_class n) {
  const mpz_class original = n;
  std::vector<mpz_class> raw;
  for (const unsigned long p : small_primes) {
    while (n % p == 0) {
      raw.emplace_back(p);
      n /= p;
    }
    if (n == 1 || mpz_class(p) * p > n) break;
  }
  if (n > 1) factor_recursive(n, raw);
  std::sort(raw.begin(), raw.end());

  std::vector<std::pair<mpz_class, int>> answer;
  mpz_class product = 1;
  for (const mpz_class& prime : raw) {
    if (answer.empty() || answer.back().first != prime)
      answer.push_back({prime, 1});
    else
      ++answer.back().second;
    product *= prime;
  }
  if (product != original) {
    std::fprintf(stderr, "factorization product check failed\n");
    std::abort();
  }
  return answer;
}

static std::mutex factor_log_mutex;

static std::string factorization_string(
    const std::vector<std::pair<mpz_class, int>>& factors) {
  std::string result;
  for (size_t i = 0; i < factors.size(); ++i) {
    if (i) result += "*";
    result += factors[i].first.get_str();
    result += "^" + std::to_string(factors[i].second);
  }
  return result;
}

struct DivisorSearch {
  const mpz_class& a;
  const mpz_class& b;
  const mpz_class b_squared;
  const mpz_class minimum_divisor;
  const mpz_class target_residue;
  const unsigned long lower;
  Counters& counters;
  bool found = false;

  static mpz_class at_least_one(mpz_class value) {
    if (value < 1) return mpz_class(1);
    return value;
  }

  DivisorSearch(const mpz_class& a_in, const mpz_class& b_in,
                unsigned long lower_in, Counters& counters_in)
      : a(a_in),
        b(b_in),
        b_squared(b_in * b_in),
        minimum_divisor(at_least_one(mpz_class(a_in * lower_in - b_in))),
        target_residue(((-b_in) % a_in + a_in) % a_in),
        lower(lower_in),
        counters(counters_in) {}
};

static void enumerate_divisors(
    DivisorSearch& search,
    const std::vector<std::pair<mpz_class, int>>& factors, size_t index,
    const mpz_class& current) {
  if (search.found) return;
  if (index == factors.size()) {
    ++search.counters.divisor_candidates;
    if (current < search.minimum_divisor || current >= search.b ||
        current % search.a != search.target_residue)
      return;

    const mpz_class other = search.b_squared / current;
    const mpz_class x_numerator = search.b + current;
    const mpz_class y_numerator = search.b + other;
    if (x_numerator % search.a != 0 || y_numerator % search.a != 0) return;
    const mpz_class x = x_numerator / search.a;
    const mpz_class y = y_numerator / search.a;
    if (x >= search.lower && y > x) search.found = true;
    return;
  }

  mpz_class value = current;
  for (int exponent = 0; exponent <= 2 * factors[index].second; ++exponent) {
    if (value > search.b) break;
    enumerate_divisors(search, factors, index + 1, value);
    if (search.found) return;
    value *= factors[index].first;
  }
}

static bool scan_two_terms(const mpz_class& a, const mpz_class& b,
                           const mpz_class& first, const mpz_class& last,
                           Counters& counters) {
  if (a.fits_ulong_p() && b.fits_ulong_p() && first.fits_ulong_p() &&
      last.fits_ulong_p()) {
    const unsigned long av = a.get_ui();
    const unsigned long bv = b.get_ui();
    const unsigned long begin = first.get_ui();
    const unsigned long end = last.get_ui();
    for (unsigned long x = begin; x <= end; ++x) {
      ++counters.scan_candidates;
      const unsigned __int128 numerator =
          static_cast<unsigned __int128>(av) * x - bv;
      const unsigned __int128 denominator =
          static_cast<unsigned __int128>(bv) * x;
      if (denominator % numerator == 0 && denominator / numerator > x)
        return true;
    }
    return false;
  }

  for (mpz_class x = first; x <= last; ++x) {
    ++counters.scan_candidates;
    const mpz_class numerator = a * x - b;
    const mpz_class denominator = b * x;
    if (mpz_divisible_p(denominator.get_mpz_t(), numerator.get_mpz_t()) &&
        denominator / numerator > x)
      return true;
  }
  return false;
}

static bool finish_with_two(const mpq_class& remainder, unsigned long lower,
                            Counters& counters) {
  ++counters.two_states;
  const mpz_class a = remainder.get_num();
  const mpz_class b = remainder.get_den();
  mpz_class first = b / a + 1;
  if (first < lower) first = lower;
  const mpz_class last = 2 * b / a;
  if (last < first) return false;

  const mpz_class width = last - first + 1;
  constexpr unsigned long factor_threshold = 65536;
  if (width <= factor_threshold)
    return scan_two_terms(a, b, first, last, counters);

  ++counters.factored_states;
  const auto factors = factor(b);
  mpz_class divisor_count = 1;
  for (const auto& [prime, exponent] : factors)
    divisor_count *= 2 * exponent + 1;
  const mpz_class candidates_below_b = (divisor_count + 1) / 2;
  if (width < candidates_below_b)
    return scan_two_terms(a, b, first, last, counters);

  ++counters.divisor_states;
  {
    std::lock_guard<std::mutex> lock(factor_log_mutex);
    gmp_printf("DIVISOR_STATE a=%Zd b=%Zd lower=%lu width=%Zd factors=%s\n",
               a.get_mpz_t(), b.get_mpz_t(), lower, width.get_mpz_t(),
               factorization_string(factors).c_str());
    std::fflush(stdout);
  }
  DivisorSearch search(a, b, lower, counters);
  enumerate_divisors(search, factors, 0, mpz_class(1));
  return search.found;
}

static std::atomic<bool> solution_found{false};

static bool search(const mpq_class& remainder, unsigned long lower, int left,
                   Counters& counters) {
  ++counters.states;
  if (solution_found.load(std::memory_order_relaxed)) return true;
  if (tail_is_too_small(lower, left, remainder)) return false;
  if (left == 1) {
    const bool found = remainder.get_num() == 1 && remainder.get_den() >= lower;
    if (found) solution_found.store(true);
    return found;
  }
  if (left == 2) {
    const bool found = finish_with_two(remainder, lower, counters);
    if (found) solution_found.store(true);
    return found;
  }

  const mpz_class a = remainder.get_num();
  const mpz_class b = remainder.get_den();
  mpz_class first = b / a + 1;
  if (first < lower) first = lower;
  const mpz_class last = left * b / a;
  if (last < first) return false;
  if (!last.fits_ulong_p()) {
    std::fprintf(stderr, "interior denominator does not fit unsigned long\n");
    std::abort();
  }

  for (unsigned long denominator = first.get_ui();
       denominator <= last.get_ui(); ++denominator) {
    const mpq_class child = remainder - mpq_class(1, denominator);
    if (tail_is_too_small(denominator + 1, left - 1, child)) break;
    if (search(child, denominator + 1, left - 1, counters)) return true;
  }
  return false;
}

struct Task {
  mpq_class remainder;
  unsigned long lower;
  int left;
};

static void make_frontier(const mpq_class& remainder, unsigned long lower,
                          int left, int depth, int level,
                          std::vector<Task>& tasks, uint64_t& prefix_states) {
  if (level == depth) {
    tasks.push_back({remainder, lower, left});
    return;
  }
  ++prefix_states;
  if (tail_is_too_small(lower, left, remainder)) return;

  const mpz_class a = remainder.get_num();
  const mpz_class b = remainder.get_den();
  mpz_class first = b / a + 1;
  if (first < lower) first = lower;
  const mpz_class last = left * b / a;
  if (!last.fits_ulong_p()) std::abort();
  for (unsigned long denominator = first.get_ui();
       denominator <= last.get_ui(); ++denominator) {
    const mpq_class child = remainder - mpq_class(1, denominator);
    if (tail_is_too_small(denominator + 1, left - 1, child)) break;
    make_frontier(child, denominator + 1, left - 1, depth, level + 1,
                  tasks, prefix_states);
  }
}

int main(int argc, char** argv) {
  if (argc < 4) {
    std::fprintf(stderr, "usage: %s MINIMUM TERMS THREADS [FRONTIER_DEPTH]\n",
                 argv[0]);
    return 2;
  }
  const unsigned long minimum = std::strtoul(argv[1], nullptr, 10);
  const int terms = std::atoi(argv[2]);
  const int thread_count = std::atoi(argv[3]);
  const int frontier_depth = argc > 4 ? std::atoi(argv[4]) : 20;
  if (frontier_depth >= terms - 2 || thread_count < 1) return 2;

  make_small_primes(100000);
  const auto start = std::chrono::steady_clock::now();
  std::vector<Task> tasks;
  uint64_t prefix_states = 0;
  make_frontier(mpq_class(1), minimum, terms, frontier_depth, 0, tasks,
                prefix_states);
  std::printf("frontier_depth=%d tasks=%zu prefix_states=%llu\n",
              frontier_depth, tasks.size(),
              static_cast<unsigned long long>(prefix_states));

  std::atomic<size_t> next_task{0};
  std::vector<Counters> per_thread(thread_count);
  std::vector<std::thread> workers;
  for (int thread = 0; thread < thread_count; ++thread) {
    workers.emplace_back([&, thread] {
      while (!solution_found.load(std::memory_order_relaxed)) {
        const size_t index = next_task.fetch_add(1);
        if (index >= tasks.size()) break;
        search(tasks[index].remainder, tasks[index].lower, tasks[index].left,
               per_thread[thread]);
      }
    });
  }
  for (auto& worker : workers) worker.join();

  Counters total;
  total.states = prefix_states;
  for (const Counters& counters : per_thread) total.add(counters);
  const double seconds = std::chrono::duration<double>(
                             std::chrono::steady_clock::now() - start)
                             .count();
  std::printf("min=%lu terms=%d found=%s\n", minimum, terms,
              solution_found.load() ? "TRUE" : "false");
  std::printf("states=%llu two_states=%llu scan_candidates=%llu\n",
              static_cast<unsigned long long>(total.states),
              static_cast<unsigned long long>(total.two_states),
              static_cast<unsigned long long>(total.scan_candidates));
  std::printf("factored_states=%llu divisor_states=%llu divisor_candidates=%llu\n",
              static_cast<unsigned long long>(total.factored_states),
              static_cast<unsigned long long>(total.divisor_states),
              static_cast<unsigned long long>(total.divisor_candidates));
  std::printf("seconds=%.3f\n", seconds);
  return solution_found.load() ? 10 : 20;
}
