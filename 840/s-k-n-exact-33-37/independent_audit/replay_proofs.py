#!/usr/bin/env python3
"""Independently decompress and replay every frozen #840 DRAT proof."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
from pathlib import Path
import shutil
import subprocess
import tempfile


BUNDLE = Path("/tmp/erdos840_n33_37_bundle")
CHECKER = Path("/home/exedev/MathDyad/erdos813/tools/drat-trim/drat-trim")
OUT = Path("/tmp/erdos840_n37_hostile_audit")


def replay(compressed: Path):
    cnf = compressed.with_suffix("").with_suffix(".cnf")
    with tempfile.TemporaryDirectory(prefix="hostile-840-proof-") as raw:
        proof = Path(raw) / "proof.drat"
        with gzip.open(compressed, "rb") as source, proof.open("wb") as target:
            shutil.copyfileobj(source, target)
        completed = subprocess.run(
            ["nice", "-n", "10", str(CHECKER), str(cnf), str(proof)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    log = OUT / f"fresh_replay_{compressed.name.removesuffix('.drat.gz')}.log"
    log.write_text(completed.stdout)
    assert completed.returncode == 0 and "s VERIFIED" in completed.stdout, compressed
    return compressed.name, len(completed.stdout)


def main():
    proofs = sorted(BUNDLE.glob("sat*/*.drat.gz"))
    assert len(proofs) == 7
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending = {pool.submit(replay, proof): proof for proof in proofs}
        for future in as_completed(pending):
            name, log_bytes = future.result()
            print(f"{name}: VERIFIED ({log_bytes} log characters)", flush=True)
    print("ALL SEVEN FRESH HOSTILE DRAT REPLAYS PASS", flush=True)


if __name__ == "__main__":
    main()
