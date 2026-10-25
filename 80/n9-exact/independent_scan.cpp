#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// Independent literal scan of one graph6 representative of every
// unlabelled graph of order 9.  No SAT variables or triangle auxiliaries.

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: independent_scan all_n9.g6\n";
        return 2;
    }
    std::ifstream in(argv[1]);
    if (!in) return 3;

    std::array<int, 8> best{};
    best.fill(-1);
    std::array<std::string, 8> witness{};
    std::array<std::uint64_t, 8> exact_book_count{};
    std::array<std::uint64_t, 37> edge_hist{};
    std::uint64_t records = 0, admissible = 0;
    std::string line;

    while (std::getline(in, line)) {
        if (line.empty()) continue;
        ++records;
        if (static_cast<unsigned char>(line[0]) != 63 + 9 || line.size() != 7) {
            std::cerr << "unexpected graph6 record at " << records << "\n";
            return 4;
        }
        std::array<std::uint16_t, 9> adj{};
        int byte = 1, bit = 5;
        for (int v = 1; v < 9; ++v) {
            for (int u = 0; u < v; ++u) {
                const int present = (static_cast<unsigned char>(line[byte]) - 63) >> bit & 1;
                if (present) {
                    adj[u] |= std::uint16_t(1u << v);
                    adj[v] |= std::uint16_t(1u << u);
                }
                if (--bit < 0) {
                    bit = 5;
                    ++byte;
                }
            }
        }

        int edges = 0;
        for (int u = 0; u < 9; ++u) edges += std::popcount(adj[u]);
        edges /= 2;

        int book = 0;
        bool covered = true;
        for (int u = 0; u < 9; ++u) {
            for (int v = u + 1; v < 9; ++v) {
                if (!(adj[u] >> v & 1u)) continue;
                const int q = std::popcount(std::uint16_t(adj[u] & adj[v]));
                if (q == 0) covered = false;
                if (q > book) book = q;
            }
        }
        if (!covered) continue;
        ++admissible;
        ++exact_book_count[book];
        ++edge_hist[edges];
        for (int cap = book; cap <= 7; ++cap) {
            if (edges > best[cap]) {
                best[cap] = edges;
                witness[cap] = line;
            }
        }
    }

    if (records != 274668) {
        std::cerr << "wrong unlabelled graph count: " << records << "\n";
        return 5;
    }
    std::cout << "records=" << records << " admissible=" << admissible << "\n";
    std::cout << "frontier=";
    for (int k = 0; k <= 7; ++k) std::cout << (k ? "," : "") << best[k];
    std::cout << "\n";
    for (int k = 0; k <= 7; ++k) {
        std::cout << "k=" << k << " best=" << best[k]
                  << " witness_graph6=" << witness[k] << "\n";
    }
    std::cout << "exact_book_counts=";
    for (int k = 0; k <= 7; ++k)
        std::cout << (k ? "," : "") << exact_book_count[k];
    std::cout << "\nedge_hist=";
    bool first = true;
    for (int e = 0; e <= 36; ++e) {
        if (!edge_hist[e]) continue;
        std::cout << (first ? "" : ",") << e << ":" << edge_hist[e];
        first = false;
    }
    std::cout << "\n";
}
