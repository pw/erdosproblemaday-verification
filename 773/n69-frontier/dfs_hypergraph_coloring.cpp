#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int N = 69;
constexpr int TARGET_BELOW_69 = 32;

struct Bits {
    std::uint64_t lo = 0;
    std::uint64_t hi = 0;
};

Bits operator&(Bits left, Bits right) {
    return {left.lo & right.lo, left.hi & right.hi};
}

Bits without(Bits left, Bits right) {
    return {left.lo & ~right.lo, left.hi & ~right.hi};
}

bool any(Bits bits) {
    return bits.lo != 0 || bits.hi != 0;
}

int count(Bits bits) {
    return __builtin_popcountll(bits.lo) + __builtin_popcountll(bits.hi);
}

void set_bit(Bits& bits, int vertex) {
    if (vertex <= 64) {
        bits.lo |= 1ULL << (vertex - 1);
    } else {
        bits.hi |= 1ULL << (vertex - 65);
    }
}

void clear_bit(Bits& bits, int vertex) {
    if (vertex <= 64) {
        bits.lo &= ~(1ULL << (vertex - 1));
    } else {
        bits.hi &= ~(1ULL << (vertex - 65));
    }
}

int take_first(Bits& bits) {
    if (bits.lo != 0) {
        const int vertex = __builtin_ctzll(bits.lo) + 1;
        bits.lo &= bits.lo - 1;
        return vertex;
    }
    const int vertex = __builtin_ctzll(bits.hi) + 65;
    bits.hi &= bits.hi - 1;
    return vertex;
}

Bits prefix_bits(int k) {
    if (k <= 0) {
        return {};
    }
    if (k < 64) {
        return {(1ULL << k) - 1, 0};
    }
    if (k == 64) {
        return {~0ULL, 0};
    }
    return {~0ULL, (1ULL << (k - 64)) - 1};
}

std::array<int, N> prefix_max{};
std::array<signed char, N> forced{};
std::array<unsigned char, N + 1> chosen{};
std::array<unsigned short, N + 1> block_count{};
std::array<std::array<unsigned short, N + 1>, N + 1> pair_count{};
std::array<Bits, N + 1> pair_neighbors{};
Bits blocked;
std::vector<std::vector<int>> supports;
std::array<std::vector<int>, N + 1> incident;
std::vector<unsigned char> support_selected;
std::vector<unsigned char> support_excluded;
std::uint64_t nodes = 0;
std::uint64_t prefix_prunes = 0;
std::uint64_t blocked_prunes = 0;
std::uint64_t color_calls = 0;
std::uint64_t color_prunes = 0;
int color_slack = 0;
std::chrono::steady_clock::time_point started;

