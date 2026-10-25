#!/usr/bin/env python3
"""From-scratch verifier for the finite computation in erdos864_wave6p.md.

The exhaustive part proves that no 18-element near-Sidon set has diameter at
most 115.  It uses only Python integers as bitsets; no SAT/MIP package and no
downloaded table is used.

Run:
    python runs/erdos864_wave6p_reverify.py

The search classifies a hypothetical set by q, the number of representations
of its unique exceptional sum.  A difference count forces q >= 7.  Its
reflection-closed core consequently has one of the following forms:

    core size 18, 17, 16, 15, 14
    outliers    0,  1,  2,  3,  4

Every reflection-closed core is generated from its lower half B.  B must be a
Golomb ruler (equivalently, an ordinary Sidon set), so distinct-difference
backtracking enumerates it without omissions.  Outliers are then added
monotonically: once a forbidden second repeated sum occurs, later additions
cannot repair it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from typing import Iterable


MAX_FORBIDDEN_DIAMETER = 115
TARGET_SIZE = 18

# Normalized witnesses (minimum 0).
WITNESS_16 = (0, 2, 3, 10, 16, 28, 33, 37, 48, 52, 57, 69, 75, 82, 83, 85)
WITNESS_17 = (
    0,
    1,
    3,
    7,
    15,
    24,
    35,
    40,
    53,
    66,
    71,
    82,
    91,
    99,
    103,
    105,
    106,
)
WITNESS_18 = (
    0,
    1,
    3,
    11,
    15,
    20,
    36,
    43,
    49,
    67,
    73,
    80,
    96,
    101,
    105,
    113,
    115,
    116,
)


# Optimized implementation of exactly the same exhaustive search as the
# readable Python class below.  The wrapper compiles this source in a temporary
# directory; no generated source or binary is retained.
CXX_SOURCE = r"""
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <utility>
#include <vector>

using std::array;
using std::cout;
using std::map;
using std::pair;
using std::vector;

constexpr int MAXD = 115;
constexpr int TARGET = 18;
constexpr int WORDS = 7; // enough for all shifted sums (maximum is 336)

struct Bits {
    array<uint64_t, WORDS> w{};

    void set(int position) {
        if (position < 0 || position >= 64 * WORDS) std::abort();
        w[position >> 6] |= uint64_t(1) << (position & 63);
    }

    void merge(const Bits& other) {
        for (int i = 0; i < WORDS; ++i) w[i] |= other.w[i];
    }

    bool only(int position) const {
        for (int i = 0; i < WORDS; ++i) {
            uint64_t expected = 0;
            if (i == (position >> 6))
                expected = uint64_t(1) << (position & 63);
            if (w[i] != expected) return false;
        }
        return true;
    }

    bool intersects_outside(const Bits& other, int allowed) const {
        for (int i = 0; i < WORDS; ++i) {
            uint64_t collision = w[i] & other.w[i];
            if (i == (allowed >> 6))
                collision &= ~(uint64_t(1) << (allowed & 63));
            if (collision) return true;
        }
        return false;
    }
};

pair<Bits, Bits> sum_bits(const vector<int>& values) {
    Bits once, multiple;
    for (size_t i = 0; i < values.size(); ++i) {
        for (size_t j = i; j < values.size(); ++j) {
            int sum = values[i] + values[j];
            int word = sum >> 6;
            uint64_t bit = uint64_t(1) << (sum & 63);
            if (once.w[word] & bit) multiple.w[word] |= bit;
            else once.w[word] |= bit;
        }
    }
    return {once, multiple};
}

struct Stats {
    int core_size = 0;
    int outliers = 0;
    uint64_t lower_halves = 0;
    uint64_t core_candidates = 0;
    uint64_t valid_cores = 0;
    uint64_t extension_nodes = 0;
    uint64_t digest = 1469598103934665603ULL;
};

struct Search {
    map<int, Stats> stats;
    vector<int> marks;
    vector<int> counterexample;

    Search() {
        for (int size = 14; size <= 18; ++size)
            stats[size] = Stats{size, TARGET - size};
        marks.push_back(0);
    }

    static int diameter_lb(int size) { return size * size / 4; }

    static bool contains(const vector<int>& values, int value) {
        return std::find(values.begin(), values.end(), value) != values.end();
    }

    void record_core(int size, const vector<int>& core) {
        Stats& s = stats[size];
        ++s.valid_cores;
        for (int x : core) {
            s.digest ^= uint64_t(x + 1);
            s.digest *= 1099511628211ULL;
        }
        s.digest ^= 255;
        s.digest *= 1099511628211ULL;
    }

