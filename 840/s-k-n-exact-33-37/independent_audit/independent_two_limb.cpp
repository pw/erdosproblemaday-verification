#include <array>
#include <bit>
#include <cstdint>
#include <iostream>

// Clean-room exhaustive checker for s(k,n), n <= 37.
//
// This intentionally does not use unsigned __int128.  A sumset is represented
// by two ordinary 64-bit limbs, so it exercises the producer's most delicate
// implementation choice independently.

namespace {
constexpr unsigned width = 37;

struct Bits73 {
    std::uint64_t low = 0;
    std::uint64_t high = 0;
};

std::array<std::array<unsigned char, width + 1>, width> by_diameter{};
std::uint64_t visited = 0;

unsigned score(Bits73 bits) {
    return std::popcount(bits.low) + std::popcount(bits.high);
}

Bits73 add_new_max(Bits73 old_sums, std::uint64_t old_set, unsigned value) {
    Bits73 answer = old_sums;
    answer.low |= old_set << value;
    answer.high |= old_set >> (64U - value);
    const unsigned twice = 2U * value;
    if (twice < 64U) {
        answer.low |= std::uint64_t{1} << twice;
    } else {
        answer.high |= std::uint64_t{1} << (twice - 64U);
    }
    return answer;
}

void enumerate(unsigned next, std::uint64_t set, Bits73 sums,
               unsigned cardinality, unsigned maximum) {
    ++visited;
    auto &slot = by_diameter[maximum][cardinality];
    const unsigned current = score(sums);
    if (current > slot) slot = static_cast<unsigned char>(current);

    for (unsigned value = next; value < width; ++value) {
        enumerate(value + 1U,
                  set | (std::uint64_t{1} << value),
                  add_new_max(sums, set, value),
                  cardinality + 1U,
                  value);
    }
}
}  // namespace

int main() {
    enumerate(1, 1, Bits73{1, 0}, 1, 0);
    if (visited != (std::uint64_t{1} << 36U)) return 2;

    std::array<unsigned, width + 1> prefix{};
    for (unsigned diameter = 0; diameter < width; ++diameter) {
        for (unsigned k = 1; k <= width; ++k) {
            if (by_diameter[diameter][k] > prefix[k]) {
                prefix[k] = by_diameter[diameter][k];
            }
        }
        const unsigned n = diameter + 1U;
        if (n < 32U) continue;
        std::cout << "ROW " << n;
        for (unsigned k = 1; k <= n; ++k) std::cout << ' ' << prefix[k];
        std::cout << '\n';
    }
    std::cout << "VISITED " << visited << "\nCLEAN-ROOM ENUMERATION PASS\n";
}
