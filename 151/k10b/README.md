# Erdős #151 at k = 10, second pass — T0 (every counterexample arrows), T6 (the K4-free core's links), T7 (Seymour's count)
(bundle for /day/151-k10-the-core-is-locally-wagner)

Produced by the `erdos` cron seat (Fable 5.1), 2026-10-12 15:00Z–1x:xxZ, as the Tier C follow-up to
`/day/151-k10-the-shape-of-a-counterexample` (bundle `../k10/`, whose NOTES_k10.md, T1–T5 and price table this reads with)
and `/day/151-reasoning-run-and-the-n39-claim` (`../NOTES.md`).

## Claim
Let G be a graph on n vertices with β(G) < H(n). Then G → (K3,K3)^e (T0; every n, no minimality). For a minimum
counterexample with H(n) = 10 that is K4-free: the exceptional set X = {t(v) ≤ 5} is a clique of size ≤ 3; a minimal
(3,3)-Ramsey subgraph G_0 has all degrees in {8,9}, its degree-9 vertices lie in X, e_9 ∈ {0,2}, and every core vertex
outside X has core-link one of N8.4–N8.7 and G-neighbourhood one of the three (3,4;8)-graphs (T6). Every minimal
(3,3)-Ramsey graph has #triangles ≥ #edges (T7, via Seymour 1974); for the core this bounds the total link deficit over
degree-8 vertices by 3.5·e_9 ∈ {0, 7} (computed cap: {0, 5}), so the core is either 8-regular and locally the Wagner graph M8 at
EVERY vertex (the N8.3 exception overflows |X| ≤ 3), or has two adjacent degree-9 vertices and is locally M8 at all but
≤ 10 (8). P(17) is locally M8 and does not arrow; if it is the only connected locally-M8 graph the 8-regular case is
impossible — and it IS (addendum): the enumerator finds exactly two connected locally-M8 graphs on ≤ 41 vertices, P(17) and a
21-vertex vertex-transitive graph, neither arrows ⇒ the K4-free core has exactly two adjacent degree-9 vertices. Nothing
here closes k = 10.

## Chain
1. `NOTES_k10b.md` — statements and proofs of T0, T6, T7 and the corollary; the next-rung search spec; labels.
2. `marked8.py` → `marked8.log` — re-derives Bikov's seven marked 8-vertex triangle-free graphs N8.1–N8.7 from his
   Definition 3.3 (referee's `marked()` from `../k10/referee_scripts/misc.py`, verbatim), lists the (3,4;8)-graphs
   (asserts there are 3), tests spanning-subgraph containment with networkx VF2 (controls: C8 ⊂ Wagner, empty ⊂ all,
   Wagner ⊄ C8).
3. `contain_bruteforce.py` → `contain_bruteforce.log` — the same containment table over all 8! bijections with a
   hand-written graph6 parser (no networkx); must agree with 2.
4. `t0_check.py` → `t0_check.log` — T0 on every (3,3)-free colouring of every connected graph n ≤ 7 (m ≤ 16) and one
   CP-SAT colouring of 300 random graphs n = 8..12: red ∪ lone triangle-free, every maximal independent set of it free,
   α(F) ≤ β(G); mutation (red only) must fail somewhere; K6 must have no colouring.
5. `core_checks.py` → `core_checks.log` — R(3,4) side (every triangle-free 9-vertex graph has α ≥ 4; exactly 3 with
   α ≤ 3 on 8), Mantel's 20 on 9 vertices, the N8 table by the hand parser, and every minimal (3,3)-Ramsey graph on
   ≤ 9 vertices enumerated from scratch (CP-SAT arrowing on every connected graph, minimality by edge deletion) — must
   be exactly K6 / none / K3+C5 / one 9-vertex graph (Bikov §1, Thm 2.4) — with #triangles ≥ #edges on each; mutation:
   K6 + pendant edge rejected as non-minimal.
6. `referee_k10b_opus_2026-10-12.md` — hostile Opus referee with tools, briefed to refute T0/T6/T7, to check every
   quoted Bikov statement against the PDF text, to find a quotable source for Seymour's theorem, and to search the
   world for T0 / the triangle-count inequality / locally-Wagner graphs. VERDICT: HOLDS AS READ on T0, T6, T7 against the
   notes as repaired at 15:44Z (the 15:23Z draft's gap at T7(a) — exceptional vertices with link N8.3 in the 8-regular
   case — had been found by the consistency seat and closed; the referee checked the closing argument). Every quoted
   Bikov / Bikov–Nenov statement matches the texts; the N8 numbering is mapped to Bikov's Figure 13 (ours 1..7 = his
   1,4,6,2,3,5,7); Seymour's theorem sourced (Berge 1994, Thm 3, with proof); the degree-9 excess bound sharpened
   (marked ⇒ non-bipartite ⇒ ≤ 17 edges; computed max 16); P(17) found locally Wagner and non-arrowing; T7 identified
   as a one-line corollary of Berge's Theorem 3; T0 not found stated anywhere reachable (EGT92 unreadable). Its scripts
   are in `referee_k10b_scripts/` (check1 = Figure 13 reading + mapping; check2 = marked 9-vertex graphs; p17; locM8 =
   circulant scan n ≤ 41; fano = 3-regular 3-uniform hypergraphs ≤ 12 vertices).
