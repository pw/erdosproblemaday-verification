#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <mutex>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

#include <nlohmann/json.hpp>
#include <omp.h>

using json = nlohmann::json;

struct Cube {
  std::vector<std::array<int, 2>> edges;
  std::vector<std::array<int, 4>> squares;
  std::vector<std::array<int, 8>> edge_squares;
};

static Cube build_cube() {
  constexpr int n = 9;
  Cube cube;
  std::unordered_map<int, int> index;
  for (int u = 0; u < (1 << n); ++u) {
    for (int direction = 0; direction < n; ++direction) {
      int v = u ^ (1 << direction);
      if (u < v) {
        index[(u << n) | v] = static_cast<int>(cube.edges.size());
        cube.edges.push_back({u, v});
      }
    }
  }
  cube.edge_squares.resize(cube.edges.size());
  std::vector<int> degree(cube.edges.size());
  for (int d1 = 0; d1 < n; ++d1) {
    for (int d2 = d1 + 1; d2 < n; ++d2) {
      int m1 = 1 << d1, m2 = 1 << d2;
      for (int base = 0; base < (1 << n); ++base) {
        if (base & (m1 | m2)) continue;
        int a = base, b = base | m1, c = base | m2, d = base | m1 | m2;
        auto get = [&](int x, int y) {
          if (x > y) std::swap(x, y);
          return index.at((x << n) | y);
        };
        std::array<int, 4> square{get(a, b), get(a, c), get(b, d), get(c, d)};
        int si = static_cast<int>(cube.squares.size());
        cube.squares.push_back(square);
        for (int edge : square) cube.edge_squares[edge][degree[edge]++] = si;
      }
    }
  }
  for (int d : degree) if (d != 8) throw std::runtime_error("bad incidence degree");
  return cube;
}

struct Buckets {
  std::array<std::vector<int>, 9> items;
  std::vector<int> score;
  std::vector<int> position;

  explicit Buckets(int n) : score(n, -1), position(n, -1) {}

  void add(int edge, int value) {
    score[edge] = value;
    position[edge] = static_cast<int>(items[value].size());
    items[value].push_back(edge);
  }

  void remove(int edge) {
    int value = score[edge], pos = position[edge];
    int last = items[value].back();
    items[value][pos] = last;
    position[last] = pos;
    items[value].pop_back();
    score[edge] = position[edge] = -1;
  }

  void change(int edge, int delta) {
    int value = score[edge];
    remove(edge);
    add(edge, value + delta);
  }
};

static void vector_remove(std::vector<int>& values, std::vector<int>& positions, int value) {
  int pos = positions[value], last = values.back();
  values[pos] = last;
  positions[last] = pos;
  values.pop_back();
  positions[value] = -1;
}

static void vector_add(std::vector<int>& values, std::vector<int>& positions, int value) {
  positions[value] = static_cast<int>(values.size());
  values.push_back(value);
}

