#!/usr/bin/env python3
"""Small-n controls for the hostile audit of the Problem 196 bundle."""

from collections import Counter, defaultdict
from itertools import permutations
from math import factorial


EXPECTED = [1, 2, 6, 22, 102, 564, 3336, 22266, 168864]


def oriented_words(n):
    words = []
    for step in range(1, n):
        for start in range(n - 3 * step):
            forward = tuple(start + j * step for j in range(4))
            words.extend((forward, forward[::-1]))
    return tuple(words)


def contains_word(word, pattern):
    cursor = iter(word)
    return all(any(value == target for value in cursor) for target in pattern)


def avoids(word, patterns):
    return not any(contains_word(word, pattern) for pattern in patterns)


def endpoint_allows(prefix, value, n):
    position = {entry: index for index, entry in enumerate(prefix)}
    for step in range(1, n):
        lower = (value - 3 * step, value - 2 * step, value - step)
        if lower[0] >= 0 and all(entry in position for entry in lower):
            if position[lower[0]] < position[lower[1]] < position[lower[2]]:
                return False
        upper = (value + 3 * step, value + 2 * step, value + step)
        if upper[0] < n and all(entry in position for entry in upper):
            if position[upper[0]] < position[upper[1]] < position[upper[2]]:
                return False
    return True


def prefix_transition_control(n):
    patterns = oriented_words(n)
    level = {()}
    visited = 1
    for depth in range(n):
        next_level = set()
        for prefix in level:
            remaining = set(range(n)) - set(prefix)
            for value in remaining:
                candidate = prefix + (value,)
                by_words = avoids(candidate, patterns)
                by_endpoint = endpoint_allows(prefix, value, n)
                assert by_words == by_endpoint, (n, prefix, value)
                if by_words:
                    next_level.add(candidate)
        assert len(next_level) == sum(
            endpoint_allows(prefix, value, n)
            for prefix in level
            for value in set(range(n)) - set(prefix)
        )
        level = next_level
        visited += len(level)
    assert len(level) == EXPECTED[n - 1]
    return visited


def main():
    for n, expected in enumerate(EXPECTED, start=1):
        patterns = oriented_words(n)
        ap_count = len(patterns) // 2
        assert ap_count == sum(n - 3 * step for step in range(1, (n - 1) // 3 + 1))

        avoiders = []
        incidence = 0
        first_counts = Counter()
        fixed_reverse_complement = 0
        prefix_subtrees = defaultdict(int)
        for word in permutations(range(n)):
            occurrences = sum(contains_word(word, pattern) for pattern in patterns)
            incidence += occurrences
            if occurrences:
                continue
            avoiders.append(word)
            first_counts[word[0]] += 1
            if n >= 2:
                prefix_subtrees[word[:2]] += 1
            complement = tuple(n - 1 - value for value in word)
            reverse_complement = complement[::-1]
            assert avoids(complement, patterns)
            assert avoids(word[::-1], patterns)
            fixed_reverse_complement += word == reverse_complement

        assert len(avoiders) == expected
        assert incidence == factorial(n) * ap_count // 12 if n >= 4 else incidence == 0
        assert all(first_counts[value] == first_counts[n - 1 - value] for value in range(n))

        if n >= 2:
            canonical = 0
            for a in range(n):
                for b in range(n):
                    if a == b:
                        continue
                    pair = (a, b)
                    complement_pair = (n - 1 - a, n - 1 - b)
                    assert pair != complement_pair
                    assert prefix_subtrees[pair] == prefix_subtrees[complement_pair]
                    canonical += pair < complement_pair
            assert canonical * 2 == n * (n - 1)

        print(
            f"n={n} theta4={len(avoiders)} oriented_words={len(patterns)} "
            f"incidence={incidence} rc_fixed={fixed_reverse_complement} "
            f"first_counts={','.join(str(first_counts[x]) for x in range(n))}"
        )

    for n in range(1, 9):
        print(f"prefix_transition_n={n} visited_avoiding_prefixes={prefix_transition_control(n)}")

    # Both value orientations are load-bearing: deleting the descending word
    # accepts the reverse identity at n=4 and changes 22 to 23.
    ascending_only = ((0, 1, 2, 3),)
    ascending_only_count = sum(avoids(word, ascending_only) for word in permutations(range(4)))
    assert ascending_only_count == 23
    print("negative_control_ascending_only_n4=23 expected_full=22")
    print("all_exhaustive_controls_passed=1")


if __name__ == "__main__":
    main()