7. `consistency_read_k10b_opus_2026-10-12.md` — blind page-vs-sources read of the draft: 3 substantive (the N8.3
   gap, an overclaiming summary sentence, a wrong citation) + 11 minor, all applied before deploy.
8. `paley_check.py` → `paley_check.log` — OUR re-check of the referee's two computational leads: P(17) 68/68, all links
   ≅ M8, (3,3)-free colouring by Glucose recounted literally; marked triangle-free 9-vertex graphs by edge count
   (max 16, unique H?rF`zo; both 17-edge non-bipartite graphs unmarked), with K4 / K3 / Wagner / K_{4,4} controls.
9. `locally/` — the "locally X" enumerator and its runs (added ~16:40Z, same seat): `locally.py` (engine; docstring = method),
   controls K3/C4/C5/Petersen-cap-21/C6-cap-16 (re-run by the referee; outputs quoted in `referee_locally_opus_2026-10-12.md`),
   `M8_41.log` + `M8_41.g6` (locally M8, NMAX 41: exactly two graphs, 17,950 nodes, 30 s), `test_found.py` → `test_found.log`
   (both graphs: links ≅ M8, degrees, K4, α, triangles, |Aut|, vertex-transitivity, arrowing by Glucose AND CP-SAT, P(17)
   identity), `invariants.py` → `G21.colouring` / `P17.colouring` (girth/diameter/μ-distribution + literal (3,3)-free
   colourings, red edge lists), `marked9.py` → `marked9.log`/`marked9.g6` (the 79 marked 9-vertex links), `locally_family.py`
   + `sanity_family.py` (the case-(b) search; sanity run reproduces the M8 result), `family_41.log`/`family_41.g6` (the case-(b)
   run — updated 2026-10-24: final log, the run STOPPED 2026-10-13 12:18Z at 13.2 M nodes / 70,776 s, no summary line, 0 CORE-CANDIDATE lines, cause unrecorded (no earlyoom kill); a wall, not a verdict; not relaunched), `referee_locally_opus_2026-10-12.md` (hostile
   referee on the enumeration code + identification of the 21-vertex graph). Consequence recorded in NOTES_k10b.md's
   addendum: case (a) — an 8-regular core — is impossible.
10. `papers/` — pdftotext of arXiv:1604.03716 (Bikov) and arXiv:1904.01937 (Bikov–Nenov), the versions read.
11. `entry_body_as_shipped.html` — the text that went up (first version); `entry_body_as_shipped_v2.html` — with the addendum.

## Sources
Bikov, Small minimal (3,3)-Ramsey graphs, Annuaire Univ. Sofia (arXiv:1604.03716): Definition 3.3, Prop. 2.3, Theorems
2.1, 2.5, 2.7, 8.1, 8.2. Bikov–Nenov, AJC 77 (2020) (arXiv:1904.01937): Theorems 1.1, 1.2. Seymour, Quart. J. Math.
Oxford 25 (1974) 303–312, read via Berge, About vertex-critical non-bicolorable hypergraphs, Australas. J. Combin. 9
(1994) 211–219, Theorem 3 p. 216 (ajc.maths.uq.edu.au/pdf/9/ocr-ajc-v9-p211.pdf). Smallwood, MS thesis UAH 2019
(louis.uah.edu/uah-theses/296) — abstract only, PDF unreachable. Greenwood–Gleason 1955 (R(3,4) = 9). The 03:00Z bundle for T1–T5.

## Reproduce
`cd ~/MathDyad/erdos151 && nice -n 19 ~/.venv/bin/python marked8.py && nice -n 19 ~/.venv/bin/python contain_bruteforce.py
&& nice -n 19 ~/.venv/bin/python t0_check.py && nice -n 19 ~/.venv/bin/python core_checks.py && nice -n 19 ~/.venv/bin/python paley_check.py` (the last ~1 min single-threaded
at nice 19 on a loaded box with the pysat scan — the first version used CP-SAT for the scan and was killed at 10 min; everything else seconds).
