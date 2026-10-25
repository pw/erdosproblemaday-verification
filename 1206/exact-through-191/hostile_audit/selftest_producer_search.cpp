#define main frozen_verifier_main
#include "/tmp/erdos1206_exact_132_191/verify_exact.cpp"
#undef main

#include <random>

static int brute_tau(int n, const vector<vector<int>>& edges) {
    int best = n + 1;
    for (uint64_t selected = 0; selected < (1ULL << n); ++selected) {
        int size = __builtin_popcountll(selected);
        if (size >= best) continue;
        bool covers = true;
        for (const auto& edge : edges) {
            bool hit = false;
            for (int v : edge) hit |= (selected >> (v - 1)) & 1ULL;
            if (!hit) { covers = false; break; }
        }
        if (covers) best = size;
    }
    return best;
}

static void check_instance(int n, const vector<vector<int>>& edges) {
    const int tau = brute_tau(n, edges);
    for (int budget = 0; budget <= n; ++budget) {
        ExhaustiveCoverSearch candidate;
        candidate.n = n;
        candidate.edges = edges;
        bool got = candidate.has_cover_at_most(budget);
        bool expected = tau <= budget;
        if (got != expected) {
            cerr << "mismatch n=" << n << " edges=" << edges.size()
                 << " budget=" << budget << " got=" << got
                 << " expected=" << expected << '\n';
            abort();
        }
    }
}

int main() {
    // Exhaust every hypergraph on the 15 nonempty subsets of four vertices.
    vector<vector<int>> possible;
    for (int mask = 1; mask < 16; ++mask) {
        vector<int> edge;
        for (int v = 1; v <= 4; ++v)
            if (mask & (1 << (v - 1))) edge.push_back(v);
        possible.push_back(edge);
    }
    uint64_t exhaustive = 0;
    for (uint64_t family = 0; family < (1ULL << possible.size()); ++family) {
        vector<vector<int>> edges;
        for (size_t i = 0; i < possible.size(); ++i)
            if (family & (1ULL << i)) edges.push_back(possible[i]);
        check_instance(4, edges);
        ++exhaustive;
    }

    // Larger deterministic hostile instances stress memoization and
    // domination while brute force remains cheap.
    mt19937_64 rng(0x1206c01dcafeULL);
    uint64_t random_cases = 0;
    for (int n = 5; n <= 12; ++n) {
        for (int trial = 0; trial < 250; ++trial) {
            set<vector<int>> unique;
            const int max_edges = min<int>(45, (1ULL << n) - 1);
            int wanted = static_cast<int>(rng() % (max_edges + 1));
            while (static_cast<int>(unique.size()) < wanted) {
                uint64_t mask = 1 + rng() % ((1ULL << n) - 1);
                vector<int> edge;
                for (int v = 1; v <= n; ++v)
                    if (mask & (1ULL << (v - 1))) edge.push_back(v);
                unique.insert(move(edge));
            }
            vector<vector<int>> edges(unique.begin(), unique.end());
            check_instance(n, edges);
            ++random_cases;
        }
    }
    cout << "FROZEN SEARCH SELF-TEST PASS exhaustive_hypergraphs=" << exhaustive
         << " random_hypergraphs=" << random_cases << '\n';
}
