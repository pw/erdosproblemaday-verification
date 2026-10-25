#!/usr/bin/env python3
"""Independent hostile audit of the frozen Erdos problem 1106 certificate.

The audited bundle uses a Python generalized-pentagonal recurrence.  This
audit instead asks PARI/GP's built-in numbpart() for every partition value.
It also recomputes the base window a second way, by coefficient dynamic
programming plus SymPy factorint, and requires the two base results to agree.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile

from sympy import factorint, isprime


BUNDLE = Path("/home/exedev/erdos_scratch/erdos1106_frontier_10100_20260811")
BUNDLE_MANIFEST_SHA256 = (
    "9986a3ddf33382f5250c5e54c1916eac7f329301ba6cfd5f958aea6e03ede2a8"
)
WITNESS_PAIR_SHA256 = (
    "8be6ca45b91f080164c979e8b60654c01820a24276a0f4ec683e340483683f93"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_integer_table(path: Path, first: int, last: int) -> dict[int, int]:
    rows: dict[int, int] = {}
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        fields = raw.split()
        if len(fields) != 2:
            raise AssertionError((path, line_number, "expected two fields"))
        n, value = map(int, fields)
        if n in rows:
            raise AssertionError((path, line_number, "duplicate index", n))
        rows[n] = value
    expected = list(range(first, last + 1))
    if sorted(rows) != expected:
        raise AssertionError((path, "noncontiguous or wrong index range"))
    return rows


def coefficient_dp_partitions(limit: int) -> list[int]:
    """Coefficient DP for product_{k>=1} 1/(1-x^k), not Euler recurrence."""
    values = [0] * (limit + 1)
    values[0] = 1
    for part in range(1, limit + 1):
        for total in range(part, limit + 1):
            values[total] += values[total - part]
    return values


def parse_gp_vector(output: str, prefix: str) -> list[int]:
    rows = [line for line in output.splitlines() if line.startswith(prefix)]
    if len(rows) != 1:
        raise AssertionError((prefix, len(rows)))
    value = ast.literal_eval(rows[0][len(prefix):])
    if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
        raise AssertionError((prefix, "not an integer vector"))
    return value


def independent_base_crosscheck(gp_output: str) -> None:
    parts = coefficient_dp_partitions(116)
    primes_115: set[int] = set()
    primes_116: set[int] = set()
    for n in range(1, 117):
        factors = factorint(parts[n])
        recomposed = 1
        for prime, exponent in factors.items():
            assert isprime(prime), (n, prime)
            recomposed *= prime**exponent
            primes_116.add(prime)
            if n <= 115:
                primes_115.add(prime)
        assert recomposed == parts[n], n

    gp_parts = parse_gp_vector(gp_output, "GP_PARTITIONS_1_116 ")
    gp_primes_115 = parse_gp_vector(gp_output, "GP_BASE115_PRIMES ")
    gp_primes_116 = parse_gp_vector(gp_output, "GP_BASE116_PRIMES ")
    assert gp_parts == parts[1:]
    assert gp_primes_115 == sorted(primes_115)
    assert gp_primes_116 == sorted(primes_116)
    assert len(primes_115) == 115
    assert len(primes_116) == 117
    assert sorted(primes_116 - primes_115) == [157, 7823]
    print("SECOND_BASE_ENGINE coefficient-DP + SymPy factorint/isprime")
    print("SECOND_BASE_CHECK exact F(115)=115 and exact F(116)=117")
    print("SECOND_BASE_NEW_AT_116 [157, 7823]")


def main() -> None:
    assert sha256(BUNDLE / "SHA256SUMS") == BUNDLE_MANIFEST_SHA256
    manifest = subprocess.run(
        ["sha256sum", "-c", "SHA256SUMS"],
        cwd=BUNDLE,
        text=True,
        capture_output=True,
        check=True,
    )
    assert not manifest.stderr
    assert manifest.stdout.count(": OK\n") == 23
    print("AUTHOR_MANIFEST_OK 23 files")
    print(f"AUTHOR_MANIFEST_SHA256 {BUNDLE_MANIFEST_SHA256}")

    counts = read_integer_table(BUNDLE / "b194259_20260811.txt", 1, 10_000)
    published = read_integer_table(BUNDLE / "b194261_20260811.txt", 1, 10_000)
    extension = read_integer_table(
        BUNDLE / "extension_witnesses_10001_10100.tsv", 10_001, 10_100
    )
    assert counts[115] == 115
    assert counts[116] == 117
    assert counts[10_000] == 28_312

    pairs = [
        (n, published[n] if n <= 10_000 else extension[n])
        for n in range(117, 10_101)
    ]
    pair_digest = hashlib.sha256()
    for n, prime in pairs:
        pair_digest.update(f"{n}:{prime}\n".encode())
    assert pair_digest.hexdigest() == WITNESS_PAIR_SHA256
    assert len(pairs) == 9_984

    gp_rows = ",\n".join(f"[{n},{prime}]" for n, prime in pairs)
    gp_program = f"""{{
witnesses=[{gp_rows}];
base115=Map();
base116=Map();
baseparts=vector(116);
for(n=1,116,
  pn=numbpart(n);
  baseparts[n]=pn;
  ff=factor(pn);
  recomposed=1;
  for(i=1,matsize(ff)[1],
    q=ff[i,1]; e=ff[i,2];
    if(!isprime(q),error(Str("unproved base factor at n=",n,", q=",q)));
    recomposed *= q^e;
    mapput(base116,q,1);
    if(n<=115,mapput(base115,q,1));
  );
  if(recomposed!=pn,error(Str("base recomposition failed at n=",n)));
  print("BASE_FACTORIZATION ",n," ",pn," ",ff);
);
if(#base115!=115,error(Str("wrong F(115): ",#base115)));
if(#base116!=117,error(Str("wrong F(116): ",#base116)));
print("GP_PARTITIONS_1_116 ",baseparts);
print("GP_BASE115_PRIMES ",Vec(base115));
print("GP_BASE116_PRIMES ",Vec(base116));
print("GP_BASE_NEW_AT_116 ",setminus(Vec(base116),Vec(base115)));
used=Map();
basevec=Vec(base116);
for(i=1,#basevec,mapput(used,basevec[i],1));
for(i=1,#witnesses,
  n=witnesses[i][1]; q=witnesses[i][2];
  if(n!=116+i,error(Str("witness index failure at row ",i)));
  if(q<=1,error(Str("nonpositive witness at n=",n)));
  if(mapisdefined(used,q),error(Str("nonfresh witness at n=",n,", q=",q)));
  pn=numbpart(n);
  if(pn%q,error(Str("nondivisor witness at n=",n,", q=",q)));
  if(!isprime(q),error(Str("composite witness at n=",n,", q=",q)));
  mapput(used,q,n);
  if(#used!=n+1,error(Str("wrong running lower bound at n=",n)));
  if(n==117||n==1000||n==5000||n==10000||n==10001||n==10100,
    print("WITNESS_CHECKPOINT n=",n," q=",q," used=",#used)
  );
);
print("GP_BASE_CHECK exact F(115)=115 and exact F(116)=117");
print("GP_WITNESS_PRIMALITY_CHECKS ",#witnesses);
print("GP_WITNESS_DIVISIBILITY_CHECKS ",#witnesses);
print("GP_WITNESS_FRESHNESS_CHECKS ",#witnesses);
print("GP_FINAL_EXHIBITED_PRIMES ",#used);
print("GP_LOWER_BOUND every n in [116,10100] has F(n)>=n+1");
print("GP_AUDIT_PASS");
}}
"""

    with tempfile.TemporaryDirectory(prefix="audit-erdos1106-") as temp_dir:
        program_path = Path(temp_dir) / "audit.gp"
        program_path.write_text(gp_program)
        completed = subprocess.run(
            ["gp", "-q", "-f", str(program_path)],
            text=True,
            capture_output=True,
            check=True,
        )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    assert "GP_AUDIT_PASS" in completed.stdout
    independent_base_crosscheck(completed.stdout)
    print(f"WITNESS_PAIR_SHA256 {pair_digest.hexdigest()}")
    print(completed.stdout, end="")
    print("INDEPENDENT_AUDIT_PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"INDEPENDENT_AUDIT_FAIL: {exc!r}", file=sys.stderr)
        raise
