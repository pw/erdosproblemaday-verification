# Source notes

Access date: 2026-08-11 UTC.

## Live problem

The files `sources/live_149_20260811.txt`,
`sources/live_149_latex_20260811.txt`, and
`sources/live_149_discussion_20260811.txt` are rendered Bright Data browser
captures. The page displayed `OPEN`, `0 claimed proofs for this problem`, and
`Currently working on this problem: None`.

## Strong-clique theorem

Hitesh Kumar, Bojan Mohar, and Shivaramakrishna Pragada, "An improved bound
for the strong clique index of graphs," arXiv:2607.02698v1, submitted 2 July
2026.

Bundled artifacts:

- `sources/2607.02698v1.pdf`
- `sources/2607.02698v1.txt`
- `sources/2607.02698v1-source.tar.gz`
- extracted source under `sources/2607.02698v1-source/`

Corollary 1.7 is unconditional and quantified over every finite simple graph
under the paper's opening convention. It states

```text
omega(L(G)^2) <= (2607/1987) Delta(G)^2.
```

The source also gives the cycle blowup construction used for equality. The
v1 auxiliary beta-star interval typo is documented in `PROOF_AUDIT.md`.

## Conditional reduction used by KMP

Maxime Faron and Luke Postle, "On the clique number of the square of a line
graph and its relation to Ore-degree," arXiv:1708.02264; published in Journal
of Graph Theory 92 (2019), 261-274.

The bundled PDF and TeX source contain Theorem 1.9, the conditional theorem
quoted as Theorem 1.5 by KMP. For `a` in `[1/4,1/3]`, it converts the stated
bipartite-subgraph Ore-degree bound into coefficient `(1+a)/4` for a general
strong clique.

## Delta=4 coloring upper bound

Mingfang Huang, Michael Santana, and Gexin Yu, "Strong Chromatic Index of
Graphs With Maximum Degree Four," Electronic Journal of Combinatorics 25(3)
(2018), P3.31, DOI 10.37236/7016.

The official PDF and extracted text are bundled. Theorem 2 states that every
graph of maximum degree four has strong chromatic index at most 21.
