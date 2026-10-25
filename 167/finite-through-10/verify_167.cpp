#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

// Definition-level finite checker for Erdos problem 167 (Tuza's conjecture).
// Input: one graph6 graph per line, with at most 10 vertices.
// For every graph containing a triangle, the program constructs
//   (1) an edge-disjoint triangle packing P, and
//   (2) an edge set C meeting every triangle,
// and checks |C| <= 2|P|.  Since |P| <= nu(G) and tau(G) <= |C|, this
// directly certifies tau(G) <= 2 nu(G).

struct Bits {
    uint64_t lo = 0, hi = 0;
    bool empty() const { return (lo | hi) == 0; }
    int count() const { return __builtin_popcountll(lo) + __builtin_popcountll(hi); }
    bool operator==(const Bits &o) const { return lo == o.lo && hi == o.hi; }
};

static inline Bits operator|(Bits a, Bits b) { return {a.lo | b.lo, a.hi | b.hi}; }
static inline Bits operator&(Bits a, Bits b) { return {a.lo & b.lo, a.hi & b.hi}; }
static inline Bits minus_bits(Bits a, Bits b) { return {a.lo & ~b.lo, a.hi & ~b.hi}; }
static inline bool has_bit(Bits a, int i) {
    return i < 64 ? ((a.lo >> i) & 1ULL) : ((a.hi >> (i - 64)) & 1ULL);
}
static inline void set_bit(Bits &a, int i) {
    if (i < 64) a.lo |= 1ULL << i;
    else a.hi |= 1ULL << (i - 64);
}
static inline int first_bit(Bits a) {
    if (a.lo) return __builtin_ctzll(a.lo);
    assert(a.hi);
    return 64 + __builtin_ctzll(a.hi);
}

struct BitsHash {
    size_t operator()(const Bits &b) const {
        uint64_t x = b.lo ^ (b.hi + 0x9e3779b97f4a7c15ULL + (b.lo << 6) + (b.lo >> 2));
        x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
        x ^= x >> 27; x *= 0x94d049bb133111ebULL;
        x ^= x >> 31;
        return static_cast<size_t>(x);
    }
};

struct GraphCheck {
    int n = 0;
    int m = 0;
    std::array<std::array<int, 10>, 10> edge_id{};
    std::vector<uint64_t> tri_edges;
    std::array<Bits, 45> hit{};
    std::vector<Bits> conflict;
    Bits all_triangles{};
    uint64_t graph_edge_mask = 0;

    uint64_t cover_nodes = 0;
    std::unordered_map<Bits, int, BitsHash> failed_budget;
    std::vector<int> found_cover;

