#include <algorithm>
#include <bit>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

struct Point {
    int x;
    int y;
    auto operator<=>(const Point&) const = default;
};

static const Point O{0, 0};

[[noreturn]] static void fail(const std::string& message) {
    throw std::runtime_error(message);
}

static void require(bool condition, const std::string& message) {
    if (!condition) fail(message);
}

static std::int64_t norm2(Point p) {
    return std::int64_t(p.x) * p.x + std::int64_t(p.y) * p.y;
}

static std::int64_t distance2(Point p, Point q) {
    // Polarization identity, independently of coordinate differences.
    return norm2(p) + norm2(q)
        - 2 * (std::int64_t(p.x) * q.x + std::int64_t(p.y) * q.y);
}

static std::int64_t double_area(Point p, Point q, Point r) {
    // Six-term shoelace formula.
    const std::int64_t signed_area =
        std::int64_t(p.x) * q.y + std::int64_t(q.x) * r.y
        + std::int64_t(r.x) * p.y - std::int64_t(p.y) * q.x
        - std::int64_t(q.y) * r.x - std::int64_t(r.y) * p.x;
    return std::llabs(signed_area);
}

static std::int64_t margin(int n, Point p, Point q, Point r) {
    const std::int64_t a2 = double_area(p, q, r);
    const std::int64_t d2 = std::max({distance2(p, q), distance2(p, r), distance2(q, r)});
    const std::int64_t delta = a2 - 2LL * n;
    return delta * delta - 4 * d2;
}

static bool triples_good(int n, const std::vector<Point>& points) {
    for (std::size_t i = 0; i < points.size(); ++i) {
        for (std::size_t j = i; j < points.size(); ++j) {
            for (std::size_t k = j; k < points.size(); ++k) {
                if (margin(n, points[i], points[j], points[k]) <= 0) return false;
            }
        }
    }
    return true;
}

static std::vector<Point> diameter_directions(int n, std::int64_t& raw_count) {
    std::set<Point> reps;
    raw_count = 0;
    for (int x = -(n - 1); x < n; ++x) {
        for (int y = -(n - 1); y < n; ++y) {
            if ((x == 0 && y == 0) || std::int64_t(x) * x + std::int64_t(y) * y >= std::int64_t(n) * n) {
                continue;
            }
            ++raw_count;
            int a = std::abs(x), b = std::abs(y);
            if (a < b) std::swap(a, b);
            reps.insert({a, b});
        }
    }
    std::vector<Point> out(reps.begin(), reps.end());
    std::sort(out.begin(), out.end(), [](Point p, Point q) {
        return std::tuple(norm2(p), p.x, p.y) < std::tuple(norm2(q), q.x, q.y);
    });
    std::int64_t reconstructed = 0;
    for (Point p : out) reconstructed += (p.y == 0 || p.x == p.y) ? 4 : 8;
    require(reconstructed == raw_count, "D4 orbit accounting mismatch");
    return out;
}

static int integer_sqrt(std::int64_t value) {
    int root = static_cast<int>(std::sqrt(static_cast<long double>(value)));
    while (std::int64_t(root + 1) * (root + 1) <= value) ++root;
    while (std::int64_t(root) * root > value) --root;
    return root;
}

static std::vector<Point> lens_candidates(int n, Point b) {
    const std::int64_t d2 = norm2(b);
    const int radius = integer_sqrt(d2);
    std::vector<Point> out;
    for (int x = -radius; x <= radius; ++x) {
        for (int y = -radius; y <= radius; ++y) {
            const Point p{x, y};
            if (p == O || p == b || norm2(p) > d2 || distance2(p, b) > d2) continue;
            if (triples_good(n, {O, b, p})) out.push_back(p);
        }
    }
    require(std::set<Point>(out.begin(), out.end()).size() == out.size(), "duplicate lens point");
    return out;
}

static std::vector<Point> branch_pool(
    int n,
    const std::vector<Point>& source,
    const std::vector<Point>& forced,
    std::int64_t diameter2
) {
    std::set<Point> forced_set(forced.begin(), forced.end());
    std::vector<Point> out;
    for (Point p : source) {
        if (forced_set.contains(p)) continue;
        bool distance_ok = true;
        for (Point q : forced) {
            if (distance2(p, q) > diameter2) distance_ok = false;
        }
        if (!distance_ok) continue;
        std::vector<Point> trial = forced;
        trial.push_back(p);
        if (triples_good(n, trial)) out.push_back(p);
    }
    return out;
}

static bool pair_can_coexist_fast(
    int n,
    const std::vector<Point>& forced,
    Point p,
    Point q,
    std::int64_t diameter2
) {
    // Individual compatibility with forced was checked while building the
    // pool.  These are exactly the remaining triple types after adding p,q.
    if (distance2(p, q) > diameter2) return false;
    if (margin(n, p, p, q) <= 0 || margin(n, p, q, q) <= 0) return false;
    for (Point r : forced) {
        if (margin(n, p, q, r) <= 0) return false;
    }
    return true;
}

