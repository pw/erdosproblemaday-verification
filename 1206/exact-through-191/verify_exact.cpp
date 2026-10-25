#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

using namespace std;

// Definition-level exhaustive verifier for the new exact table in Erdős
// problem #1206.  A collision edge is the union of two different unordered
// root-pairs with equal sums of cubes.  A Sidon set of cube roots is exactly
// the complement of a vertex cover of this collision hypergraph.

struct Bits {
    array<uint64_t, 4> w{};
    bool operator==(const Bits& other) const { return w == other.w; }
};

struct BitsHash {
    size_t operator()(const Bits& bits) const {
        uint64_t h = 0x9e3779b97f4a7c15ULL;
        for (uint64_t x : bits.w) {
            x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
            x ^= x >> 27; x *= 0x94d049bb133111ebULL;
            x ^= x >> 31;
            h ^= x + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
        }
        return static_cast<size_t>(h);
    }
};

static bool empty_bits(const Bits& a) {
    return !(a.w[0] | a.w[1] | a.w[2] | a.w[3]);
}
static bool has_bit(const Bits& a, int index) {
    return (a.w[index >> 6] >> (index & 63)) & 1ULL;
}
static void set_bit(Bits& a, int index) {
    a.w[index >> 6] |= 1ULL << (index & 63);
}
static Bits intersect_bits(const Bits& a, const Bits& b) {
    Bits c;
    for (int i = 0; i < 4; ++i) c.w[i] = a.w[i] & b.w[i];
    return c;
}
static Bits and_not(const Bits& a, const Bits& b) {
    Bits c;
    for (int i = 0; i < 4; ++i) c.w[i] = a.w[i] & ~b.w[i];
    return c;
}
static bool subseteq(const Bits& a, const Bits& b) {
    for (int i = 0; i < 4; ++i) if (a.w[i] & ~b.w[i]) return false;
    return true;
}
static int popcount(const Bits& a) {
    return __builtin_popcountll(a.w[0]) + __builtin_popcountll(a.w[1])
         + __builtin_popcountll(a.w[2]) + __builtin_popcountll(a.w[3]);
}

struct CollisionData {
    vector<vector<int>> edges;
    uint64_t pair_count{};
    uint64_t sum_count{};
    uint64_t collision_group_count{};
    int max_representations{};
};

static CollisionData collision_data(int n) {
    map<uint64_t, vector<pair<int, int>>> groups;
    for (int a = 1; a <= n; ++a) {
        for (int b = a; b <= n; ++b) {
            const uint64_t sum = static_cast<uint64_t>(a) * a * a
                               + static_cast<uint64_t>(b) * b * b;
            groups[sum].push_back({a, b});
        }
    }

    set<vector<int>> unique_edges;
    uint64_t collision_groups = 0;
    int max_representations = 0;
    for (const auto& [sum, representations] : groups) {
        (void)sum;
        max_representations = max(max_representations,
                                  static_cast<int>(representations.size()));
        if (representations.size() > 1) ++collision_groups;
        for (int i = 1; i < static_cast<int>(representations.size()); ++i) {
            for (int j = 0; j < i; ++j) {
                vector<int> edge{
                    representations[i].first, representations[i].second,
                    representations[j].first, representations[j].second
                };
                sort(edge.begin(), edge.end());
                edge.erase(unique(edge.begin(), edge.end()), edge.end());
                unique_edges.insert(edge);
            }
        }
    }

    CollisionData result;
    result.edges.assign(unique_edges.begin(), unique_edges.end());
    result.pair_count = static_cast<uint64_t>(n) * (n + 1) / 2;
    result.sum_count = groups.size();
    result.collision_group_count = collision_groups;
    result.max_representations = max_representations;
    return result;
}

struct ExhaustiveCoverSearch {
    int n{};
    vector<vector<int>> edges;
    vector<Bits> incidence;
    unordered_map<Bits, int, BitsHash> failed_budget;
    uint64_t calls{};