    bool extension_rec(
        const vector<int>& core,
        int center_sum,
        int diameter,
        int slack,
        const vector<int>& shifted_core,
        int shifted_exception,
        int need,
        int start_index,
        Bits represented,
        vector<int>& chosen,
        Stats& s
    ) {
        ++s.extension_nodes;
        if (int(chosen.size()) == need) {
            counterexample = core;
            counterexample.insert(
                counterexample.end(), chosen.begin(), chosen.end()
            );
            std::sort(counterexample.begin(), counterexample.end());
            return true;
        }

        const int candidate_count = MAXD + slack + 1;
        for (int index = start_index; index < candidate_count; ++index) {
            int z = index - slack;
            if (contains(core, z)) continue;
            if (2 * z == center_sum) continue;
            int partner = center_sum - z;
            if (contains(core, partner) || contains(chosen, partner)) continue;

            int low = std::min(0, z);
            int high = std::max(diameter, z);
            for (int x : chosen) {
                low = std::min(low, x);
                high = std::max(high, x);
            }
            if (high - low > MAXD) continue;

            int zs = z + slack;
            Bits news;
            news.set(2 * zs);
            for (int x : shifted_core) news.set(zs + x);
            for (int x : chosen) news.set(zs + x + slack);
            if (represented.intersects_outside(news, shifted_exception))
                continue;

            Bits updated = represented;
            updated.merge(news);
            chosen.push_back(z);
            if (extension_rec(
                    core, center_sum, diameter, slack, shifted_core,
                    shifted_exception, need, index + 1, updated, chosen, s
                ))
                return true;
            chosen.pop_back();
        }
        return false;
    }

    bool extend_core(
        const vector<int>& core, int center_sum, const Bits& once, int need,
        Stats& s
    ) {
        if (need == 0) {
            counterexample = core;
            return true;
        }
        int diameter = core.back();
        int slack = MAXD - diameter;
        vector<int> shifted_core;
        for (int x : core) shifted_core.push_back(x + slack);
        int shifted_exception = center_sum + 2 * slack;

        // Translate the represented-sum bitset by 2*slack.
        Bits shifted_once;
        for (int position = 0; position < 64 * WORDS; ++position) {
            if (once.w[position >> 6] &
                (uint64_t(1) << (position & 63)))
                shifted_once.set(position + 2 * slack);
        }
        vector<int> chosen;
        return extension_rec(
            core, center_sum, diameter, slack, shifted_core,
            shifted_exception, need, 0, shifted_once, chosen, s
        );
    }

    bool process_core(
        const vector<int>& lower, int diameter, bool odd_core
    ) {
        vector<int> core = lower;
        int size;
        if (odd_core) {
            if (diameter & 1) return false;
            size = 2 * int(lower.size()) + 1;
            core.push_back(diameter / 2);
        } else {
            size = 2 * int(lower.size());
        }
        for (auto it = lower.rbegin(); it != lower.rend(); ++it)
            core.push_back(diameter - *it);

        Stats& s = stats[size];
        ++s.core_candidates;
        auto [once, multiple] = sum_bits(core);
        if (!multiple.only(diameter)) return false;
        record_core(size, core);
        return extend_core(core, diameter, once, TARGET - size, s);
    }

    bool leaf(int k) {
        vector<int> lower = marks;
        int max_lower = lower.back();
        int even_size = 2 * k;
        if (stats.count(even_size)) {
            ++stats[even_size].lower_halves;
            int start = std::max(2 * max_lower + 1, diameter_lb(even_size));
            for (int diameter = start; diameter <= MAXD; ++diameter)
                if (process_core(lower, diameter, false)) return true;
        }

        int odd_size = 2 * k + 1;
        if (stats.count(odd_size)) {
            ++stats[odd_size].lower_halves;
            int start = std::max(2 * max_lower + 1, diameter_lb(odd_size));
            if (start & 1) ++start;
            for (int diameter = start; diameter <= MAXD; diameter += 2)
                if (process_core(lower, diameter, true)) return true;
        }
        return false;
    }

    bool lower_dfs(int k, int start, uint64_t differences) {
        int need = k - int(marks.size());
        if (need == 0) return leaf(k);
        int max_mark = (MAXD - 1) / 2;
        int max_candidate = max_mark - (need - 1); // inclusive
        for (int candidate = start; candidate <= max_candidate; ++candidate) {
            uint64_t new_differences = 0;
            bool ok = true;
            for (int old : marks) {
                uint64_t bit = uint64_t(1) << (candidate - old);
                if ((differences | new_differences) & bit) {
                    ok = false;
                    break;
                }
                new_differences |= bit;
            }
            if (!ok) continue;
            marks.push_back(candidate);
            if (lower_dfs(k, candidate + 1,
                          differences | new_differences))
                return true;
            marks.pop_back();
        }
        return false;
    }

