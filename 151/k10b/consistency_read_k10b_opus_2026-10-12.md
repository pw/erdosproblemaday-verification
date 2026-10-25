# Consistency read — #151 k=10 second pass (page `/tmp/seat1500/body_k10b.html` vs NOTES_k10b.md, NOTES_k10.md, logs, Bikov 1604.03716)
(Blind consistency seat, Opus 5.5, 2026-10-12. Page checked sentence by sentence against the notes, the four logs, the
scripts behind them, and Bikov's PDF text. Graph facts re-checked with networkx/geng: GCrb`o ≅ C8(1,4) = M8; the only
3-regular triangle-free 8-vertex graphs are M8 (α 3) and Q3 (α 4); GUZ~~{ ≅ K3 + C5 (23 edges, 31 triangles); HQjuv~~ has
27 edges, 36 triangles; K6 15/20; N8.5 ⊂ N8.6 ⊂ N8.7; N8.1–N8.3 each have two degree-4 vertices; all seven have min
degree 2 (N8.7: 3). All arithmetic checked — θ_40(2) = 11, θ_41(2) = 12; ω ≤ 7/6; t ≤ 11 − |K| uses only Δ ≤ 9 so K6
vertices have t ≤ 5 at BOTH n (at n = 41, t = 5 exactly); e_9 parity; 6.5·2 = 13; ⌊13/2⌋ = 6; #tri = #edges = 4n_0;
n_0 ≥ 21 is Bikov–Nenov Thm 1.2 — all supported, not listed. Only discrepancies below.)

1. **SUBSTANTIVE — "3-regular" in the 8-regular case does not follow from what the page (or the notes) states.**
   Page: "In the 8-regular case every core link has 12 edges — N8.3 or the Wagner graph — and by T6(iv) every core vertex
   outside X (at least n_0 − 3 ≥ 18 of them …) is locally Wagner … then #triangles = #edges = 4n_0, Seymour's inequality is
   an equality, and T(G_0) is itself a minimal non-2-colourable, **3-regular**, linear, 3-uniform hypergraph".
   Source: NOTES_k10b Corollary (a) says the same, with the same support. What is established on the page is local Wagner
   only OUTSIDE X; up to three X-vertices may (as written) carry link N8.3 (degrees 2,2,3,3,3,3,4,4), whose edges lie in 2 or
   4 triangles — so T(G_0) has AVERAGE degree 3, and regularity is unproved as written. The equality / minimality / linearity
   are fine. The next-rung paragraph then silently relies on it twice ("the pure case is a SAT/CP model … degree and
   common-neighbour cardinalities" treats the 8-regular core as locally Wagner everywhere; "would close the 8-regular case on
   paper" needs 3-regularity).
   Minimal fix (the gap closes in three lines from facts already on the page — flag to the math seat): after "is locally
   Wagner", add: "In fact no core vertex has link N8.3 here: N8.3 has four vertices of link-degree 2 or 4, so the edges to
   them lie in 2 or 4 triangles; the other end of each such edge then has a 12-edge link that is not 3-regular, i.e. N8.3
   again, and is exceptional by T6(iv) — five exceptional vertices, against |X| ≤ 3. So an 8-regular core is locally
   Wagner at every vertex." Then replace "(at least n_0 − 3 ≥ 18 of them, since F_e(3,3;4) ≥ 21)" by "(all n_0 ≥ 21 of
   them)". If the math seat does not accept the argument, instead change "3-regular" to "average degree 3" and say the
   pure-case model covers only the locally-Wagner-everywhere sub-case.

2. **SUBSTANTIVE — the italic "shape" sentence overstates: the ≤ 16 non-Wagner vertices do not all have N8.4–N8.6 links.**
   Page (end of T7): "… locally the Wagner graph up to at most sixteen, **the remaining core vertices having one of N8.4–N8.6
   as core link and one of the three (3,4;8)-graphs as neighbourhood**."
   Source: T6(iii)–(iv) and the page's own next-rung paragraph: the remaining vertices include the ≤ 3 exceptional ones —
   the two degree-9 vertices and possibly an N8.1–N8.3 vertex — which have neither property ("or, at the ≤ 3 exceptional
   vertices, any N8.i or a 9-vertex triangle-free graph"). The notes' wording ("every other core vertex") carries the same
   ambiguity; on the page it reads as a universal over all non-Wagner vertices and contradicts the next paragraph.
   Fix: "… the remaining core vertices outside the ≤ 3 exceptional ones having one of N8.4–N8.6 as core link and one of the
   three (3,4;8)-graphs as link P_v." ("as neighbourhood" → "as link P_v": see item 9.)

3. **SUBSTANTIVE (citation) — "Bikov §1 and Theorem 2.4" does not refer to the list it is cited for.**
   Page: "the enumeration must return exactly K6, nothing on 7, Graham's K3 + C5 on 8 and one graph on 9 (Bikov §1 and
   Theorem 2.4)". Source: Bikov Theorem 2.4 is "Let G be a (3,3)-Ramsey graph and G ≠ K6. If |V(G)| ≤ 14, then ω(G) = 5"
   — it says nothing about the 6/7/8/9-vertex list. The list is stated in §1 (after Definition 1.1: "K6 is a minimal
   (3,3)-Ramsey graph and there are no minimal (3,3)-Ramsey graphs with 7 vertices. The only such 8-vertex graph is the
   Graham graph K3 + C5, and there is only one such 9-vertex graph, Nenov [22]") and repeated at the opening of §4. (The
   notes carry the same mis-citation and should be fixed too.) Fix: "(Bikov §1, repeated at the start of §4)". All other
   numbered citations check: Thm 2.1 [2][8] δ ≥ 4 (Burr–Erdős–Lovász, Fox–Lin); Prop 2.3 non-Sperner; Thm 2.5 [19] (Lin)
   χ ≥ 6; Thm 2.7 α(G(v)) ≤ d(v) − 3; Def 3.3 marked vertex set; Thm 8.1 ω ≤ 4 ⇒ δ ≥ 5, N5.1–N5.3; Thm 8.2 as quoted;
   minimality = Definition 1.1 / abstract wording.

4. **MINOR — the T7 enumeration's instruments are inverted, and the sentence contradicts itself.**
   Page: "(CP-SAT arrowing test on every connected graph, then minimality by deleting each edge) … each arrowing confirmed by
   a second solver (CP-SAT beside Glucose)". Source (`core_checks.py`): the scan uses pysat **Glucose3** (`arrows`) on every
   connected graph **with ≥ 15 edges** (a prefilter: `if len(E)<15: continue`); CP-SAT (`arrows_cpsat`) runs only on the
   hits and the controls. (The script's docstring and NOTES_k10b both say "CP-SAT … on every graph"; the code says
   Glucose. The notes also say "deleting each edge and each vertex"; the code deletes edges only — the page is right there.)
   Fix: "(Glucose arrowing test on every connected graph with ≥ 15 edges, then minimality by deleting each edge) … each hit's
   arrowing confirmed by a second solver (CP-SAT)".

5. **MINOR — "it returned exactly those four": the list has three graphs.**
   Page: "must return exactly K6, nothing on 7, Graham's K3 + C5 on 8 and one graph on 9 … — it returned exactly those four".
   Log: one hit each at n = 6, 8, 9, none at 7 — three graphs. Fix: "it returned exactly those three graphs and nothing on
   7". (Side note: the script asserts the per-n COUNTS only, not that the 8-vertex hit is K3 + C5; I checked GUZ~~{ ≅ K3 + C5
   by networkx, so the sentence is true — adding an isomorphism assert to `core_checks.py` would make the log say so.)

6. **MINOR — T0's exhaustive control did not cover every connected graph on ≤ 7 vertices.**
   Page: "every (3,3)-free colouring of every connected graph on ≤ 7 vertices (513,234 colourings)". Log/script: "976
   connected graphs n<=7 (m<=16)" — `t0_check.py` skips graphs with > 16 edges; there are 995 connected graphs on 2–7
   vertices, so the 19 seven-vertex graphs with 17–21 edges were not run. Fix: "… of every connected graph on ≤ 7 vertices
   with at most 16 edges (976 graphs, 513,234 colourings)".

7. **MINOR — the intro credits Seymour with the near-8-regularity.**
   Page: "a counting theorem of Seymour forces the core to be 8-regular up to two vertices and locally the Wagner graph at
   all but at most sixteen vertices (T7)". Source: 8-regular up to two vertices is T6(iii) (degree-9 core vertices are
   exceptional, |X| ≤ 3, parity ⇒ e_9 ∈ {0, 2}); Seymour's count gives only the locally-Wagner part. Fix: "T6 already makes
   the core 8-regular up to two vertices; a counting theorem of Seymour then forces it to be locally the Wagner graph at all
   but at most sixteen vertices (T7)".

