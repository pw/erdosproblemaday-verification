#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

using std::array;
using std::cerr;
using std::cout;
using std::sort;
using std::string;
using std::vector;

constexpr int TARGET = 20;
constexpr int OFFSET = 512;
constexpr int SUMS = 1025;

struct Search {
    int cap;
    int core_size;
    int t_lo;
    int t_hi;
    uint64_t orbit_nodes = 0;
    uint64_t complete_cores = 0;
    uint64_t valid_cores = 0;
    uint64_t extension_nodes = 0;
    vector<int> witness;
    vector<int> core;
    array<unsigned char, SUMS> counts{};

    static int duplicate_differences(int r) {
        if ((r & 1) == 0) {
            int q = r / 2;
            return q * (q - 1);
        }
        int q_minus_1 = (r - 1) / 2;
        return q_minus_1 * q_minus_1;
    }

    static int core_diameter_lb(int r) { return (r * r) / 4; }

    bool add_values(const vector<int>& added, int exception,
                    vector<int>& changed) {
        changed.clear();
        // New unordered sums: new-old, then pairs within the new block.
        for (int z : added) {
            for (int x : core) changed.push_back(z + x);
        }
        for (size_t i = 0; i < added.size(); ++i) {
            for (size_t j = i; j < added.size(); ++j)
                changed.push_back(added[i] + added[j]);
        }
        array<unsigned char, SUMS> delta{};
        for (int s : changed) {
            int index = s + OFFSET;
            if (index < 0 || index >= SUMS) std::abort();
            ++delta[index];
        }
        for (int s : changed) {
            int index = s + OFFSET;
            if (s != exception && counts[index] + delta[index] > 1)
                return false;
        }
        for (int s : changed) ++counts[s + OFFSET];
        core.insert(core.end(), added.begin(), added.end());
        return true;
    }

    void undo_values(const vector<int>& added, const vector<int>& changed) {
        core.resize(core.size() - added.size());
        for (int s : changed) --counts[s + OFFSET];
    }

    bool valid_extension_candidate(int z, int exception) const {
        if (std::find(core.begin(), core.end(), z) != core.end()) return false;
        if (2 * z == exception) return false;
        int partner = exception - z;
        if (std::find(core.begin(), core.end(), partner) != core.end())
            return false;
        return true;
    }

    bool extend(int exception, int need, int chosen, int start_z) {
        ++extension_nodes;
        if (chosen == need) {
            witness = core;
            sort(witness.begin(), witness.end());
            return true;
        }
        int remaining_after = need - chosen - 1;
        int max_z = cap;
        for (int z = start_z; z <= max_z - remaining_after; ++z) {
            if (!valid_extension_candidate(z, exception)) continue;
            int low = z;
            int high = z;
            for (int y : core) {
                low = std::min(low, y);
                high = std::max(high, y);
            }
            if (high - low > cap) continue;

            vector<int> added{z};
            vector<int> changed;
            if (!add_values(added, exception, changed)) continue;
            if (extend(exception, need, chosen + 1, z + 1)) return true;
            undo_values(added, changed);
        }
        return false;
    }

    bool finish_core(int exception) {
        ++complete_cores;
        ++valid_cores;
        int need = TARGET - core_size;
        if (need == 0) {
            witness = core;
            sort(witness.begin(), witness.end());
            return true;
        }
        int slack = cap - exception;
        return extend(exception, need, 0, -slack);
    }

    bool orbit_dfs(int exception, int next_b, int orbits_needed) {
        ++orbit_nodes;
        if (orbits_needed == 0) return finish_core(exception);
        // Lower marks lie in [1,floor((T-1)/2)].  Keep the endpoint when T
        // is odd; dropping it is the classic inclusive-boundary bug here.
        int max_lower = (exception - 1) / 2;
        int max_b = max_lower - orbits_needed + 1;
        for (int b = next_b; b <= max_b; ++b) {
            int c = exception - b;
            vector<int> added{b, c};
            vector<int> changed;
            if (!add_values(added, exception, changed)) continue;
            if (orbit_dfs(exception, b + 1, orbits_needed - 1)) return true;
            undo_values(added, changed);
        }
        return false;
    }

    bool search_exception(int exception) {
        core.clear();
        counts.fill(0);
        core.push_back(0);
        core.push_back(exception);
        counts[0 + OFFSET] = 1;
        counts[exception + OFFSET] = 1;
        counts[2 * exception + OFFSET] = 1;
        int pair_orbits = core_size / 2;
        int orbits_needed = pair_orbits - 1;  // {0,T} is already one orbit.
        if (core_size & 1) {
            if (exception & 1) return false;
            int midpoint = exception / 2;
            vector<int> added{midpoint};
            vector<int> changed;
            if (!add_values(added, exception, changed)) std::abort();
            // Keep midpoint permanently for this exception.
        }
        return orbit_dfs(exception, 1, orbits_needed);
    }

    bool run() {
        int total_lb = TARGET * (TARGET - 1) / 2
                     - duplicate_differences(core_size);
        if (total_lb > cap) {
            cout << "SKIP core=" << core_size << " total_diameter_lb="
                 << total_lb << " cap=" << cap << "\n";
            return false;
        }
        int lo = std::max(t_lo, core_diameter_lb(core_size));
        int hi = std::min(t_hi, cap);
        if (core_size & 1) {
            if (lo & 1) ++lo;
            for (int t = lo; t <= hi; t += 2) {
                if (search_exception(t)) return true;
            }
        } else {
            for (int t = lo; t <= hi; ++t) {
                if (search_exception(t)) return true;
            }
        }
        return false;
    }
};

int main(int argc, char** argv) {
    if (argc != 5) {
        cerr << "usage: search864_20_orbit CAP CORE_SIZE T_LO T_HI\n";
        return 64;
    }
    Search search{std::stoi(argv[1]), std::stoi(argv[2]),
                  std::stoi(argv[3]), std::stoi(argv[4])};
    auto started = std::chrono::steady_clock::now();
    bool found = search.run();
    double seconds = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    cout << "RESULT cap=" << search.cap << " core=" << search.core_size
         << " t_range=" << search.t_lo << ".." << search.t_hi
         << " found=" << (found ? 1 : 0)
         << " orbit_nodes=" << search.orbit_nodes
         << " complete_cores=" << search.complete_cores
         << " valid_cores=" << search.valid_cores
         << " extension_nodes=" << search.extension_nodes
         << " seconds=" << seconds << "\n";
    if (found) {
        cout << "WITNESS";
        for (int x : search.witness) cout << " " << x;
        cout << "\n";
        return 2;
    }
    return 0;
}