static bool pair_can_coexist_full(
    int n,
    const std::vector<Point>& forced,
    Point p,
    Point q,
    std::int64_t diameter2
) {
    if (distance2(p, q) > diameter2) return false;
    std::vector<Point> trial = forced;
    trial.push_back(p);
    trial.push_back(q);
    return triples_good(n, trial);
}

static std::vector<int> static_coloring(const std::vector<std::vector<int>>& adjacency) {
    std::vector<int> order(adjacency.size()), colors(adjacency.size(), -1);
    std::iota(order.begin(), order.end(), 0);
    std::sort(order.begin(), order.end(), [&](int a, int b) {
        return std::pair(adjacency[a].size(), a) > std::pair(adjacency[b].size(), b);
    });
    for (int v : order) {
        std::uint64_t used = 0;
        for (int w : adjacency[v]) {
            if (colors[w] >= 0) used |= std::uint64_t(1) << colors[w];
        }
        int color = 0;
        while (used & (std::uint64_t(1) << color)) ++color;
        colors[v] = color;
    }
    return colors;
}

static std::vector<int> dsatur_coloring(const std::vector<std::vector<int>>& adjacency) {
    const int count = static_cast<int>(adjacency.size());
    std::vector<int> colors(count, -1);
    std::vector<std::uint64_t> neighbor_colors(count, 0);
    for (int done = 0; done < count; ++done) {
        int best = -1;
        for (int v = 0; v < count; ++v) {
            if (colors[v] >= 0) continue;
            if (best < 0 || std::tuple(std::popcount(neighbor_colors[v]), adjacency[v].size(), -v)
                    > std::tuple(std::popcount(neighbor_colors[best]), adjacency[best].size(), -best)) {
                best = v;
            }
        }
        int color = 0;
        while (neighbor_colors[best] & (std::uint64_t(1) << color)) ++color;
        colors[best] = color;
        for (int w : adjacency[best]) {
            if (colors[w] < 0) neighbor_colors[w] |= std::uint64_t(1) << color;
        }
    }
    return colors;
}

static int color_count(const std::vector<int>& colors) {
    return colors.empty() ? 0 : *std::max_element(colors.begin(), colors.end()) + 1;
}

static void write_point(std::ostream& out, Point p) {
    out << '[' << p.x << ',' << p.y << ']';
}

static void write_points(std::ostream& out, const std::vector<Point>& points) {
    out << '[';
    for (std::size_t i = 0; i < points.size(); ++i) {
        if (i) out << ',';
        write_point(out, points[i]);
    }
    out << ']';
}

static void write_ints(std::ostream& out, const std::vector<int>& values) {
    out << '[';
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i) out << ',';
        out << values[i];
    }
    out << ']';
}

struct Summary {
    std::int64_t raw_vectors = 0;
    std::int64_t directions = 0;
    std::int64_t directions_with_high = 0;
    std::int64_t high_branches = 0;
    std::int64_t branches = 0;
    std::int64_t pool_memberships = 0;
    std::int64_t producer_same_pairs = 0;
    std::int64_t independent_same_pairs = 0;
    std::int64_t max_pool = 0;
    std::int64_t dsatur_worse_branches = 0;
    std::int64_t fast_full_pair_checks = 0;
    int global_upper = 0;
    int producer_global_upper = 0;
    std::vector<Point> tight;
    std::vector<Point> producer_tight;
};