    bool run() {
        for (int k : {9, 8, 7}) {
            marks.assign(1, 0);
            if (lower_dfs(k, 1, 0)) return false;
        }
        return true;
    }
};

int main() {
    Search search;
    bool exhausted = search.run();
    for (int size = 18; size >= 14; --size) {
        const Stats& s = search.stats[size];
        cout << "CASE " << size
             << " outliers=" << s.outliers
             << " lower_halves=" << s.lower_halves
             << " core_candidates=" << s.core_candidates
             << " valid_cores=" << s.valid_cores
             << " extension_nodes=" << s.extension_nodes
             << " fnv64=" << std::hex << std::setw(16)
             << std::setfill('0') << s.digest << std::dec << "\n";
    }
    if (!exhausted) {
        cout << "COUNTEREXAMPLE";
        for (int x : search.counterexample) cout << " " << x;
        cout << "\n";
        return 2;
    }
    cout << "EXHAUSTED: no 18-element near-Sidon set has diameter <= 115\n";
    return 0;
}
"""


def representation_counts(values: Iterable[int]) -> dict[int, int]:
    """Return counts of unordered representations s=a+b, allowing a=b."""
    a = tuple(sorted(values))
    counts: dict[int, int] = {}
    for i, x in enumerate(a):
        for y in a[i:]:
            counts[x + y] = counts.get(x + y, 0) + 1
    return counts


def exceptional_sums(values: Iterable[int]) -> dict[int, int]:
    return {s: c for s, c in representation_counts(values).items() if c > 1}


def is_near_sidon(values: Iterable[int]) -> bool:
    a = tuple(sorted(values))
    return len(a) == len(set(a)) and len(exceptional_sums(a)) <= 1


def sum_bitsets(values: tuple[int, ...]) -> tuple[int, int]:
    """Return (represented-at-least-once, represented-at-least-twice)."""
    once = 0
    multiple = 0
    for i, x in enumerate(values):
        for y in values[i:]:
            bit = 1 << (x + y)
            if once & bit:
                multiple |= bit
            else:
                once |= bit
    return once, multiple


@dataclass
class CaseStats:
    core_size: int
    outliers: int
    lower_halves: int = 0
    core_candidates: int = 0
    valid_cores: int = 0
    extension_nodes: int = 0
    digest: str = ""


class ExhaustiveSearch:
    def __init__(self, max_diameter: int = MAX_FORBIDDEN_DIAMETER) -> None:
        self.max_diameter = max_diameter
        self.counterexample: tuple[int, ...] | None = None
        self._hashers: dict[int, hashlib._Hash] = {}
        self.stats = {
            18: CaseStats(18, 0),
            17: CaseStats(17, 1),
            16: CaseStats(16, 2),
            15: CaseStats(15, 3),
            14: CaseStats(14, 4),
        }

    @staticmethod
    def _diameter_lower_bound(core_size: int) -> int:
        # A centrally symmetric m-set has floor(m^2/4) distinct positive
        # differences; all lie between 1 and its diameter.
        return (core_size * core_size) // 4

    def _record_core(self, core_size: int, core: tuple[int, ...]) -> None:
        stats = self.stats[core_size]
        stats.valid_cores += 1
        h = self._hashers.setdefault(core_size, hashlib.sha256())
        h.update(",".join(map(str, core)).encode("ascii"))
        h.update(b";")

    def _extend_core(
        self,
        core: tuple[int, ...],
        center_sum: int,
        once: int,
        need: int,
        stats: CaseStats,
    ) -> bool:
        """Try every exact-core outlier set of the requested size."""
        if need == 0:
            self.counterexample = core
            return True

        diameter = core[-1] - core[0]
        assert core[0] == 0 and core[-1] == diameter
        slack = self.max_diameter - diameter
        shift = slack  # makes every possible relative outlier nonnegative
        shifted_core = tuple(x + shift for x in core)
        shifted_exception = center_sum + 2 * shift
        once_shifted = once << (2 * shift)
        core_set = set(core)

        # These are exactly the relative coordinates which can occur after
        # translating a configuration of total diameter <= max_diameter.
        candidates = tuple(range(-slack, self.max_diameter + 1))
        chosen: list[int] = []

        def rec(start: int, represented: int) -> bool:
            stats.extension_nodes += 1
            if len(chosen) == need:
                self.counterexample = tuple(sorted(core + tuple(chosen)))
                return True

            for index in range(start, len(candidates)):
                z = candidates[index]
                if z in core_set:
                    continue

                # The core is, by definition, all elements paired by
                # reflection in the exceptional sum.  Outliers therefore
                # cannot be a midpoint or a reflection partner of a core
                # element or a previously chosen outlier.
                if 2 * z == center_sum:
                    continue
                partner = center_sum - z
                if partner in core_set or partner in chosen:
                    continue

                low = min(0, z, *chosen)
                high = max(diameter, z, *chosen)
                if high - low > self.max_diameter:
                    continue

                z_shifted = z + shift
                new_sums = 1 << (2 * z_shifted)
                for x in shifted_core:
                    new_sums |= 1 << (z_shifted + x)
                for x in chosen:
                    new_sums |= 1 << (z_shifted + x + shift)

                # Sums newly involving z are mutually distinct: equality
                # z+x=z+y gives x=y, and 2z=z+x would give x=z, excluded
                # above.  Thus only collisions with old sums need testing.
                collisions = represented & new_sums
                if collisions & ~(1 << shifted_exception):
                    continue

                chosen.append(z)
                if rec(index + 1, represented | new_sums):
                    return True
                chosen.pop()
            return False

        return rec(0, once_shifted)

    def _process_core(
        self,
        lower: tuple[int, ...],
        diameter: int,
        odd_core: bool,
    ) -> bool:
        k = len(lower)
        if odd_core:
            core_size = 2 * k + 1
            if diameter % 2:
                return False
            core = lower + (diameter // 2,) + tuple(
                diameter - x for x in reversed(lower)
            )
        else:
            core_size = 2 * k
            core = lower + tuple(diameter - x for x in reversed(lower))

        stats = self.stats[core_size]
        stats.core_candidates += 1
        once, multiple = sum_bitsets(core)

        # Symmetry supplies many representations of `diameter`; validity is
        # exactly the assertion that no other sum is represented twice.
        if multiple != 1 << diameter:
            return False

        self._record_core(core_size, core)
        return self._extend_core(
            core=core,
            center_sum=diameter,
            once=once,
            need=TARGET_SIZE - core_size,
            stats=stats,
        )

    def _enumerate_lower_halves(self, k: int) -> bool:
        """Generate every k-mark Golomb ruler B with min(B)=0."""
        max_mark = (self.max_diameter - 1) // 2
        marks = [0]

        def leaf() -> bool:
            lower = tuple(marks)
            max_lower = lower[-1]

            # Even core 2k: all integer diameters T with 2*max(B) < T.
            even_core_size = 2 * k
            if even_core_size in self.stats:
                self.stats[even_core_size].lower_halves += 1
                start = max(
                    2 * max_lower + 1,
                    self._diameter_lower_bound(even_core_size),
                )
                for diameter in range(start, self.max_diameter + 1):
                    if self._process_core(lower, diameter, odd_core=False):
                        return True

            # Odd core 2k+1: T must be even so that T/2 is an integer mark.
            odd_core_size = 2 * k + 1
            if odd_core_size in self.stats:
                self.stats[odd_core_size].lower_halves += 1
                start = max(
                    2 * max_lower + 1,
                    self._diameter_lower_bound(odd_core_size),
                )
                if start % 2:
                    start += 1
                for diameter in range(start, self.max_diameter + 1, 2):
                    if self._process_core(lower, diameter, odd_core=True):
                        return True
            return False

        def dfs(start: int, differences: int) -> bool:
            need = k - len(marks)
            if need == 0:
                return leaf()

            # Inclusive upper bound is max_mark-(need-1).  The +2 in range's
            # endpoint is deliberate and is regression-tested in quick_checks.
            stop = max_mark - need + 2
            for candidate in range(start, stop):
                new_differences = 0
                for old in marks:
                    bit = 1 << (candidate - old)
                    if (differences | new_differences) & bit:
                        break
                    new_differences |= bit
                else:
                    marks.append(candidate)
                    if dfs(candidate + 1, differences | new_differences):
                        return True
                    marks.pop()
            return False

        return dfs(1, 0)

    def run(self) -> bool:
        # k=9 covers core size 18; k=8 covers 16,17; k=7 covers 14,15.
        for k in (9, 8, 7):
            if self._enumerate_lower_halves(k):
                return False
        for core_size, h in self._hashers.items():
            self.stats[core_size].digest = h.hexdigest()
        return True


def quick_checks() -> None:
    assert is_near_sidon(WITNESS_16)
    assert is_near_sidon(WITNESS_17)
    assert is_near_sidon(WITNESS_18)
    assert exceptional_sums(WITNESS_16) == {85: 8}
    assert exceptional_sums(WITNESS_17) == {106: 9}
    assert exceptional_sums(WITNESS_18) == {116: 9}
    assert WITNESS_16[-1] - WITNESS_16[0] == 85
    assert WITNESS_17[-1] - WITNESS_17[0] == 106
    assert WITNESS_18[-1] - WITNESS_18[0] == 116

    # Difference-reflection count for m=18.  With q representations of the
    # exceptional sum, the number D of duplicated positive-difference values
    # is q(q-1) without a midpoint and (q-1)^2 with one.  For q<=6, D<=30,
    # so at least C(18,2)-30=123 distinct positive differences are required.
    # For q=7 with a midpoint, D=36 and the required diameter is at least
    # 117.  Under the cap 115 the only cases are therefore the five core
    # sizes 14,15,16,17,18 enumerated above.
    pair_count = TARGET_SIZE * (TARGET_SIZE - 1) // 2
    max_duplicates_for_q_at_most_6 = 6 * 5
    assert pair_count == 153
    assert pair_count - max_duplicates_for_q_at_most_6 == 123
    assert pair_count - (7 - 1) ** 2 == 117

    # Boundary regression for the corrected inclusive DFS endpoint: this
    # 9-mark Golomb ruler uses the largest globally admissible lower mark 57.
    boundary_ruler = (0, 1, 3, 7, 12, 26, 36, 44, 57)
    diffs = [
        boundary_ruler[j] - boundary_ruler[i]
        for j in range(len(boundary_ruler))
        for i in range(j)
    ]
    assert len(diffs) == len(set(diffs))
    assert boundary_ruler[-1] == (MAX_FORBIDDEN_DIAMETER - 1) // 2


def run_compiled_full_search() -> float:
    compiler = shutil.which("g++")
    if compiler is None:
        raise SystemExit(
            "g++ is required for the default optimized full search; "
            "use --python-full for the slow pure-Python implementation"
        )
    with tempfile.TemporaryDirectory(prefix="erdos864_verify_") as tmp:
        source = f"{tmp}/verify.cpp"
        binary = f"{tmp}/verify"
        with open(source, "w", encoding="utf-8") as handle:
            handle.write(CXX_SOURCE)
        subprocess.run(
            [compiler, "-O3", "-DNDEBUG", "-std=c++17", source, "-o", binary],
            check=True,
        )
        started = time.perf_counter()
        result = subprocess.run(
            [binary],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        elapsed = time.perf_counter() - started
        print(result.stdout, end="")
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        return elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quick",
        action="store_true",
        help="check witnesses and arithmetic only; skip exhaustive search",
    )
    parser.add_argument(
        "--python-full",
        action="store_true",
        help="use the readable but much slower pure-Python exhaustive search",
    )
    args = parser.parse_args()

    quick_checks()
    print("quick checks: PASS")
    print("16-witness:", list(WITNESS_16), exceptional_sums(WITNESS_16))
    print("17-witness:", list(WITNESS_17), exceptional_sums(WITNESS_17))
    print("18-witness:", list(WITNESS_18), exceptional_sums(WITNESS_18))
    if args.quick:
        return

    if not args.python_full:
        elapsed = run_compiled_full_search()
        print(f"elapsed_seconds: {elapsed:.6f}")
        print("CONCLUSION: F(107)=...=F(116)=17 and F(117)=18")
        return

    started = time.perf_counter()
    search = ExhaustiveSearch()
    exhausted = search.run()
    elapsed = time.perf_counter() - started

    serializable_stats = {
        size: {
            "outliers": s.outliers,
            "lower_halves": s.lower_halves,
            "core_candidates": s.core_candidates,
            "valid_cores": s.valid_cores,
            "extension_nodes": s.extension_nodes,
            "sha256": s.digest,
        }
        for size, s in sorted(search.stats.items(), reverse=True)
    }
    print(json.dumps(serializable_stats, indent=2, sort_keys=True))
    print(f"elapsed_seconds: {elapsed:.6f}")
    if not exhausted:
        raise SystemExit(
            "COUNTEREXAMPLE FOUND: " + repr(search.counterexample)
        )
    print("EXHAUSTED: no 18-element near-Sidon set has diameter <= 115")
    print("CONCLUSION: F(107)=...=F(116)=17 and F(117)=18")


if __name__ == "__main__":
    main()