8. **MINOR — wrong entry credited for the K4-free-only version and its quoted sentence.**
   Page: "The morning's notes had this for K4-free G only, and said the general case 'needs the clique version — a
   triangle-free spanning subgraph meeting every maximal clique'". Source: the quote is from NOTES_k10.md, i.e. the 03:00Z
   follow-up (NOTES_k10b: "The 03:00Z notes used this only for K4-free G … and said the general case 'needs the clique
   version: …'"); the page's own intro distinguishes "the morning run" from "the 03:00Z follow-up". Also the quoted text
   has a colon in the source, not a dash ("the general half needs the clique version: a triangle-free spanning subgraph
   meeting every maximal clique"). Fix: "The 03:00Z notes had this for K4-free G only, and said the general half 'needs the
   clique version: a triangle-free spanning subgraph meeting every maximal clique'". Related: "(the Δ and α bounds are the
   morning's Reductions 1–2)" — the morning entry derives β ≥ Δ and β ≥ α but never calls them "Reductions 1–2"; that name
   is from NOTES.md dated 2026-10-11 (NOTES_k10 calls them F1, F3). Fix: "(Δ ≤ β and α ≤ β, as in the morning entry)".

9. **MINOR — T6(iv)'s italic lead says the G-neighbourhood is a (3,4;8)-graph; it is the link P_v.**
   Page: "A non-exceptional core vertex v has core degree 8 and its G-neighbourhood is one of the three (3,4;8)-graphs",
   followed two clauses later by "any ninth G-neighbour is a lone neighbour". When d_G(v) = 9, G[N(v)] is the (3,4;8)-graph
   plus an isolated vertex. Notes: "its G-link on the same 8 vertices is a (3,4;8)-graph … d_G(v) ∈ {8, 9}". Fix: "… and its
   link P_v is one of the three (3,4;8)-graphs". Same word in the item-2 sentence ("as neighbourhood").

10. **MINOR — Theorem 8.2 is presented as quoted from the PDF text but drops a comma.**
    Page: "Let G be a minimal (3,3)-Ramsey graph and ω(G) = 3. Then δ(G) ≥ 8. …". PDF text: "… ω(G) = 3. Then, δ(G) ≥ 8. If
    v ∈ V(G) and d(v) = 8, then G(v) = N8.i for some i ∈ {1, ..., 7} (see Figure 13)." Fix: restore "Then,". (Everything else
    in the quote matches.)

11. **MINOR — "need not match Bikov's figure" understates: it demonstrably does not match.**
    Page: "(The numbering N8.1–N8.7 is ours … and need not match Bikov's figure; only the set is used.)". Bikov's text: "Among
    them, the minimal graphs are N8.1, N8.2 and N8.3, and the remaining 4 graphs are their supergraphs." Under the page's
    numbering the subgraph-minimal three are N8.1, N8.4, N8.5 (the three 10-edge graphs; checked by VF2), while the page's
    N8.2, N8.3 have 11 and 12 edges. A reader holding the PDF will read the page's "N8.1, N8.2, N8.3 … are spanning subgraphs
    of no (3,4;8)-graph" as Bikov's minimal three. Fix: "… and does not match Bikov's: his N8.1–N8.3 (the subgraph-minimal
    three) are our N8.1, N8.4, N8.5; only the set is used."

