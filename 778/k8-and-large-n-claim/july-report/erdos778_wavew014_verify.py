#!/usr/bin/env python3
"""
From-scratch exact minimax checker for the three games in Erdős problem #778.

No graph/game package is used.  A state is two bit masks on E(K_n).  The
default solver quotients states only by explicitly enumerated vertex
relabelings after an elementary colour-refinement step.  The --cross-check
mode repeats the small computations without any symmetry quotient.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import time
from fractions import Fraction
from functools import lru_cache


class Solver:
    def __init__(
        self,
        n: int,
        metric: str,
        alice_batch: int = 1,
        bob_batch: int = 1,
        symmetry: bool = True,
    ) -> None:
        # functools caches on methods are shared by all instances.  Runs here
        # are sequential, so clear them to make state counts local and to avoid
        # retaining previous solver instances.
        type(self).metric.cache_clear()
        type(self).canonical.cache_clear()
        type(self).bob_can_force_win.cache_clear()
        if metric not in {"clique", "degree"}:
            raise ValueError(metric)
        self.n = n
        self.metric_name = metric
        self.p = alice_batch
        self.q = bob_batch
        self.symmetry = symmetry
        self.edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        self.m = len(self.edges)
        self.full = (1 << self.m) - 1
        self.edge_index = [[-1] * n for _ in range(n)]
        for e, (i, j) in enumerate(self.edges):
            self.edge_index[i][j] = self.edge_index[j][i] = e
        self.calls = 0
        self.bound_true = 0
        self.bound_false = 0
        self.generated_children = 0
        self.start_time = 0.0

    @lru_cache(maxsize=None)
    def metric(self, mask: int) -> int:
        if self.metric_name == "degree":
            deg = [0] * self.n
            for e, (i, j) in enumerate(self.edges):
                if mask >> e & 1:
                    deg[i] += 1
                    deg[j] += 1
            return max(deg, default=0)

        # Every one-vertex set is a clique.  n <= 7 in the reported runs, so
        # direct subset enumeration is both transparent and fast enough.
        for size in range(self.n, 1, -1):
            for vertices in itertools.combinations(range(self.n), size):
                if all(
                    mask >> self.edge_index[i][j] & 1
                    for i, j in itertools.combinations(vertices, 2)
                ):
                    return size
        return 1 if self.n else 0

    def _refined_cells(self, red: int, blue: int) -> list[tuple[int, ...]]:
        """Return isomorphism-invariant vertex cells for a 3-edge-coloured K_n."""
        colours = (0,) * self.n
        while True:
            k = max(colours, default=-1) + 1
            signatures = []
            for v in range(self.n):
                counts = [[0, 0, 0] for _ in range(k)]
                for w in range(self.n):
                    if v == w:
                        continue
                    e = self.edge_index[v][w]
                    edge_colour = 0 if red >> e & 1 else 1 if blue >> e & 1 else 2
                    counts[colours[w]][edge_colour] += 1
                signatures.append(
                    (colours[v], tuple(tuple(row) for row in counts))
                )
            ranks = {sig: i for i, sig in enumerate(sorted(set(signatures)))}
            new_colours = tuple(ranks[sig] for sig in signatures)
            if new_colours == colours:
                break
            colours = new_colours
        return [
            tuple(v for v, colour in enumerate(colours) if colour == c)
            for c in range(max(colours, default=-1) + 1)
        ]

    @lru_cache(maxsize=None)
    def canonical(self, red: int, blue: int) -> tuple[int, int]:
        if not self.symmetry:
            return red, blue
        cells = self._refined_cells(red, blue)
        best_code = None
        best_pair = None
        cell_orders = [tuple(itertools.permutations(cell)) for cell in cells]
        for pieces in itertools.product(*cell_orders):
            # order[new_vertex] = old_vertex
            order = tuple(v for piece in pieces for v in piece)
            new_red = 0
            new_blue = 0
            for new_e, (i, j) in enumerate(self.edges):
                old_e = self.edge_index[order[i]][order[j]]
                if red >> old_e & 1:
                    new_red |= 1 << new_e
                elif blue >> old_e & 1:
                    new_blue |= 1 << new_e
            code = new_red | (new_blue << self.m)
            if best_code is None or code < best_code:
                best_code = code
                best_pair = (new_red, new_blue)
        assert best_pair is not None
        return best_pair

    def _player_and_batch(self, coloured: int) -> tuple[str, int]:
        phase = coloured % (self.p + self.q)
        if phase == 0:
            return "Alice", min(self.p, self.m - coloured)
        if phase == self.p:
            return "Bob", min(self.q, self.m - coloured)
        raise AssertionError("recursion entered in the middle of a batch")

    def _terminal_bob_win(self, red: int, blue: int) -> bool:
        a = self.metric(red)
        b = self.metric(blue)
        return b > a if self.q > self.p else b >= a

    def _bounds(self, red: int, blue: int) -> bool | None:
        """Monotone exact early decisions; None means that search is needed."""
        uncoloured = self.full ^ (red | blue)
        a_now = self.metric(red)
        b_now = self.metric(blue)
        a_ceiling = self.metric(red | uncoloured)
        b_ceiling = self.metric(blue | uncoloured)
        if self.q > self.p:
            if b_now > a_ceiling:
                self.bound_true += 1
                return True
            if b_ceiling <= a_now:
                self.bound_false += 1
                return False
        else:
            if b_now >= a_ceiling:
                self.bound_true += 1
                return True
            if b_ceiling < a_now:
                self.bound_false += 1
                return False
        return None

    @lru_cache(maxsize=None)
    def bob_can_force_win(self, red: int, blue: int) -> bool:
        self.calls += 1
        coloured_mask = red | blue
        coloured = coloured_mask.bit_count()
        if coloured == self.m:
            return self._terminal_bob_win(red, blue)
        bound = self._bounds(red, blue)
        if bound is not None:
            return bound

        player, batch = self._player_and_batch(coloured)
        free_bits = [
            1 << e for e in range(self.m) if not (coloured_mask >> e & 1)
        ]
        child_set = set()
        for chosen in itertools.combinations(free_bits, batch):
            move = 0
            for bit in chosen:
                move |= bit
            child = (
                self.canonical(red | move, blue)
                if player == "Alice"
                else self.canonical(red, blue | move)
            )
            child_set.add(child)
        self.generated_children += len(child_set)

        # Search likely decisive moves first; this changes speed, never logic.
        if player == "Alice":
            children = sorted(
                child_set,
                key=lambda rb: (self.metric(rb[0]), -self.metric(rb[1])),
                reverse=True,
            )
            # Alice chooses a move on which Bob cannot force a win.
            return all(self.bob_can_force_win(*child) for child in children)
        children = sorted(
            child_set,
            key=lambda rb: (self.metric(rb[1]), -self.metric(rb[0])),
            reverse=True,
        )
        # Bob chooses a move on which he can force a win.
        return any(self.bob_can_force_win(*child) for child in children)

    def solve(self) -> dict[str, object]:
        self.start_time = time.monotonic()
        result = self.bob_can_force_win(0, 0)
        elapsed = time.monotonic() - self.start_time
        return {
            "n": self.n,
            "metric": self.metric_name,
            "batches": f"{self.p}:{self.q}",
            "winner": "Bob" if result else "Alice",
            "states": self.bob_can_force_win.cache_info().currsize,
            "canonical_inputs": self.canonical.cache_info().currsize,
            "children": self.generated_children,
            "bound_true": self.bound_true,
            "bound_false": self.bound_false,
            "seconds": elapsed,
            "symmetry": self.symmetry,
        }


class TriangleAvoidanceSolver(Solver):
    """The stronger (1:2) game in which Bob forbids every red triangle."""

    def __init__(self, n: int, symmetry: bool = True) -> None:
        super().__init__(n, "clique", 1, 2, symmetry)

    def _terminal_bob_win(self, red: int, blue: int) -> bool:
        del blue
        return self.metric(red) < 3

    def _bounds(self, red: int, blue: int) -> bool | None:
        if self.metric(red) >= 3:
            self.bound_false += 1
            return False
        uncoloured = self.full ^ (red | blue)
        if self.metric(red | uncoloured) < 3:
            self.bound_true += 1
            return True
        return None


def format_result(result: dict[str, object]) -> str:
    return (
        f"{result['metric']:6s} {result['batches']:3s} n={result['n']}: "
        f"{result['winner']:5s}  states={result['states']} "
        f"children={result['children']} bounds=({result['bound_true']},"
        f"{result['bound_false']}) time={result['seconds']:.3f}s "
        f"symmetry={result['symmetry']}"
    )


def verify_elementary_n4_n5() -> dict[str, int]:
    """
    Exhaustively check the two short human strategies stated in the report.

    n=4: after Alice's first edge, Bob takes its unique disjoint edge and an
    arbitrary second edge.

    n=5: after each of Alice's first three moves, Bob first takes every free
    edge which would complete a red triangle, then fills his quota with the
    lexicographically first free edges.
    """
    n4 = Solver(4, "clique", 1, 2, symmetry=False)
    n4_leaves = 0
    for first_a in range(n4.m):
        u, v = n4.edges[first_a]
        opposite = next(
            e for e, edge in enumerate(n4.edges) if not ({u, v} & set(edge))
        )
        for filler in range(n4.m):
            if filler in {first_a, opposite}:
                continue
            red = 1 << first_a
            blue = (1 << opposite) | (1 << filler)
            for second_a in range(n4.m):
                if (red | blue) >> second_a & 1:
                    continue
                final_red = red | (1 << second_a)
                final_blue = n4.full ^ final_red
                assert n4.metric(final_blue) == 3
                assert n4.metric(final_red) == 2
                n4_leaves += 1

    n5 = Solver(5, "clique", 1, 2, symmetry=False)
    n5_leaves = 0
    max_threats = 0

    def threats(red: int, blue: int) -> list[int]:
        answer = []
        for e, (u, v) in enumerate(n5.edges):
            if (red | blue) >> e & 1:
                continue
            if any(
                w not in {u, v}
                and red >> n5.edge_index[u][w] & 1
                and red >> n5.edge_index[v][w] & 1
                for w in range(5)
            ):
                answer.append(e)
        return answer

    def play_n5(red: int, blue: int) -> None:
        nonlocal n5_leaves, max_threats
        if (red | blue) == n5.full:
            assert n5.metric(red) == 2       # no red triangle
            assert n5.metric(blue) >= 3      # alpha(red) >= 3
            n5_leaves += 1
            return
        for alice_edge in range(n5.m):
            if (red | blue) >> alice_edge & 1:
                continue
            next_red = red | (1 << alice_edge)
            if (next_red | blue) == n5.full:
                play_n5(next_red, blue)
                continue
            forced = threats(next_red, blue)
            max_threats = max(max_threats, len(forced))
            assert len(forced) <= 2
            next_blue = blue
            for e in forced:
                next_blue |= 1 << e
            for e in range(n5.m):
                if (next_blue.bit_count() - blue.bit_count()) == 2:
                    break
                if not (next_red | next_blue) >> e & 1:
                    next_blue |= 1 << e
            play_n5(next_red, next_blue)

    play_n5(0, 0)
    return {
        "n4_terminal_branches": n4_leaves,
        "n5_terminal_branches": n5_leaves,
        "n5_max_live_threats": max_threats,
    }


def enumerate_biased_targets(n: int) -> dict[str, int]:
    """
    Count possible final red graphs in Clique_(1,2)(n).

    Alice receives ceil(|E(K_n)|/3) edges.  Since blue is the complement,
    a terminal red graph is winning for Alice exactly when omega(red) is at
    least omega(blue), equivalently omega(red) >= alpha(red).
    """
    solver = Solver(n, "clique", 1, 2, symmetry=True)
    red_edges = (solver.m + 2) // 3
    labelled_winning = 0
    unlabelled_winning = set()
    for chosen in itertools.combinations(range(solver.m), red_edges):
        red = sum(1 << e for e in chosen)
        blue = solver.full ^ red
        if solver.metric(red) >= solver.metric(blue):
            labelled_winning += 1
            unlabelled_winning.add(solver.canonical(red, blue))
    return {
        "n": n,
        "red_edges": red_edges,
        "labelled_total": sum(
            1 for _ in itertools.combinations(range(solver.m), red_edges)
        ),
        "labelled_alice_targets": labelled_winning,
        "unlabelled_alice_targets": len(unlabelled_winning),
    }


def minimal_target_potential(n: int) -> tuple[dict[int, int], Fraction]:
    """Enumerate attainable inclusion-minimal sets with omega(G) >= alpha(G)."""
    solver = Solver(n, "clique", 1, 2, symmetry=False)
    red_edge_limit = (solver.m + 2) // 3
    counts: collections.Counter[int] = collections.Counter()

    def alice_target(mask: int) -> bool:
        return solver.metric(mask) >= solver.metric(solver.full ^ mask)

    for size in range(red_edge_limit + 1):
        for chosen in itertools.combinations(range(solver.m), size):
            mask = sum(1 << e for e in chosen)
            if alice_target(mask) and all(
                not alice_target(mask ^ (1 << e)) for e in chosen
            ):
                counts[size] += 1
    potential = sum(
        (Fraction(count, 3**size) for size, count in counts.items()),
        start=Fraction(),
    )
    return dict(sorted(counts.items())), potential


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min-n",
        type=int,
        default=3,
        help="smallest n for the biased-clique table (default: 3)",
    )
    parser.add_argument(
        "--max-n",
        type=int,
        default=7,
        help="largest n for the biased-clique table (default: 7)",
    )
    parser.add_argument(
        "--all-three",
        action="store_true",
        help="also recompute the two unbiased games through min(max-n, 6)",
    )
    parser.add_argument(
        "--cross-check",
        action="store_true",
        help="repeat n <= 6 without symmetry and assert identical winners",
    )
    parser.add_argument(
        "--deep-cross-check",
        action="store_true",
        help="repeat n=7 without symmetry (~2.2 CPU-min, ~3.5 GB RAM here)",
    )
    parser.add_argument(
        "--targets",
        action="store_true",
        help="enumerate terminal Alice-winning red graphs up to max-n",
    )
    parser.add_argument(
        "--triangle-avoidance",
        action="store_true",
        help="check the stronger claim that Bob keeps red triangle-free",
    )
    parser.add_argument(
        "--potential",
        action="store_true",
        help="enumerate the attainable minimal targets and Beck potential",
    )
    args = parser.parse_args()

    results = []
    for n in range(args.min_n, args.max_n + 1):
        solver = Solver(n, "clique", 1, 2, symmetry=True)
        result = solver.solve()
        results.append(result)
        print(format_result(result), flush=True)

    if args.all_three:
        for metric in ("clique", "degree"):
            for n in range(max(3, args.min_n), min(args.max_n, 6) + 1):
                result = Solver(n, metric, 1, 1, symmetry=True).solve()
                results.append(result)
                print(format_result(result), flush=True)

    if args.cross_check:
        for expected in list(results):
            if expected["n"] > 6:
                continue
            p, q = map(int, str(expected["batches"]).split(":"))
            check = Solver(
                int(expected["n"]),
                str(expected["metric"]),
                p,
                q,
                symmetry=False,
            ).solve()
            print("cross  " + format_result(check), flush=True)
            assert check["winner"] == expected["winner"], (check, expected)

    if args.deep_cross_check and args.min_n <= 7 <= args.max_n:
        expected = next(
            result
            for result in results
            if result["n"] == 7
            and result["metric"] == "clique"
            and result["batches"] == "1:2"
        )
        check = Solver(7, "clique", 1, 2, symmetry=False).solve()
        print("deep   " + format_result(check), flush=True)
        assert check["winner"] == expected["winner"], (check, expected)

    if args.targets:
        expected_targets = {
            3: (1, 3, 3, 1),
            4: (2, 15, 3, 1),
            5: (4, 210, 70, 2),
            6: (5, 3003, 600, 3),
            7: (7, 116280, 13335, 12),
        }
        for n in range(args.min_n, args.max_n + 1):
            counts = enumerate_biased_targets(n)
            if n in expected_targets:
                observed = (
                    counts["red_edges"],
                    counts["labelled_total"],
                    counts["labelled_alice_targets"],
                    counts["unlabelled_alice_targets"],
                )
                assert observed == expected_targets[n], (observed, n)
            print(
                "targets "
                + " ".join(f"{key}={value}" for key, value in counts.items()),
                flush=True,
            )

    elementary = verify_elementary_n4_n5()
    print(
        "elementary "
        + " ".join(f"{key}={value}" for key, value in elementary.items()),
        flush=True,
    )

    if args.triangle_avoidance:
        for n in range(max(4, args.min_n), min(7, args.max_n) + 1):
            result = TriangleAvoidanceSolver(n, symmetry=True).solve()
            print("triangle " + format_result(result), flush=True)
            assert result["winner"] == "Bob"

    if args.potential:
        expected_potentials = {
            4: ({2: 3}, Fraction(1, 3)),
            5: ({3: 10}, Fraction(10, 27)),
            6: ({4: 60}, Fraction(20, 27)),
            7: ({5: 105, 6: 105}, Fraction(140, 243)),
        }
        for n in range(max(4, args.min_n), args.max_n + 1):
            counts, potential = minimal_target_potential(n)
            if n in expected_potentials:
                assert (counts, potential) == expected_potentials[n]
            print(
                f"potential n={n} counts={counts} "
                f"sum={potential.numerator}/{potential.denominator} "
                f"decimal={float(potential):.12f}",
                flush=True,
            )

    expected_biased = {
        3: "Alice",
        4: "Bob",
        5: "Bob",
        6: "Bob",
        7: "Bob",
    }
    for result in results:
        if result["metric"] == "clique" and result["batches"] == "1:2":
            n = int(result["n"])
            if n in expected_biased:
                assert result["winner"] == expected_biased[n]
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