    explicit GraphCheck(const std::vector<std::vector<int>> &adj) {
        n = static_cast<int>(adj.size());
        for (auto &row : edge_id) row.fill(-1);
        for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) {
            if (adj[i][j]) {
                edge_id[i][j] = edge_id[j][i] = m;
                graph_edge_mask |= 1ULL << m;
                ++m;
            }
        }
        for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j)
            for (int k = j + 1; k < n; ++k) {
                if (adj[i][j] && adj[i][k] && adj[j][k]) {
                    uint64_t mask = (1ULL << edge_id[i][j]) |
                                    (1ULL << edge_id[i][k]) |
                                    (1ULL << edge_id[j][k]);
                    int t = static_cast<int>(tri_edges.size());
                    tri_edges.push_back(mask);
                    set_bit(all_triangles, t);
                    for (int e = 0; e < m; ++e) if ((mask >> e) & 1ULL) set_bit(hit[e], t);
                }
            }
        conflict.resize(tri_edges.size());
        for (int t = 0; t < static_cast<int>(tri_edges.size()); ++t) {
            Bits b{};
            uint64_t x = tri_edges[t];
            while (x) {
                int e = __builtin_ctzll(x); x &= x - 1;
                b = b | hit[e];
            }
            conflict[t] = b;
        }
    }

    std::vector<int> greedy_packing(int mode) const {
        std::vector<int> order(tri_edges.size());
        for (int i = 0; i < static_cast<int>(order.size()); ++i) order[i] = i;
        auto score = [&](int t) {
            int s = 0;
            uint64_t x = tri_edges[t];
            while (x) { int e = __builtin_ctzll(x); x &= x - 1; s += hit[e].count(); }
            return s;
        };
        if (mode == 1) {
            std::stable_sort(order.begin(), order.end(), [&](int a, int b) {
                int sa = score(a), sb = score(b);
                return sa != sb ? sa < sb : a < b;
            });
        } else if (mode == 2) {
            std::stable_sort(order.begin(), order.end(), [&](int a, int b) {
                int sa = score(a), sb = score(b);
                return sa != sb ? sa > sb : a < b;
            });
        } else if (mode >= 3) {
            uint64_t seed = 0x9e3779b97f4a7c15ULL * static_cast<uint64_t>(mode + 17);
            auto key = [&](int t) {
                uint64_t z = seed ^ (static_cast<uint64_t>(t + 1) * 0xbf58476d1ce4e5b9ULL);
                z ^= z >> 30; z *= 0xbf58476d1ce4e5b9ULL;
                z ^= z >> 27; z *= 0x94d049bb133111ebULL;
                return z ^ (z >> 31);
            };
            std::sort(order.begin(), order.end(), [&](int a, int b) { return key(a) < key(b); });
        }
        uint64_t used = 0;
        std::vector<int> ans;
        for (int t : order) if ((used & tri_edges[t]) == 0) {
            used |= tri_edges[t];
            ans.push_back(t);
        }
        return ans;
    }

    std::vector<int> greedy_cover(Bits uncovered) const {
        std::vector<int> ans;
        while (!uncovered.empty()) {
            int best = -1, best_count = 0;
            for (int e = 0; e < m; ++e) {
                int c = (uncovered & hit[e]).count();
                if (c > best_count) { best_count = c; best = e; }
            }
            assert(best >= 0 && best_count > 0);
            ans.push_back(best);
            uncovered = minus_bits(uncovered, hit[best]);
        }
        return ans;
    }

    int packing_lower_bound(Bits uncovered) const {
        int p = 0;
        while (!uncovered.empty()) {
            int best_t = -1, best_conflicts = std::numeric_limits<int>::max();
            Bits scan = uncovered;
            while (!scan.empty()) {
                int t = first_bit(scan);
                if (t < 64) scan.lo &= scan.lo - 1; else scan.hi &= scan.hi - 1;
                int c = (uncovered & conflict[t]).count();
                if (c < best_conflicts) { best_conflicts = c; best_t = t; }
            }
            ++p;
            uncovered = minus_bits(uncovered, conflict[best_t]);
        }
        return p;
    }

    bool cover_rec(Bits uncovered, int budget, std::vector<int> &chosen) {
        ++cover_nodes;
        if (uncovered.empty()) { found_cover = chosen; return true; }
        if (budget <= 0) return false;
        auto greedy = greedy_cover(uncovered);
        if (static_cast<int>(greedy.size()) <= budget) {
            found_cover = chosen;
            found_cover.insert(found_cover.end(), greedy.begin(), greedy.end());
            return true;
        }
        if (packing_lower_bound(uncovered) > budget) return false;
        auto it = failed_budget.find(uncovered);
        if (it != failed_budget.end() && it->second >= budget) return false;

        // Branch on the uncovered triangle whose least useful edge is as useful
        // as possible; within it, try the most useful edge first.
        int branch_t = -1, branch_score = -1;
        Bits scan = uncovered;
        while (!scan.empty()) {
            int t = first_bit(scan);
            if (t < 64) scan.lo &= scan.lo - 1; else scan.hi &= scan.hi - 1;
            int mn = 1000000;
            uint64_t x = tri_edges[t];
            while (x) {
                int e = __builtin_ctzll(x); x &= x - 1;
                mn = std::min(mn, (uncovered & hit[e]).count());
            }
            if (mn > branch_score) { branch_score = mn; branch_t = t; }
        }
        std::array<std::pair<int,int>, 3> options{};
        int q = 0;
        uint64_t x = tri_edges[branch_t];
        while (x) {
            int e = __builtin_ctzll(x); x &= x - 1;
            options[q++] = {(uncovered & hit[e]).count(), e};
        }
        std::sort(options.begin(), options.end(), std::greater<std::pair<int,int>>());
        for (auto [score, e] : options) {
            (void)score;
            chosen.push_back(e);
            if (cover_rec(minus_bits(uncovered, hit[e]), budget - 1, chosen)) return true;
            chosen.pop_back();
        }
        auto [jt, inserted] = failed_budget.emplace(uncovered, budget);
        if (!inserted && jt->second < budget) jt->second = budget;
        return false;
    }

    bool construct_pair(std::vector<int> &packing, std::vector<int> &cover) {
        if (tri_edges.empty()) { packing.clear(); cover.clear(); return true; }
        packing.clear();
        for (int mode = 0; mode < 11; ++mode) {
            auto p = greedy_packing(mode);
            if (p.size() > packing.size()) packing = std::move(p);
        }
        failed_budget.clear(); found_cover.clear(); cover_nodes = 0;
        std::vector<int> chosen;
        bool ok = cover_rec(all_triangles, 2 * static_cast<int>(packing.size()), chosen);
        if (!ok) return false;
        cover = found_cover;
        return verify_pair(packing, cover);
    }

    bool verify_pair(const std::vector<int> &packing, const std::vector<int> &cover) const {
        uint64_t used = 0, selected = 0;
        for (int t : packing) {
            if (t < 0 || t >= static_cast<int>(tri_edges.size())) return false;
            if (used & tri_edges[t]) return false;
            used |= tri_edges[t];
        }
        for (int e : cover) {
            if (e < 0 || e >= m || ((selected >> e) & 1ULL)) return false;
            selected |= 1ULL << e;
        }
        if (cover.size() > 2 * packing.size()) return false;
        for (uint64_t t : tri_edges) if ((t & selected) == 0) return false;
        return true;
    }
};