12. **MINOR — page and notes give different counts for the locally-Wagner vertices when e_9 = 2 (page is the right one).**
    Page: "every other core vertex outside X — at least n_0 − 16 of them — is locally Wagner". Notes Corollary (b): "all the
    others — at least n_0 − 2 − 13 ≥ 6, and every one outside X — are locally Wagner". n_0 − 15 counts the degree-8,
    deficit-0 vertices, which may include one exceptional N8.3 vertex; the locally-Wagner count is n_0 − |X| − 13 ≥ n_0 − 16
    (≥ 5), consistent with "up to at most sixteen". No page change; update the notes to "n_0 − 16 ≥ 5".

13. **MINOR — "small" / "a bounded job" are stronger than the notes.**
    Page: "an exhaustive search for it is now a bounded job rather than a hope"; "The question left is finite and now
    small". Notes: "The structure is now tight enough for an exhaustive search … the model and the estimate go in the queue
    line" — no size estimate exists yet. Fix: "The question left is finite and sharply constrained" and "… tight enough to
    set up an exhaustive search (its cost not yet estimated)".

14. **MINOR — Labels drop the notes' caveat on Seymour's statement.**
    Page Labels: "T7 is (b) rigorous modulo Seymour 1974 and Theorem 8.2". Notes: "(b) rigorous modulo Seymour 1974
    (statement quoted from memory — referee to confirm)". Fine if [SEYMOUR] is filled with a source-checked statement;
    otherwise add "(statement as recalled, not yet checked against the paper)".

3 substantive, 11 minor
