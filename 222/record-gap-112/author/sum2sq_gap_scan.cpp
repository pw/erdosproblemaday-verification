#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Gap {
    u64 size = 0;
    u64 left = 0;
    u64 right = 0;
};

struct ChunkResult {
    u64 lo = 0;
    u64 hi = 0;
    u64 represented_count = 0;
    u64 first = 0;
    u64 last = 0;
    u64 max_gap = 0;
    u64 max_gap_left = 0;
    u64 max_gap_right = 0;
    double seconds = 0.0;
    std::vector<Gap> reported_gaps;
};

static u64 floor_sqrt(u64 n) {
    u64 x = static_cast<u64>(std::sqrt(static_cast<long double>(n)));
    while (static_cast<u128>(x + 1) * (x + 1) <= n) ++x;
    while (static_cast<u128>(x) * x > n) --x;
    return x;
}

static u64 ceil_sqrt(u64 n) {
    const u64 x = floor_sqrt(n);
    return static_cast<u128>(x) * x == n ? x : x + 1;
}

static ChunkResult scan_chunk(u64 lo, u64 hi, u64 report_gap_at_least) {
    const auto started = std::chrono::steady_clock::now();
    const u64 width = hi - lo + 1;
    std::vector<u64> bits((width + 63) / 64, 0);

    const u64 max_a = floor_sqrt(hi);
    for (u64 a = 0; a <= max_a; ++a) {
        const u64 a2 = a * a;
        const u64 residual_hi = hi - a2;
        u64 b_hi = floor_sqrt(residual_hi);
        if (b_hi < a) continue;

        u64 b_lo = a;
        if (a2 < lo) b_lo = std::max(b_lo, ceil_sqrt(lo - a2));
        if (b_lo > b_hi) continue;

        u64 value = a2 + b_lo * b_lo;
        u64 delta = 2 * b_lo + 1;
        for (u64 b = b_lo; b <= b_hi; ++b) {
            const u64 offset = value - lo;
            bits[offset >> 6] |= u64{1} << (offset & 63);
            value += delta;
            delta += 2;
        }
    }

    ChunkResult result;
    result.lo = lo;
    result.hi = hi;
    u64 previous = 0;
    bool have_previous = false;
    for (u64 word_index = 0; word_index < bits.size(); ++word_index) {
        u64 word = bits[word_index];
        while (word != 0) {
            const unsigned bit = static_cast<unsigned>(__builtin_ctzll(word));
            const u64 offset = word_index * 64 + bit;
            if (offset >= width) break;
            const u64 value = lo + offset;
            if (!have_previous) {
                result.first = value;
                have_previous = true;
            } else {
                const u64 gap = value - previous;
                if (gap >= report_gap_at_least) {
                    result.reported_gaps.push_back({gap, previous, value});
                }
                if (gap > result.max_gap) {
                    result.max_gap = gap;
                    result.max_gap_left = previous;
                    result.max_gap_right = value;
                }
            }
            previous = value;
            result.last = value;
            ++result.represented_count;
            word &= word - 1;
        }
    }

    result.seconds = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    return result;
}

static u64 parse_u64(const char* value, const char* name) {
    char* end = nullptr;
    const unsigned long long parsed = std::strtoull(value, &end, 10);
    if (value[0] == '\0' || *end != '\0') {
        std::cerr << "invalid " << name << ": " << value << "\n";
        std::exit(2);
    }
    return static_cast<u64>(parsed);
}

