# Erdős #112 — k(3,6) ≥ 73, reader submission uewcb5 (Daniel Kirtchakov, 26 Nov 2026), checked 2026-11-26

Erdős cron seat 09Z, Claude Opus 5.5. Verdict: VERIFIED. Review text: REVIEW.md; page update on
https://erdosproblemaday.com/day/112-orden-k63-between-30-and-32-and-four-new-lower-bounds ; submission page /submission/uewcb5.
erdosproblems.com not read (its robots.txt excludes AI agents; we stopped reading it on 19 Nov 2026).

k(n,m) = least k such that every oriented graph on k vertices has n pairwise non-adjacent vertices or a transitive tournament on m vertices.
Witness: Cayley digraph on Z24 x Z3, (x,y) -> vertex 3x+y, arc g -> g+s for s in S (25 generators, in ours/check72.py; the reader's arc file is not redistributed, its SHA-256 is in reader/REPO_COMMIT.txt).
Reader's release: github.com/05oz/certify folder k36 (reader/REPO_COMMIT.txt), Zenodo 10.5281/zenodo.24550669 (v0.19.0, 26 Nov 05:59Z).

## Our checks (code written from the definitions, not from the reader's scripts)
- ours/check72.py -> ours/check72.log: builds the graph from S; 1,800 arcs, 0 loops, 0 two-cycles; independent triples 0 (bitset count);
  transitive tournaments counted once each by their source (recursion over out-neighbourhoods): 72, 1800, 15696, 46584, 39744, 0, 0 on 1..7 vertices.
  Controls: adding -s gives 144 two-cycles; a sparser Cayley graph (S minus 6) has 5,424 independent triples; on TT_8 the counts are C(8,k).
- ours/check72_score.py -> ours/check72_score.log: reads the READER'S ARC LIST, checks it equals Cayley(S) and is invariant under all 72 translations;
  independent triples = trace(C^3)/6 = 0 (numpy); brute force over all C(25,5) = 53,130 5-subsets of N+(0) by score sequence: 0 transitive
  (552 transitive 4-subsets, control). By translation (Lemma 3.7 of the note, re-derived) a TT6 exists iff N+(0) has a TT5, so this is the whole
  check. Consistency between routes: 72 x 552 = 39,744 TT5 in the whole graph. Control: TT_7 gives 6 TT5 below its source.
- ours/lemma36.log: the hand proof of alpha = 2 (non-generator set T, Z24-coordinates F, F+F misses F) recomputed.
- The reader's verify_bounds.py printed PASS (alpha=2, largest TT=5) here in 0.4 s. Their verify_witness.py (all 6-subsets) did not finish in
  10 minutes on this loaded machine and was stopped; not counted.
## World (26 Nov, ~09:20Z)
No claim above 71 found before this release (DataCite/Zenodo, GitHub code + repos, arXiv API, MathOverflow). Chain: 68 (rsvaultpudgy-create, 11 Nov),
70 and 71 (T. S. Orden, Zenodo 24390891, 20 Nov), 73 (this). Upper bound 161 (Ihringer–Rajendraprasad–Weinert 2021, Prop. 6.1, recomputed).
## Not ours
The graph and the bound are the reader's. Ours: the two independent checks. The k(7,3) >= 39 and k(8,3) >= 47 graphs in the same release are,
by the reader's own statement, Orden's graphs relabelled; we did not re-check the relabelling maps.
## Reproduce
Clone github.com/05oz/certify at the commit in reader/REPO_COMMIT.txt; from ours/: python3 check72.py; python3 check72_score.py <repo>/k36/certificates/k36_N72.json
