#!/usr/bin/env python3
"""Offline consistency checks for the dated public-frontier and site captures."""

from __future__ import annotations

import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
AUTHOR = ROOT / "author_bundle"
UPSTREAM_COMMIT = "74e84382cbbc20b32a2ac679bff977cad3ac5d24"
PUBLIC_1505_SHA256 = "0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338"
SITE_1506_SHA256 = "883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c"
SITE_INDEX_SHA256 = "08e988d080d5317adf768ba827b4f21397699b30d28cc749807616b6753a3b76"
SITE_1506_COMMIT = "8648597d27e13aaa11409ee94b7bd9860db2173a"


class EvidenceFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceFailure(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> object:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def main() -> None:
    upstream = EVIDENCE / "upstream_q9_public_1505_current.json"
    frozen_public = AUTHOR / "provenance" / "q9_public_1505.json"
    require(sha256(upstream) == PUBLIC_1505_SHA256, "live upstream Q9 hash mismatch")
    require(upstream.read_bytes() == frozen_public.read_bytes(), "upstream/frozen 1505 differ")

    remote_lines = (EVIDENCE / "upstream_ls_remote_20260811.txt").read_text().splitlines()
    require(len(remote_lines) == 2, "unexpected ls-remote line count")
    require(
        all(line.startswith(UPSTREAM_COMMIT + "\t") for line in remote_lines),
        "upstream HEAD/main commit mismatch",
    )
    commit = load_json("upstream_main_commit_20260811.json")
    require(commit["sha"] == UPSTREAM_COMMIT, "upstream commit JSON mismatch")

    problem = (EVIDENCE / "live_problem86_20260811.txt").read_text(encoding="utf-8")
    forum = (EVIDENCE / "live_forum86_20260811.txt").read_text(encoding="utf-8")
    for label, text in (("problem", problem), ("forum", forum)):
        require("OPEN - $100" in text, f"{label}: OPEN marker missing")
        require("0 claimed proofs for this problem" in text, f"{label}: proof count changed")
        require(
            "Currently working on this problem\tNone" in text,
            f"{label}: current-worker state changed",
        )
    require("9 1,505 1,497.6 +7.4 4,608" in forum, "forum Q9=1505 row missing")
    require("1,531" not in problem + forum and "1531" not in problem + forum, "1531 already on live source pages")

    oeis_lines = (EVIDENCE / "oeis_A245762_20260811.txt").read_text().splitlines()
    require(
        oeis_lines == [
            "# A245762 (b-file synthesized from sequence entry)",
            "1 1",
            "2 3",
            "3 9",
            "4 24",
            "5 56",
            "6 132",
        ],
        "OEIS A245762 capture differs from n=1..6 table",
    )

    arxiv_root = ET.parse(EVIDENCE / "arxiv_2603.29127_20260811.xml").getroot()
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    entry = arxiv_root.find("atom:entry", namespace)
    require(entry is not None, "arXiv entry missing")
    arxiv_id = entry.findtext("atom:id", default="", namespaces=namespace)
    title = entry.findtext("atom:title", default="", namespaces=namespace)
    summary = entry.findtext("atom:summary", default="", namespaces=namespace)
    require(arxiv_id.endswith("2603.29127v4"), "unexpected arXiv version")
    require("Q6, Q7, and Q8" in title, "unexpected Minamoto title")
    require("Q_7" in summary and "Q_8" in summary and "Q_9" not in summary, "unexpected preprint scope")

    filename_search = load_json("github_search_q9_edges_1531_20260811.json")
    hash_search = load_json("github_search_candidate_hash_20260811.json")
    require(filename_search["total_count"] == 0, "candidate filename appeared in search")
    require(hash_search["total_count"] == 0, "candidate hash appeared in search")
    term_search = load_json("github_search_1531_terms_20260811.json")
    require(term_search["total_count"] == 1, "unexpected broad-term search count")
    require(
        term_search["items"][0]["repository"] == "techno-optimist/erdos-frontier-atlas",
        "unexpected broad-term search hit",
    )
    atlas = (EVIDENCE / "frontier_atlas_problem86_20260811.json").read_text(encoding="utf-8")
    require("1531" not in atlas and "1,531" not in atlas, "broad search hit is Q9=1531")
    repositories = load_json("github_search_repositories_20260811.json")
    require(repositories["total_count"] == 1, "unexpected repository search count")
    require(
        repositories["items"][0]["full_name"] == "rafalwronapl/erdos86-hypercube-c4",
        "unexpected identified construction repository",
    )

    site_index = EVIDENCE / "site_index_1703f9d_20260811.js"
    require(sha256(site_index) == SITE_INDEX_SHA256, "site index snapshot hash mismatch")
    index_text = site_index.read_text(encoding="utf-8")
    require(index_text.count('slug: "86-hypercube-q9-1506"') == 1, "site slug count mismatch")
    require(index_text.count("problemNum: 86,") == 1, "site problem-86 entry count mismatch")
    require(sha256(AUTHOR / "provenance" / "q9_edges_1506.json") == SITE_1506_SHA256, "site predecessor hash mismatch")
    site_commit = (EVIDENCE / "site_1506_commit_20260811.txt").read_text(encoding="ascii")
    require(f"commit={SITE_1506_COMMIT}" in site_commit, "site predecessor commit mismatch")
    require("commit_date=2026-08-11T16:47:17+00:00" in site_commit, "site predecessor date mismatch")

    live_site = (EVIDENCE / "live_site_q9_1506_20260811.html").read_text(encoding="utf-8")
    sitemap = (EVIDENCE / "live_site_sitemap_20260811.xml").read_text(encoding="utf-8")
    require("a 1,506-edge C4-free subgraph of Q9" in live_site, "live site title mismatch")
    require("f(9)&ge;1,506" in live_site, "live site lower bound mismatch")
    require("1,531" not in live_site and "1531" not in live_site, "live site already has 1531")
    require(
        sitemap.count("/day/86-hypercube-q9-1506") == 1,
        "live sitemap predecessor count mismatch",
    )

    print(
        "PUBLIC_PROVENANCE_PASS capture_date=2026-08-11 upstream_commit=" + UPSTREAM_COMMIT
        + " public1505_sha256=" + PUBLIC_1505_SHA256
        + " problem_status=OPEN claimed_proofs=0 current_workers=0 "
        "oeis_q9_term=absent preprint_q9=absent"
    )
    print(
        "SITE_PREPUBLICATION_CAPTURE_PASS capture_date=2026-08-11 "
        "predecessor_entries=1 predecessor_edges=1506 ledger_record86=0 "
        "captured_1531=absent intended_action=update_existing_entry "
        "published1506_sha256=" + SITE_1506_SHA256
        + " published1506_commit=" + SITE_1506_COMMIT
    )
    print(
        "SEARCH_BOUNDARY_PASS capture_date=2026-08-11 "
        "candidate_filename_hits=0 candidate_hash_hits=0 "
        "broad_false_positive=1 global_priority_proved=no"
    )


if __name__ == "__main__":
    try:
        main()
    except (EvidenceFailure, OSError, ET.ParseError, json.JSONDecodeError) as exc:
        print(f"EXTERNAL_EVIDENCE_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
