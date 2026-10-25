#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <tuple>
#include <vector>

using namespace std;

static long long nodes = 0;

static bool all_coprime(const vector<int>& a) {
    for (size_t i = 0; i < a.size(); ++i) {
        for (size_t j = 0; j < i; ++j) {
            if (std::gcd(a[i], a[j]) != 1) return false;
        }
    }
    return true;
}

struct CliqueDecision {
    int target;
    vector<vector<unsigned char>> adjacent;
    mutable vector<int> found;

    // A greedy proper coloring of the candidate subgraph.  Vertices are
    // emitted color-class by color-class; color[i] is then a valid upper
    // bound for a clique contained in the prefix ending at i.
    void color_order(const vector<int>& candidates,
                     vector<int>& order,
                     vector<int>& colors) const {
        vector<int> uncolored = candidates;
        order.clear();
        colors.clear();
        int color = 0;
        while (!uncolored.empty()) {
            ++color;
            vector<int> next;
            vector<int> this_class;
            for (int v : uncolored) {
                bool compatible_with_class = true;
                for (int w : this_class) {
                    if (adjacent[v][w]) {
                        compatible_with_class = false;
                        break;
                    }
                }
                if (compatible_with_class) {
                    this_class.push_back(v);
                    order.push_back(v);
                    colors.push_back(color);
                } else {
                    next.push_back(v);
                }
            }
            uncolored.swap(next);
        }
    }

    bool expand(vector<int>& chosen, vector<int> candidates) const {
        ++nodes;
        if (static_cast<int>(chosen.size()) >= target) {
            found = chosen;
            return true;
        }
        if (static_cast<int>(chosen.size() + candidates.size()) < target) return false;

        vector<int> order, colors;
        color_order(candidates, order, colors);
        for (int i = static_cast<int>(order.size()) - 1; i >= 0; --i) {
            if (static_cast<int>(chosen.size()) + colors[i] < target) return false;
            int v = order[i];

            vector<int> next;
            next.reserve(i);
            for (int j = 0; j < i; ++j) {
                int w = order[j];
                if (adjacent[v][w]) next.push_back(w);
            }
            chosen.push_back(v);
            if (expand(chosen, std::move(next))) return true;
            chosen.pop_back();
        }
        return false;
    }
};

static bool exists_for_gap(int x, int d, int target, vector<int>* witness = nullptr) {
    vector<int> starts;
    for (int v = 2; v + d <= x; ++v) {
        if (std::gcd(v, v + d) == 1) starts.push_back(v);
    }

    CliqueDecision solver;
    solver.target = target;
    solver.adjacent.assign(starts.size(), vector<unsigned char>(starts.size(), 0));
    for (size_t i = 0; i < starts.size(); ++i) {
        for (size_t j = 0; j < i; ++j) {
            vector<int> four = {
                starts[i], starts[i] + d, starts[j], starts[j] + d
            };
            if (all_coprime(four)) {
                solver.adjacent[i][j] = solver.adjacent[j][i] = 1;
            }
        }
    }

    vector<int> candidates(starts.size());
    iota(candidates.begin(), candidates.end(), 0);
    vector<int> chosen;
    bool ok = solver.expand(chosen, std::move(candidates));
    if (ok && witness) {
        witness->clear();
        for (int index : solver.found) witness->push_back(starts[index]);
        sort(witness->begin(), witness->end());
    }
    return ok;
}

static bool exists_grid(int x, int target, int* witness_gap = nullptr,
                        vector<int>* witness = nullptr) {
    for (int d = 1; d <= x - 2; ++d) {
        if (exists_for_gap(x, d, target, witness)) {
            if (witness_gap) *witness_gap = d;
            return true;
        }
    }
    return false;
}

struct Row {
    int n;
    int threshold;
    int d;
    vector<int> starts;
};