#ifdef ERDOS773_AUDIT
void verify_state(int k) {
    std::array<unsigned short, N + 1> expected_blocks{};
    std::array<std::array<unsigned short, N + 1>, N + 1> expected_pairs{};
    for (std::size_t edge_id = 0; edge_id < supports.size(); ++edge_id) {
        int selected = 0;
        int excluded = 0;
        std::vector<int> remaining;
        for (int vertex : supports[edge_id]) {
            if (chosen[vertex]) {
                ++selected;
            } else if (vertex > k) {
                ++excluded;
            } else {
                remaining.push_back(vertex);
            }
        }
        if ((excluded == 0 && selected != support_selected[edge_id]) ||
            excluded != support_excluded[edge_id]) {
            std::cerr << "support state mismatch at edge " << edge_id
                      << " k=" << k << " expected_selected=" << selected
                      << " actual_selected=" << static_cast<int>(support_selected[edge_id])
                      << " expected_excluded=" << excluded
                      << " actual_excluded=" << static_cast<int>(support_excluded[edge_id])
                      << " support=";
            for (int vertex : supports[edge_id]) {
                std::cerr << vertex << ':' << static_cast<int>(chosen[vertex]) << ',';
            }
            std::cerr << '\n';
            std::exit(3);
        }
        if (selected == static_cast<int>(supports[edge_id].size())) {
            std::cerr << "fully selected collision support\n";
            std::exit(3);
        }
        if (excluded == 0 && remaining.size() == 1) {
            ++expected_blocks[remaining[0]];
        } else if (excluded == 0 && remaining.size() == 2) {
            int first = remaining[0];
            int second = remaining[1];
            if (first > second) {
                std::swap(first, second);
            }
            ++expected_pairs[first][second];
        }
    }
    for (int first = 1; first <= k; ++first) {
        if (block_count[first] != expected_blocks[first]) {
            std::cerr << "block state mismatch at vertex " << first << '\n';
            std::exit(3);
        }
        const bool block_bit = any(prefix_bits(first) & blocked) &&
                               count(prefix_bits(first) & blocked) !=
                                   count(prefix_bits(first - 1) & blocked);
        if (block_bit != (expected_blocks[first] != 0)) {
            std::cerr << "block mask mismatch at vertex " << first << '\n';
            std::exit(3);
        }
        for (int second = first + 1; second <= k; ++second) {
            if (pair_count[first][second] != expected_pairs[first][second]) {
                std::cerr << "pair state mismatch at vertices " << first << ','
                          << second << '\n';
                std::exit(3);
            }
            Bits singleton{};
            set_bit(singleton, second);
            const bool neighbor_bit = any(pair_neighbors[first] & singleton);
            if (neighbor_bit != (expected_pairs[first][second] != 0)) {
                std::cerr << "pair mask mismatch at vertices " << first << ','
                          << second << '\n';
                std::exit(3);
            }
        }
    }
}
#endif

void add_block(int vertex) {
    if (block_count[vertex]++ == 0) {
        set_bit(blocked, vertex);
    }
}

void remove_block(int vertex) {
    if (block_count[vertex] == 0) {
        std::cerr << "internal block-count underflow\n";
        std::exit(3);
    }
    if (--block_count[vertex] == 0) {
        clear_bit(blocked, vertex);
    }
}

void add_pair(int first, int second) {
    if (first > second) {
        std::swap(first, second);
    }
    if (pair_count[first][second]++ == 0) {
        set_bit(pair_neighbors[first], second);
        set_bit(pair_neighbors[second], first);
    }
}

void remove_pair(int first, int second) {
    if (first > second) {
        std::swap(first, second);
    }
    if (pair_count[first][second] == 0) {
        std::cerr << "internal pair-count underflow\n";
        std::exit(3);
    }
    if (--pair_count[first][second] == 0) {
        clear_bit(pair_neighbors[first], second);
        clear_bit(pair_neighbors[second], first);
    }
}

std::array<int, 2> remaining_two(int edge_id) {
    std::array<int, 2> result{};
    int size = 0;
    for (int vertex : supports[edge_id]) {
        if (!chosen[vertex]) {
            if (size == 2) {
                std::cerr << "internal remaining-two overflow\n";
                std::exit(3);
            }
            result[size++] = vertex;
        }
    }
    if (size != 2) {
        std::cerr << "internal remaining-two count error\n";
        std::exit(3);
    }
    return result;
}

int remaining_one(int edge_id) {
    int result = 0;
    for (int vertex : supports[edge_id]) {
        if (!chosen[vertex]) {
            if (result != 0) {
                std::cerr << "internal remaining-one overflow\n";
                std::exit(3);
            }
            result = vertex;
        }
    }
    if (result == 0) {
        std::cerr << "internal remaining-one count error\n";
        std::exit(3);
    }
    return result;
}

int densest_vertex(Bits candidates) {
    Bits scan = candidates;
    int best_vertex = 0;
    int best_degree = -1;
    while (any(scan)) {
        const int vertex = take_first(scan);
        const int degree = count(pair_neighbors[vertex] & candidates);
        if (degree > best_degree) {
            best_vertex = vertex;
            best_degree = degree;
        }
    }
    return best_vertex;
}

