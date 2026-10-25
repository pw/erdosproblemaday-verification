#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>

// Exhaustive computation of
//   s(k,n) = max{|A+A| : A subset {1,...,n}, |A|=k}
// through n=32.  Translation lets us enumerate, exactly once, the sets
// A subset {0,...,31} which contain 0.  Along a depth-first traversal we use
// Sigma(A union {x}) = Sigma(A) union (x+A) union {2x}.

namespace {
constexpr int LIMIT = 32;
using U64 = std::uint64_t;

std::array<std::array<int, LIMIT + 1>, LIMIT> exact_best{};
std::array<std::array<U64, LIMIT + 1>, LIMIT> exact_witness{};
unsigned long long nodes = 0;

void visit(int next_x, U64 elements, U64 sums, int cardinality, int diameter) {
    ++nodes;
    const int score = std::popcount(sums);
    if (score > exact_best[diameter][cardinality]) {
        exact_best[diameter][cardinality] = score;
        exact_witness[diameter][cardinality] = elements;
    }

    for (int x = next_x; x < LIMIT; ++x) {
        visit(x + 1,
              elements | (U64{1} << x),
              sums | (elements << x) | (U64{1} << (2 * x)),
              cardinality + 1,
              x);
    }
}

U64 direct_sumset(U64 elements) {
    U64 sums = 0;
    for (U64 rest = elements; rest; rest &= rest - 1) {
        const int x = std::countr_zero(rest);
        sums |= elements << x;
    }
    return sums;
}

void print_set(U64 mask) {
    std::cout << '[';
    bool first = true;
    for (int x = 0; x < LIMIT; ++x) {
        if ((mask >> x) & 1U) {
            if (!first) std::cout << ',';
            std::cout << (x + 1);
            first = false;
        }
    }
    std::cout << ']';
}
}  // namespace

int main() {
    for (auto &row : exact_best) row.fill(-1);
    const auto start = std::chrono::steady_clock::now();
    visit(1, U64{1}, U64{1}, 1, 0);
    const auto finish = std::chrono::steady_clock::now();

    const unsigned long long expected_nodes = U64{1} << (LIMIT - 1);
    if (nodes != expected_nodes) {
        std::cerr << "wrong node count: " << nodes << " != " << expected_nodes << '\n';
        return 1;
    }

    std::array<int, LIMIT + 1> prefix_best{};
    std::array<U64, LIMIT + 1> prefix_witness{};
    prefix_best.fill(-1);
    for (int diameter = 0; diameter < LIMIT; ++diameter) {
        for (int k = 1; k <= LIMIT; ++k) {
            if (exact_best[diameter][k] > prefix_best[k]) {
                prefix_best[k] = exact_best[diameter][k];
                prefix_witness[k] = exact_witness[diameter][k];
            }
        }
        const int n = diameter + 1;
        if (n < 27) continue;
        std::cout << "ROW n=" << n << ':';
        for (int k = 1; k <= n; ++k) std::cout << ' ' << prefix_best[k];
        std::cout << '\n';
        if (n >= 28) {
            for (int k = 1; k <= n; ++k) {
                const U64 witness = prefix_witness[k];
                if (witness == 0 || std::popcount(witness) != k ||
                    std::popcount(direct_sumset(witness)) != prefix_best[k]) {
                    std::cerr << "invalid witness at n=" << n << " k=" << k << '\n';
                    return 2;
                }
                if (k >= 7 && k <= 14) {
                    std::cout << "WITNESS n=" << n << " k=" << k
                              << " score=" << prefix_best[k] << " A=";
                    print_set(witness);
                    std::cout << '\n';
                }
            }
        }
    }

    const double seconds = std::chrono::duration<double>(finish - start).count();
    std::cout << "LIMIT " << LIMIT << '\n';
    std::cout << "NODES " << nodes << '\n';
    std::cout << std::fixed << std::setprecision(6) << "SECONDS " << seconds << '\n';
    std::cout << "ALL CHECKS PASSED\n";
}