int main(int argc, char** argv) {
    if (argc != 4 && argc != 5) {
        std::cerr << "usage: " << argv[0]
                  << " LO HI CHUNK_WIDTH [REPORT_GAP_AT_LEAST]\n";
        return 2;
    }
    const u64 global_lo = parse_u64(argv[1], "LO");
    const u64 global_hi = parse_u64(argv[2], "HI");
    const u64 chunk_width = parse_u64(argv[3], "CHUNK_WIDTH");
    const u64 report_gap_at_least = argc == 5
        ? parse_u64(argv[4], "REPORT_GAP_AT_LEAST")
        : std::numeric_limits<u64>::max();
    if (global_lo > global_hi || chunk_width == 0) {
        std::cerr << "require LO <= HI and CHUNK_WIDTH > 0\n";
        return 2;
    }

    const u64 span = global_hi - global_lo + 1;
    const u64 chunk_count = (span + chunk_width - 1) / chunk_width;
    std::vector<ChunkResult> results(chunk_count);
    std::atomic<u64> completed{0};

    const auto all_started = std::chrono::steady_clock::now();
#pragma omp parallel for schedule(dynamic, 1)
    for (std::int64_t index = 0; index < static_cast<std::int64_t>(chunk_count); ++index) {
        const u64 lo = global_lo + static_cast<u64>(index) * chunk_width;
        const u64 hi = std::min(global_hi, lo + chunk_width - 1);
        results[index] = scan_chunk(lo, hi, report_gap_at_least);
        const u64 done = ++completed;
#pragma omp critical
        {
            std::cerr << "chunk " << (index + 1) << "/" << chunk_count
                      << " [" << lo << "," << hi << "]"
                      << " count=" << results[index].represented_count
                      << " internal_max=" << results[index].max_gap
                      << " at " << results[index].max_gap_left
                      << ".." << results[index].max_gap_right
                      << " seconds=" << std::fixed << std::setprecision(3)
                      << results[index].seconds
                      << " completed=" << done << "/" << chunk_count << "\n";
        }
    }

    u64 total_count = 0;
    u64 global_max_gap = 0;
    u64 global_max_left = 0;
    u64 global_max_right = 0;
    u64 previous_last = 0;
    bool have_previous = false;
    std::vector<Gap> reported_gaps;
    for (const ChunkResult& result : results) {
        if (result.represented_count == 0) continue;
        total_count += result.represented_count;
        if (have_previous) {
            const u64 boundary_gap = result.first - previous_last;
            if (boundary_gap >= report_gap_at_least) {
                reported_gaps.push_back({boundary_gap, previous_last, result.first});
            }
            if (boundary_gap > global_max_gap) {
                global_max_gap = boundary_gap;
                global_max_left = previous_last;
                global_max_right = result.first;
            }
        }
        reported_gaps.insert(reported_gaps.end(), result.reported_gaps.begin(),
                             result.reported_gaps.end());
        if (result.max_gap > global_max_gap) {
            global_max_gap = result.max_gap;
            global_max_left = result.max_gap_left;
            global_max_right = result.max_gap_right;
        }
        previous_last = result.last;
        have_previous = true;
    }

    const double all_seconds = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - all_started).count();
    std::cout << "RANGE " << global_lo << " " << global_hi << "\n"
              << "CHUNK_WIDTH " << chunk_width << "\n"
              << "CHUNKS " << chunk_count << "\n"
              << "REPRESENTED_COUNT " << total_count << "\n"
              << "FIRST " << (results.empty() ? 0 : results.front().first) << "\n"
              << "LAST " << (results.empty() ? 0 : results.back().last) << "\n"
              << "MAX_GAP " << global_max_gap << "\n"
              << "MAX_GAP_LEFT " << global_max_left << "\n"
              << "MAX_GAP_RIGHT " << global_max_right << "\n"
              << "NONREPRESENTED_RUN " << (global_max_gap == 0 ? 0 : global_max_gap - 1) << "\n"
              << "WALL_SECONDS " << std::fixed << std::setprecision(3) << all_seconds << "\n";
    std::sort(reported_gaps.begin(), reported_gaps.end(),
              [](const Gap& a, const Gap& b) { return a.left < b.left; });
    std::cout << "REPORTED_GAP_AT_LEAST " << report_gap_at_least << "\n"
              << "REPORTED_GAP_COUNT " << reported_gaps.size() << "\n";
    for (const Gap& gap : reported_gaps) {
        std::cout << "GAP " << gap.size << " " << gap.left << " " << gap.right << "\n";
    }
    return 0;
}
