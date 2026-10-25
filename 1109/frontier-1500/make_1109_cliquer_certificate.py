#!/usr/bin/env python3
"""Normalize and validate the completed Problem 1109 Cliquer audit log."""

from hashlib import sha256
from pathlib import Path

RAW = Path("erdos1109_incremental_parallel_reverse_cliquer_2026-08-11.log")
AUDIT_SOURCE = Path("audit_1109_incremental_parallel_cliquer.py")
OUTPUT = Path("erdos1109_cliquer_certificate_2026-08-11.log")
TRANSITIONS = (1255, 1277, 1293, 1335, 1407)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def parse_record(line):
    fields = dict(field.split("=", 1) for field in line.split())
    witness = fields["witness"].strip("{}")
    return {
        "n": int(fields["n"]),
        "target": int(fields["target"]),
        "neighbors": int(fields["neighbors"]),
        "edges": int(fields["edges"]),
        "exists": fields["exists"] == "True",
        "graph_hash": fields["graph_sha256"],
        "witness": tuple(map(int, witness.split(","))) if witness else (),
    }


def main():
    raw_lines = RAW.read_text(encoding="ascii").splitlines()
    finished = [line for line in raw_lines if line.startswith("finished n=")]
    record_lines = [line for line in raw_lines if line.startswith("n=")]
    digest_lines = [line for line in raw_lines if line.startswith("audit_sha256=")]
    conclusions = [line for line in raw_lines if line.startswith("CONCLUSION ")]
    assert len(finished) == len(record_lines) == 163
    assert len(digest_lines) == len(conclusions) == 1

    records = [parse_record(line) for line in record_lines]
    assert [record["n"] for record in records] == sorted(
        record["n"] for record in records
    )
    assert len({record["n"] for record in records}) == 163
    assert tuple(record["n"] for record in records if record["exists"]) == TRANSITIONS

    digest_input = []
    for record in records:
        witness_text = ",".join(map(str, record["witness"]))
        digest_input.append(
            f"{record['n']}:{record['target']}:{int(record['exists'])}:"
            f"{record['neighbors']}:{record['edges']}:{record['graph_hash']}:"
            f"{witness_text}\n"
        )
    digest = sha256("".join(digest_input).encode("ascii")).hexdigest()
    assert digest_lines == [f"audit_sha256={digest}"]

    source_hash = file_hash(AUDIT_SOURCE)
    raw_hash = file_hash(RAW)
    output_lines = [
        "Erdos Problem 1109 normalized external-Cliquer certificate",
        "access_and_run_date=2026-08-11",
        "cliquer_version=1.21-3build1",
        "cliquer_sha256=d482f5756fff600b4ec646bedeaa9e685b859fc3810be2c7faf078b18ea51d93",
        f"audit_source_sha256={source_hash}",
        f"raw_log_sha256={raw_hash}",
        "command=python3 audit_1109_incremental_parallel_cliquer.py --jobs 6",
        "ordering=reverse",
        "eligible_decisions=163",
        "wrapper_note=the outer GNU timeout was detached after 3304 seconds; "
        "the orphaned audit and solver children continued to completion",
        "",
        *record_lines,
        f"audit_sha256={digest}",
        conclusions[0],
    ]
    OUTPUT.write_text("\n".join(output_lines) + "\n", encoding="ascii")
    print(f"records={len(records)}")
    print(f"positive_decisions={TRANSITIONS}")
    print(f"audit_sha256={digest}")
    print(f"certificate_sha256={file_hash(OUTPUT)}")
    print("CONCLUSION normalized certificate exactly matches the completed raw log")


if __name__ == "__main__":
    main()