// Partition viable candidates into conflict cliques.  A feasible extension
// can use at most one vertex from each clique, so the number of parts is an
// upper bound.  Returning as soon as the bound reaches needed saves work on
// nodes this test cannot prune.
int clique_cover_bound(int k, int needed) {
    Bits remaining = without(prefix_bits(k), blocked);
#ifdef ERDOS773_AUDIT
    const Bits original = remaining;
    Bits assigned{};
#endif
    int cliques = 0;
    while (any(remaining)) {
        if (++cliques >= needed) {
            return cliques;
        }
        const int seed = densest_vertex(remaining);
        clear_bit(remaining, seed);
#ifdef ERDOS773_AUDIT
        std::vector<int> clique{seed};
        set_bit(assigned, seed);
#endif
        Bits candidates = remaining & pair_neighbors[seed];
        while (any(candidates)) {
            const int vertex = densest_vertex(candidates);
#ifdef ERDOS773_AUDIT
            for (int prior : clique) {
                Bits singleton{};
                set_bit(singleton, vertex);
                if (!any(pair_neighbors[prior] & singleton)) {
                    std::cerr << "nonedge placed in conflict clique\n";
                    std::exit(3);
                }
            }
            clique.push_back(vertex);
            set_bit(assigned, vertex);
#endif
            clear_bit(remaining, vertex);
            clear_bit(candidates, vertex);
            candidates = candidates & pair_neighbors[vertex];
        }
    }
#ifdef ERDOS773_AUDIT
    if (assigned.lo != original.lo || assigned.hi != original.hi) {
        std::cerr << "clique cover does not partition candidates\n";
        std::exit(3);
    }
#endif
    return cliques;
}

bool search(int k, int selected_below_69) {
    ++nodes;
#ifdef ERDOS773_AUDIT
    verify_state(k);
#endif
    if ((nodes & ((1ULL << 26) - 1)) == 0) {
        const auto seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        std::cerr << "nodes=" << nodes << " k=" << k
                  << " selected=" << selected_below_69
                  << " color_calls=" << color_calls
                  << " color_prunes=" << color_prunes
                  << " seconds=" << seconds << '\n';
    }
    if (selected_below_69 == TARGET_BELOW_69) {
        return true;
    }
    const int needed = TARGET_BELOW_69 - selected_below_69;
    if (k == 0 || selected_below_69 + prefix_max[k] < TARGET_BELOW_69) {
        ++prefix_prunes;
        return false;
    }
    const int available = count(without(prefix_bits(k), blocked));
    if (available < needed) {
        ++blocked_prunes;
        return false;
    }
    if (prefix_max[k] - needed <= color_slack) {
        ++color_calls;
        if (clique_cover_bound(k, needed) < needed) {
            ++color_prunes;
            return false;
        }
    }

    if (forced[k] != 0 && block_count[k] == 0) {
        chosen[k] = 1;
        for (int edge_id : incident[k]) {
            if (support_excluded[edge_id] != 0) {
                continue;
            }
            const int old_remaining = static_cast<int>(supports[edge_id].size()) -
                                      support_selected[edge_id];
            ++support_selected[edge_id];
            if (old_remaining == 3) {
                const auto pair = remaining_two(edge_id);
                add_pair(pair[0], pair[1]);
            } else if (old_remaining == 2) {
                add_block(remaining_one(edge_id));
            } else if (old_remaining <= 1) {
                std::cerr << "selected a blocked collision vertex\n";
                std::exit(3);
            }
        }

        if (search(k - 1, selected_below_69 + 1)) {
            return true;
        }

        for (auto edge_it = incident[k].rbegin(); edge_it != incident[k].rend();
             ++edge_it) {
            const int edge_id = *edge_it;
            if (support_excluded[edge_id] != 0) {
                continue;
            }
            const int current_remaining =
                static_cast<int>(supports[edge_id].size()) -
                support_selected[edge_id];
            if (current_remaining == 2) {
                const auto pair = remaining_two(edge_id);
                remove_pair(pair[0], pair[1]);
            } else if (current_remaining == 1) {
                remove_block(remaining_one(edge_id));
            }
            --support_selected[edge_id];
        }
        chosen[k] = 0;
    }

    if (forced[k] != 1) {
        for (int edge_id : incident[k]) {
            ++support_excluded[edge_id];
        }
        const bool found = search(k - 1, selected_below_69);
        for (auto edge_it = incident[k].rbegin(); edge_it != incident[k].rend();
             ++edge_it) {
            --support_excluded[*edge_it];
        }
        return found;
    }
    return false;
}

