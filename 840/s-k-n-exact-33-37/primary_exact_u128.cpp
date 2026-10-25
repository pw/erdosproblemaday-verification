#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>

// Exhaustively compute the finite quasi-Sidon proxy
//   s(k,n) = max |A+A|, A subset [1,n], |A|=k,
// through n=37.  Translation makes min(A)=0; every translated set is then
// visited exactly once.  A+A fits into an unsigned 128-bit mask.

namespace {
constexpr int LIMIT = 37;
using U64 = std::uint64_t;
using U128 = unsigned __int128;

std::array<std::array<int, LIMIT + 1>, LIMIT> exact_best{};
std::array<std::array<U64, LIMIT + 1>, LIMIT> exact_witness{};
unsigned long long nodes = 0;

inline int popcount128(U128 value) {
    return std::popcount(static_cast<U64>(value)) +
           std::popcount(static_cast<U64>(value >> 64));
}

void visit(int next_x, U64 elements, U128 sums, int cardinality, int diameter) {
    ++nodes;
    const int score = popcount128(sums);
    if (score > exact_best[diameter][cardinality]) {
        exact_best[diameter][cardinality] = score;
        exact_witness[diameter][cardinality] = elements;
    }
    for (int x = next_x; x < LIMIT; ++x) {
        visit(x + 1,
              elements | (U64{1} << x),
              sums | (static_cast<U128>(elements) << x) | (U128{1} << (2 * x)),
              cardinality + 1,
              x);
    }
}

U128 direct_sumset(U64 elements) {
    U128 sums = 0;
    for (U64 rest = elements; rest; rest &= rest - 1) {
        const int x = std::countr_zero(rest);
        sums |= static_cast<U128>(elements) << x;
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
    visit(1, U64{1}, U128{1}, 1, 0);
    const auto finish = std::chrono::steady_clock::now();

    const unsigned long long expected = U64{1} << (LIMIT - 1);
    if (nodes != expected) {
        std::cerr << "wrong node count: " << nodes << " != " << expected << '\n';
        return 1;
    }

    std::array<int, LIMIT + 1> best{};
    std::array<U64, LIMIT + 1> witness{};
    best.fill(-1);
    for (int diameter = 0; diameter < LIMIT; ++diameter) {
        for (int k = 1; k <= LIMIT; ++k) {
            if (exact_best[diameter][k] > best[k]) {
                best[k] = exact_best[diameter][k];
                witness[k] = exact_witness[diameter][k];
            }
        }
        const int n = diameter + 1;
        if (n < 27) continue;
        std::cout << "ROW n=" << n << ':';
        for (int k = 1; k <= n; ++k) std::cout << ' ' << best[k];
        std::cout << '\n';

        for (int k = 7; k <= 16 && k <= n; ++k) {
            const U64 w = witness[k];
            if (!w || std::popcount(w) != k || popcount128(direct_sumset(w)) != best[k]) {
                std::cerr << "invalid witness at n=" << n << " k=" << k << '\n';
                return 2;
            }
            std::cout << "WITNESS n=" << n << " k=" << k << " score=" << best[k]
                      << " A=";
            print_set(w);
            std::cout << '\n';
        }
    }

    const double seconds = std::chrono::duration<double>(finish - start).count();
    std::cout << "LIMIT " << LIMIT << '\n';
    std::cout << "NODES " << nodes << '\n';
    std::cout << std::fixed << std::setprecision(6) << "SECONDS " << seconds << '\n';
    std::cout << "ALL CHECKS PASSED\n";
}
