#include <array>
#include <chrono>
#include <cstdlib>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

namespace {

constexpr int N = 69;
constexpr int TARGET_BELOW_69 = 32;
constexpr int MAX_SUM = 2 * N * N;

std::array<int, N> prefix_max{};
std::array<unsigned char, MAX_SUM + 1> used_sum{};
std::array<signed char, N> forced{};
std::vector<int> selected{N};
std::uint64_t nodes = 0;
std::chrono::steady_clock::time_point started;
bool use_candidate_bound = false;

bool individually_compatible(int candidate) {
    for (int j : selected) {
        if (used_sum[candidate * candidate + j * j]) {
            return false;
        }
    }
    return !used_sum[2 * candidate * candidate];
}

bool search(int k, int chosen_below_69) {
    ++nodes;
    if ((nodes & ((1ULL << 26) - 1)) == 0) {
        const auto seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        std::cerr << "nodes=" << nodes << " k=" << k
                  << " chosen=" << chosen_below_69
                  << " seconds=" << seconds << '\n';
    }
    if (chosen_below_69 == TARGET_BELOW_69) {
        return true;
    }
    if (k == 0 || chosen_below_69 + prefix_max[k] < TARGET_BELOW_69) {
        return false;
    }
    const int needed = TARGET_BELOW_69 - chosen_below_69;
    if (use_candidate_bound && k <= 30 && k - needed <= 4) {
        int compatible = 0;
        for (int candidate = k; candidate >= 1; --candidate) {
            if (individually_compatible(candidate)) {
                ++compatible;
                if (compatible >= needed) {
                    break;
                }
            }
            if (compatible + candidate - 1 < needed) {
                return false;
            }
        }
    }

    std::array<int, N + 1> new_sums{};
    int new_sum_count = 0;
    bool compatible = true;
    for (int j : selected) {
        const int value = k * k + j * j;
        if (used_sum[value]) {
            compatible = false;
            break;
        }
        new_sums[new_sum_count++] = value;
    }
    const int diagonal = 2 * k * k;
    if (compatible && used_sum[diagonal]) {
        compatible = false;
    }
    if (compatible && forced[k] != 0) {
        new_sums[new_sum_count++] = diagonal;
        for (int i = 0; i < new_sum_count; ++i) {
            used_sum[new_sums[i]] = 1;
        }
        selected.push_back(k);
        if (search(k - 1, chosen_below_69 + 1)) {
            return true;
        }
        selected.pop_back();
        for (int i = 0; i < new_sum_count; ++i) {
            used_sum[new_sums[i]] = 0;
        }
    }

    if (forced[k] != 1) {
        return search(k - 1, chosen_below_69);
    }
    return false;
}

}  // namespace

int main() {
    use_candidate_bound = std::getenv("ERDOS773_CANDIDATE_BOUND") != nullptr;
    forced.fill(-1);
    std::string cube;
    if (const char* cube_text = std::getenv("ERDOS773_CUBE")) {
        cube = cube_text;
        if (cube.size() > static_cast<std::size_t>(N - 1)) {
            std::cerr << "cube is too long\n";
            return 2;
        }
        for (std::size_t position = 0; position < cube.size(); ++position) {
            if (cube[position] != '0' && cube[position] != '1') {
                std::cerr << "cube must contain only 0 and 1\n";
                return 2;
            }
            forced[N - 1 - static_cast<int>(position)] = cube[position] - '0';
        }
    }
    std::ifstream input("oeis_A390813_b390813.txt");
    if (!input) {
        std::cerr << "cannot open OEIS b-file\n";
        return 2;
    }
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty() || line.front() == '#') {
            continue;
        }
        std::istringstream fields(line);
        int index = 0;
        int value = 0;
        if (!(fields >> index >> value) || index < 1 || index >= N) {
            std::cerr << "invalid OEIS b-file row: " << line << '\n';
            return 2;
        }
        prefix_max[index] = value;
    }
    for (int i = 1; i < N; ++i) {
        if (prefix_max[i] == 0) {
            std::cerr << "missing OEIS value at " << i << '\n';
            return 2;
        }
    }
    if (prefix_max[N - 1] != TARGET_BELOW_69) {
        std::cerr << "unexpected published a(68)\n";
        return 2;
    }

    used_sum[2 * N * N] = 1;
    started = std::chrono::steady_clock::now();
    const bool found = search(N - 1, 0);
    const auto seconds = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    std::cout << "status=" << (found ? "SATISFIABLE" : "UNSATISFIABLE")
              << " nodes=" << nodes << " seconds=" << seconds
              << " candidate_bound=" << (use_candidate_bound ? 1 : 0)
              << " cube=" << (cube.empty() ? "none" : cube) << '\n';
    if (found) {
        std::cout << "indices=";
        for (std::size_t i = 0; i < selected.size(); ++i) {
            if (i) {
                std::cout << ',';
            }
            std::cout << selected[i];
        }
        std::cout << '\n';
    }
    return found ? 10 : 20;
}
