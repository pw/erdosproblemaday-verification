#!/usr/bin/env python3
"""Exact witness audit for the finite frontier in Erdős problem 1106.

The proof uses one distinct prime divisor of p(n) for every n >= 117,
starting from the complete set of 117 prime divisors already present by n=116.
Large-prime certification is delegated to PARI/GP's rigorous isprime().
"""

from __future__ import annotations

import hashlib
from math import isqrt
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
OEIS_COUNT_FILE = HERE / "b194259_20260811.txt"
OEIS_WITNESS_FILE = HERE / "b194261_20260811.txt"
EXTENSION_FILE = HERE / "extension_witnesses_10001_10100.tsv"

EXPECTED_HASHES = {
    "b194259_20260811.txt":
        "a537dffd46e3ddd9833aad020d0191051abce09ba54096762847e5f7da2fef7c",
    "b194261_20260811.txt":
        "49329f215c96186f4239f68afcf6012aae8a6aca734f27251caedd06bb99df32",
    "extension_witnesses_10001_10100.tsv":
        "c1dc445efc3b6d00857c9fe564d7bf319c637ec6cace94ff966cf38a6a53d0e2",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_table(path: Path) -> dict[int, int]:
    rows: dict[int, int] = {}
    for line in path.read_text().splitlines():
        n, value = map(int, line.split())
        assert n not in rows
        rows[n] = value
    assert sorted(rows) == list(range(min(rows), max(rows) + 1))
    return rows


def partitions(limit: int) -> list[int]:
    """Euler's generalized-pentagonal recurrence, exactly over integers."""
    values = [0] * (limit + 1)
    values[0] = 1
    for n in range(1, limit + 1):
        total = 0
        j = 1
        while True:
            left = j * (3 * j - 1) // 2
            if left > n:
                break
            sign = 1 if j & 1 else -1
            total += sign * values[n - left]
            right = j * (3 * j + 1) // 2
            if right <= n:
                total += sign * values[n - right]
            j += 1
        assert total > 0
        values[n] = total
    return values


def trial_prime_factors(value: int) -> set[int]:
    """Complete trial-division factorization for the small base window."""
    factors: set[int] = set()
    remaining = value
    divisor = 2
    while divisor <= isqrt(remaining):
        if remaining % divisor == 0:
            factors.add(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.add(remaining)
    return factors


def prove_primes_with_pari(values: list[int]) -> str:
    gp = shutil.which("gp")
    assert gp is not None, "PARI/GP is required for rigorous primality proofs"
    with tempfile.TemporaryDirectory(prefix="erdos1106-primes-") as temp_dir:
        vector_file = Path(temp_dir) / "witness_primes.txt"
        vector_file.write_text("".join(f"{value}\n" for value in values))
        gp_program = f'''
v=readvec("{vector_file}");
for(i=1,#v,if(!isprime(v[i]),error(Str("composite witness at index ",i))));
print("PARI_ISPRIME_PROVED ",#v);
'''
        completed = subprocess.run(
            [gp, "-q", "-f"],
            input=gp_program,
            text=True,
            capture_output=True,
            check=True,
        )
    assert f"PARI_ISPRIME_PROVED {len(values)}" in completed.stdout
    assert not completed.stderr.strip(), completed.stderr
    version_run = subprocess.run(
        [gp, "--version"], text=True, capture_output=True, check=True
    )
    version_lines = (version_run.stdout + version_run.stderr).splitlines()
    assert version_lines
    version = version_lines[0].strip()
    return f"{completed.stdout.strip()}\n{version}"


def main() -> None:
    for filename, expected in EXPECTED_HASHES.items():
        actual = sha256(HERE / filename)
        assert actual == expected, (filename, actual)

    published_counts = read_table(OEIS_COUNT_FILE)
    published_witnesses = read_table(OEIS_WITNESS_FILE)
    extension = read_table(EXTENSION_FILE)
    assert max(published_counts) == max(published_witnesses) == 10_000
    assert sorted(extension) == list(range(10_001, 10_101))

    p = partitions(10_100)
    partition_digest = hashlib.sha256()
    for n, value in enumerate(p):
        partition_digest.update(f"{n}:{value}\n".encode())

    base_primes: set[int] = set()
    factors_through_115: set[int] = set()
    for n in range(1, 117):
        factors = trial_prime_factors(p[n])
        base_primes.update(factors)
        if n <= 115:
            factors_through_115.update(factors)

    # These two equalities are complete factorizations, not lower bounds.
    assert len(factors_through_115) == 115
    assert len(base_primes) == 117
    assert published_counts[115] == 115
    assert published_counts[116] == 117

    used = set(base_primes)
    large_prime_witnesses: list[int] = []
    witness_digest = hashlib.sha256()

    for n in range(117, 10_101):
        q = published_witnesses[n] if n <= 10_000 else extension[n]
        assert q > 1
        assert q not in used, (n, q)
        assert p[n] % q == 0, (n, q)
        used.add(q)
        large_prime_witnesses.append(q)
        witness_digest.update(f"{n}:{q}\n".encode())
        assert len(used) == n + 1

    pari_output = prove_primes_with_pari(large_prime_witnesses)

    assert len(used) == 10_101
    assert published_counts[10_000] == 28_312
    print(pari_output)
    print(f"exact F(115) = {len(factors_through_115)}")
    print(f"exact F(116) = {len(base_primes)}")
    print("certified lower bound F(n) >= n+1 for every 116 <= n <= 10100")
    print(f"distinct witness primes at n=10100: {len(used)}")
    print(f"partition-array SHA-256: {partition_digest.hexdigest()}")
    print(f"witness-pairs SHA-256: {witness_digest.hexdigest()}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