static const vector<Row> rows = {
    {11, 101, 12, {11,13,17,31,37,41,47,61,67,71,89}},
    {12, 107, 6,  {11,23,31,41,43,53,61,65,73,83,97,101}},
    {13, 127, 6,  {13,23,25,37,41,53,61,73,83,101,103,113,121}},
    {14, 131, 18, {5,13,19,29,41,43,49,53,79,83,89,103,109,113}},
    {15, 149, 10, {13,17,19,31,37,43,49,61,73,79,97,103,121,127,139}},
    {16, 167, 10, {13,19,31,37,43,49,61,73,79,97,103,121,127,139,153,157}},
    {17, 173, 10, {13,17,19,31,37,43,49,61,73,79,97,103,121,127,139,157,163}},
    {18, 191, 10, {17,19,31,37,43,61,73,79,97,103,121,127,139,151,157,163,169,181}},
    {19, 197, 18, {5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,163,173,179}},
    {20, 211, 18, {5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,173,179,181,193}},
    {21, 241, 12, {17,25,31,41,47,61,67,71,97,101,127,137,151,157,161,179,181,197,211,227,229}},
    {22, 251, 18, {19,29,41,43,49,53,79,83,89,103,109,113,137,139,149,173,179,181,211,221,223,233}},
    {23, 257, 18, {5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,173,179,181,211,223,233,239}},
    {24, 271, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,173,181,193,199,227,233,239,241}},
    {25, 281, 30, {17,23,31,41,59,67,73,83,101,107,109,121,127,149,167,173,181,193,199,227,233,239,241,247,251}},
    {26, 307, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,203,227,239,241,251,263,277}},
    {27, 313, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,203,227,239,241,263,277,281,283}},
    {28, 347, 30, {17,23,31,41,59,67,73,83,101,107,109,121,127,149,167,181,193,199,227,239,241,247,263,281,283,301,307,317}},
    {29, 361, 30, {7,17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,319,331}},
    {30, 367, 30, {7,17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,319,331,337}},
    {31, 379, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349}},
    {32, 383, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349,353}},
    {33, 389, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349,353,359}},
    {34, 431, 30, {17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,319,331,343,353,367,379,389,401}},
    {35, 439, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,401,409}},
    {36, 449, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,401,409,419}},
    {37, 463, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,409,419,431,433}},
    {38, 487, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,409,431,433,449,457}},
    {39, 491, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,401,409,433,449,457,461}},
    {40, 509, 30, {17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,401,409,419,433,457,461,479}},
};

int main(int argc, char** argv) {
    if (argc == 2) {
        int n = stoi(argv[1]);
        auto it = find_if(rows.begin(), rows.end(), [n](const Row& row) {
            return row.n == n;
        });
        if (it == rows.end()) return 3;
        vector<int> values;
        for (int v : it->starts) {
            values.push_back(v);
            values.push_back(v + it->d);
        }
        assert(all_coprime(values));
        nodes = 0;
        bool below = exists_grid(it->threshold - 1, it->n);
        cout << "n=" << it->n << " threshold=" << it->threshold
             << " witness=PASS below=" << (below ? "SAT" : "UNSAT")
             << " nodes=" << nodes << "\n";
        return below ? 2 : 0;
    }
    if (argc == 4) {
        int target = stoi(argv[1]);
        int first_x = stoi(argv[2]);
        int last_x = stoi(argv[3]);
        for (int x = first_x; x <= last_x; ++x) {
            nodes = 0;
            int gap = 0;
            vector<int> witness;
            if (exists_grid(x, target, &gap, &witness)) {
                cout << "target=" << target << " threshold=" << x
                     << " gap=" << gap << " starts=";
                for (int v : witness) cout << v << ',';
                cout << " nodes=" << nodes << "\n";
                return 0;
            }
        }
        cout << "no threshold in range\n";
        return 1;
    }
    auto started = chrono::steady_clock::now();
    for (const auto& row : rows) {
        vector<int> values;
        for (int v : row.starts) {
            values.push_back(v);
            values.push_back(v + row.d);
        }
        assert(static_cast<int>(row.starts.size()) == row.n);
        assert(*max_element(values.begin(), values.end()) <= row.threshold);
        assert(all_coprime(values));

        nodes = 0;
        bool below = exists_grid(row.threshold - 1, row.n);
        cout << "n=" << row.n << " threshold=" << row.threshold
             << " witness=PASS below=" << (below ? "SAT" : "UNSAT")
             << " nodes=" << nodes << "\n";
        if (below) return 2;
    }
    auto elapsed = chrono::duration<double>(chrono::steady_clock::now() - started).count();
    cout << "elapsed_seconds=" << elapsed << "\n";
    cout << "INDEPENDENT C++ AUDIT PASS\n";
    return 0;
}
