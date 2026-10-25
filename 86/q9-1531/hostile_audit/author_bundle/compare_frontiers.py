#!/usr/bin/env python3
"""Compare the new Q9 witness with the two frozen predecessor certificates."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges(path):
    data = json.loads(path.read_text())
    return {tuple(sorted(map(int, edge))) for edge in data["edges"]}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    new_path = ROOT / "q9_edges_1531.json"
    site_path = ROOT / "provenance/q9_edges_1506.json"
    public_path = ROOT / "provenance/q9_public_1505.json"
    new = edges(new_path)
    site = edges(site_path)
    public = edges(public_path)
    require(len(site) == 1506, "site predecessor is not 1506 edges")
    require(len(public) == 1505, "public predecessor is not 1505 edges")
    require(len(new) > len(site), "new witness does not improve the site frontier")
    print(
        "FRONTIER_COMPARISON=PASS "
        f"public={len(public)} site={len(site)} new={len(new)} "
        f"vs_site_common={len(new & site)} add={len(new-site)} remove={len(site-new)} "
        f"vs_public_common={len(new & public)} add={len(new-public)} remove={len(public-new)}"
    )
    print(f"public_sha256={sha256(public_path)}")
    print(f"site_sha256={sha256(site_path)}")
    print(f"new_sha256={sha256(new_path)}")


if __name__ == "__main__":
    main()
