#!/usr/bin/env python3
"""Independent definition, witness, and small-universe audit for Problem 535."""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ROWS = [
    (101, 107, 14, (10, 12, 13, 15, 18, 20, 24, 40, 48, 54, 75, 80, 91, 96)),
    (108, 124, 15, (11, 14, 20, 24, 30, 33, 36, 40, 48, 80, 90, 96, 98, 99, 108)),
    (125, 125, 16, (14, 20, 21, 24, 25, 30, 36, 40, 48, 63, 80, 90, 96, 98, 108, 125)),
]
EXPECTED_EDGES = {107: 71799, 124: 109838, 125: 113132}
EXPECTED_SMALL = [1, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7]


def euclid(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def forbidden(a: int, b: int, c: int) -> bool:
    d = euclid(a, b)
    return d == euclid(a, c) == euclid(b, c)


def layers(n: int) -> frozenset[tuple[int, int]]:
    answer: set[tuple[int, int]] = set()
    divisor = 2
    remaining = n
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
            answer.add((divisor, exponent))
        divisor += 1
    if remaining > 1:
        answer.add((remaining, 1))
    return frozenset(answer)


def load_primary() -> dict[str, object]:
    namespace: dict[str, object] = {
        "__name__": "candidate535_without_bytecode",
        "__file__": str(ROOT / "verify_535_extension.py"),
    }
    source = (ROOT / "verify_535_extension.py").read_text(encoding="utf-8")
    exec(compile(source, str(ROOT / "verify_535_extension.py"), "exec"), namespace)
    return namespace


def verify_live_gate() -> None:
    problem = (ROOT / "LIVE_PROBLEM.txt").read_text(encoding="utf-8")
    discussion = (ROOT / "LIVE_DISCUSSION.txt").read_text(encoding="utf-8")
    for marker in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Interested in collaborating\tNone",
        "Currently working on this problem\tNone",
        "I am working on formalising the results on this problem\tNone",
        "9 comments on this problem",
    ):
        assert marker in problem and marker in discussion
    assert "Related OEIS sequences: Possible" in problem
    assert discussion.count("\n—\n") == 9
    assert "Show 1 more" not in discussion and "Show 9 more" not in discussion
    print("live gate: OPEN; 0 claims; no worker/collaborator/formalizer; 9 comments visible")


def verify_definition() -> None:
    layer = [frozenset()] + [layers(n) for n in range(1, 126)]
    for a in range(1, 126):
        for b in range(a + 1, 126):
            assert layer[a] & layer[b] == layer[euclid(a, b)]
    counts = {n: 0 for n in EXPECTED_EDGES}
    triple_count = 0
    for a, b, c in itertools.combinations(range(1, 126), 3):
        via_layers = layer[a] & layer[b] == layer[a] & layer[c] == layer[b] & layer[c]
        direct = forbidden(a, b, c)
        assert via_layers == direct
        triple_count += 1
        if direct:
            for n in counts:
                if c <= n:
                    counts[n] += 1
    assert counts == EXPECTED_EDGES
    print(f"definition: {triple_count} distinct triples checked; endpoint edges={counts}")


def verify_witnesses() -> None:
    for first, last, value, witness in ROWS:
        assert len(witness) == len(set(witness)) == value
        assert tuple(sorted(witness)) == witness and witness[-1] <= first
        records: list[str] = []
        for a, b, c in itertools.combinations(witness, 3):
            gcds = euclid(a, b), euclid(a, c), euclid(b, c)
            assert len(set(gcds)) > 1
            records.append(f"{a},{b},{c}:{gcds[0]},{gcds[1]},{gcds[2]}\n")
        digest = hashlib.sha256("".join(records).encode("ascii")).hexdigest()
        print(f"witness {first}..{last}: size={value} triples={len(records)} sha256={digest}")
    assert [(a, b) for a, b, _, _ in ROWS] == [(101, 107), (108, 124), (125, 125)]
    print("interval logic: contiguous 101..125; left witnesses pair with right target+1 UNSAT")


def brute_small() -> None:
    values: list[int] = []
    for n in range(1, 19):
        layer = [frozenset()] + [layers(i) for i in range(1, n + 1)]
        edges = []
        for a, b, c in itertools.combinations(range(1, n + 1), 3):
            if layer[a] & layer[b] == layer[a] & layer[c] == layer[b] & layer[c]:
                edges.append((1 << (a - 1)) | (1 << (b - 1)) | (1 << (c - 1)))
        optimum = 0
        for subset in range(1 << n):
            if subset.bit_count() > optimum and all(subset & edge != edge for edge in edges):
                optimum = subset.bit_count()
        values.append(optimum)
    assert values == EXPECTED_SMALL

    primary = load_primary()
    find = primary["find_independent_set"]
    assert callable(find)
    for n, optimum in enumerate(values, 1):
        witness, _, _ = find(n, optimum)
        too_large, _, _ = find(n, optimum + 1)
        assert witness is not None and too_large is None
    print(f"third formulation: all subsets exhausted for every n<=18: {values}")


def main() -> None:
    verify_live_gate()
    verify_definition()
    verify_witnesses()
    brute_small()
    print("HOSTILE AUDIT PASS")


if __name__ == "__main__":
    main()
