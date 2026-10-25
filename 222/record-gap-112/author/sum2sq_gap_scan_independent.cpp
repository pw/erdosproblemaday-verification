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
    u64 left;
    u64 right;
};

struct Chunk {
    u64 count = 0;
    u64 first = 0;
    u64 last = 0;
    Gap widest{0, 0};
    std::vector<Gap> reported;
};

// The floating-point estimate is only a starting point; the two correction
// loops make the returned square root exact.
static u64 integer_sqrt(u64 n) {
    u64 r = static_cast<u64>(std::sqrt(static_cast<double>(n)));
    while (static_cast<u128>(r + 1) * (r + 1) <= n) {
        ++r;
    }
    while (static_cast<u128>(r) * r > n) {
        --r;
    }
    return r;
}

static u64 integer_sqrt_ceiling(u64 n) {
    const u64 r = integer_sqrt(n);
    return static_cast<u128>(r) * r == n ? r : r + 1;
}

static Chunk enumerate_chunk(u64 lo, u64 hi, u64 report_threshold) {
    const u64 width = hi - lo + 1;
    std::vector<unsigned char> represented(width, 0);

    // b is the larger coordinate.  Values b below this bound cannot reach lo
    // even when a=b, while b above the upper bound have b^2 > hi.
    const u64 half_lo_ceiling = lo / 2 + lo % 2;
    const u64 b_begin = integer_sqrt_ceiling(half_lo_ceiling);
    const u64 b_end = integer_sqrt(hi);
    for (u64 b = b_begin; b <= b_end; ++b) {
        const u64 b_squared = b * b;
        const u64 a_begin = lo > b_squared
            ? integer_sqrt_ceiling(lo - b_squared)
            : 0;
        const u64 a_end = std::min(b, integer_sqrt(hi - b_squared));
        if (a_begin > a_end) {
            continue;
        }

        u64 value = b_squared + a_begin * a_begin;
        u64 increment = 2 * a_begin + 1;
        for (u64 a = a_begin; a <= a_end; ++a) {
            represented[value - lo] = 1;
            value += increment;
            increment += 2;
        }
    }

    Chunk answer;
    bool have_previous = false;
    u64 previous = 0;
    for (u64 offset = 0; offset < width; ++offset) {
        if (!represented[offset]) {
            continue;
        }
        const u64 value = lo + offset;
        if (!have_previous) {
            answer.first = value;
            have_previous = true;
        } else {
            const u64 gap = value - previous;
            if (gap >= report_threshold) {
                answer.reported.push_back({previous, value});
            }
            if (gap > answer.widest.right - answer.widest.left) {
                answer.widest = {previous, value};
            }
        }
        previous = value;
        answer.last = value;
        ++answer.count;
    }
    return answer;
}

static u64 parse_number(const char* text, const char* label) {
    char* end = nullptr;
    const unsigned long long value = std::strtoull(text, &end, 10);
    if (text[0] == '\0' || *end != '\0') {
        std::cerr << "invalid " << label << ": " << text << "\n";
        std::exit(2);
    }
    return static_cast<u64>(value);
}

int main(int argc, char** argv) {
    if (argc != 5) {
        std::cerr << "usage: " << argv[0]
                  << " LO HI CHUNK_WIDTH REPORT_GAP_AT_LEAST\n";
        return 2;
    }

    const u64 lo = parse_number(argv[1], "LO");
    const u64 hi = parse_number(argv[2], "HI");
    const u64 chunk_width = parse_number(argv[3], "CHUNK_WIDTH");
    const u64 report_threshold = parse_number(argv[4], "REPORT_GAP_AT_LEAST");
    if (lo > hi || chunk_width == 0) {
        std::cerr << "require LO <= HI and CHUNK_WIDTH > 0\n";
        return 2;
    }

    const u64 number_of_chunks = (hi - lo) / chunk_width + 1;
    std::vector<Chunk> chunks(number_of_chunks);
    std::atomic<u64> finished{0};
    const auto start = std::chrono::steady_clock::now();

#pragma omp parallel for schedule(static, 1)
    for (std::int64_t i = 0; i < static_cast<std::int64_t>(number_of_chunks); ++i) {
        const u64 chunk_lo = lo + static_cast<u64>(i) * chunk_width;
        const u64 chunk_hi = std::min(hi, chunk_lo + chunk_width - 1);
        chunks[i] = enumerate_chunk(chunk_lo, chunk_hi, report_threshold);
        const u64 done = ++finished;
#pragma omp critical
        std::cerr << "completed " << done << "/" << number_of_chunks
                  << " chunk=" << i << " range=" << chunk_lo << ".." << chunk_hi
                  << " count=" << chunks[i].count << "\n";
    }

    u64 total = 0;
    u64 first = 0;
    u64 last = 0;
    bool have_last = false;
    Gap widest{0, 0};
    std::vector<Gap> reported;

    const auto consider_gap = [&](Gap gap) {
        const u64 size = gap.right - gap.left;
        if (size > widest.right - widest.left) {
            widest = gap;
        }
        if (size >= report_threshold) {
            reported.push_back(gap);
        }
    };

    for (const Chunk& chunk : chunks) {
        if (chunk.count == 0) {
            continue;
        }
        if (!have_last) {
            first = chunk.first;
        } else {
            consider_gap({last, chunk.first});
        }
        if (chunk.widest.right != 0) {
            const u64 size = chunk.widest.right - chunk.widest.left;
            if (size > widest.right - widest.left) {
                widest = chunk.widest;
            }
        }
        reported.insert(reported.end(), chunk.reported.begin(), chunk.reported.end());
        total += chunk.count;
        last = chunk.last;
        have_last = true;
    }

    std::sort(reported.begin(), reported.end(), [](Gap a, Gap b) {
        return a.left < b.left;
    });
    const double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - start).count();

    std::cout << "RANGE " << lo << " " << hi << "\n"
              << "CHUNK_WIDTH " << chunk_width << "\n"
              << "CHUNKS " << number_of_chunks << "\n"
              << "REPRESENTED_COUNT " << total << "\n"
              << "FIRST " << first << "\n"
              << "LAST " << last << "\n"
              << "MAX_GAP " << widest.right - widest.left << "\n"
              << "MAX_GAP_LEFT " << widest.left << "\n"
              << "MAX_GAP_RIGHT " << widest.right << "\n"
              << "NONREPRESENTED_RUN " << widest.right - widest.left - 1 << "\n"
              << "WALL_SECONDS " << std::fixed << std::setprecision(3) << elapsed << "\n"
              << "REPORTED_GAP_AT_LEAST " << report_threshold << "\n"
              << "REPORTED_GAP_COUNT " << reported.size() << "\n";
    for (const Gap gap : reported) {
        std::cout << "GAP " << gap.right - gap.left << " "
                  << gap.left << " " << gap.right << "\n";
    }
}
