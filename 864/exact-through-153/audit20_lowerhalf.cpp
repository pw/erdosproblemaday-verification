// Independent exhaustive checker for the finite Problem #864 target m=20.
//
// This is intentionally standalone and was written independently of the
// published wave-6p checker.  It uses direct pair-sum counting for every core
// and a separate signed-coordinate bitset for outlier extension.
//
// Build and run:
//   g++ -O3 -std=c++17 audit20_lowerhalf.cpp -o audit20_lowerhalf
//   ./audit20_lowerhalf

// Expected conclusion:
//   EXHAUSTED: no valid 20-set has diameter <= 151

#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

namespace {

constexpr int CAP = 151;
constexpr int TARGET = 20;
constexpr int SUM_OFFSET = 2 * CAP;
constexpr int SUM_SLOTS = 4 * CAP + 1;

using SumBits = std::bitset<SUM_SLOTS>;

struct CaseStats {
    int core_size = 0;
    int outliers = 0;
    std::uint64_t lower_halves = 0;
    std::uint64_t core_candidates = 0;
    std::uint64_t valid_cores = 0;
    std::uint64_t extension_nodes = 0;
    std::uint64_t digest_xor = 0;
    std::uint64_t digest_sum = 0;
};

std::uint64_t mix64(std::uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

std::uint64_t core_hash(const std::vector<int>& core) {
    std::uint64_t h = mix64(core.size());
    for (std::size_t i = 0; i < core.size(); ++i) {
        const std::uint64_t tagged =
            (std::uint64_t(i + 1) << 32) ^ std::uint64_t(core[i] + 1);
        h = mix64(h ^ mix64(tagged));
    }
    return h;
}

bool contains(const std::vector<int>& a, int x) {
    return std::binary_search(a.begin(), a.end(), x);
}

struct Search {
    std::array<CaseStats, TARGET + 1> stats{};
    std::vector<int> lower{0};
    std::array<bool, CAP + 1> difference_used{};
    std::vector<int> counterexample;

    Search() {
        for (int r = 14; r <= 20; ++r) {
            stats[r].core_size = r;
            stats[r].outliers = TARGET - r;
        }
    }

    // Count all unordered pair sums directly.  The core is admissible iff T
    // is represented at least twice and every other sum at most once.
    bool check_core_sums(const std::vector<int>& core, int T,
                         SumBits& represented) const {
        std::array<unsigned char, 2 * CAP + 1> count{};
        represented.reset();
        for (std::size_t i = 0; i < core.size(); ++i) {
            for (std::size_t j = i; j < core.size(); ++j) {
                const int s = core[i] + core[j];
                assert(0 <= s && s <= 2 * CAP);
                if (count[s] != 255) ++count[s];
                represented.set(s + SUM_OFFSET);
            }
        }
        if (count[T] < 2) return false;
        for (int s = 0; s <= 2 * CAP; ++s) {
            if (s != T && count[s] > 1) return false;
        }
        return true;
    }

    bool extend(const std::vector<int>& core, int T, int need,
                int next_z, SumBits represented,
                std::vector<int>& chosen, CaseStats& st) {
        ++st.extension_nodes;
        if (int(chosen.size()) == need) {
            counterexample = core;
            counterexample.insert(counterexample.end(), chosen.begin(),
                                  chosen.end());
            std::sort(counterexample.begin(), counterexample.end());
            return true;
        }

        const int slack = CAP - T;
        for (int z = next_z; z <= CAP; ++z) {
            if (z < -slack) continue;
            if (contains(core, z)) continue;
            if (2 * z == T) continue;

            const int reflected = T - z;
            if (contains(core, reflected) ||
                std::find(chosen.begin(), chosen.end(), reflected) !=
                    chosen.end())
                continue;

            int lo = std::min(0, z);
            int hi = std::max(T, z);
            for (int x : chosen) {
                lo = std::min(lo, x);
                hi = std::max(hi, x);
            }
            if (hi - lo > CAP) continue;

            SumBits fresh;
            auto add_fresh = [&](int sum) {
                const int index = sum + SUM_OFFSET;
                assert(0 <= index && index < SUM_SLOTS);
                // Since z is new, all sums newly involving z must be
                // distinct.  Retain the assertion as a hostile self-check.
                assert(!fresh.test(index));
                fresh.set(index);
            };
            add_fresh(2 * z);
            for (int x : core) add_fresh(z + x);
            for (int x : chosen) add_fresh(z + x);

            SumBits collision = represented & fresh;
            collision.reset(T + SUM_OFFSET);  // the one allowed repeated sum
            if (collision.any()) continue;

            chosen.push_back(z);
            if (extend(core, T, need, z + 1, represented | fresh, chosen, st))
                return true;
            chosen.pop_back();
        }
        return false;
    }

    bool process_core(int r, int T, bool has_midpoint) {
        std::vector<int> core = lower;
        if (has_midpoint) core.push_back(T / 2);
        for (auto it = lower.rbegin(); it != lower.rend(); ++it)
            core.push_back(T - *it);
        assert(int(core.size()) == r);
        assert(std::is_sorted(core.begin(), core.end()));

        CaseStats& st = stats[r];
        ++st.core_candidates;
        SumBits represented;
        if (!check_core_sums(core, T, represented)) return false;

        ++st.valid_cores;
        const std::uint64_t h = core_hash(core);
        st.digest_xor ^= h;
        st.digest_sum += h;

        std::vector<int> chosen;
        return extend(core, T, TARGET - r, T - CAP, represented, chosen, st);
    }

    bool visit_lower_half(int k) {
        const int largest = lower.back();

        // Deliberately enumerate diameters in descending order, unlike the
        // earlier implementation being audited.
        const int even_r = 2 * k;
        if (14 <= even_r && even_r <= 20) {
            CaseStats& st = stats[even_r];
            ++st.lower_halves;
            const int first = std::max(2 * largest + 1, even_r * even_r / 4);
            for (int T = CAP; T >= first; --T)
                if (process_core(even_r, T, false)) return true;
        }

        const int odd_r = 2 * k + 1;
        if (14 <= odd_r && odd_r <= 20) {
            CaseStats& st = stats[odd_r];
            ++st.lower_halves;
            int first = std::max(2 * largest + 1, odd_r * odd_r / 4);
            if (first & 1) ++first;
            int T = (CAP & 1) ? CAP - 1 : CAP;
            for (; T >= first; T -= 2)
                if (process_core(odd_r, T, true)) return true;
        }
        return false;
    }

    bool golomb_dfs(int k, int next) {
        if (int(lower.size()) == k) return visit_lower_half(k);

        const int still_needed_after = k - int(lower.size()) - 1;
        const int max_lower_mark = (CAP - 1) / 2;
        const int last_candidate = max_lower_mark - still_needed_after;
        for (int z = next; z <= last_candidate; ++z) {
            std::vector<int> new_differences;
            bool good = true;
            for (int x : lower) {
                const int d = z - x;
                if (difference_used[d]) {
                    good = false;
                    break;
                }
                // Differences from a new largest mark are mutually distinct,
                // but keep this explicit guard independent of that fact.
                if (std::find(new_differences.begin(), new_differences.end(), d)
                    != new_differences.end()) {
                    good = false;
                    break;
                }
                new_differences.push_back(d);
            }
            if (!good) continue;
            lower.push_back(z);
            for (int d : new_differences) difference_used[d] = true;
            if (golomb_dfs(k, z + 1)) return true;
            for (int d : new_differences) difference_used[d] = false;
            lower.pop_back();
        }
        return false;
    }

    bool run() {
        // Deliberately use the reverse core-size order from the earlier code.
        for (int k : {7, 8, 9, 10}) {
            lower.assign(1, 0);
            difference_used.fill(false);
            if (golomb_dfs(k, 1)) return false;
        }
        return true;
    }
};

bool near_sidon(const std::vector<int>& a, int& exceptional,
                int& representations) {
    if (!std::is_sorted(a.begin(), a.end())) return false;
    if (std::adjacent_find(a.begin(), a.end()) != a.end()) return false;
    std::array<int, 2 * CAP + 3> count{};
    for (std::size_t i = 0; i < a.size(); ++i)
        for (std::size_t j = i; j < a.size(); ++j)
            ++count[a[i] + a[j]];
    exceptional = -1;
    representations = 0;
    for (int s = 0; s < int(count.size()); ++s) {
        if (count[s] > 1) {
            if (exceptional != -1) return false;
            exceptional = s;
            representations = count[s];
        }
    }
    return true;
}

void check_witnesses() {
    const std::vector<int> w19 = {
        0, 4, 5, 7, 17, 33, 44, 52, 58, 67,
        76, 82, 90, 101, 117, 127, 129, 130, 134,
    };
    const std::vector<int> w20 = {
        0, 1, 6, 10, 23, 26, 34, 41, 53, 55,
        97, 99, 111, 118, 126, 129, 142, 146, 151, 152,
    };
    int exceptional = -1;
    int reps = 0;
    assert(near_sidon(w19, exceptional, reps));
    assert(exceptional == 134 && reps == 10 && w19.back() == 134);
    std::cout << "WITNESS 19 diameter=134 exceptional=134 reps=10 PASS\n";
    assert(near_sidon(w20, exceptional, reps));
    assert(exceptional == 152 && reps == 10 && w20.back() == 152);
    std::cout << "WITNESS 20 diameter=152 exceptional=152 reps=10 PASS\n";
}

void check_case_reduction() {
    // C(20,2)=190 positive-difference occurrences.  Each row retained below
    // is a possible exact reflected core when the diameter is at most 151.
    struct Row { int q, midpoint, r, outliers, duplicates, distinct; };
    std::vector<Row> retained;
    for (int q = 2; q <= 10; ++q) {
        for (int midpoint : {0, 1}) {
            const int r = 2 * q - midpoint;
            if (r > TARGET) continue;
            const int duplicates = midpoint ? (q - 1) * (q - 1)
                                             : q * (q - 1);
            const int distinct = 190 - duplicates;
            if (distinct <= CAP)
                retained.push_back({q, midpoint, r, TARGET - r,
                                    duplicates, distinct});
        }
    }
    std::sort(retained.begin(), retained.end(),
              [](const Row& a, const Row& b) { return a.r < b.r; });
    const std::vector<Row> expected = {
        {7, 0, 14, 6, 42, 148},
        {8, 1, 15, 5, 49, 141},
        {8, 0, 16, 4, 56, 134},
        {9, 1, 17, 3, 64, 126},
        {9, 0, 18, 2, 72, 118},
        {10, 1, 19, 1, 81, 109},
        {10, 0, 20, 0, 90, 100},
    };
    assert(retained.size() == expected.size());
    for (std::size_t i = 0; i < expected.size(); ++i) {
        assert(retained[i].q == expected[i].q);
        assert(retained[i].midpoint == expected[i].midpoint);
        assert(retained[i].r == expected[i].r);
        assert(retained[i].outliers == expected[i].outliers);
        assert(retained[i].duplicates == expected[i].duplicates);
        assert(retained[i].distinct == expected[i].distinct);
    }
    std::cout << "CASE REDUCTION core sizes 14,15,16,17,18,19,20 PASS\n";
}

}  // namespace

int main() {
    check_witnesses();
    check_case_reduction();

    Search search;
    const bool exhausted = search.run();
    for (int r = 20; r >= 14; --r) {
        const CaseStats& st = search.stats[r];
        std::cout << "CASE " << r
                  << " outliers=" << st.outliers
                  << " lower_halves=" << st.lower_halves
                  << " core_candidates=" << st.core_candidates
                  << " valid_cores=" << st.valid_cores
                  << " extension_nodes=" << st.extension_nodes
                  << " digest_xor=" << std::hex << std::setw(16)
                  << std::setfill('0') << st.digest_xor
                  << " digest_sum=" << std::setw(16) << st.digest_sum
                  << std::dec << "\n";
    }
    if (!exhausted) {
        std::cout << "COUNTEREXAMPLE";
        for (int x : search.counterexample) std::cout << ' ' << x;
        std::cout << "\n";
        return 2;
    }
    std::cout << "EXHAUSTED: no valid 20-set has diameter <= 151\n";
    return 0;
}