    bool search(const Bits& active, int budget) {
        ++calls;
        if (empty_bits(active)) return true;
        if (budget <= 0) return false;

        const auto memo = failed_budget.find(active);
        if (memo != failed_budget.end() && memo->second >= budget) return false;

        // A greedily chosen family of pairwise vertex-disjoint edges is a
        // valid lower bound: every such edge needs a different cover vertex.
        Bits remaining = active;
        int packing_size = 0;
        while (!empty_bits(remaining)) {
            int chosen = -1;
            int fewest_conflicts = 1'000'000;
            for (int edge_index = 0;
                 edge_index < static_cast<int>(edges.size()); ++edge_index) {
                if (!has_bit(remaining, edge_index)) continue;
                Bits conflicts{};
                for (int vertex : edges[edge_index]) {
                    for (int word = 0; word < 4; ++word)
                        conflicts.w[word] |= incidence[vertex].w[word];
                }
                const int score = popcount(intersect_bits(remaining, conflicts));
                if (score < fewest_conflicts) {
                    fewest_conflicts = score;
                    chosen = edge_index;
                }
            }
            assert(chosen >= 0);
            if (++packing_size > budget) {
                failed_budget[active] = max(failed_budget[active], budget);
                return false;
            }
            Bits conflicts{};
            for (int vertex : edges[chosen]) {
                for (int word = 0; word < 4; ++word)
                    conflicts.w[word] |= incidence[vertex].w[word];
            }
            remaining = and_not(remaining, conflicts);
        }

        vector<int> degree(n + 1);
        for (int vertex = 1; vertex <= n; ++vertex) {
            degree[vertex] = popcount(intersect_bits(active, incidence[vertex]));
        }

        // Branch on all non-dominated vertices of one uncovered edge.
        int branch_edge = -1;
        tuple<int, int, int> best_score{-1, -1, -1};
        for (int edge_index = 0;
             edge_index < static_cast<int>(edges.size()); ++edge_index) {
            if (!has_bit(active, edge_index)) continue;
            vector<int> degrees;
            for (int vertex : edges[edge_index]) degrees.push_back(degree[vertex]);
            sort(degrees.rbegin(), degrees.rend());
            const tuple<int, int, int> score{
                accumulate(degrees.begin(), degrees.end(), 0),
                degrees.back(), degrees.front()
            };
            if (score > best_score) {
                best_score = score;
                branch_edge = edge_index;
            }
        }
        assert(branch_edge >= 0);

        vector<int> branch_vertices = edges[branch_edge];
        sort(branch_vertices.begin(), branch_vertices.end(),
             [&](int a, int b) {
                 if (degree[a] != degree[b]) return degree[a] > degree[b];
                 return a < b;
             });

        vector<int> undominated;
        for (int vertex : branch_vertices) {
            const Bits incident = intersect_bits(active, incidence[vertex]);
            bool redundant = false;
            for (int other : branch_vertices) {
                if (vertex == other) continue;
                const Bits other_incident =
                    intersect_bits(active, incidence[other]);
                // If incident(vertex) is contained in incident(other), any
                // solution choosing vertex can replace it by other.
                if (subseteq(incident, other_incident)
                    && (!(incident == other_incident) || other < vertex)) {
                    redundant = true;
                    break;
                }
            }
            if (!redundant) undominated.push_back(vertex);
        }

        for (int vertex : undominated) {
            const Bits next = and_not(active, incidence[vertex]);
            if (search(next, budget - 1)) return true;
        }
        failed_budget[active] = max(failed_budget[active], budget);
        return false;
    }

    bool has_cover_at_most(int budget) {
        incidence.assign(n + 1, Bits{});
        Bits all{};
        assert(edges.size() <= 256);
        for (int edge_index = 0;
             edge_index < static_cast<int>(edges.size()); ++edge_index) {
            set_bit(all, edge_index);
            for (int vertex : edges[edge_index])
                set_bit(incidence[vertex], edge_index);
        }
        return search(all, budget);
    }
};

struct Range {
    int lo;
    int hi;
    int tau;
    vector<int> cover_at_hi;
};

static const vector<Range> RANGES{
    {132, 133, 21, {2,10,29,30,33,36,42,44,45,51,54,58,59,63,66,72,76,90,94,102,110}},
    {134, 137, 22, {2,4,6,10,33,36,42,50,51,54,58,60,63,64,66,72,76,90,92,99,110,116}},
    {138, 143, 23, {2,6,10,27,30,33,36,42,50,51,54,58,59,60,63,66,72,76,90,94,110,116,138}},
    {144, 155, 24, {1,2,4,10,18,24,33,36,42,48,50,51,54,58,60,63,72,76,84,90,92,95,99,120}},
    {156, 160, 25, {1,2,4,18,24,33,36,48,50,51,58,60,63,69,72,76,80,90,92,99,116,120,138,142,156}},
    {161, 164, 26, {1,2,4,6,10,18,23,24,33,36,42,50,51,54,58,60,63,72,76,90,92,102,108,132,138,156}},
    {165, 165, 27, {1,2,4,6,10,18,22,23,24,33,36,42,50,51,54,63,72,76,90,92,100,102,108,114,132,138,156}},
    {166, 171, 28, {2,4,6,10,14,18,23,24,27,32,33,36,38,42,50,58,60,64,72,76,80,84,90,92,108,132,150,156}},
    {172, 173, 29, {2,4,10,12,14,18,23,24,33,36,42,44,48,50,58,60,64,71,72,76,84,90,92,99,108,135,150,156,165}},
    {174, 179, 30, {1,2,4,6,10,14,18,23,24,33,36,42,48,50,51,58,60,71,72,76,84,90,92,99,108,156,164,165,166,174}},
    {180, 185, 31, {2,4,10,14,18,23,24,33,36,42,44,48,50,51,58,60,64,66,71,72,76,84,90,92,99,108,141,150,156,165,166}},
    {186, 191, 32, {2,4,10,18,23,30,33,36,42,48,50,51,55,58,59,60,63,64,66,71,72,76,90,99,120,136,138,150,156,165,166,168}},
};