static Summary run(int n, int target, const std::string& stream_path) {
    Summary summary;
    std::vector<Point> directions = diameter_directions(n, summary.raw_vectors);
    summary.directions = directions.size();
    std::ofstream stream(stream_path, std::ios::binary | std::ios::trunc);
    require(bool(stream), "cannot open producer transcript stream");

    for (Point b : directions) {
        const std::int64_t d2 = norm2(b);
        const std::vector<Point> base = lens_candidates(n, b);
        std::vector<Point> low, high;
        for (Point p : base) {
            const auto a2 = double_area(O, b, p);
            if (a2 < 2LL * n) low.push_back(p);
            else if (a2 > 2LL * n) high.push_back(p);
            else fail("area-band equality survived strict predicate");
        }
        if (!high.empty()) ++summary.directions_with_high;

        int direction_upper = 0;
        int producer_direction_upper = 0;
        auto process = [&](const std::string& label, const std::vector<Point>& forced,
                           const std::vector<Point>& source) {
            ++summary.branches;
            if (label.starts_with("high:")) ++summary.high_branches;
            require(triples_good(n, forced), "bad forced set");
            const std::vector<Point> pool = branch_pool(n, source, forced, d2);
            summary.pool_memberships += pool.size();
            summary.max_pool = std::max<std::int64_t>(summary.max_pool, pool.size());

            std::vector<std::vector<int>> adjacency(pool.size());
            for (int i = 0; i < static_cast<int>(pool.size()); ++i) {
                for (int j = i + 1; j < static_cast<int>(pool.size()); ++j) {
                    if (pair_can_coexist_fast(n, forced, pool[i], pool[j], d2)) {
                        adjacency[i].push_back(j);
                        adjacency[j].push_back(i);
                    }
                }
            }
            const std::vector<int> producer_colors = static_coloring(adjacency);
            const std::vector<int> dsatur_colors = dsatur_coloring(adjacency);
            const int producer_count = color_count(producer_colors);
            const int dsatur_count = color_count(dsatur_colors);
            const std::vector<int>& independent_colors =
                dsatur_count <= producer_count ? dsatur_colors : producer_colors;
            const int independent_count = std::min(dsatur_count, producer_count);
            if (dsatur_count > producer_count) ++summary.dsatur_worse_branches;

            for (int i = 0; i < static_cast<int>(pool.size()); ++i) {
                for (int j = i + 1; j < static_cast<int>(pool.size()); ++j) {
                    const bool same_producer = producer_colors[i] == producer_colors[j];
                    const bool same_independent = independent_colors[i] == independent_colors[j];
                    if (same_producer || same_independent) {
                        const bool fast = pair_can_coexist_fast(n, forced, pool[i], pool[j], d2);
                        const bool full = pair_can_coexist_full(n, forced, pool[i], pool[j], d2);
                        ++summary.fast_full_pair_checks;
                        require(fast == full, "optimized/full pair predicate mismatch");
                        require(!full, "compatible same-color pair");
                    }
                    if (same_producer) ++summary.producer_same_pairs;
                    if (same_independent) ++summary.independent_same_pairs;
                }
            }

            const int threshold = target - static_cast<int>(forced.size());
            require(producer_count <= threshold, "producer-style coloring misses target");
            require(independent_count <= threshold, "independent coloring misses target");
            producer_direction_upper = std::max(
                producer_direction_upper,
                static_cast<int>(forced.size()) + producer_count
            );
            direction_upper = std::max(
                direction_upper,
                static_cast<int>(forced.size()) + independent_count
            );

            // Exact json.dumps(sort_keys=True,separators=(",",":")) layout
            // of the Python producer's committed transcript record.
            stream << "{\"B\":";
            write_point(stream, b);
            stream << ",\"N\":" << n << ",\"branch\":\"" << label << "\",\"colors\":";
            write_ints(stream, producer_colors);
            stream << ",\"forced\":";
            write_points(stream, forced);
            stream << ",\"pool\":";
            write_points(stream, pool);
            stream << "}\n";
        };

        process("no-high", {O, b}, low);
        for (Point h : high) {
            process(
                "high:" + std::to_string(h.x) + "," + std::to_string(h.y),
                {O, b, h},
                base
            );
        }

        if (direction_upper > summary.global_upper) {
            summary.global_upper = direction_upper;
            summary.tight = {b};
        } else if (direction_upper == summary.global_upper) {
            summary.tight.push_back(b);
        }
        if (producer_direction_upper > summary.producer_global_upper) {
            summary.producer_global_upper = producer_direction_upper;
            summary.producer_tight = {b};
        } else if (producer_direction_upper == summary.producer_global_upper) {
            summary.producer_tight.push_back(b);
        }
    }
    require(summary.global_upper == target, "independent global upper mismatch");
    require(summary.producer_global_upper == target, "producer global upper mismatch");
    stream.close();
    require(bool(stream), "producer transcript write failed");
    return summary;
}

static void print_points(std::ostream& out, const std::vector<Point>& points) {
    write_points(out, points);
}

int main(int argc, char** argv) {
    try {
        if (argc != 4) {
            std::cerr << "usage: audit_352_upper N TARGET PRODUCER_STREAM\n";
            return 2;
        }
        const int n = std::stoi(argv[1]);
        const int target = std::stoi(argv[2]);
        const Summary s = run(n, target, argv[3]);
        std::cout << "{\"N\":" << n
                  << ",\"target\":" << target
                  << ",\"raw_vectors\":" << s.raw_vectors
                  << ",\"diameter_directions\":" << s.directions
                  << ",\"directions_with_high\":" << s.directions_with_high
                  << ",\"fixed_high_branches\":" << s.high_branches
                  << ",\"all_branches\":" << s.branches
                  << ",\"pool_memberships\":" << s.pool_memberships
                  << ",\"producer_same_color_pairs\":" << s.producer_same_pairs
                  << ",\"independent_same_color_pairs\":" << s.independent_same_pairs
                  << ",\"max_pool\":" << s.max_pool
                  << ",\"dsatur_worse_branches\":" << s.dsatur_worse_branches
                  << ",\"fast_full_same_pair_checks\":" << s.fast_full_pair_checks
                  << ",\"global_upper\":" << s.global_upper
                  << ",\"producer_global_upper\":" << s.producer_global_upper
                  << ",\"tight\":";
        print_points(std::cout, s.tight);
        std::cout << ",\"producer_tight\":";
        print_points(std::cout, s.producer_tight);
        std::cout << "}\nHOSTILE_CPP_UPPER_PASS\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "HOSTILE_CPP_UPPER_FAIL: " << error.what() << '\n';
        return 1;
    }
}