static bool parse_graph6(const std::string &line, std::vector<std::vector<int>> &adj) {
    if (line.empty() || line[0] == '>') return false;
    int n = static_cast<unsigned char>(line[0]) - 63;
    if (n < 0 || n > 10) {
        std::cerr << "unsupported graph6 order: " << n << "\n";
        std::exit(2);
    }
    adj.assign(n, std::vector<int>(n, 0));
    int pos = 1, bitpos = 0;
    auto nextbit = [&]() {
        if (pos >= static_cast<int>(line.size())) {
            std::cerr << "truncated graph6 line\n";
            std::exit(2);
        }
        int v = static_cast<unsigned char>(line[pos]) - 63;
        int bit = (v >> (5 - bitpos)) & 1;
        if (++bitpos == 6) { bitpos = 0; ++pos; }
        return bit;
    };
    for (int j = 1; j < n; ++j) for (int i = 0; i < j; ++i)
        adj[i][j] = adj[j][i] = nextbit();
    return true;
}

int main() {
    std::string line;
    uint64_t graphs = 0, triangle_free = 0, certified = 0, tight_pair = 0;
    uint64_t total_triangles = 0, total_cover_nodes = 0, max_cover_nodes = 0;
    uint64_t fnv = 1469598103934665603ULL;
    int seen_n = -1, worst_slack = std::numeric_limits<int>::min();
    std::string first_tight;
    while (std::getline(std::cin, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        std::vector<std::vector<int>> adj;
        if (!parse_graph6(line, adj)) continue;
        ++graphs;
        seen_n = static_cast<int>(adj.size());
        for (unsigned char c : line) { fnv ^= c; fnv *= 1099511628211ULL; }
        fnv ^= '\n'; fnv *= 1099511628211ULL;

        GraphCheck gc(adj);
        total_triangles += gc.tri_edges.size();
        if (gc.tri_edges.empty()) { ++triangle_free; continue; }
        std::vector<int> packing, cover;
        if (!gc.construct_pair(packing, cover)) {
            std::cerr << "FAILED graph6=" << line << " n=" << gc.n
                      << " m=" << gc.m << " triangles=" << gc.tri_edges.size()
                      << " greedy_packing=" << packing.size() << "\n";
            return 1;
        }
        ++certified;
        total_cover_nodes += gc.cover_nodes;
        max_cover_nodes = std::max(max_cover_nodes, gc.cover_nodes);
        int slack = 2 * static_cast<int>(packing.size()) - static_cast<int>(cover.size());
        worst_slack = std::max(worst_slack, -slack);
        if (slack == 0) {
            ++tight_pair;
            if (first_tight.empty()) first_tight = line;
        }
    }
    std::cout << "PASS\n"
              << "n=" << seen_n << "\n"
              << "graphs=" << graphs << "\n"
              << "triangle_free=" << triangle_free << "\n"
              << "nontrivial_certified=" << certified << "\n"
              << "total_triangles=" << total_triangles << "\n"
              << "constructed_equality_pairs=" << tight_pair << "\n"
              << "first_equality_graph6=" << (first_tight.empty() ? "NONE" : first_tight) << "\n"
              << "total_cover_search_nodes=" << total_cover_nodes << "\n"
              << "max_cover_search_nodes=" << max_cover_nodes << "\n"
              << "graph6_stream_seeded_fnv_style64=" << std::hex << fnv << std::dec << "\n";
    return 0;
}
