#!/usr/bin/env python3
"""Cross-check the completed #1109 primary transcript against the PMC audit."""

from hashlib import sha256
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
PRIMARY_OUT = HERE / "primary_2000.stdout"
PRIMARY_ERR = HERE / "primary_2000.stderr"
PMC_LOG = HERE / "pmc_1501_2000_strict.log"

PUBLISHED = (
    1, 5, 19, 23, 37, 41, 59, 87, 101, 105, 113, 131, 151, 159, 167,
    195, 203, 239, 259, 303, 307, 403, 451, 499, 517, 553, 573, 609,
    645, 701, 719, 787, 807, 827, 889, 1003, 1055, 1067, 1103,
)
BASE_EXTENSION = (1255, 1277, 1293, 1335, 1407)
NEW_EXTENSION = (1509, 1535, 1595, 1707, 1735, 1779, 1835, 1919, 1991, 1999)
EXPECTED_TRANSITIONS = PUBLISHED + BASE_EXTENSION + NEW_EXTENSION


def squarefree(value: int) -> bool:
    if value < 1:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % (divisor * divisor) == 0:
            return False
        divisor += 1
    return True


def parse_primary_decisions(text: str) -> list[tuple[int, int, bool, int]]:
    decisions = []
    pattern = re.compile(r"decision n=(\d+) target=(\d+) exists=([01]) nodes=(\d+)")
    for line in text.splitlines():
        match = pattern.fullmatch(line)
        if match:
            decisions.append(
                (
                    int(match.group(1)),
                    int(match.group(2)),
                    match.group(3) == "1",
                    int(match.group(4)),
                )
            )
    return decisions


def parse_pmc_decisions(text: str) -> list[tuple[int, int, bool]]:
    decisions = []
    pattern = re.compile(
        r"n=(\d+) target=(\d+) neighbors=\d+ edges=\d+ exists=(True|False) "
        r"graph_sha256=[0-9a-f]{64} witness=\{[^}]*\}"
    )
    for line in text.splitlines():
        match = pattern.fullmatch(line)
        if match:
            decisions.append(
                (int(match.group(1)), int(match.group(2)), match.group(3) == "True")
            )
    return decisions


def parse_transitions(text: str) -> list[tuple[int, int, tuple[int, ...]]]:
    transitions = []
    pattern = re.compile(r"f=(\d+) first_N=(\d+) witness=\{([^}]*)\}")
    for line in text.splitlines():
        match = pattern.fullmatch(line)
        if not match:
            continue
        witness = tuple(int(token) for token in match.group(3).split(","))
        transitions.append((int(match.group(1)), int(match.group(2)), witness))
    return transitions


def main() -> None:
    primary_out = PRIMARY_OUT.read_text(encoding="ascii")
    primary_err = PRIMARY_ERR.read_text(encoding="ascii")
    pmc_text = PMC_LOG.read_text(encoding="ascii")

    assert "Exit status: 0" in primary_err
    assert "Command terminated by signal" not in primary_err
    assert "Assertion" not in primary_err
    assert "runtime error:" not in primary_err
    assert "CONCLUSION exact f(N) certified for 1<=N<=2000" in primary_out
    assert primary_out.startswith("Erdos Problem 1109 C++ exact frontier verifier\n")

    summary = re.search(
        r"^MAX_N=2000 eligible_vertices=(\d+) final_f=(\d+) decision_nodes=(\d+)$",
        primary_out,
        re.MULTILINE,
    )
    assert summary
    assert (int(summary.group(1)), int(summary.group(2))) == (811, 54)
    assert int(summary.group(3)) > 0

    transitions = parse_transitions(primary_out)
    assert sum(line.startswith("f=") for line in primary_out.splitlines()) == len(transitions)
    assert len(transitions) == 54
    assert [level for level, _, _ in transitions] == list(range(1, 55))
    assert tuple(first_n for _, first_n, _ in transitions) == EXPECTED_TRANSITIONS

    checked_sums = 0
    for level, first_n, witness in transitions:
        assert len(witness) == len(set(witness)) == level
        assert tuple(sorted(witness)) == witness
        assert witness[-1] == first_n
        assert all(1 <= value <= first_n for value in witness)
        for left_index, left in enumerate(witness):
            for right in witness[left_index:]:
                assert squarefree(left + right), (level, first_n, left, right)
                checked_sums += 1

    all_primary_decisions = parse_primary_decisions(primary_err)
    assert sum(
        line.startswith("decision ") for line in primary_err.splitlines()
    ) == len(all_primary_decisions)
    assert all(nodes > 0 for _, _, _, nodes in all_primary_decisions)
    primary_extension = [
        (n, target, exists)
        for n, target, exists, _ in all_primary_decisions
        if n > 1500
    ]
    pmc_extension = parse_pmc_decisions(pmc_text)
    assert len(primary_extension) == len(pmc_extension) == 201
    assert primary_extension == pmc_extension
    assert [n for n, _, exists in primary_extension if exists] == list(NEW_EXTENSION)

    out_hash = sha256(PRIMARY_OUT.read_bytes()).hexdigest()
    err_hash = sha256(PRIMARY_ERR.read_bytes()).hexdigest()
    decisions_hash = sha256(
        "".join(
            f"{n}:{target}:{int(exists)}\n"
            for n, target, exists in primary_extension
        ).encode("ascii")
    ).hexdigest()
    print(f"primary_stdout_sha256={out_hash}")
    print(f"primary_stderr_sha256={err_hash}")
    print(f"extension_decisions={len(primary_extension)} decisions_sha256={decisions_hash}")
    print(f"primary_transitions={len(transitions)} checked_witness_sums={checked_sums}")
    print("new_transitions=" + ",".join(map(str, NEW_EXTENSION)))
    print("CONCLUSION primary and PMC agree on all extension decisions; primary f(2000)=54")


if __name__ == "__main__":
    main()