static bool run_trial(const Cube& cube, const std::vector<char>& baseline,
                      uint64_t seed, int64_t steps, std::vector<char>& answer) {
  std::mt19937_64 rng(seed);
  int m = static_cast<int>(cube.edges.size());
  int ns = static_cast<int>(cube.squares.size());
  std::vector<char> selected = baseline;
  std::vector<int> count(ns);
  for (int si = 0; si < ns; ++si)
    for (int edge : cube.squares[si]) count[si] += selected[edge];

  std::vector<std::pair<int, int>> seeds;
  for (int edge = 0; edge < m; ++edge) if (!selected[edge]) {
    int conflicts = 0;
    for (int si : cube.edge_squares[edge]) conflicts += count[si] == 3;
    seeds.push_back({conflicts, edge});
  }
  std::sort(seeds.begin(), seeds.end());
  int seed_pool = std::min<int>(69, seeds.size());
  int added = seeds[rng() % seed_pool].second;
  selected[added] = true;
  for (int si : cube.edge_squares[added]) ++count[si];

  std::vector<int> violations, violation_pos(ns, -1);
  for (int si = 0; si < ns; ++si)
    if (count[si] == 4) vector_add(violations, violation_pos, si);

  Buckets buckets(m);
  for (int edge = 0; edge < m; ++edge) if (!selected[edge]) {
    int score = 0;
    for (int si : cube.edge_squares[edge]) score += count[si] == 3;
    buckets.add(edge, score);
  }
  std::vector<int64_t> tabu_until(m);

  for (int64_t step = 0; step < steps; ++step) {
    if (violations.empty()) {
      answer = std::move(selected);
      return true;
    }
    int square = violations[rng() % violations.size()];
    int edge_out = cube.squares[square][rng() & 3];

    for (int si : cube.edge_squares[edge_out]) {
      int old = count[si];
      if (old == 4) vector_remove(violations, violation_pos, si);
      if (old == 3) {
        for (int edge : cube.squares[si]) {
          if (!selected[edge]) { buckets.change(edge, -1); break; }
        }
      }
      --count[si];
    }
    selected[edge_out] = false;
    int out_score = 0;
    for (int si : cube.edge_squares[edge_out]) out_score += count[si] == 3;
    buckets.add(edge_out, out_score);
    tabu_until[edge_out] = step + 7 + static_cast<int>(rng() % 17);

    int edge_in = -1;
    bool noise = (rng() % 1000) < 25;
    int start_score = 0;
    if (noise) start_score = static_cast<int>(rng() % 3);
    for (int score = start_score; score < 9 && edge_in < 0; ++score) {
      auto& choices = buckets.items[score];
      if (choices.empty()) continue;
      int offset = static_cast<int>(rng() % choices.size());
      for (int j = 0; j < static_cast<int>(choices.size()); ++j) {
        int candidate = choices[(offset + j) % choices.size()];
        if (tabu_until[candidate] <= step) { edge_in = candidate; break; }
      }
    }
    if (edge_in < 0) {
      for (int score = 0; score < 9 && edge_in < 0; ++score)
        if (!buckets.items[score].empty())
          edge_in = buckets.items[score][rng() % buckets.items[score].size()];
    }

    buckets.remove(edge_in);
    selected[edge_in] = true;
    for (int si : cube.edge_squares[edge_in]) {
      int old = count[si];
      if (old == 2) {
        for (int edge : cube.squares[si]) {
          if (!selected[edge]) { buckets.change(edge, +1); break; }
        }
      }
      ++count[si];
      if (old == 3) vector_add(violations, violation_pos, si);
    }
  }
  return false;
}

int main(int argc, char** argv) {
  if (argc < 5) {
    std::cerr << "usage: q9_min_conflicts INPUT OUTPUT THREADS STEPS_PER_THREAD [SEED]\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  json source = json::parse(input);
  Cube cube = build_cube();
  std::unordered_map<int, int> index;
  for (int i = 0; i < static_cast<int>(cube.edges.size()); ++i)
    index[(cube.edges[i][0] << 9) | cube.edges[i][1]] = i;
  std::vector<char> baseline(cube.edges.size());
  for (const auto& edge : source.at("edges")) {
    int u = edge[0], v = edge[1];
    if (u > v) std::swap(u, v);
    baseline[index.at((u << 9) | v)] = true;
  }
  int threads = std::stoi(argv[3]);
  int64_t steps = std::stoll(argv[4]);
  uint64_t master_seed = argc > 5 ? std::stoull(argv[5]) : 861506;
  std::atomic<bool> found(false);
  std::vector<char> answer;
  std::mutex answer_mutex;
  omp_set_num_threads(threads);
#pragma omp parallel
  {
    int tid = omp_get_thread_num();
    std::vector<char> local_answer;
    if (!found.load() && run_trial(cube, baseline,
          master_seed + 0x9e3779b97f4a7c15ULL * (tid + 1), steps, local_answer)) {
      std::lock_guard<std::mutex> lock(answer_mutex);
      if (!found.exchange(true)) answer = std::move(local_answer);
    }
  }
  if (!found.load()) {
    std::cout << "no witness in " << threads << " trials x " << steps << " steps\n";
    return 1;
  }
  json output;
  output["n"] = 9;
  output["num_edges"] = 0;
  output["construction"] = "parallel min-conflicts swaps from published Q9=1505";
  output["meta"] = {{"source", argv[1]}, {"seed", master_seed}, {"steps_per_thread", steps}};
  output["edges"] = json::array();
  for (int edge = 0; edge < static_cast<int>(answer.size()); ++edge) if (answer[edge]) {
    output["edges"].push_back({cube.edges[edge][0], cube.edges[edge][1]});
    output["num_edges"] = output["num_edges"].get<int>() + 1;
  }
  std::ofstream out(argv[2]);
  out << output.dump(2) << '\n';
  std::cout << "FOUND " << output["num_edges"] << " edges; wrote " << argv[2] << '\n';
  return 0;
}
