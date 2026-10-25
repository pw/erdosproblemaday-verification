#!/usr/bin/env python3
"""Verify the frozen eligibility and provenance facts for Problem 1117."""

from __future__ import annotations

import json
import re
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
NUMBER = 1117


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def exact_problem_mentions(text: str) -> list[str]:
    patterns = (
        rf"\bproblemNum\s*:\s*{NUMBER}\b",
        rf"\bn\s*:\s*{NUMBER}\b",
    )
    return [match.group(0) for pattern in patterns for match in re.finditer(pattern, text)]


def read_primary_tex(archive: Path, suffix: str) -> str:
    with tarfile.open(archive) as tf:
        names = [name for name in tf.getnames() if name.endswith(suffix)]
        require(len(names) == 1, f"expected one {suffix} in {archive.name}, got {names}")
        member = tf.extractfile(names[0])
        require(member is not None, f"could not read {names[0]}")
        return member.read().decode("utf-8", errors="strict")


def main() -> None:
    index = (SOURCES / "site_index_20260811.js").read_text()
    ledger = (SOURCES / "site_ledger_data_20260811.js").read_text()

    require(not exact_problem_mentions(index), "Problem 1117 occurs in frozen index.js")
    require(not exact_problem_mentions(ledger), "Problem 1117 occurs in frozen ledger_data.js")

    combined = index + "\n" + ledger
    defining_phrases = (
        "maximum modulus point",
        "maximum-modulus point",
        "maximum modulus set",
        "maximum-modulus set",
        "maximum curve",
    )
    for phrase in defining_phrases:
        require(phrase not in combined.lower(), f"defining phrase already present: {phrase}")

    # These broad thematic neighbors are disclosed, not silently treated as absent.
    require(re.search(r"\{n:513,", ledger) is not None, "thematic neighbor 513 missing")
    require(re.search(r"\{n:517,", ledger) is not None, "thematic neighbor 517 missing")
    require("maximum modulus" in ledger.lower(), "expected broad maximum-modulus adjacency")
    require("entire function" in ledger.lower(), "expected broad entire-function adjacency")

    upstream = (SOURCES / "upstream_problems_20260811.yaml").read_text()
    block_match = re.search(
        rf"(?ms)^- number: ['\"]?{NUMBER}['\"]?\s*$.*?(?=^- number:|\Z)", upstream
    )
    require(block_match is not None, "upstream Problem 1117 metadata missing")
    block = block_match.group(0)
    require(re.search(r"state:\s*['\"]open['\"]", block), "upstream state is not open")
    require(re.search(r"oeis:\s*\[['\"]N/A['\"]\]", block), "upstream OEIS marker is not N/A")

    live = json.loads((SOURCES / "live_1117_20260811.json").read_text())
    require(len(live["pages"]) == 5, "unexpected live-page snapshot count")
    by_url = {page["requested_url"]: page["body_text"] for page in live["pages"]}
    main_url = "https://www.erdosproblems.com/1117"
    proof_url = "https://www.erdosproblems.com/forum/thread/1117/proof-claims"
    main = by_url[main_url]
    require("OPEN" in main, "live page is not OPEN")
    require("0 claimed proofs for this problem" in main, "live claimed-proof count changed")
    require("Currently working on this problem\tNone" in main, "live worker is not None")
    require("Interested in collaborating\tNone" in main, "live collaborator is not None")
    require("No proof claims have been submitted yet." in by_url[proof_url], "proof-claim page changed")
    require("The second question is still open" in main, "live page no longer calls part (2) open")

    scratch = json.loads((SOURCES / "scratch_collision_scan_20260811.json").read_text())
    require(not any("1117" in row["name"] for row in scratch["top_level_directories"]),
            "another top-level scratch directory targets 1117")
    expected_passive_hits = {
        "/home/exedev/erdos_scratch/fresh10_gate_audit_20260811/README.md",
        "/home/exedev/erdos_scratch/fresh5_frontier_20260811/live_pages.json",
    }
    require(set(scratch["exact_1117_text_hits_outside_bundle"]) == expected_passive_hits,
            "unexpected Problem 1117 scratch collision")

    query = (SOURCES / "arxiv_query_maximum_modulus_points_20260811.xml").read_text()
    require("2607.09462v1" in query, "current 2026 primary preprint missing from arXiv query")
    require("2208.11154v2" in query, "2024 approximate-result preprint missing from arXiv query")
    primary_query = (SOURCES / "arxiv_query_primary_ids_20260811.xml").read_text()
    for identifier in ("2007.07529v1", "2208.11154v2", "2607.09462v1"):
        require(identifier in primary_query, f"current primary version missing: {identifier}")

    current_tex = read_primary_tex(
        SOURCES / "arxiv_2607.09462v1_source.tar", "Erdos_finite_order_v8_arxiv.tex"
    )
    require(r"\label{th:1}" in current_tex, "Theorem 1.1 source marker missing")
    require(r"There is an entire function \(f\in\B\), of finite order" in current_tex,
            "Theorem 1.1 finite-order/class-B quantifier missing")
    require(r"\limsup_{r\to\infty} v_f(r)=\infty" in current_tex,
            "Theorem 1.1 limsup conclusion missing")
    require("The second part remains open" in current_tex,
            "current primary source does not preserve the open liminf statement")

    approximate_tex = read_primary_tex(
        SOURCES / "arxiv_2208.11154v2_source.tar", "maxmod_revision3.tex"
    )
    require("approximate" in approximate_tex.lower(), "approximate paper source mismatch")
    require("unable to conclude" in approximate_tex.lower(),
            "approximate paper's non-solution disclaimer missing")

    print("PASS exact-number absence: index.js and ledger_data.js")
    print("PASS defining-framework phrase absence; #513/#517 adjacency disclosed")
    print("PASS live gate: OPEN, 0 claims, no worker, no collaborator")
    print("PASS scratch gate: no competing 1117 target; two passive cache/report mentions disclosed")
    print("PASS upstream gate: OPEN, OEIS N/A")
    print("PASS primary provenance: arXiv:2607.09462v1 and 2208.11154v2")


if __name__ == "__main__":
    main()
