#!/usr/bin/env python3
"""Independent checks for the hostile audit of Erdos Problem 149."""

from __future__ import annotations

import gzip
import hashlib
import re
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx
import sympy as sp


ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT.parent / "problem149_delta4_strong_clique_exact_20260811"
SOURCES = BUNDLE / "sources"
PROVENANCE = ROOT / "provenance"

EXPECTED_HASHES = {
    SOURCES / "2607.02698v1-source.tar.gz":
        "29aee6e2b4269210a02c98287cb3798591ef0dc1d16439f5befdb309d47bf115",
    SOURCES / "2607.02698v1.pdf":
        "bf79c035f6eced5515c84d248de73ec03f24a5198d27c62c4adff033a4608153",
    SOURCES / "2607.02698v1-source/line_graph.tex":
        "6983ce3fdf55cb3fe4f4842439548f65d38aaff496f934b49568fe244bb25285",
    SOURCES / "Faron_Postle_1708.02264-source.tex.gz":
        "e0f6df674fc5eb9f272a5566ff1f0f5dced115307dd79cb11e5ba55b30edcedb",
    SOURCES / "Faron_Postle_1708.02264-source.tex":
        "9dfb8f7581890612200d26a86f656694842aee9394986dc77129be82d5ff7314",
    SOURCES / "Faron_Postle_1708.02264.pdf":
        "36e577c86122b44e72cb9e99497da96b186e997edbb4840864bdf9476843d028",
    SOURCES / "HSY2018_v25i3p31.pdf":
        "e122bdde52f1f03d2adfed404c2d80557f269a64b954c251854b8631e75eb653",
    SOURCES / "HSY2018/v25i3p31.txt":
        "a8f22b175270b86db73ada430fd64f17f9026e4d48111ddb3696b24833ce9e17",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sources() -> None:
    for path, expected in EXPECTED_HASHES.items():
        assert digest(path) == expected, path

    kmp = (SOURCES / "2607.02698v1-source/line_graph.tex").read_text()
    assert "For a finite simple graph $G$" in kmp
    assert r"\beta\in [0,1/4]" in kmp
    assert r"\frac{620}{1987}\,\sigma_G(H)^2" in kmp
    assert r"\frac{2607}{1987}\,\Delta(G)^2" in kmp

    fp = (SOURCES / "Faron_Postle_1708.02264-source.tex").read_text()
    assert "For all bipartite subgraphs $H'$ of $H$" in fp
    assert r"\sigma_{G[V(H')]}(H')^2" in fp
    assert r"\left(\frac{1+a}{4}\right)\sigma_G(H)^2" in fp

    hsy = (SOURCES / "HSY2018/v25i3p31.txt").read_text()
    assert "Theorem 2. For every graph G with maximum degree four" in hsy
    assert "21." in hsy

    arxiv = (PROVENANCE / "arxiv_2607.02698_abs_20260811.html").read_text()
    assert "Submitted on 2 Jul 2026" in arxiv
    assert 'content="https://arxiv.org/abs/2607.02698v1"' in arxiv
    assert "<strong>[v1]</strong>" in arxiv


def check_live_gate() -> None:
    page = (PROVENANCE / "live_149_brightdata_20260811.txt").read_text()
    forum = (PROVENANCE / "live_149_forum_brightdata_20260811.txt").read_text()
    for text in (page, forum):
        assert "OPEN" in text
        assert "0 claimed proofs for this problem" in text
        assert "Currently working on this problem\tNone" in text
        assert "Interested in collaborating\tNone" in text
        assert "This page was last edited 10 April 2026" in text
    assert "4 comments on this problem" in forum


def check_exact_algebra() -> None:
    x, t = sp.symbols("x t", real=True)
    beta = sp.Rational(620, 1987)
    assert sp.Rational(1, 4) < beta < sp.Rational(1, 3)

    p_beta = (
        beta * x**4
        + (2 * beta - 1) * x**3
        + beta**2 * x**2
        + beta * (2 * beta - 1) * x
        + beta**2
    )
    certificate = beta * (
        x**2 - sp.Rational(747, 1240) * x - sp.Rational(211, 1000)
    ) ** 2 + (
        708654527125 * x**2
        - 1203303717450 * x
        + 510806838853
    ) / sp.Integer(6119661950000)
    assert sp.expand(p_beta - certificate) == 0

    quadratic = (
        708654527125 * x**2
        - 1203303717450 * x
        + 510806838853
    )
    discriminant = sp.discriminant(quadratic, x)
    assert discriminant == -2478929365735048000

    denominator = t**2 + beta * (1 - t) ** 2
    induction_bound = (
        t * (1 - t)
        + beta * t**2 * (1 - t) ** 2 / denominator
    )
    certificate_at_t = (
        (1 - t) ** 4
        * p_beta.subs(x, t / (1 - t))
        / denominator
    )
    assert sp.factor(sp.together(beta - induction_bound - certificate_at_t)) == 0

    conversion = (1 + beta) / 4
    assert conversion == sp.Rational(2607, 7948)
    assert 4 * conversion == sp.Rational(2607, 1987)
    delta_four = 16 * sp.Rational(2607, 1987)
    assert delta_four == sp.Rational(41712, 1987)
    assert 21 - delta_four == sp.Rational(15, 1987)
    assert sp.floor(delta_four) == 20


def check_blowup() -> Counter[int]:
    graph = nx.Graph()
    parts = [[(i, j) for j in range(2)] for i in range(5)]
    graph.add_nodes_from(vertex for part in parts for vertex in part)
    for i in range(5):
        graph.add_edges_from(
            (left, right)
            for left in parts[i]
            for right in parts[(i + 1) % 5]
        )

    assert graph.number_of_nodes() == 10
    assert graph.number_of_edges() == 20
    assert set(dict(graph.degree()).values()) == {4}

    line = nx.line_graph(graph)
    square = nx.power(line, 2)
    assert line.number_of_nodes() == 20
    assert square.number_of_edges() == 190
    assert set(dict(square.degree()).values()) == {19}

    distance = dict(nx.all_pairs_shortest_path_length(line))
    histogram: Counter[int] = Counter()
    line_vertices = list(line)
    for left, right in combinations(line_vertices, 2):
        histogram[distance[left][right]] += 1
    assert histogram == Counter({2: 130, 1: 60})
    return histogram


def referenced_numbers(text: str) -> set[int]:
    result = {int(value) for value in re.findall(r"\bproblemNum\s*:\s*(\d+)", text)}
    result.update(
        int(value)
        for value in re.findall(
            r"\bn\s*:\s*(\d+)\s*,\s*(?:verdict|problem)\s*:", text
        )
    )
    return result


def check_site_snapshot() -> int:
    with gzip.open(PROVENANCE / "site_index_20260811.js.gz", "rt") as handle:
        index = handle.read()
    with gzip.open(PROVENANCE / "site_ledger_20260811.js.gz", "rt") as handle:
        ledger = handle.read()
    combined = index + "\n" + ledger
    numbers = referenced_numbers(combined)
    assert 149 not in numbers
    assert "arXiv:2607.02698" in ledger
    assert "Section 3 explicitly disproves" in ledger
    assert "2607/1987" not in combined
    assert "2607}{1987" not in combined
    assert "620/1987" not in combined
    assert "620}{1987" not in combined
    return len(numbers)


def main() -> None:
    check_sources()
    check_live_gate()
    check_exact_algebra()
    histogram = check_blowup()
    site_count = check_site_snapshot()

    print("HOSTILE AUDIT 149: INDEPENDENT CHECKS")
    print("source hashes and current-v1 metadata: PASS")
    print("live page gate: OPEN, 0 claims, no worker: PASS")
    print("fixed beta = 620/1987 in (1/4,1/3): PASS")
    print("sum-of-square certificate and discriminant: PASS")
    print("final induction identity: PASS")
    print("Faron-Postle quantifier fragments: PASS")
    print("Delta=4: 41712/1987 = 21 - 15/1987, floor 20: PASS")
    print(f"C5^(2): 20 edges; line-distance histogram {dict(sorted(histogram.items()))}: PASS")
    print(f"frozen site snapshot: {site_count} referenced problems; #149 absent: PASS")
    print("same-paper #934 Section 3 overlap found and disclosed: PASS")
    print("VERDICT: PASS for Omega_4=20; GAP/OPEN for X_4=20")


if __name__ == "__main__":
    main()