static bool cover_hits_all(const vector<int>& cover,
                           const vector<vector<int>>& edges) {
    set<int> chosen(cover.begin(), cover.end());
    for (const auto& edge : edges) {
        bool hit = false;
        for (int vertex : edge) if (chosen.count(vertex)) hit = true;
        if (!hit) return false;
    }
    return true;
}

static bool complement_is_sidon(int n, const vector<int>& cover) {
    vector<bool> deleted(n + 1, false);
    for (int vertex : cover) deleted[vertex] = true;
    map<uint64_t, pair<int, int>> seen;
    for (int a = 1; a <= n; ++a) if (!deleted[a]) {
        for (int b = a; b <= n; ++b) if (!deleted[b]) {
            const uint64_t sum = static_cast<uint64_t>(a) * a * a
                               + static_cast<uint64_t>(b) * b * b;
            if (!seen.emplace(sum, make_pair(a, b)).second) return false;
        }
    }
    return true;
}

int main() {
    assert(RANGES.front().lo == 132);
    assert(RANGES.back().hi == 191);
    for (size_t i = 1; i < RANGES.size(); ++i)
        assert(RANGES[i - 1].hi + 1 == RANGES[i].lo);

    uint64_t total_calls = 0;
    const auto total_start = chrono::steady_clock::now();
    for (const Range& range : RANGES) {
        CollisionData lower = collision_data(range.lo);
        ExhaustiveCoverSearch search;
        search.n = range.lo;
        search.edges = move(lower.edges);
        const auto start = chrono::steady_clock::now();
        const bool too_small = search.has_cover_at_most(range.tau - 1);
        const double seconds = chrono::duration<double>(
            chrono::steady_clock::now() - start).count();
        assert(!too_small);
        total_calls += search.calls;

        const CollisionData upper = collision_data(range.hi);
        assert(static_cast<int>(range.cover_at_hi.size()) == range.tau);
        assert(is_sorted(range.cover_at_hi.begin(), range.cover_at_hi.end()));
        assert(adjacent_find(range.cover_at_hi.begin(),
                             range.cover_at_hi.end()) == range.cover_at_hi.end());
        assert(range.cover_at_hi.front() >= 1);
        assert(range.cover_at_hi.back() <= range.hi);
        assert(cover_hits_all(range.cover_at_hi, upper.edges));
        assert(complement_is_sidon(range.hi, range.cover_at_hi));

        cout << "N=" << range.lo << ".." << range.hi
             << " tau=" << range.tau
             << " g3(N)=N-" << range.tau
             << " lower_edges=" << search.edges.size()
             << " upper_edges=" << upper.edges.size()
             << " exhaustive_calls=" << search.calls
             << " seconds=" << seconds << '\n';
    }

    const CollisionData final_data = collision_data(191);
    assert(final_data.pair_count == 18'336);
    assert(final_data.sum_count == 18'212);
    assert(final_data.collision_group_count == 124);
    assert(final_data.edges.size() == 124);
    assert(final_data.max_representations == 2);
    for (const auto& edge : final_data.edges) assert(edge.size() == 4);

    const double total_seconds = chrono::duration<double>(
        chrono::steady_clock::now() - total_start).count();
    cout << "FINAL N=191 pairs=18336 sums=18212 collision_groups=124"
         << " edges=124 max_representations=2\n";
    cout << "ALL CHECKS PASSED; exact table g3(N) for 132<=N<=191;"
         << " exhaustive_calls=" << total_calls
         << " seconds=" << total_seconds << '\n';
}
