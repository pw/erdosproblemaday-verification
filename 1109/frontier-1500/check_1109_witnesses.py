#!/usr/bin/env python3
"""Cold direct checker for the five new Problem 1109 lower certificates."""

from hashlib import sha256

WITNESSES = {
    1255: (
        31, 35, 51, 123, 139, 143, 159, 231, 247, 251, 267, 323, 335,
        339, 359, 371, 443, 463, 467, 535, 555, 623, 647, 659, 663,
        731, 751, 771, 843, 859, 863, 947, 967, 971, 1039, 1055,
        1163, 1167, 1235, 1255,
    ),
    1277: (
        5, 41, 53, 65, 77, 105, 141, 161, 213, 221, 249, 281, 293,
        305, 321, 341, 353, 377, 461, 521, 593, 641, 653, 665, 677,
        713, 761, 861, 881, 893, 941, 965, 1077, 1121, 1181, 1193,
        1217, 1241, 1253, 1265, 1277,
    ),
    1293: (
        5, 41, 53, 65, 77, 105, 141, 161, 213, 221, 249, 281, 293,
        305, 321, 341, 353, 377, 461, 521, 593, 641, 653, 665, 677,
        713, 761, 861, 881, 893, 941, 965, 1077, 1121, 1181, 1193,
        1217, 1241, 1253, 1265, 1277, 1293,
    ),
    1335: (
        23, 35, 71, 83, 95, 107, 119, 183, 191, 251, 263, 291, 311,
        323, 335, 551, 611, 623, 635, 647, 671, 683, 695, 707, 719,
        791, 851, 863, 911, 923, 1151, 1163, 1211, 1223, 1235, 1247,
        1263, 1271, 1283, 1295, 1307, 1319, 1335,
    ),
    1407: (
        23, 35, 71, 83, 95, 107, 119, 183, 191, 251, 263, 291, 311,
        323, 335, 551, 611, 623, 635, 647, 671, 683, 695, 707, 719,
        791, 851, 863, 911, 923, 1151, 1163, 1211, 1223, 1235, 1247,
        1263, 1271, 1283, 1295, 1307, 1319, 1335, 1407,
    ),
}


def is_squarefree_trial(value):
    divisor = 2
    while divisor * divisor <= value:
        if value % (divisor * divisor) == 0:
            return False
        divisor += 1
    return value > 0


def main():
    records = []
    for expected_size, (maximum, witness) in enumerate(WITNESSES.items(), start=40):
        assert tuple(sorted(witness)) == witness
        assert len(witness) == len(set(witness)) == expected_size
        assert witness[-1] == maximum
        checked_sums = 0
        for left_index, left in enumerate(witness):
            for right in witness[left_index:]:
                assert is_squarefree_trial(left + right), (maximum, left, right)
                checked_sums += 1
        text = ",".join(map(str, witness))
        records.append(f"{expected_size}:{maximum}:{text}\n")
        print(
            f"N={maximum} size={expected_size} checked_sums={checked_sums} "
            "all_squarefree=YES"
        )
    print("witness_sha256=" + sha256("".join(records).encode("ascii")).hexdigest())
    print("CONCLUSION all five new lower certificates pass direct trial division")


if __name__ == "__main__":
    main()