void build_supports() {
    std::map<int, std::vector<std::pair<int, int>>> representations;
    for (int i = 1; i <= N; ++i) {
        for (int j = i; j <= N; ++j) {
            representations[i * i + j * j].push_back({i, j});
        }
    }
    std::set<std::vector<int>> unique_supports;
    for (const auto& [sum, pairs] : representations) {
        (void)sum;
        for (std::size_t first = 0; first < pairs.size(); ++first) {
            for (std::size_t second = first + 1; second < pairs.size(); ++second) {
                std::vector<int> support = {
                    pairs[first].first,
                    pairs[first].second,
                    pairs[second].first,
                    pairs[second].second,
                };
                std::sort(support.begin(), support.end());
                support.erase(std::unique(support.begin(), support.end()), support.end());
                unique_supports.insert(std::move(support));
            }
        }
    }
    supports.assign(unique_supports.begin(), unique_supports.end());
    if (supports.size() != 712) {
        std::cerr << "unexpected collision-support count\n";
        std::exit(2);
    }
    support_selected.assign(supports.size(), 0);
    support_excluded.assign(supports.size(), 0);
    for (std::size_t edge_id = 0; edge_id < supports.size(); ++edge_id) {
        for (int vertex : supports[edge_id]) {
            incident[vertex].push_back(static_cast<int>(edge_id));
        }
    }
}

}  // namespace

int main() {
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
    if (const char* slack_text = std::getenv("ERDOS773_COLOR_SLACK")) {
        color_slack = std::stoi(slack_text);
        if (color_slack < 0 || color_slack > TARGET_BELOW_69) {
            std::cerr << "invalid color slack\n";
            return 2;
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

    build_supports();
    chosen[N] = 1;
    for (int edge_id : incident[N]) {
        ++support_selected[edge_id];
    }
    for (std::size_t edge_id = 0; edge_id < supports.size(); ++edge_id) {
        const int remaining = static_cast<int>(supports[edge_id].size()) -
                              support_selected[edge_id];
        if (remaining == 2) {
            const auto pair = remaining_two(static_cast<int>(edge_id));
            add_pair(pair[0], pair[1]);
        }
    }

    started = std::chrono::steady_clock::now();
    const bool found = search(N - 1, 0);
    const auto seconds = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    std::cout << "status=" << (found ? "SATISFIABLE" : "UNSATISFIABLE")
              << " nodes=" << nodes << " seconds=" << seconds
              << " prefix_prunes=" << prefix_prunes
              << " blocked_prunes=" << blocked_prunes
              << " color_calls=" << color_calls
              << " color_prunes=" << color_prunes
              << " color_slack=" << color_slack
              << " cube=" << (cube.empty() ? "none" : cube) << '\n';
    if (found) {
        std::cout << "indices=";
        bool first = true;
        for (int i = 1; i <= N; ++i) {
            if (chosen[i]) {
                std::cout << (first ? "" : ",") << i;
                first = false;
            }
        }
        std::cout << '\n';
    }
    return found ? 10 : 20;
}
