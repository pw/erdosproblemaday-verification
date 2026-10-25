#include <array>
#include <bit>
#include <cstdint>
#include <iostream>

// Exhaust exactly the cardinalities that can be nontrivial in rows 32..37.
// Cardinalities >=14 are separately closed by a full-interval witness.

namespace {
constexpr unsigned width = 37;
constexpr unsigned max_k = 13;

struct Sums { std::uint64_t lo, hi; };
std::array<std::array<unsigned char, max_k + 1>, width> exact{};
std::uint64_t nodes = 0;

unsigned pop(Sums value) {
    return std::popcount(value.lo) + std::popcount(value.hi);
}

void walk(unsigned next, std::uint64_t set, Sums sums,
          unsigned cardinality, unsigned maximum) {
    ++nodes;
    auto &record = exact[maximum][cardinality];
    const unsigned current = pop(sums);
    if (current > record) record = static_cast<unsigned char>(current);
    if (cardinality == max_k) return;

    for (unsigned value = next; value < width; ++value) {
        Sums enlarged = sums;
        enlarged.lo |= set << value;
        enlarged.hi |= set >> (64U - value);
        const unsigned diagonal = 2U * value;
        if (diagonal < 64U) enlarged.lo |= std::uint64_t{1} << diagonal;
        else enlarged.hi |= std::uint64_t{1} << (diagonal - 64U);
        walk(value + 1, set | (std::uint64_t{1} << value), enlarged,
             cardinality + 1, value);
    }
}
}  // namespace

int main() {
    walk(1, 1, Sums{1, 0}, 1, 0);
    constexpr std::uint64_t expected = 2241812648ULL;
    if (nodes != expected) return 2;
    std::array<unsigned, max_k + 1> prefix{};
    for (unsigned diameter = 0; diameter < width; ++diameter) {
        for (unsigned k = 1; k <= max_k; ++k) {
            if (exact[diameter][k] > prefix[k]) prefix[k] = exact[diameter][k];
        }
        const unsigned n = diameter + 1;
        if (n < 32) continue;
        std::cout << "ROW " << n;
        for (unsigned k = 1; k <= max_k; ++k) std::cout << ' ' << prefix[k];
        std::cout << '\n';
    }
    std::cout << "NODES " << nodes << "\nHARD-CELL ENUMERATION PASS\n";
}
